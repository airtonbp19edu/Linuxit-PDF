"""Explicit snapshots and recovery of local indexes; never removes a live lock."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import socket
import tempfile
import uuid

from collection_index import load_index, index_writer_lock, MAX_INDEX_BYTES, _sha, _publish_new_index


def _alive(pid):
    if os.name=='nt':
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.OpenProcess.restype=ctypes.c_void_p
        kernel.CloseHandle.argtypes=[ctypes.c_void_p]
        kernel.GetExitCodeProcess.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_ulong)]
        handle=kernel.OpenProcess(0x1000,False,pid)
        if not handle:return False if ctypes.get_last_error()==87 else None
        try:
            code=ctypes.c_ulong()
            return code.value==259 if kernel.GetExitCodeProcess(handle,ctypes.byref(code)) else None
        finally:kernel.CloseHandle(handle)
    try:os.kill(pid,0);return True
    except ProcessLookupError:return False
    except PermissionError:return None


def inspect_lock(index):
    lock=Path(index).with_name(Path(index).name+'.lock')
    if lock.is_symlink():raise ValueError('Trava simbólica exige revisão manual.')
    if not lock.exists():return dict(state='absent',removable=False)
    if lock.stat().st_size>8192:raise ValueError('Trava acima de 8KiB; revisão manual necessária.')
    raw=lock.read_bytes();identity=hashlib.sha256(raw).hexdigest()
    try:record=json.loads(raw)
    except (ValueError,UnicodeError):return dict(state='unknown',removable=False,sha256=identity)
    known=isinstance(record,dict) and record.get('host')==socket.gethostname() and type(record.get('pid')) is int and 0<record['pid']<2**32 and isinstance(record.get('token'),str) and len(record['token'])==32
    alive=_alive(record['pid']) if known else None
    return dict(state='dead' if alive is False else 'live' if alive else 'unknown',removable=alive is False,
                sha256=identity,pid=record.get('pid') if isinstance(record,dict) else None)


def remove_dead_lock(index,expected_sha256):
    current=inspect_lock(index)
    if not current['removable'] or current['sha256']!=expected_sha256:
        raise ValueError('A trava está ativa, mudou ou sua origem não pode ser confirmada.')
    lock=Path(index).with_name(Path(index).name+'.lock')
    if lock.is_symlink() or _sha(lock,8192)!=expected_sha256:raise ValueError('A trava mudou antes da remoção.')
    lock.unlink()
    return dict(removed=True)


def snapshot_index(source,destination):
    source=Path(source);destination=Path(destination).absolute()
    _,identity=load_index(source)
    if destination.is_symlink() or destination.exists() or not destination.parent.is_dir():
        raise ValueError('Escolha um arquivo de backup novo em pasta existente.')
    raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=identity:raise ValueError('O índice mudou durante o backup.')
    _write_new(raw,destination)
    return dict(path=str(destination),sha256=identity)


def _write_new(raw,destination):
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent,prefix='.linuxit-recovery-',delete=False) as stream:
            temporary=Path(stream.name);stream.write(raw);stream.flush();os.fsync(stream.fileno())
        _publish_new_index(temporary,destination)
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)


def restore_index(backup,destination,expected_sha256=None):
    backup=Path(backup);destination=Path(destination).absolute()
    _,identity=load_index(backup)
    if not destination.name.endswith('.linuxit-index.json') or not destination.parent.is_dir() or destination.is_symlink():
        raise ValueError('Destino deve ser um índice Linuxit sem link simbólico.')
    if backup.resolve()==destination.resolve():raise ValueError('Backup e destino devem ser diferentes.')
    raw=backup.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=identity:raise ValueError('O backup mudou durante a leitura.')
    saved=None;temporary=None
    with index_writer_lock(destination):
        actual=_sha(destination,MAX_INDEX_BYTES) if destination.exists() else None
        if actual!=expected_sha256:raise ValueError('O destino mudou; revise a recuperação antes de confirmar.')
        if actual:
            saved=destination.with_name(destination.name+'.before-recovery-'+uuid.uuid4().hex+'.bak')
            old=destination.read_bytes()
            if hashlib.sha256(old).hexdigest()!=actual:raise ValueError('O destino mudou durante a preservação.')
            _write_new(old,saved)
        try:
            with tempfile.NamedTemporaryFile(dir=destination.parent,prefix='.linuxit-recovery-',delete=False) as stream:
                temporary=Path(stream.name);stream.write(raw);stream.flush();os.fsync(stream.fileno())
            load_index(temporary)
            if actual:
                if destination.is_symlink() or _sha(destination,MAX_INDEX_BYTES)!=actual:raise ValueError('O destino mudou antes da recuperação.')
                os.replace(temporary,destination);temporary=None
            else:_publish_new_index(temporary,destination)
        finally:
            if temporary is not None:temporary.unlink(missing_ok=True)
    return dict(path=str(destination),sha256=identity,preserved_previous=str(saved) if saved else None)
