"""Own copy-only PDF edits; never overwrite inputs or execute PDF actions."""
from contextlib import contextmanager
import hashlib
import math
from pathlib import Path
import re
import shutil
import tempfile

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NullObject, NumberObject

MAX_OPERATIONS = 1000
MAX_TEXT_BYTES = 64 * 1024


def _sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _require(value, message):
    if not value:
        raise ValueError(message)


def _text(value, name, limit=MAX_TEXT_BYTES):
    _require(isinstance(value, str) and value.strip() and len(value.encode('utf-8')) <= limit,
             f'{name} vazio, inválido ou acima do limite.')
    return value


def _inherited(field, name, default=None):
    reference = getattr(field, 'indirect_reference', None)
    _require(reference is not None, 'Campos diretos sem referência PDF ainda não são suportados.')
    current = reference.get_object()
    seen = set()
    while current is not None:
        _require(id(current) not in seen and len(seen) < 64, 'Hierarquia de campo inválida ou muito profunda.')
        seen.add(id(current))
        if name in current:
            return current[name]
        parent = current.get('/Parent')
        current = parent.get_object() if parent is not None else None
        if isinstance(current, NullObject):
            current = None
    return default


def _terminal(field):
    raw = field.indirect_reference.get_object()
    kids = raw.get('/Kids')
    if kids is None:
        return True
    kids = kids.get_object()
    if isinstance(kids, NullObject):
        return True
    _require(isinstance(kids, ArrayObject), 'Subcampos do formulário inválidos.')
    children = [child.get_object() for child in kids]
    _require(all(isinstance(child, DictionaryObject) for child in children), 'Subcampo de formulário inválido.')
    return not any('/T' in child for child in children)


@contextmanager
def _editable(path, expected=None):
    path = Path(path)
    identity = _sha(path)
    if expected is not None:
        _require(isinstance(expected, str) and re.fullmatch('[0-9a-f]{64}', expected),
                 'Informe o SHA-256 atual do PDF.')
        _require(identity == expected, 'O PDF mudou. Leia o documento novamente.')
    with path.open('rb') as stream:
        reader = PdfReader(stream, strict=True)
        if reader.is_encrypted:
            raise NotImplementedError('Gravação de cópias de PDFs criptografados ainda não é suportada.')
        fields = reader.get_fields() or {}
        if '/Perms' in reader.root_object or any(_inherited(f, '/FT') == '/Sig' for f in fields.values()):
            raise NotImplementedError('Gravação de documentos com assinatura ou campos de assinatura ainda não é suportada.')
        form = reader.root_object.get('/AcroForm')
        if form is not None and not isinstance(form.get_object(), NullObject) and '/XFA' in form.get_object():
            raise NotImplementedError('Gravação de formulários XFA ainda não é suportada.')
        if '/Collection' in reader.root_object:
            raise NotImplementedError('Gravação de portfólios ainda não é suportada.')
        yield reader, fields, identity


def inspect_editable_document(path):
    """Describe the bounded edit contract without decoding embedded payloads."""
    with _editable(path) as (reader, fields, identity):
        result = {'schema': 'linuxit-copy-edit-info-v1', 'source_sha256': identity,
                  'pages': len(reader.pages), 'text_fields': []}
        for name, field in fields.items():
            if _inherited(field, '/FT') == '/Tx' and _terminal(field):
                value = _inherited(field, '/V', '')
                if isinstance(value, NullObject):
                    value = ''
                _require(isinstance(value, str), 'Valor original de campo de texto inválido.')
                result['text_fields'].append({'name': name, 'value': value,
                                             'read_only': bool(int(_inherited(field, '/Ff', 0)) & 1)})
    _require(_sha(path) == identity, 'O PDF foi alterado durante a leitura.')
    return result


def _page(writer, index):
    _require(type(index) is int and 0 <= index < len(writer.pages), 'Página inválida; índices usam base zero.')
    return writer.pages[index]


def _apply(writer, operation):
    _require(isinstance(operation, dict), 'Cada alteração deve ser um objeto JSON.')
    kind = operation.get('kind')
    if kind == 'add-bookmark':
        _require(set(operation) == {'kind', 'title', 'page'}, 'Opções de marcador inválidas.')
        _page(writer, operation['page'])
        writer.add_outline_item(_text(operation['title'], 'Título', 4096), operation['page'])
    elif kind == 'add-note':
        _require({'kind', 'text', 'page', 'rect'} <= operation.keys()
                 and set(operation) <= {'kind', 'text', 'page', 'rect', 'author'}, 'Opções de nota inválidas.')
        page = _page(writer, operation['page'])
        rect = operation['rect']
        left, bottom, right, top = map(float, page.cropbox)
        if rect is None:
            width, height = right - left, top - bottom
            _require(all(math.isfinite(v) for v in (left, bottom, right, top)) and width > 0 and height > 0,
                     'Dimensões da página inválidas.')
            margin = min(10, width / 10, height / 10)
            rect = [left + margin, top - margin - min(20, height - margin * 2),
                    left + margin + min(20, width - margin * 2), top - margin]
        _require(isinstance(rect, list) and len(rect) == 4 and all(
            type(v) in (int, float) and math.isfinite(v) for v in rect), 'Retângulo de nota inválido.')
        _require(left <= rect[0] < rect[2] <= right and bottom <= rect[1] < rect[3] <= top,
                 'A nota deve ficar dentro do CropBox da página, em coordenadas PDF.')
        author = operation.get('author')
        if author is not None:
            author = _text(author, 'Autor', 4096)
        note = Text(rect=tuple(rect), text=_text(operation['text'], 'Texto'), title_bar=author)
        # The PDF annotation flag key is /F; normalize the library helper's key.
        note.pop('/Flags', None)
        note[NameObject('/F')] = NumberObject(4)
        writer.add_annotation(operation['page'], note)
    elif kind == 'fill-text-fields':
        _require(set(operation) == {'kind', 'values'}, 'Opções de formulário inválidas.')
        values = operation['values']
        _require(isinstance(values, dict) and 0 < len(values) <= 256, 'Informe de 1 a 256 campos de texto.')
        fields = writer.get_fields() or {}
        for name, value in values.items():
            _require(name in fields and _inherited(fields[name], '/FT') == '/Tx', 'Campo de texto não encontrado.')
            field = fields[name]
            _require(_terminal(field), 'Selecione um campo de texto terminal, sem subcampos nomeados.')
            _require(not (int(_inherited(field, '/Ff', 0)) & 1), 'Campo somente leitura não pode ser alterado.')
            _require(isinstance(value, str) and len(value.encode('utf-8')) <= MAX_TEXT_BYTES, 'Valor de campo inválido.')
            # get_fields() presents a reduced Field view which omits /MaxLen.
            limit = _inherited(field, '/MaxLen')
            if limit is not None:
                _require(isinstance(limit, int) and limit >= 0, 'Limite de caracteres do campo inválido.')
                _require(len(value) <= int(limit), 'Valor acima do limite de caracteres do campo.')
            raw = field.indirect_reference.get_object()
            if '/FT' not in raw:
                # Materialize the equivalent inherited type for combined child widgets.
                raw[NameObject('/FT')] = NameObject('/Tx')
        writer.update_page_form_field_values(None, values, auto_regenerate=None)
        updated = writer.get_fields() or {}
        _require(all(updated[name].get('/V') == value for name, value in values.items()),
                 'O formulário não possui widgets de página suportados para todos os campos.')
    else:
        raise ValueError('Tipo de alteração não suportado.')


def save_edited_copy(path, destination, *, source_sha256, operations):
    """Apply a bounded batch to a clone and create a new PDF exclusively."""
    _require(isinstance(operations, list) and 0 < len(operations) <= MAX_OPERATIONS,
             f'Informe de 1 a {MAX_OPERATIONS} alterações.')
    destination = Path(destination)
    _require(destination.parent.is_dir(), 'A pasta de destino deve existir.')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    temporary = None
    created = False
    try:
        with _editable(path, source_sha256) as (reader, fields, identity):
            writer = PdfWriter(clone_from=reader)
            for operation in operations:
                _apply(writer, operation)
            with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-copy-', suffix='.pdf', delete=False) as stream:
                temporary = Path(stream.name)
                writer.write(stream)
            with temporary.open('rb') as stream:
                _require(len(PdfReader(stream, strict=True).pages) == len(reader.pages), 'A cópia gerada não preservou as páginas.')
        _require(_sha(path) == identity, 'O PDF foi alterado durante a preparação da cópia.')
        with temporary.open('rb') as source, destination.open('xb') as output:
            created = True
            shutil.copyfileobj(source, output, 64 * 1024)
        return {'schema': 'linuxit-copy-edit-result-v1', 'source_sha256': identity,
                'output_sha256': _sha(destination), 'path': str(destination),
                'pages': len(writer.pages), 'operations_applied': len(operations)}
    except BaseException:
        if created:
            destination.unlink()
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
