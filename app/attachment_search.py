"""Read embedded text/PDF in a bounded worker; never execute or export attachments."""
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
import subprocess

from pdf_attachments import _document, _entries, _name, _declared_size
from search_tasks import run_search_worker
from search_matching import normalized, query_spans, validate_query
from attachment_formats import OFFICE_SUFFIXES, HTML_SUFFIXES, extract_passive_text
from pypdf import PdfReader
from pypdf.errors import PyPdfError

MAX_FILES = 100
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 8 * 1024 * 1024
MAX_PAGES = 100
MAX_REPLY = 16 * 1024 * 1024
TEXT_SUFFIXES = {'.txt', '.csv', '.md', '.log', '.json', '.xml'}


def search_attachment_text(path, request):
    expected = {'query', 'match_case', 'ignore_accents', 'whole_words', 'mode', 'proximity_distance', 'max_hits'}
    if not isinstance(request, dict) or set(request) != expected:
        raise ValueError('Opções da busca em anexos inválidas.')
    query = request['query']
    validate_query(query, request['mode'], request['proximity_distance'])
    if any(type(request[k]) is not bool for k in ('match_case', 'ignore_accents', 'whole_words')):
        raise ValueError('Flags da busca em anexos inválidas.')
    limit = request['max_hits']
    if type(limit) is not int or not 1 <= limit <= 5000:
        raise ValueError('Limite da busca em anexos inválido.')
    needle = ' '.join(normalized(query, request['match_case'], request['ignore_accents']).split())
    hits, omissions, total = [], [], 0
    limit_reached = False
    with _document(path, enforce_copy=True) as (reader, identity):
        if needle:
            for index, (entry, origin, host_page) in _entries(reader):
                name = _name(entry)[:240]
                if index >= MAX_FILES:
                    omissions.append({'index': None, 'name': 'Anexos restantes', 'reason': 'Limite de 100 entradas por busca.'})
                    break
                suffix = Path(name).suffix.lower()
                if suffix not in TEXT_SUFFIXES | OFFICE_SUFFIXES | HTML_SUFFIXES | {'.pdf'}:
                    omissions.append({'index': index, 'name': name, 'reason': 'Formato não suportado pela busca textual.'})
                    continue
                try:
                    declared = _declared_size(entry)
                    if declared is not None and declared > MAX_FILE_BYTES:
                        raise ValueError('Tamanho declarado acima de 2 MiB.')
                    if total >= MAX_TOTAL_BYTES:
                        raise ValueError('Orçamento de 8 MiB de conteúdo esgotado.')
                    payload = entry.content
                    total += len(payload)
                    if len(payload) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                        raise ValueError('Conteúdo decodificado excede 2 MiB por anexo ou 8 MiB no total.')
                    payload_hash = hashlib.sha256(payload).hexdigest()
                    if suffix == '.pdf':
                        embedded = PdfReader(BytesIO(payload), strict=True)
                        if embedded.is_encrypted:
                            raise ValueError('PDF anexo criptografado não pesquisado.')
                        if len(embedded.pages) > MAX_PAGES:
                            raise ValueError('PDF anexo excede 100 páginas.')
                        # Stage the entire attachment before exposing its results: failed page
                        # extraction must not silently present only earlier pages as complete.
                        texts = [(page_no, page.extract_text() or '') for page_no, page in enumerate(embedded.pages)]
                    elif suffix in OFFICE_SUFFIXES | HTML_SUFFIXES:
                        text, partial = extract_passive_text(payload, suffix)
                        texts = [(None, text)]
                        if partial:
                            omissions.append({'index': index, 'name': name, 'reason': partial})
                    else:
                        text = payload.decode('utf-8-sig', errors='strict')
                        if '\0' in text:
                            raise ValueError('Conteúdo binário não pesquisado como UTF-8.')
                        texts = [(None, text)]
                    if sum(len(text.encode('utf-8')) for _, text in texts) > MAX_FILE_BYTES:
                        raise ValueError('Texto extraído acima de 2 MiB.')
                    staged = []
                    for page_no, text in texts:
                        haystack = ' '.join(normalized(text, request['match_case'], request['ignore_accents']).split())
                        for start, end in query_spans(haystack, needle, request['whole_words'],
                                                     request['mode'], request['proximity_distance']):
                            staged.append({'source': 'attachment', 'page': None, 'width': 0, 'height': 0,
                                           'rects': [], 'text': haystack[start:end][:180],
                                           'snippet': haystack[max(0, start - 50):end + 100][:180],
                                           'attachment_index': index, 'attachment_name': name,
                                           'attachment_sha256': payload_hash, 'attachment_page': page_no,
                                           'attachment_origin': origin, 'attachment_host_page': host_page,
                                           'source_sha256': identity})
                            if len(hits) + len(staged) >= limit:
                                break
                        if len(hits) + len(staged) >= limit:
                            break
                    hits.extend(staged)
                    if len(hits) >= limit:
                        limit_reached = True
                        break
                except (ValueError, TypeError, KeyError, UnicodeError, OSError, PyPdfError) as exc:
                    # A partial report must make unsupported/malformed entries visible.
                    omissions.append({'index': index, 'name': name, 'reason': str(exc)[:240] or type(exc).__name__})
    return {'schema': 'linuxit-attachment-search-v1', 'source_sha256': identity,
            'hits': hits, 'omissions': omissions, 'limit_reached': limit_reached,
            'complete': not omissions and not limit_reached}


def invoke_attachment_search(path, query, options, max_hits, cancel=None, timeout=120):
    """Wait with cancellation, bounded file-backed pipes and a terminated child."""
    empty = {'hits': [], 'omissions': [], 'limit_reached': False}
    if cancel is not None and cancel.is_set():
        return empty
    request = {key: getattr(options, key) for key in
               ('match_case', 'ignore_accents', 'whole_words', 'mode', 'proximity_distance')}
    request.update(query=query, max_hits=max_hits)
    report = run_search_worker('search-attachments', path, request, cancel, timeout)
    if report is None:
        return empty
    try:
        if (report['schema'] != 'linuxit-attachment-search-v1'
                or not re.fullmatch('[0-9a-f]{64}', report['source_sha256'])
                or not isinstance(report['hits'], list) or len(report['hits']) > max_hits
                or not isinstance(report['omissions'], list) or type(report['limit_reached']) is not bool
                or type(report['complete']) is not bool
                or report['complete'] != (not report['omissions'] and not report['limit_reached'])):
            raise ValueError('Invalid search reply')
        for hit in report['hits']:
            if (hit['source'] != 'attachment' or hit['page'] is not None or hit['rects'] != []
                    or hit['source_sha256'] != report['source_sha256']
                    or type(hit['attachment_index']) is not int or not 0 <= hit['attachment_index'] < MAX_FILES
                    or not isinstance(hit['attachment_name'], str) or not isinstance(hit['snippet'], str)
                    or not re.fullmatch('[0-9a-f]{64}', hit['attachment_sha256'])
                    or not (hit['attachment_page'] is None or type(hit['attachment_page']) is int and 0 <= hit['attachment_page'] < MAX_PAGES)):
                raise ValueError('Invalid attachment hit')
        for omission in report['omissions']:
            if not isinstance(omission['name'], str) or not isinstance(omission['reason'], str):
                raise ValueError('Invalid omission')
        return report
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError('O worker não retornou uma busca em anexos válida.') from exc
