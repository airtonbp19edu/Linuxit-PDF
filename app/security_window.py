"""Explicit security operations; no password persistence or command-line secrets."""
from pathlib import Path
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from async_core import BackgroundRunner
from pdf_security import invoke_security, PERMISSION_FLAGS


class SecurityWindow(Gtk.Window):
    def __init__(self, parent, path=None):
        super().__init__(title='Senhas e permissões PDF', transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(780, 600)
        self.runner = BackgroundRunner(workers=1);self.cancel = threading.Event()
        self.closed = self.busy = False;self.info = None;self.secrets = {};self.controls = []
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10);box.set_border_width(14);self.add(box)
        self.path = Gtk.Entry();self.path.get_accessible().set_name('PDF para inspeção ou proteção')
        row = Gtk.Box(spacing=6);row.pack_start(self.path, True, True, 0)
        browse = Gtk.Button(label='Escolher PDF…');browse.connect('clicked', self._browse);row.pack_start(browse, False, False, 0)
        box.pack_start(row, False, False, 0);self.controls += [self.path, browse]
        grid = Gtk.Grid(column_spacing=10, row_spacing=8);box.pack_start(grid, False, False, 0)
        for i, (key, label) in enumerate([('inspect','Senha atual do PDF:'), ('user','Nova senha de abertura:'),
                ('user_confirm','Confirmar senha de abertura:'), ('owner','Nova senha de proprietário:'), ('owner_confirm','Confirmar senha de proprietário:')]):
            field = Gtk.Entry();field.set_visibility(False);field.set_input_purpose(Gtk.InputPurpose.PASSWORD);field.set_hexpand(True)
            field.get_accessible().set_name(label.rstrip(':'));self.secrets[key] = field;self.controls.append(field)
            text = Gtk.Label(label=label, xalign=0);text.set_mnemonic_widget(field)
            grid.attach(text, 0, i, 1, 1);grid.attach(field, 1, i, 1, 1)
        hint = Gtk.Label(label='Novas senhas: 8–64 caracteres ASCII imprimíveis, diferentes entre si. Guarde a senha de proprietário.', xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint, False, False, 0)
        permission_box = Gtk.Grid(column_spacing=10, row_spacing=8);self.permissions = {}
        labels = ['Imprimir', 'Copiar', 'Modificar', 'Anotar', 'Preencher', 'Montar páginas']
        for i, (key, label) in enumerate(zip(PERMISSION_FLAGS, labels)):
            control = Gtk.CheckButton(label=label);control.set_active(True);self.permissions[key] = control;self.controls.append(control)
            permission_box.attach(control, i % 3, i // 3, 1, 1)
        box.pack_start(permission_box, False, False, 0)
        note = Gtk.Label(label='AES-256 em cópia nova. Cópia sem senha exige proprietário. A fonte será preservada; permissões dependem do leitor.', xalign=0)
        note.set_line_wrap(True);box.pack_start(note, False, False, 0)
        actions = Gtk.Grid(column_spacing=8, row_spacing=8);box.pack_start(actions, False, False, 0)
        for i, (label, action) in enumerate([('Inspecionar', self._inspect), ('Salvar cópia com senha…', self._protect), ('Salvar cópia sem senha…', self._unprotect) ]):
            button = Gtk.Button(label=label);button.connect('clicked', action);actions.attach(button, i % 2, i // 2, 1, 1);self.controls.append(button)
        cancel = Gtk.Button(label='Cancelar');cancel.connect('clicked', self._cancel);actions.attach(cancel,1,1,1,1)
        self.status = Gtk.Label(label='Inspecione um PDF antes de criar uma cópia protegida.', xalign=0)
        self.status.set_line_wrap(True);self.status.set_selectable(True);box.pack_start(self.status, False, False, 0)
        if path:self.path.set_text(str(path))
        self.path.connect('changed', self._changed);self.connect('destroy', self._destroy)

    def _choose(self, save=False):
        dialog = Gtk.FileChooserDialog(title='Salvar cópia protegida' if save else 'Escolher PDF', transient_for=self,
            modal=True, action=Gtk.FileChooserAction.SAVE if save else Gtk.FileChooserAction.OPEN)
        dialog.set_destroy_with_parent(True);dialog.add_buttons('Cancelar', Gtk.ResponseType.CANCEL, 'Selecionar', Gtk.ResponseType.OK)
        if save:dialog.set_current_name(Path(self.path.get_text()).stem+'-copia.pdf')
        try:return dialog.get_filename() if dialog.run() == Gtk.ResponseType.OK else None
        finally:dialog.destroy()

    def _browse(self, *_):
        if self.busy or self.closed:return
        path = self._choose()
        if path and not self.closed:self.path.set_text(path)

    def _clear_secrets(self):
        for field in self.secrets.values():field.set_text('')

    def _changed(self, *_):
        self._cancel();self.info = None;self._clear_secrets();self.status.set_text('Inspecione o arquivo selecionado.')

    def _inspect(self, *_):
        if self.busy or self.closed:return
        path = self.path.get_text();request = {'password':self.secrets['inspect'].get_text()};self._clear_secrets();self.info = None
        def loaded(result):
            self.info = result
            if not result['encrypted']:message = f"PDF sem criptografia: {result['pages']} página(s). Pode criar uma cópia protegida."
            elif not result['authenticated']:message = 'PDF criptografado; a senha não autenticou. O conteúdo não foi exposto.'
            else:
                role = 'proprietário' if result['role'] == 'owner' else 'abertura'
                allowed = ', '.join(button.get_label() for key, button in self.permissions.items() if result['permissions'][key]) or 'nenhuma das opções'
                message = f"PDF criptografado, {result['bits']} bits, revisão {result['revision']}; senha de {role} autenticada. {result['pages']} página(s). Permissões declaradas: {allowed}."
            self.status.set_text(message)
        self._submit(lambda cancel:invoke_security('security-info', path, request, cancel), loaded)

    def _protect(self, *_):
        if self.busy or self.closed:return
        if not self.info or self.info['encrypted']:
            self._clear_secrets();self.status.set_text('Inspecione um PDF sem criptografia para criar uma cópia protegida.');return
        info, path = self.info, self.path.get_text()
        values = {key:field.get_text() for key, field in self.secrets.items()};self._clear_secrets()
        if values['user'] != values['user_confirm'] or values['owner'] != values['owner_confirm']:
            self.status.set_text('As confirmações não coincidem. Informe as senhas novamente.');return
        destination = self._choose(save=True)
        if not destination or self.closed or self.info is not info or self.path.get_text() != path:return
        request = {'destination':destination, 'source_sha256':info['source_sha256'], 'user_password':values['user'],
                   'owner_password':values['owner'], 'permissions':{key:c.get_active() for key, c in self.permissions.items()}}
        self._submit(lambda cancel:invoke_security('protect-copy', path, request, cancel),
            lambda result:self.status.set_text(f"Cópia AES-256 criada e verificada: {Path(result['path']).name}. Guarde suas senhas."))

    def _unprotect(self, *_):
        if self.busy or self.closed:return
        info, path = self.info, self.path.get_text()
        password = self.secrets['inspect'].get_text();self._clear_secrets()
        if not info or not info['encrypted'] or not password:
            self.status.set_text('Inspecione um PDF criptografado e informe a senha atual de proprietário para criar a cópia sem senha.');return
        destination = self._choose(save=True)
        if not destination or self.closed or self.info is not info or self.path.get_text() != path:return
        request = {'destination':destination,'source_sha256':info['source_sha256'],'owner_password':password}
        self._submit(lambda cancel:invoke_security('owner-copy',path,request,cancel),
            lambda result:self.status.set_text(f"Cópia sem senha criada pelo proprietário: {Path(result['path']).name}. O original foi preservado."))

    def _submit(self, task, success):
        self.cancel = threading.Event();cancel = self.cancel;self.busy = True
        for widget in self.controls:widget.set_sensitive(False)
        self.status.set_text('Processando PDF…')
        def finish():
            self.busy = False
            for widget in self.controls:widget.set_sensitive(True)
        def done(result):
            if self.closed or cancel.is_set():return
            finish()
            if result is not None:success(result)
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('security', lambda:task(cancel), done, failed, priority='background')

    def _cancel(self, *_):
        if not self.busy:return
        self.cancel.set();self.runner.invalidate('security');self.busy = False
        for widget in self.controls:widget.set_sensitive(True)
        self._clear_secrets();self.status.set_text('Cancelado. Confira o destino antes de repetir uma gravação.')

    def _destroy(self, *_):
        self.closed = True;self.cancel.set();self._clear_secrets();self.runner.shutdown()
