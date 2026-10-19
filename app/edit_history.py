"""Transactional draft history: validate real copies before advancing the cursor."""
from concurrent.futures import CancelledError
from copy import deepcopy
from pathlib import Path
import tempfile
import threading

from edit_tasks import invoke_edit_worker


class EditSession:
    MAX_STEPS = 100

    def __init__(self, path, *, cancel=None, invoke=invoke_edit_worker, auth=None):
        self.path = str(path)
        self.cancel = cancel if cancel is not None else threading.Event()
        self._auth=deepcopy(auth)
        def transport(command,path,destination=None,request=None,**kwargs):
            if self._auth is None:
                if destination is None and request is None:return invoke(command,path,**kwargs)
                return invoke(command,path,destination,request,**kwargs)
            payload={**(request or {}),'auth':self._auth}
            return invoke(command,path,destination,payload,**kwargs)
        self._invoke = transport
        self._temp = tempfile.TemporaryDirectory(prefix='linuxit-edit-draft-')
        self._timeline, self.cursor, self._serial = [], 0, 0
        self._working = False
        self.preview = None
        try:
            self.info = self._invoke('edit-info', self.path, cancel=self.cancel)
            self.identity = self.info['source_sha256']
        except BaseException:
            self._temp.cleanup()
            raise

    @property
    def operations(self):return deepcopy(self._timeline[:self.cursor])

    @property
    def can_undo(self):return self.cursor > 0

    @property
    def can_redo(self):return self.cursor < len(self._timeline)

    def _check(self):
        if self.cancel.is_set():raise CancelledError()

    def _change(self, timeline, cursor):
        self._working = True
        target = None
        try:
            self._check()
            operations = deepcopy(timeline[:cursor])
            if operations:
                self._serial += 1
                target = Path(self._temp.name) / f'draft-{self._serial}.pdf'
                self._invoke('copy-edit', self.path, target,
                             {'source_sha256':self.identity, 'operations':operations}, cancel=self.cancel)
                info = self._invoke('edit-info', target, cancel=self.cancel)
            else:
                info = self._invoke('edit-info', self.path, cancel=self.cancel)
                if info['source_sha256'] != self.identity:raise ValueError('O PDF mudou. Reabra o editor.')
            self._check()
            if self.preview is not None:self.preview.unlink(missing_ok=True)
            self._timeline, self.cursor, self.info, self.preview = deepcopy(timeline), cursor, info, target
            target = None
        finally:
            if target is not None:target.unlink(missing_ok=True)
            self._working = False
            if self.cancel.is_set():self._temp.cleanup()

    def add(self, operation):
        self._check()
        if self.cursor >= self.MAX_STEPS:raise ValueError('O rascunho atingiu o limite de 100 alterações.')
        timeline = self._timeline[:self.cursor] + [deepcopy(operation)]
        self._change(timeline, len(timeline))

    def undo(self):
        self._check()
        if not self.can_undo:raise ValueError('Não há alteração para desfazer.')
        self._change(self._timeline, self.cursor - 1)

    def redo(self):
        self._check()
        if not self.can_redo:raise ValueError('Não há alteração para refazer.')
        self._change(self._timeline, self.cursor + 1)

    def save(self, destination):
        self._working = True
        try:
            self._check()
            if not self.cursor:raise ValueError('Prepare ao menos uma alteração antes de salvar.')
            return self._invoke('copy-edit', self.path, destination,
                                {'source_sha256':self.identity, 'operations':self.operations}, cancel=self.cancel)
        finally:
            self._working = False
            if self.cancel.is_set():self._temp.cleanup()

    def close(self):
        self.cancel.set()
        self._auth=None
        if not self._working:self._temp.cleanup()
