"""Versioned local text snapshots of explicitly selected PDFs; no directory scan."""
from datetime import datetime, timezone
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from search_matching import normalized, query_spans, validate_query
from search_tasks import run_search_worker

MAX_DOCUMENTS = 100
MAX_PAGES = 1000
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_INPUT_BYTES = 256 * 1024 * 1024
MAX_TEXT_BYTES = 16 * 1024 * 1024
MAX_INDEX_BYTES = 64 * 1024 * 1024
SCHEMA = 'linuxit-local-text-index-v1'


def _require(value, message):
    if not value:raise ValueError(message)


def _sha(path, limit=MAX_FILE_BYTES):
    _require(Path(path).is_file() and Path(path).stat().st_size <= limit, 'Arquivo ausente ou acima do limite de tamanho.')
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream, 'sha256').hexdigest()


def _body_hash(body):
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def load_index(path):
    path = Path(path)
    _require(path.is_file() and path.stat().st_size <= MAX_INDEX_BYTES, 'Índice ausente ou acima de 64 MiB.')
    raw = path.read_bytes()
    body = json.loads(raw)
    _require(isinstance(body, dict) and set(body) == {'schema', 'created_at_utc', 'documents', 'body_sha256'}
             and body['schema'] == SCHEMA, 'Arquivo não é um índice Linuxit compatível.')
    identity = body['body_sha256']
    _require(isinstance(identity, str) and identity == _body_hash({k: v for k, v in body.items() if k != 'body_sha256'}),
             'Conteúdo do índice não confere com seu hash.')
    _require(isinstance(body['created_at_utc'], str) and datetime.fromisoformat(body['created_at_utc']).utcoffset() is not None,
             'Data do índice inválida.')
    documents = body['documents']
    _require(isinstance(documents, list) and 1 <= len(documents) <= MAX_DOCUMENTS, 'Quantidade de documentos inválida.')
    names, pages, text_bytes, source_bytes = set(), 0, 0, 0
    for doc in documents:
        _require(isinstance(doc, dict) and set(doc) == {'path', 'sha256', 'bytes', 'pages'}, 'Entrada de índice inválida.')
        _require(isinstance(doc['path'], str) and Path(doc['path']).is_absolute() and doc['path'] not in names,
                 'Caminho de documento inválido ou repetido.')
        _require(isinstance(doc['sha256'], str) and re.fullmatch('[0-9a-f]{64}', doc['sha256']), 'Identidade de documento inválida.')
        _require(type(doc['bytes']) is int and 0 < doc['bytes'] <= MAX_FILE_BYTES, 'Tamanho de documento inválido.')
        _require(isinstance(doc['pages'], list) and 1 <= len(doc['pages']) <= MAX_PAGES
                 and all(isinstance(t, str) for t in doc['pages']), 'Páginas do índice inválidas.')
        names.add(doc['path']);pages += len(doc['pages']);source_bytes += doc['bytes']
        text_bytes += sum(len(t.encode('utf-8')) for t in doc['pages'])
    _require(pages <= MAX_PAGES and text_bytes <= MAX_TEXT_BYTES and source_bytes <= MAX_INPUT_BYTES,
             'Índice excede o orçamento de páginas, texto ou fontes.')
    return body, hashlib.sha256(raw).hexdigest()


def verify_document(path, expected):
    try:return _sha(path) == expected
    except (OSError, ValueError):return False


@contextmanager
def index_writer_lock(destination):
    """Cooperating writers serialize; abandoned locks require explicit review."""
    lock = destination.with_name(destination.name + '.lock')
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    except FileExistsError as exc:
        raise ValueError('Índice em atualização ou trava abandonada. Confira o outro processo antes de remover o arquivo .lock.') from exc
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump({'pid': os.getpid(), 'created_at_utc': datetime.now(timezone.utc).isoformat()}, stream)
        yield
    finally:
        lock.unlink(missing_ok=True)


def build_index(path, request):
    _require(isinstance(request, dict) and {'paths'} <= set(request) <= {'paths', 'expected_index_sha256'} and isinstance(request['paths'], list)
             and 1 <= len(request['paths']) <= MAX_DOCUMENTS and all(isinstance(p, str) for p in request['paths']),
             'Escolha de 1 a 100 PDFs explicitamente.')
    destination = Path(path).absolute()
    _require(destination.name.lower().endswith('.linuxit-index.json') and destination.parent.is_dir()
             and not destination.is_symlink(), 'Use um arquivo .linuxit-index.json em pasta existente, sem link simbólico.')
    with index_writer_lock(destination):
        return _build_index_locked(destination, request)


def _publish_new_index(temporary, destination):
    if os.name == 'nt':
        # Windows rename is atomic and fails if the target already exists.
        os.rename(temporary, destination)
    else:
        os.link(temporary, destination)


def _build_index_locked(destination, request):
    paths = [Path(p).resolve(strict=True) for p in request['paths']]
    _require(len(set(paths)) == len(paths) and destination.resolve() not in paths, 'Fontes repetidas ou destino sobre um PDF.')
    old_hash = None
    if destination.exists():
        _, old_hash = load_index(destination)
    if 'expected_index_sha256' in request:
        _require(request['expected_index_sha256'] == old_hash and old_hash is not None,
                 'O índice mudou desde a seleção da lista; abra a versão atual antes de repetir.')
    documents, page_count, source_bytes, text_bytes = [], 0, 0, 0
    for source in paths:
        identity = _sha(source)
        source_bytes += source.stat().st_size
        _require(source_bytes <= MAX_INPUT_BYTES, 'Fontes excedem 256 MiB no total.')
        with source.open('rb') as stream:
            reader = PdfReader(stream, strict=True)
            _require(not reader.is_encrypted, 'PDF criptografado não pode ser indexado neste contrato.')
            _require(0 < len(reader.pages) <= MAX_PAGES - page_count, 'Coleção excede 1000 páginas ou possui PDF sem páginas.')
            texts = []
            for page in reader.pages:
                text = page.extract_text() or ''
                text_bytes += len(text.encode('utf-8'));page_count += 1
                _require(text_bytes <= MAX_TEXT_BYTES, 'Texto extraído excede 16 MiB.')
                texts.append(text)
        _require(_sha(source) == identity, 'Um PDF mudou durante a indexação.')
        documents.append({'path': str(source), 'sha256': identity, 'bytes': source.stat().st_size, 'pages': texts})
    body = {'schema': SCHEMA, 'created_at_utc': datetime.now(timezone.utc).isoformat(), 'documents': documents}
    body['body_sha256'] = _body_hash(body)
    serialized = (json.dumps(body, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    _require(len(serialized) <= MAX_INDEX_BYTES, 'Índice gerado acima de 64 MiB.')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-index-', suffix='.json', delete=False) as output:
            temporary = Path(output.name);output.write(serialized)
        load_index(temporary)
        _require(all(verify_document(doc['path'], doc['sha256']) for doc in documents), 'Uma fonte mudou antes de salvar o índice.')
        if old_hash is None:
            # Same-directory hard link publishes the complete file exclusively.
            # Unsupported filesystems fail safely; no partially written index.
            _publish_new_index(temporary, destination)
        else:
            _require(_sha(destination, MAX_INDEX_BYTES) == old_hash and not destination.is_symlink(),
                     'O índice mudou durante a atualização; abra a versão atual antes de repetir.')
            os.replace(temporary, destination)
            temporary = None
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)
    return {'schema': 'linuxit-index-built-v1', 'path': str(destination), 'documents': len(documents),
            'pages': page_count, 'index_sha256': _sha(destination, MAX_INDEX_BYTES)}


def search_index(path, request):
    expected = {'query', 'match_case', 'ignore_accents', 'whole_words', 'mode', 'proximity_distance', 'max_hits'}
    _require(isinstance(request, dict) and set(request) == expected, 'Opções de consulta do índice inválidas.')
    validate_query(request['query'], request['mode'], request['proximity_distance'])
    _require(all(type(request[k]) is bool for k in ('match_case', 'ignore_accents', 'whole_words')),
             'Flags de consulta inválidas.')
    limit = request['max_hits'];_require(type(limit) is int and 1 <= limit <= 5000, 'Limite de resultados inválido.')
    body, identity = load_index(path)
    hits, stale = [], []
    limit_reached = False
    needle = ' '.join(normalized(request['query'], request['match_case'], request['ignore_accents']).split())
    for document in body['documents']:
        if not verify_document(document['path'], document['sha256']):
            stale.append({'path': document['path'], 'reason': 'Fonte alterada, ausente ou inacessível; atualize o índice.'})
            continue
        if limit_reached:continue  # Still inspect freshness of all documents.
        for page, text in enumerate(document['pages']):
            haystack = ' '.join(normalized(text, request['match_case'], request['ignore_accents']).split())
            for start, end in query_spans(haystack, needle, request['whole_words'], request['mode'], request['proximity_distance']):
                hits.append({'path': document['path'], 'source_sha256': document['sha256'], 'page': page,
                             'snippet': haystack[max(0, start - 50):end + 100][:180]})
                if len(hits) >= limit:
                    limit_reached = True;break
            if limit_reached:break
    _require(_sha(path, MAX_INDEX_BYTES) == identity, 'O índice mudou durante a consulta.')
    # Recheck after matching, before exposing any old text as current.
    changed = {doc['path'] for doc in body['documents'] if not verify_document(doc['path'], doc['sha256'])}
    known = {item['path'] for item in stale}
    stale.extend({'path': p, 'reason': 'Fonte alterada durante a consulta; atualize o índice.'} for p in sorted(changed - known))
    hits = [hit for hit in hits if hit['path'] not in changed]
    return {'schema': 'linuxit-index-search-v1', 'index_sha256': identity, 'hits': hits,
            'stale': stale, 'limit_reached': limit_reached, 'documents': len(body['documents'])}


def invoke_collection(command, path, request, cancel=None):
    _require(command in {'index-build', 'index-search'}, 'Comando de coleção inválido.')
    result = run_search_worker(command, path, request, cancel)
    if result is None:return None
    try:
        expected = 'linuxit-index-built-v1' if command == 'index-build' else 'linuxit-index-search-v1'
        _require(result['schema'] == expected and re.fullmatch('[0-9a-f]{64}', result['index_sha256']), 'Resposta inválida.')
        _require(type(result['documents']) is int and 1 <= result['documents'] <= MAX_DOCUMENTS, 'Quantidade inválida.')
        if command == 'index-build':
            _require(Path(result['path']).resolve() == Path(path).resolve() and type(result['pages']) is int
                     and 1 <= result['pages'] <= MAX_PAGES, 'Gravação não confirmada.')
        else:
            _require(isinstance(result['hits'], list) and len(result['hits']) <= request['max_hits']
                     and isinstance(result['stale'], list) and type(result['limit_reached']) is bool, 'Consulta inválida.')
            for hit in result['hits']:
                _require(isinstance(hit['path'], str) and Path(hit['path']).is_absolute()
                         and type(hit['page']) is int and 0 <= hit['page'] < MAX_PAGES
                         and isinstance(hit['snippet'], str) and re.fullmatch('[0-9a-f]{64}', hit['source_sha256']), 'Hit inválido.')
            for stale in result['stale']:
                _require(isinstance(stale['path'], str) and isinstance(stale['reason'], str), 'Entrada obsoleta inválida.')
        return result
    except (TypeError, KeyError, ValueError) as exc:
        raise RuntimeError('O worker não retornou uma confirmação de coleção válida.') from exc
