"""Independent, local extraction of flat catalog EmbeddedFiles; no attachment execution."""
from contextlib import contextmanager
import hashlib
from pathlib import Path
import re
import unicodedata

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from pypdf.generic import DictionaryObject, NullObject

MAX_ATTACHMENTS = 1000
MAX_ATTACHMENT_BYTES = 64 * 1024 * 1024


def _stream_hash(stream):
    position = stream.tell()
    try:
        stream.seek(0)
        return hashlib.file_digest(stream, 'sha256').hexdigest()
    finally:
        stream.seek(position)


@contextmanager
def _document(path, expected_sha256=None):
    with Path(path).open('rb') as stream:
        identity = _stream_hash(stream)
        if expected_sha256 is not None and identity != expected_sha256:
            raise ValueError('O PDF mudou desde a listagem dos anexos. Liste novamente.')
        reader = PdfReader(stream, strict=True)
        if reader.is_encrypted and not reader.decrypt(''):
            raise ValueError('O PDF exige senha; extração com senha não é suportada neste contrato.')
        if '/Collection' in reader.root_object:
            raise NotImplementedError('Portfólios PDF ainda não são suportados.')
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
                if '/Kids' in tree:
                    raise NotImplementedError('Árvores de anexos com /Kids ainda não são suportadas.')
        yield reader, identity
        if _stream_hash(stream) != identity:
            raise ValueError('O PDF foi alterado durante a leitura dos anexos.')


def _entries(reader):
    for index, entry in enumerate(reader.attachment_list):
        if index >= MAX_ATTACHMENTS:
            raise ValueError(f'O PDF excede o limite de {MAX_ATTACHMENTS} anexos.')
        yield index, entry


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
        for index, entry in _entries(reader):
            name = _name(entry)
            try:
                _filename(name)
                filename_error = None
            except ValueError as exc:
                filename_error = str(exc)
            items.append({'index': index, 'name': name, 'declared_size_bytes': _declared_size(entry),
                          'filename_allowed': filename_error is None, 'filename_error': filename_error})
    return {'schema': 'linuxit-attachments-v1', 'source_sha256': identity,
            'supported_scope': 'flat_catalog_embedded_files', 'attachments': items}


def extract_attachment(path, index, directory, *, source_sha256):
    """Extract one listed entry by index/hash; existing files are never replaced."""
    if type(index) is not int or not 0 <= index < MAX_ATTACHMENTS:
        raise ValueError('Índice de anexo inválido.')
    if not isinstance(source_sha256, str) or not re.fullmatch('[0-9a-f]{64}', source_sha256):
        raise ValueError('Informe o SHA-256 da listagem atual do PDF.')
    destination = Path(directory).resolve(strict=True)
    if not destination.is_dir():
        raise NotADirectoryError('O destino deve ser uma pasta existente escolhida para extração.')
    with _document(path, source_sha256) as (reader, identity):
        selected = next((entry for number, entry in _entries(reader) if number == index), None)
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
