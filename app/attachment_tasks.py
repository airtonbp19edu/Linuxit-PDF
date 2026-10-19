"""Portable attachment panel coordination; callbacks are delivered by the UI runner."""
import json
from pathlib import Path
import subprocess
import unicodedata

from platform_runtime import worker_python, subprocess_options

WORKER = Path(__file__).with_name('worker_cli.py')


def display_attachment_name(name):
    return ''.join('\ufffd' if unicodedata.category(char).startswith('C') else char for char in str(name))


def _worker_error(stderr):
    last = next((line for line in reversed(stderr.splitlines()) if line.strip()), '')
    kind, _, message = last.partition(': ')
    fixed = {'FileExistsError': 'Já existe um arquivo com esse nome. Escolha outra pasta.',
             'FileNotFoundError': 'O arquivo ou a pasta não está mais disponível.',
             'PermissionError': 'Não foi possível acessar o arquivo ou gravar na pasta escolhida.',
             'NotADirectoryError': 'Escolha uma pasta existente para salvar o anexo.',
             'PdfReadError': 'Não foi possível ler os anexos deste PDF.'}
    if kind in fixed:
        return fixed[kind]
    if kind in {'ValueError', 'RuntimeError', 'NotImplementedError'} and message:
        return message
    return 'Não foi possível concluir a operação com os anexos deste PDF.'


def invoke_attachment_worker(command, path, directory=None, request=None):
    if command not in {'attachments', 'extract-attachment'}:
        raise ValueError('Comando de anexos inválido.')
    argv = [worker_python(), '-X', 'utf8', str(WORKER), command, str(path)]
    if command == 'extract-attachment':
        argv.append(str(directory))
    try:
        proc = subprocess.run(argv, input=json.dumps(request) if request is not None else None,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                              encoding='utf-8', errors='replace', timeout=600, **subprocess_options())
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError('A operação com anexos excedeu o tempo disponível. Confira a pasta de destino antes de tentar novamente.') from exc
    if proc.returncode:
        raise RuntimeError(_worker_error(proc.stderr)) from subprocess.CalledProcessError(
            proc.returncode, argv, output=proc.stdout, stderr=proc.stderr)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError('Não foi possível ler o resultado da operação com anexos.') from exc


class AttachmentPanelController:
    def __init__(self, runner, on_change, invoke=invoke_attachment_worker):
        self.runner, self.on_change, self.invoke = runner, on_change, invoke
        self.document = None
        self.session = None
        self.allow_extract = True
        self.generation = 0
        self.closed = False
        self.items = []
        self.source_sha256 = None
        self.selected_index = None
        self.loading = self.extracting = self.requested = False
        self.message = 'Abra um PDF para consultar os anexos.'
        self.error = False
        self._job_id = 0

    def _publish(self):
        if not self.closed:
            self.on_change({'document': self.document, 'items': [dict(item) for item in self.items],
                            'selected_index': self.selected_index, 'loading': self.loading,
                            'extracting': self.extracting, 'message': self.message, 'error': self.error,
                            'can_extract': self.selection_token() is not None and not self.extracting,
                            'can_refresh': self.document is not None and not self.loading})

    def set_document(self, path, session=None, allow_extract=True):
        if self.closed:
            return
        self.generation += 1
        self.runner.invalidate('attachments-list')
        self.document = str(path) if path is not None else None
        self.session, self.allow_extract = session, bool(allow_extract)
        self.items, self.source_sha256, self.selected_index = [], None, None
        self.loading = self.requested = self.error = False
        self.message = 'Clique em Atualizar para consultar os anexos.' if path else 'Abra um PDF para consultar os anexos.'
        self._publish()

    def ensure_loaded(self):
        if not self.requested:
            self.refresh()

    def refresh(self):
        if self.closed or self.document is None or self.loading:
            return
        self.generation += 1
        generation, path, session = self.generation, self.document, self.session
        self.items, self.source_sha256, self.selected_index = [], None, None
        self.loading = self.requested = True
        self.error = False
        self.message = 'Carregando anexos…'
        self._publish()
        def current():
            return not self.closed and self.generation == generation
        def task():
            if not current():
                raise RuntimeError('Consulta de anexos cancelada.')
            return session.call(lambda read_path:self.invoke('attachments',read_path)) if session else self.invoke('attachments', path)
        def failed(exc):
            if current():
                self.loading, self.error = False, True
                self.message = str(exc)
                self._publish()
        def loaded(data):
            if not current():
                return
            try:
                if data['schema'] != 'linuxit-attachments-v1':
                    raise ValueError('Resultado de anexos inválido.')
                self.source_sha256 = data['source_sha256']
                self.items = data['attachments']
                self.selected_index = next((item['index'] for item in self.items if item['filename_allowed']), None)
            except (KeyError, TypeError, ValueError) as exc:
                self.items, self.source_sha256, self.selected_index = [], None, None
                failed(RuntimeError('Não foi possível ler a lista de anexos.'))
                return
            self.loading = False
            self.message = f'{len(self.items)} anexo(s).' if self.items else 'Nenhum anexo encontrado neste catálogo.'
            if data.get('portfolio'):self.message += ' Portfólio: arquivos incorporados; layout e campos adicionais não interpretados.'
            self._publish()
        try:
            if self.runner.submit('attachments-list', task, loaded, failed) is None:
                failed(RuntimeError('Consulta de anexos indisponível.'))
        except RuntimeError as exc:
            failed(exc)

    def select(self, index):
        if self.closed:
            return
        self.selected_index = index if any(item['index'] == index for item in self.items) else None
        self._publish()

    def selection_token(self):
        if self.closed or self.loading or not self.document or not self.source_sha256 or not self.allow_extract:
            return None
        if not any(item['index'] == self.selected_index and item['filename_allowed'] for item in self.items):
            return None
        return self.generation, self.document, self.selected_index, self.source_sha256

    def extract(self, directory, selection):
        if self.closed or self.extracting or selection is None or selection != self.selection_token():
            return False
        generation, path, index, identity = selection
        session = self.session
        self._job_id += 1
        job_id = self._job_id
        self.extracting, self.error = True, False
        self.message = 'Salvando anexo…'
        self._publish()
        def task():
            if self.closed:
                raise RuntimeError('Extração de anexo cancelada.')
            def extract(read_path):return self.invoke('extract-attachment',read_path,directory,
                                                      {'index':index,'source_sha256':identity})
            return session.call(extract) if session else extract(path)
        def finish(result=None, error=None):
            if self.closed or self._job_id != job_id:
                return
            self.extracting = False
            if self.generation == generation:
                if error is None and (not isinstance(result, dict) or
                                      result.get('schema') != 'linuxit-extracted-attachment-v1' or
                                      result.get('source_sha256') != identity or not result.get('path')):
                    error = RuntimeError('Não foi possível confirmar a extração. Confira a pasta de destino.')
                self.error = error is not None
                self.message = str(error) if error else f"Anexo salvo em {result['path']}"
            self._publish()
        try:
            if self.runner.submit('attachment-extract', task, lambda value: finish(result=value),
                                  lambda exc: finish(error=exc)) is None:
                finish(error=RuntimeError('Extração de anexo indisponível.'))
                return False
        except RuntimeError as exc:
            finish(error=exc)
            return False
        return True

    def close(self):
        self.closed = True
        self.generation += 1
        self.runner.invalidate('attachments-list')
        self.runner.invalidate('attachment-extract')
