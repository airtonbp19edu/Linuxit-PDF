"""Cancelable JSON workers for bounded own search and image creation services."""
import json
import os
from pathlib import Path
import subprocess
import signal
import tempfile
import time

from platform_runtime import worker_python, subprocess_options

MAX_REPLY = 16 * 1024 * 1024


def run_search_worker(command, path, request, cancel=None, timeout=120):
    if command not in {'search-attachments', 'index-build', 'index-search', 'images-to-pdf', 'security-info', 'protect-copy', 'accessible-text', 'owner-copy', 'signature-info', 'copy-file'}:
        raise ValueError('Comando de pesquisa inválido.')
    if cancel is not None and cancel.is_set():
        return None
    payload = json.dumps(request, ensure_ascii=True).encode('utf-8')
    limit = 16384 if command in {'security-info', 'protect-copy', 'accessible-text', 'owner-copy'} else 65536 if command == 'search-attachments' else 256 * 1024
    if len(payload) > limit:
        raise ValueError('O pedido excede o limite permitido para esta operação.')
    argv = [worker_python(), '-X', 'utf8', str(Path(__file__).with_name('worker_cli.py')), command, str(path)]
    with tempfile.TemporaryDirectory(prefix='linuxit-worker-', ignore_cleanup_errors=True) as work, tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as error:
        options = subprocess_options()
        if os.name != 'nt':options['start_new_session'] = True
        environment = os.environ.copy()
        for name in ('TMPDIR','TEMP','TMP'):environment[name] = work
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=output, stderr=error, env=environment, **options)
        try:
            with proc.stdin:
                proc.stdin.write(payload)
            deadline = time.monotonic() + timeout
            while proc.poll() is None:
                if cancel is not None and cancel.is_set():
                    return None
                if time.monotonic() >= deadline:
                    raise RuntimeError('A operação excedeu o tempo disponível. Confira o destino antes de repetir uma gravação.')
                if cancel is not None:cancel.wait(.05)
                else:time.sleep(.05)
            if proc.returncode:
                error.seek(0)
                tail = error.read(65536).decode('utf-8', errors='replace').splitlines()
                last = tail[-1] if tail else ''
                kind, _, message = last.partition(': ')
                if kind in {'ValueError', 'FileExistsError', 'NotImplementedError'} and message:
                    raise RuntimeError(message)
                raise RuntimeError('Não foi possível concluir esta operação.')
            output.seek(0)
            raw = output.read(MAX_REPLY + 1)
            if len(raw) > MAX_REPLY:
                raise RuntimeError('Resposta da pesquisa acima do limite.')
        finally:
            if proc.poll() is None:
                try:
                    if os.name == 'nt':proc.kill()
                    else:os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:pass
            proc.wait()
    try:return json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError('O worker não retornou uma resposta de pesquisa válida.') from exc
