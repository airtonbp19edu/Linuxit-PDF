"""Transactional, password-aware reading sessions; original bytes stay untouched."""
from contextlib import contextmanager
import hashlib
import logging
import math
import os
from pathlib import Path
import shutil
import tempfile
import threading

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions as Permissions
from pypdf.errors import PdfReadError
from local_files import file_stamp

MAX_BYTES = 256 * 1024**2
MAX_PAGES = 20000


# Parser messages that mean the file was repaired while reading (E17). Only the fixed
# category names leave the worker; the messages themselves may carry untrusted text.
REPAIR_MARKERS = (('ref repaired', 'xref'), ('wrong pointing object', 'xref'), ('incorrect startxref', 'xref'),
                  ('xref table', 'xref'), ('not defined', 'objeto_ausente'), ('eof marker', 'fim_do_arquivo'),
                  ('truncated', 'fim_do_arquivo'), ('invalid pdf header', 'cabecalho'))


REPAIR_LABELS = {'xref': 'tabela de referências danificada', 'objeto_ausente': 'objeto ausente',
                 'fim_do_arquivo': 'fim do arquivo perdido', 'cabecalho': 'cabeçalho inválido',
                 'conteudo_ilegivel': 'conteúdo de página ilegível (página em branco)',
                 'pagina_ausente': 'página inexistente omitida', 'estrutura': 'estrutura irregular',
                 'desconhecido': 'problema não classificado'}


def describe_repairs(repairs):
    """Fixed Portuguese text for repair categories reported by the worker; unknown values are ignored."""
    return ', '.join(REPAIR_LABELS[r] for r in repairs if isinstance(r, str) and r in REPAIR_LABELS)


class _RepairLog(logging.Handler):
    def __init__(self):
        super().__init__(logging.WARNING);self.found = set()

    def note(self, text):
        text = str(text).lower()
        self.found.update(category for marker, category in REPAIR_MARKERS if marker in text)

    def emit(self, record):
        try:self.note(record.getMessage())
        except Exception:self.found.add('desconhecido')


def _check_pages(reader, repair=False):
    """Resolve every page and its content streams so missing or unreadable objects are noticed now.

    With repair=True (recovery consented), an unreadable or missing content stream is
    replaced by an empty one in memory, so the page stays but shows nothing invented.
    """
    from pypdf.generic import DecodedStreamObject, NameObject
    count = len(reader.pages)
    if not 1 <= count <= MAX_PAGES:
        raise DocumentError('A leitura aceita PDFs com 1–20000 páginas.')
    missing = emptied = 0
    for page in reader.pages:
        contents = page.get('/Contents')
        if contents is None:continue
        bad = False
        try:
            items = contents.get_object()
            refs = list(items) if isinstance(items, list) else [contents]
            for ref in refs:
                target = ref.get_object() if hasattr(ref, 'get_object') else ref
                if target is None or type(target).__name__ == 'NullObject' or not hasattr(target, 'get_data'):bad = True
                elif repair:target.get_data()  # recovery only: a truncated stream must decode now, not later
        except Exception:
            if not repair:raise
            bad = True
        if bad:
            missing += 1
            if repair:
                # PageObject is a copy; also change the cached object the writer will clone.
                empty = DecodedStreamObject();page[NameObject('/Contents')] = empty;emptied += 1
                if page.indirect_reference is not None:
                    page.indirect_reference.get_object()[NameObject('/Contents')] = empty
    return count, missing


def _normalise_page_tree(writer):
    """Drop page-tree entries that point to nothing and recount, so no blank page is invented."""
    from pypdf.generic import ArrayObject, NameObject, NumberObject
    def walk(node, depth=0):
        if depth > 64:raise DocumentError('Árvore de páginas profunda demais.')
        kids = node.get('/Kids')
        kids = kids.get_object() if kids is not None else ArrayObject()
        kept, total = ArrayObject(), 0
        for ref in kids:
            try:child = ref.get_object()
            except Exception:child = None
            if not hasattr(child, 'get'):continue
            if child.get('/Type') == '/Pages' or '/Kids' in child:
                pages = walk(child, depth + 1)
                if not pages:continue
                total += pages
            else:
                total += 1
            kept.append(ref)
        node[NameObject('/Kids')] = kept;node[NameObject('/Count')] = NumberObject(total)
        return total
    return walk(writer.root_object['/Pages'].get_object())


def _rebuilt(data):
    """Recovery candidates for files whose end was lost: an end marker, then a minimal trailer."""
    yield data + b'\n%%EOF\n'
    import re
    catalog = re.search(rb'(\d{1,7})\s+(\d{1,5})\s+obj\s*<<(?:(?!endobj).){0,4096}?/Type\s*/Catalog', data, re.S)
    if catalog:
        numbers = [int(n) for n in re.findall(rb'(?m)^\s*(\d{1,7})\s+\d{1,5}\s+obj\b', data)] or [0]
        yield (data + b'\ntrailer\n<< /Root ' + catalog.group(1) + b' ' + catalog.group(2) + b' R /Size '
               + str(max(numbers) + 1).encode() + b' >>\nstartxref\n0\n%%EOF\n')


class DocumentError(ValueError):
    """Fixed user-facing errors; credentials never enter exception messages."""


def _sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def prepare_document(path, request):
    if (not isinstance(request, dict) or set(request) != {'password', 'recover', 'view_dir'}
            or type(request['recover']) is not bool
            or not isinstance(request['password'], str) or len(request['password']) > 127
            or not isinstance(request['view_dir'], str)):
        raise DocumentError('Pedido de abertura inválido.')
    source = Path(path).resolve()
    folder = Path(request['view_dir'])
    if (not source.is_file() or not 0 < source.stat().st_size <= MAX_BYTES):
        raise DocumentError('Selecione um PDF não vazio de até 256 MiB.')
    if (folder.is_symlink() or not folder.is_dir() or not folder.name.startswith('linuxit-document-')):
        raise DocumentError('Pasta privada de leitura inválida.')
    folder = folder.resolve()
    target = folder / 'view.pdf'
    if target.exists() or target.is_symlink():
        raise DocumentError('A sessão de leitura já possui uma cópia.')
    stamp, identity = file_stamp(source), _sha(source)
    # Parser diagnostics may contain untrusted metadata. Only fixed messages
    # cross this isolated worker's protocol; restore the logger on every exit.
    logger = logging.getLogger('pypdf')
    previous = logger.disabled, logger.propagate, logger.level
    repairs = _RepairLog()
    logger.disabled, logger.propagate = False, False
    logger.setLevel(logging.WARNING);logger.addHandler(repairs)
    import warnings
    try:
        with source.open('rb') as stream, warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            reader, recovered = None, False
            try:
                reader = PdfReader(stream, strict=True)
                if not reader.is_encrypted:
                    _, missing = _check_pages(reader)
                    if missing:repairs.found.add('objeto_ausente')
            except PdfReadError:
                reader = None
            for item in caught:repairs.note(item.message)
            damaged = reader is None or bool(repairs.found)
            if damaged and not request['recover']:
                return {'status': 'recovery_required', 'repairs': sorted(repairs.found or {'estrutura'})}
            if reader is None:
                recovered = True
                stream.seek(0)
                try:
                    reader = PdfReader(stream, strict=False)
                    if not reader.is_encrypted and _check_pages(reader, repair=True)[1]:repairs.found.add('conteudo_ilegivel')
                except DocumentError:
                    raise
                except Exception:
                    # Lost end of file: retry in memory with an end marker / minimal trailer.
                    stream.seek(0);data = stream.read(MAX_BYTES + 1);reader = None
                    from io import BytesIO
                    for candidate in _rebuilt(data):
                        try:
                            attempt = PdfReader(BytesIO(candidate), strict=False)
                            if not attempt.is_encrypted and _check_pages(attempt, repair=True)[1]:repairs.found.add('conteudo_ilegivel')
                            reader = attempt;repairs.found.add('fim_do_arquivo');break
                        except DocumentError:
                            raise
                        except Exception:
                            continue
                    if reader is None:
                        raise DocumentError('Não foi possível recuperar este PDF: a estrutura de páginas está perdida ou não é um PDF.') from None
            elif damaged:
                recovered = True
                if not reader.is_encrypted and _check_pages(reader, repair=True)[1]:repairs.found.add('conteudo_ilegivel')
            if recovered and not repairs.found:repairs.found.add('estrutura')
            for item in caught:repairs.note(item.message)
            encrypted = reader.is_encrypted
            role = int(reader.decrypt(request['password'])) if encrypted else 2
            if not role:
                return {'status': 'password_invalid' if request['password'] else 'password_required'}
            count, _ = _check_pages(reader, repair=recovered)
            sizes = []
            for page in reader.pages:
                width, height = float(page.cropbox.width), float(page.cropbox.height)
                if not all(math.isfinite(x) and 0 < x <= 200000 for x in (width, height)):
                    raise DocumentError('O PDF possui dimensões de página inválidas.')
                sizes.append([height, width] if page.rotation % 180 else [width, height])
            md = reader.metadata or {}
            metadata = {name: str(md.get('/' + name.title()) or '')[:4096]
                        for name in ('title', 'author', 'subject', 'creator', 'producer')}
            flags = Permissions(int(reader.trailer['/Encrypt'].get('/P', 0))).to_dict() if encrypted else {}
            allowed = lambda bit: not encrypted or role == 2 or bool(flags.get(bit))
            permissions = {'copy': allowed('extract'), 'print': allowed('print'),
                           'accessibility': allowed('extract_text_and_graphics'),
                           'print_high_quality':allowed('print_to_representation'),
                           'modify':allowed('modify'),'annotate':allowed('add_or_modify'),
                           'fill_forms':allowed('fill_form_fields') or allowed('add_or_modify'),
                           'assemble':allowed('assemble_doc') or allowed('modify')}
            view = source
            if encrypted or recovered:
                # This is a disposable reading representation. Signature checks,
                # editing, saving the original and security operations still use source.
                writer = PdfWriter(clone_from=reader)
                declared = writer.root_object['/Pages'].get_object().get('/Count')
                if recovered and _normalise_page_tree(writer) != declared:
                    # Entries without a real page were dropped; the reading copy has only real pages.
                    repairs.found.add('pagina_ausente')
                try:
                    with target.open('xb') as output:
                        if os.name != 'nt':os.fchmod(output.fileno(), 0o600)
                        writer.write(output)
                    if target.stat().st_size > 512 * 1024**2:
                        raise DocumentError('A representação de leitura excede 512 MiB.')
                    with target.open('rb') as check_stream:
                        check = PdfReader(check_stream, strict=True)
                        if check.is_encrypted or len(check.pages) != len(writer.pages):
                            raise DocumentError('Não foi possível conferir a representação de leitura.')
                        count = len(check.pages)
                    view = target
                except BaseException:
                    target.unlink(missing_ok=True)
                    raise
            if file_stamp(source) != stamp or _sha(source) != identity:
                target.unlink(missing_ok=True)
                raise DocumentError('O PDF mudou durante a abertura. Abra o arquivo novamente.')
            return {'status': 'ready', 'schema': 'linuxit-document-session-v1',
                    'source_sha256': identity, 'source_stamp': stamp, 'read_path': str(view),
                    'pages': count, 'sizes': sizes, 'metadata': metadata,
                    'encrypted': encrypted, 'recovered': recovered, 'permissions': permissions,
                    'repairs': sorted(repairs.found) if recovered else []}
    except DocumentError:
        raise
    except Exception:
        target.unlink(missing_ok=True)
        raise DocumentError('Não foi possível abrir ou recuperar este PDF com a credencial informada.') from None
    finally:
        logger.removeHandler(repairs)
        logger.disabled, logger.propagate = previous[0], previous[1];logger.setLevel(previous[2])


class DocumentSession:
    """Leases keep a private reading file alive until active readers finish."""
    def __init__(self, path):
        self.source = str(Path(path).resolve())
        self.root = Path(tempfile.mkdtemp(prefix='linuxit-document-'))
        self.info = None
        self._password = ''
        self._lock = threading.RLock()
        self._users = 0
        self._path_users = {}
        self._retired_paths = set()
        self.closed = False

    @property
    def read_path(self):
        return self.info['read_path'] if self.info else self.source

    @contextmanager
    def lease(self,path=None):
        with self._lock:
            if self.closed:raise DocumentError('A sessão do documento foi encerrada.')
            self._users += 1
            path=str(Path(path).resolve()) if path is not None else self.read_path
            if path!=self.source and (not Path(path).is_relative_to(self.root.resolve()) or not Path(path).is_file()):
                self._users-=1
                raise DocumentError('Representação de leitura indisponível.')
            self._path_users[path]=self._path_users.get(path,0)+1
        try:
            yield path
        finally:
            with self._lock:
                self._users -= 1
                self._path_users[path]-=1
                if self._path_users[path]==0:
                    self._path_users.pop(path)
                    if path in self._retired_paths:
                        try:Path(path).unlink(missing_ok=True);self._retired_paths.discard(path)
                        except OSError:pass
                if self.closed and not self._users:self._cleanup()

    def replace_read_path(self,path):
        candidate=Path(path).resolve()
        with self._lock:
            if self.closed or not self.info:raise DocumentError('Sessão de leitura indisponível.')
            if not candidate.is_relative_to(self.root.resolve()) or not candidate.is_file():
                raise DocumentError('Representação de leitura deve ficar na pasta privada da sessão.')
            previous=self.read_path;self.info['read_path']=str(candidate)
            if previous!=self.source and previous!=str(candidate):
                if self._path_users.get(previous,0):self._retired_paths.add(previous)
                else:
                    try:Path(previous).unlink(missing_ok=True)
                    except OSError:self._retired_paths.add(previous)

    def prepare(self, password='', recover=False, cancel=None):
        from search_tasks import run_search_worker
        with self.lease():
            result = run_search_worker('document-open', self.source,
                {'password': password, 'recover': recover, 'view_dir': str(self.root)}, cancel, timeout=180)
            if result is None:return None
            if result.get('status') == 'ready':
                allowed = {Path(self.source), self.root / 'view.pdf'}
                if Path(result.get('read_path', '')).resolve() not in allowed:
                    raise DocumentError('O worker retornou uma sessão inválida.')
                self.info = result
                self._password=password
            return result

    def call(self, function, *args, **kwargs):
        with self.lease() as path:
            return function(path, *args, **kwargs)

    def edit_authorization(self):
        with self._lock:
            if self.closed or not self.info:raise DocumentError('Sessão de edição indisponível.')
            if not self.info['encrypted'] and not self.info['recovered']:return None
            return dict(password=self._password if self.info['encrypted'] else None,recover=self.info['recovered'])

    def assert_source_unchanged(self):
        if (not self.info or file_stamp(self.source)!=self.info['source_stamp']
                or _sha(self.source)!=self.info['source_sha256']):
            raise DocumentError('O PDF original mudou. Reabra o documento antes de continuar.')

    def _cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def close(self):
        with self._lock:
            self.closed = True
            self._password=''
            if not self._users:self._cleanup()
