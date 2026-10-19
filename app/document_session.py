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
    previous = logger.disabled
    logger.disabled = True
    try:
        with source.open('rb') as stream:
            try:
                reader = PdfReader(stream, strict=True)
                recovered = False
            except PdfReadError:
                if not request['recover']:
                    return {'status': 'recovery_required'}
                stream.seek(0)
                reader = PdfReader(stream, strict=False)
                recovered = True
            encrypted = reader.is_encrypted
            role = int(reader.decrypt(request['password'])) if encrypted else 2
            if not role:
                return {'status': 'password_invalid' if request['password'] else 'password_required'}
            count = len(reader.pages)
            if not 1 <= count <= MAX_PAGES:
                raise DocumentError('A leitura aceita PDFs com 1–20000 páginas.')
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
                try:
                    with target.open('xb') as output:
                        if os.name != 'nt':os.fchmod(output.fileno(), 0o600)
                        writer.write(output)
                    if target.stat().st_size > 512 * 1024**2:
                        raise DocumentError('A representação de leitura excede 512 MiB.')
                    with target.open('rb') as check_stream:
                        check = PdfReader(check_stream, strict=True)
                        if check.is_encrypted or len(check.pages) != count:
                            raise DocumentError('Não foi possível conferir a representação de leitura.')
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
                    'encrypted': encrypted, 'recovered': recovered, 'permissions': permissions}
    except DocumentError:
        raise
    except Exception:
        target.unlink(missing_ok=True)
        raise DocumentError('Não foi possível abrir ou recuperar este PDF com a credencial informada.') from None
    finally:
        logger.disabled = previous


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
