"""Portable worker adapter for explicit copy-only PDF changes."""
import json
from pathlib import Path
import subprocess
import re

from platform_runtime import worker_python, subprocess_options


def invoke_edit_worker(command, path, destination=None, request=None):
    if command not in {'edit-info', 'copy-edit'}:
        raise ValueError('Comando de alteração inválido.')
    if command == 'copy-edit' and (destination is None or not isinstance(request, dict)):
        raise ValueError('Informe um destino novo e um pedido de alterações.')
    argv = [worker_python(), '-X', 'utf8', str(Path(__file__).with_name('worker_cli.py')), command, str(path)]
    if command == 'copy-edit':
        argv.append(str(destination))
    try:
        result = subprocess.run(argv, input=json.dumps(request, ensure_ascii=True) if request is not None else None,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                encoding='utf-8', errors='replace', timeout=600, **subprocess_options())
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('A gravação excedeu o tempo disponível. Confira o destino antes de repetir.') from exc
    if result.returncode:
        last = next((line for line in reversed(result.stderr.splitlines()) if line.strip()), '')
        kind, _, message = last.partition(': ')
        if kind == 'FileExistsError':
            message = 'Escolha um nome novo. Nenhum arquivo existente será substituído.'
        elif kind not in {'ValueError', 'NotImplementedError'} or not message:
            message = 'Não foi possível preparar ou salvar a cópia deste PDF.'
        raise RuntimeError(message)
    try:
        data = json.loads(result.stdout)
        expected = 'linuxit-copy-edit-info-v1' if command == 'edit-info' else 'linuxit-copy-edit-result-v1'
        if data['schema'] != expected:
            raise ValueError('Unexpected edit protocol')
        if not isinstance(data['source_sha256'], str) or not re.fullmatch('[0-9a-f]{64}', data['source_sha256']):
            raise ValueError('Invalid source identity')
        if type(data['pages']) is not int or data['pages'] < 1:
            raise ValueError('Invalid page count')
        if command == 'edit-info':
            if not isinstance(data['text_fields'], list) or not all(isinstance(f, dict)
                    and isinstance(f['name'], str) and isinstance(f['value'], str)
                    and type(f['read_only']) is bool for f in data['text_fields']):
                raise ValueError('Invalid text fields')
        elif (data['source_sha256'] != request['source_sha256']
                or Path(data['path']).resolve() != Path(destination).resolve()
                or data['operations_applied'] != len(request['operations'])
                or not re.fullmatch('[0-9a-f]{64}', data['output_sha256'])):
            raise ValueError('Incomplete copy confirmation')
        return data
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError('O worker não retornou uma confirmação de alteração válida.') from exc
