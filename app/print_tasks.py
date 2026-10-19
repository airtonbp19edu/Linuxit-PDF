"""Cancelable preparation and atomic publication; printer submission is separate."""
import os
from pathlib import Path
import shutil
import tempfile

from search_tasks import run_search_worker


def prepare_print(path, destination, job, cancel=None):
    target = Path(destination)
    if target.exists():raise FileExistsError('Use um destino temporário novo para preparar impressão.')
    try:
        report = run_search_worker('prepare-print', path, job, cancel, timeout=600, destination=target)
        if report is None:return None
        if (report.get('schema') != 'linuxit-print-prepared-v1'
                or Path(report.get('path', '')).resolve() != target.resolve()
                or not target.is_file() or not target.stat().st_size):
            raise RuntimeError('Preparação não confirmou o PDF de saída.')
        return str(target)
    except BaseException:
        target.unlink(missing_ok=True)
        raise
    finally:
        if cancel is not None and cancel.is_set():target.unlink(missing_ok=True)


def publish_print_copy(prepared, destination, source):
    target, original = Path(destination), Path(source).resolve()
    if (target.is_symlink() or target.resolve() == original
            or (target.exists() and os.path.samefile(target, original))):
        raise ValueError('Salvar impressão não pode substituir o original ou um link simbólico.')
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.linuxit-print-', delete=False) as output:
            temporary = Path(output.name)
            with Path(prepared).open('rb') as stream:shutil.copyfileobj(stream, output)
            output.flush();os.fsync(output.fileno())
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)
    return f'PDF salvo em {target}'
