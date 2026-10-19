"""Independent extraction of catalog and page attachments; no attachment execution."""
from contextlib import contextmanager
import hashlib
from pathlib import Path
import re
import unicodedata

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, EmbeddedFile, NullObject
from pypdf.constants import UserAccessPermissions

MAX_ATTACHMENTS = 1000
MAX_ATTACHMENT_BYTES = 64 * 1024 * 1024
MAX_TREE_DEPTH = 64
MAX_TREE_NODES = 4000


def _stream_hash(stream):
    position = stream.tell()
    try:
        stream.seek(0)
        return hashlib.file_digest(stream, 'sha256').hexdigest()
    finally:
        stream.seek(position)


@contextmanager
def _document(path, expected_sha256=None, enforce_copy=False):
    with Path(path).open('rb') as stream:
        identity = _stream_hash(stream)
        if expected_sha256 is not None and identity != expected_sha256:
            raise ValueError('O PDF mudou desde a listagem dos anexos. Liste novamente.')
        reader = PdfReader(stream, strict=True)
        if reader.is_encrypted:
            role=reader.decrypt('')
            if not role:raise ValueError('O PDF exige senha; abra-o na sessão de leitura antes de extrair anexos.')
            if enforce_copy and int(role)!=2 and not UserAccessPermissions(int(reader.trailer['/Encrypt'].get('/P',0))).to_dict().get('extract'):
                raise PermissionError('As permissões deste PDF não autorizam extrair anexos.')
        if '/Collection' in reader.root_object and not isinstance(reader.root_object['/Collection'],DictionaryObject):
            raise ValueError('Estrutura de portfólio /Collection inválida.')
        names = reader.root_object.get('/Names')
        if names is not None and not isinstance(names, NullObject):
            names = names.get_object()
            if not isinstance(names, DictionaryObject):
                raise ValueError('Estrutura /Names de anexos inválida.')
            tree = names.get('/EmbeddedFiles')
            if tree is not None and not isinstance(tree, NullObject):
                tree = tree.get_object()
                if not isinstance(tree, DictionaryObject):
                    raise ValueError('Estrutura /EmbeddedFiles inválida.')
        yield reader, identity
        if _stream_hash(stream) != identity:
            raise ValueError('O PDF foi alterado durante a leitura dos anexos.')


def _catalog_entries(reader):
    names = reader.root_object.get('/Names')
    if names is None or isinstance(names, NullObject):
        return
    tree = names.get_object().get('/EmbeddedFiles')
    if tree is None or isinstance(tree, NullObject):
        return
    visited = set()
    def walk(value, depth=0):
        node = value.get_object()
        if not isinstance(node, DictionaryObject):
            raise ValueError('Nó da árvore de anexos inválido.')
        if id(node) in visited:
            raise ValueError('Árvore de anexos contém ciclo ou referência repetida.')
        visited.add(id(node))
        if depth > MAX_TREE_DEPTH or len(visited) > MAX_TREE_NODES:
            raise ValueError('Árvore de anexos excede o limite de profundidade ou nós.')
        if '/Kids' in node and '/Names' in node:
            raise ValueError('Nó de anexos mistura /Kids e /Names.')
        if '/Kids' in node:
            kids = node['/Kids']
            if not isinstance(kids, ArrayObject):
                raise ValueError('Filhos /Kids de anexos inválidos.')
            for child in kids:
                yield from walk(child, depth + 1)
        elif '/Names' in node:
            pairs = node['/Names']
            if not isinstance(pairs, ArrayObject) or len(pairs) % 2:
                raise ValueError('Lista /Names de anexos inválida.')
            for offset in range(0, len(pairs), 2):
                name, spec = pairs[offset], pairs[offset + 1].get_object()
                if not isinstance(name, str) or not isinstance(spec, DictionaryObject):
                    raise ValueError('Par nome/arquivo de anexo inválido.')
                yield EmbeddedFile(name=name, pdf_object=spec, parent=pairs), 'catalog', None
    yield from walk(tree)


def _all_entries(reader):
    yield from _catalog_entries(reader)
    for page_number, page in enumerate(reader.pages):
        annotations = page.get('/Annots')
        if annotations is None or isinstance(annotations, NullObject):
            continue
        annotations = annotations.get_object()
        if not isinstance(annotations, ArrayObject):
            raise ValueError('Lista de anotações inválida.')
        for reference in annotations:
            annotation = reference.get_object()
            if not isinstance(annotation, DictionaryObject):
                raise ValueError('Anotação inválida.')
            if annotation.get('/Subtype') != '/FileAttachment':
                continue
            spec = annotation.get('/FS')
            spec = spec.get_object() if spec is not None else None
            if not isinstance(spec, DictionaryObject):
                raise ValueError('Anexo de anotação sem especificação de arquivo válida.')
            name = spec.get('/UF') or spec.get('/F')
            if not isinstance(name, str):
                raise ValueError('Anexo de anotação sem nome válido.')
            yield EmbeddedFile(name=name, pdf_object=spec), 'annotation', page_number


def _entries(reader):
    for index, item in enumerate(_all_entries(reader)):
        if index >= MAX_ATTACHMENTS:
            raise ValueError(f'O PDF excede o limite de {MAX_ATTACHMENTS} anexos.')
        yield index, item


def _filename(name):
    if not isinstance(name, str) or not name or name in {'.', '..'}:
        raise ValueError('Nome de anexo vazio ou inválido.')
    if any(char in '<>:"/\\|?*' or unicodedata.category(char).startswith('C') for char in name):
        raise ValueError('Nome de anexo contém caminho ou caracteres não permitidos.')
    if name[0] == ' ' or name[-1] in '. ' or len(name.encode('utf-8')) > 240:
        raise ValueError('Nome de anexo tem espaço nas extremidades, termina em ponto ou excede 240 bytes UTF-8.')
    stem = name.split('.')[0].rstrip(' ').upper()
    if stem in {'CON', 'PRN', 'AUX', 'NUL', 'CLOCK$', 'CONIN$', 'CONOUT$'} or re.fullmatch(r'(COM|LPT)[1-9¹²³]', stem):
        raise ValueError('Nome de anexo reservado pelo sistema.')
    return name


def _name(entry):
    return str(entry.alternative_name or entry.name)


def _declared_size(entry):
    value = entry.size
    return int(value) if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def list_attachments(path):
    """List metadata without decoding payloads. Sizes are declared, not measured."""
    items = []
    with _document(path) as (reader, identity):
        for index, (entry, origin, page) in _entries(reader):
            name = _name(entry)
            try:
                _filename(name)
                filename_error = None
            except ValueError as exc:
                filename_error = str(exc)
            items.append({'index': index, 'name': name, 'declared_size_bytes': _declared_size(entry),
                          'filename_allowed': filename_error is None, 'filename_error': filename_error,
                          'origin': origin, 'page': page})
        portfolio = '/Collection' in reader.root_object
    return {'schema': 'linuxit-attachments-v1', 'source_sha256': identity,
            'supported_scope': 'catalog_name_tree_and_page_annotations', 'attachments': items,
            'portfolio':portfolio,
            'portfolio_scope':'Arquivos incorporados; layout, ordenação e campos de coleção não interpretados.' if portfolio else None}


def extract_attachment(path, index, directory, *, source_sha256):
    """Extract one listed entry by index/hash; existing files are never replaced."""
    if type(index) is not int or not 0 <= index < MAX_ATTACHMENTS:
        raise ValueError('Índice de anexo inválido.')
    if not isinstance(source_sha256, str) or not re.fullmatch('[0-9a-f]{64}', source_sha256):
        raise ValueError('Informe o SHA-256 da listagem atual do PDF.')
    destination = Path(directory).resolve(strict=True)
    if not destination.is_dir():
        raise NotADirectoryError('O destino deve ser uma pasta existente escolhida para extração.')
    with _document(path, source_sha256, enforce_copy=True) as (reader, identity):
        selected = next((item[0] for number, item in _entries(reader) if number == index), None)
        if selected is None:
            raise ValueError('Anexo não encontrado; liste os anexos novamente.')
        name = _filename(_name(selected))
        declared = _declared_size(selected)
        if declared is not None and declared > MAX_ATTACHMENT_BYTES:
            raise ValueError('O tamanho declarado do anexo excede 64 MiB.')
        content = selected.content
        if len(content) > MAX_ATTACHMENT_BYTES:
            raise ValueError('O conteúdo do anexo excede 64 MiB.')
    # Decode, validate and recheck source identity before creating a destination.
    target = destination / name
    created = False
    try:
        with target.open('xb') as output:
            created = True
            output.write(content)
    except BaseException:
        if created:
            target.unlink()
        raise
    return {'schema': 'linuxit-extracted-attachment-v1', 'index': index, 'name': name,
            'path': str(target), 'size_bytes': len(content),
            'sha256': hashlib.sha256(content).hexdigest(), 'source_sha256': identity}
