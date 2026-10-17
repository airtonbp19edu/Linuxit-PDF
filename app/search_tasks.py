"""Cancelable JSON workers for own attachment and collection search services."""
import json
from pathlib import Path
import subprocess
import tempfile
import time

from platform_runtime import worker_python, subprocess_options

MAX_REPLY = 16 * 1024 * 1024


def run_search_worker(command, path, request, cancel=None, timeout=120):
    if command not in {'search-attachments', 'index-build', 'index-search'}:
        raise ValueError('Comando de pesquisa inválido.')
    if cancel is not None and cancel.is_set():
        return None
    argv = [worker_python(), '-X', 'utf8', str(Path(__file__).with_name('worker_cli.py')), command, str(path)]
    with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as error:
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=output, stderr=error, **subprocess_options())
        try:
            with proc.stdin:
                proc.stdin.write(json.dumps(request, ensure_ascii=True).encode('utf-8'))
            deadline = time.monotonic() + timeout
            while proc.poll() is None:
                if cancel is not None and cancel.is_set():
                    return None
                if time.monotonic() >= deadline:
                    raise RuntimeError('A pesquisa ou indexação excedeu o tempo disponível.')
                if cancel is not None:cancel.wait(.05)
                else:time.sleep(.05)
            if proc.returncode:
                error.seek(0)
                tail = error.read(65536).decode('utf-8', errors='replace').splitlines()
                last = tail[-1] if tail else ''
                kind, _, message = last.partition(': ')
                if kind in {'ValueError', 'FileExistsError', 'NotImplementedError'} and message:
                    raise RuntimeError(message)
                raise RuntimeError('Não foi possível concluir a pesquisa ou indexação.')
            output.seek(0)
            raw = output.read(MAX_REPLY + 1)
            if len(raw) > MAX_REPLY:
                raise RuntimeError('Resposta da pesquisa acima do limite.')
        finally:
            if proc.poll() is None:proc.kill()
            proc.wait()
    try:return json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError('O worker não retornou uma resposta de pesquisa válida.') from exc
