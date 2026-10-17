"""Local folder preferences and complete, exclusive publication of new copies."""
import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile


def folders_path():
    return Path(os.environ.get('XDG_CONFIG_HOME') or Path.home()/'.config')/'linuxit-pdf'/'folders.json'


def read_folders():
    try:
        path = folders_path()
        if path.stat().st_size > 16384:return {}
        data = json.loads(path.read_text(encoding='utf-8'))
        return {k:v for k,v in data.items() if k in {'sync_folder','last_open','last_save'}
                and isinstance(v,str) and len(v) <= 4096 and '\x00' not in v and Path(v).is_absolute()}
    except (OSError, ValueError, TypeError, AttributeError):return {}


def remember_folder(key, directory):
    if key not in {'sync_folder','last_open','last_save'}:raise ValueError('Preferência de pasta inválida.')
    data = read_folders()
    if directory is None:data.pop(key,None)
    else:
        folder = Path(directory)
        if not folder.is_absolute() or not folder.is_dir() or len(str(folder)) > 4096:
            raise ValueError('Escolha uma pasta local disponível.')
        data[key] = str(folder)
    path = folders_path();path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd, staging = tempfile.mkstemp(prefix='.folders-',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as output:
            json.dump(data,output,ensure_ascii=False);output.write('\n');output.flush();os.fsync(output.fileno())
        os.replace(staging,path)
    finally:Path(staging).unlink(missing_ok=True)


def preferred_folder(operation='open', source=None):
    data = read_folders()
    choices = [data.get('sync_folder'),data.get('last_save' if operation=='save' else 'last_open')]
    if source:choices.append(str(Path(source).parent))
    for name in choices:
        try:
            if name and Path(name).is_dir():return name
        except OSError:pass
    return None


def file_stamp(path):
    s = Path(path).stat()
    return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def _rename_new(staging, destination):
    """Never fall back to a rename that can replace an existing destination."""
    if os.name == 'nt':
        os.rename(staging,destination)  # Windows rename rejects an existing target.
        return
    if sys.platform.startswith('linux'):
        libc = ctypes.CDLL(None,use_errno=True)
        rename = getattr(libc,'renameat2',None)
        if rename is not None:
            rename.argtypes = [ctypes.c_int,ctypes.c_char_p,ctypes.c_int,ctypes.c_char_p,ctypes.c_uint]
            rename.restype = ctypes.c_int
            if rename(-100,os.fsencode(staging),-100,os.fsencode(destination),1)==0:return
            code = ctypes.get_errno()
            if code not in (errno.ENOSYS,errno.EINVAL,errno.EOPNOTSUPP):
                if code == errno.EEXIST:raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
                raise OSError(code,os.strerror(code))
    # A hard link also publishes the already complete inode without replacement.
    try:os.link(staging,destination)
    except FileExistsError:
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.') from None
    except OSError as exc:
        raise OSError('A pasta não oferece publicação segura sem sobrescrita. Escolha outra pasta local.') from exc
    Path(staging).unlink()


def publish_copy(source, destination, before_publish=None):
    """The final name is absent until a complete copy is closed and checked.

    Hidden staging files may be visible to an external synchronizer. A forced
    kill can leave staging behind; no upload or remote transaction is asserted.
    """
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    fd, name = tempfile.mkstemp(prefix='.linuxit-publish-',suffix='.tmp',dir=destination.parent)
    staging = Path(name)
    try:
        with os.fdopen(fd,'wb') as output, Path(source).open('rb') as input_:
            shutil.copyfileobj(input_,output,65536);output.flush();os.fsync(output.fileno())
        if before_publish:before_publish()
        _rename_new(staging,destination)
    finally:staging.unlink(missing_ok=True)
    return destination


def copy_local_document(source, request):
    if (not isinstance(request,dict) or set(request) != {'destination','source_stamp'}
            or not isinstance(request['destination'],str) or '\x00' in request['destination']
            or not isinstance(request['source_stamp'],list) or len(request['source_stamp']) != 5
            or not all(type(x) is int for x in request['source_stamp'])):
        raise ValueError('Pedido de cópia local inválido.')
    source = Path(source);destination = Path(request['destination'])
    if not source.is_file() or source.stat().st_size > 512*1024**2:
        raise ValueError('A cópia local aceita arquivos disponíveis de até 512 MiB.')
    if destination.suffix.lower() != '.pdf' or not destination.parent.is_dir():
        raise ValueError('Escolha um nome .pdf novo em uma pasta disponível.')
    def identity(path):
        with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
    def unchanged():
        if file_stamp(source) != request['source_stamp']:
            raise ValueError('O PDF foi alterado externamente. Reabra o documento antes de salvar a cópia.')
    unchanged();digest = identity(source)
    def check():
        unchanged()
        if identity(source) != digest:raise ValueError('O PDF mudou durante a cópia; reabra o documento.')
    publish_copy(source,destination,check)
    return {'schema':'linuxit-local-copy-v1','path':str(destination),'source_sha256':digest,
            'output_sha256':digest,'saved_locally':True,'remote_sync_confirmed':False}
