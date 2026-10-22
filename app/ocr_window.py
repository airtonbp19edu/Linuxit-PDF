"""GTK workflow for an explicit rasterized searchable copy of the open PDF."""
import hashlib
from pathlib import Path
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from async_core import BackgroundRunner
from attachment_tasks import display_attachment_name
from folder_dialogs import prepare_chooser, remember_selection
from local_files import file_stamp
from pdf_ocr import invoke_ocr, source_identity
from tool_preferences import read_tool_preferences


class OCRWindow(Gtk.Window):
    def __init__(self, parent, path, open_result):
        super().__init__(title='Criar cópia pesquisável com OCR', transient_for=parent)
        self.set_destroy_with_parent(True)
        self.set_default_size(640, 340)
        self.path = str(Path(path).resolve())
        defaults=read_tool_preferences()
        self.source_stamp = file_stamp(self.path)
        self.open_result = open_result
        self.closed = self.busy = False
        self.cancel = threading.Event()
        self.runner = BackgroundRunner(workers=1)
        self.result = None
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(14)
        self.add(box)
        hint = Gtk.Label(label='OCR local · até 20 páginas · português/inglês\n'
                         'A cópia usa imagens das páginas e texto reconhecido. Links, campos editáveis, '
                         'marcadores, camadas e assinaturas digitais não são preservados. '
                         'O original permanece intacto. Revise o texto: o reconhecimento pode errar.', xalign=0)
        hint.set_line_wrap(True)
        box.pack_start(hint, False, False, 0)
        source = Gtk.Label(label='Fonte: ' + display_attachment_name(Path(self.path).name), xalign=0)
        source.set_line_wrap(True)
        box.pack_start(source, False, False, 0)
        bar = Gtk.Box(spacing=8)
        box.pack_start(bar, False, False, 0)
        bar.pack_start(Gtk.Label(label='Idioma:'), False, False, 0)
        self.language = Gtk.ComboBoxText()
        for key, label in [('por', 'Português'), ('eng', 'Inglês'), ('por+eng', 'Português e inglês')]:
            self.language.append(key, label)
        self.language.set_active_id(defaults['ocr_language'])
        bar.pack_start(self.language, False, False, 0)
        bar.pack_start(Gtk.Label(label='Resolução:'), False, False, 0)
        self.dpi = Gtk.ComboBoxText()
        for value in ('150', '300'):
            self.dpi.append(value, value + ' DPI')
        self.dpi.set_active_id(str(defaults['ocr_dpi']))
        bar.pack_start(self.dpi, False, False, 0)
        self.psm=Gtk.ComboBoxText()
        for value,label in [('3','Layout automático'),('6','Bloco único de texto'),('11','Texto esparso')]:self.psm.append(value,label)
        self.psm.set_active_id(str(defaults['ocr_psm']));box.pack_start(self.psm,False,False,0)
        self.preprocess=Gtk.ComboBoxText()
        for value,label in [('none','Imagem original'),('contrast','Limpar contraste (escaneamento apagado)'),('threshold','Preto e branco automático (pode perder detalhes)')]:self.preprocess.append(value,label)
        self.preprocess.set_active_id('none');self.preprocess.get_accessible().set_name('Pré-processamento OCR');box.pack_start(self.preprocess,False,False,0)
        self.pages=Gtk.Entry();self.pages.set_placeholder_text('Páginas para OCR:1,3,5 (vazio=todas);demais páginas copiadas')
        self.pages.get_accessible().set_name('Páginas selecionadas para OCR');box.pack_start(self.pages,False,False,0)
        buttons = Gtk.Box(spacing=8)
        box.pack_start(buttons, False, False, 0)
        self.create = Gtk.Button(label='Criar cópia com OCR…')
        self.create.connect('clicked', self._create)
        buttons.pack_start(self.create, False, False, 0)
        self.open_button = Gtk.Button(label='Abrir cópia')
        self.open_button.set_sensitive(False)
        self.open_button.connect('clicked', self._open)
        buttons.pack_start(self.open_button, False, False, 0)
        cancel = Gtk.Button(label='Cancelar operação')
        cancel.connect('clicked', self._cancel)
        buttons.pack_end(cancel, False, False, 0)
        self.controls = [self.create, self.language, self.dpi,self.psm,self.pages,self.preprocess]
        self.status = Gtk.Label(label='Escolha um nome novo para salvar todas as páginas.', xalign=0)
        self.status.set_line_wrap(True)
        self.status.set_selectable(True)
        box.pack_start(self.status, False, False, 0)
        self.connect('destroy', self._destroy)

    def _choose(self):
        dialog = Gtk.FileChooserDialog(title='Salvar nova cópia pesquisável', transient_for=self, modal=True,
                                      action=Gtk.FileChooserAction.SAVE)
        dialog.set_destroy_with_parent(True)
        dialog.add_buttons('Cancelar', Gtk.ResponseType.CANCEL, 'Selecionar', Gtk.ResponseType.OK)
        dialog.set_current_name(Path(self.path).stem + '-ocr.pdf')
        prepare_chooser(dialog, 'save')
        try:
            if dialog.run() != Gtk.ResponseType.OK:
                return None
            path = dialog.get_filename()
            remember_selection(path, 'save')
            return path
        finally:
            dialog.destroy()

    def _create(self, *_):
        if self.closed or self.busy:
            return
        destination = self._choose()
        if not destination or self.closed:
            return
        language, dpi = self.language.get_active_id(), int(self.dpi.get_active_id())
        pages=self.pages.get_text().strip();psm=int(self.psm.get_active_id());preprocess=self.preprocess.get_active_id()
        try:selected=[int(value.strip()) for value in pages.split(',')] if pages else None
        except ValueError:self.status.set_text('Informe números de páginas separados por vírgulas.');return
        self.result = None
        def task(cancel):
            if file_stamp(self.path) != self.source_stamp:
                raise ValueError('O PDF mudou. Reabra o documento antes do OCR.')
            identity = source_identity(self.path)
            if file_stamp(self.path) != self.source_stamp:
                raise ValueError('O PDF mudou. Reabra o documento antes do OCR.')
            request={'source_sha256': identity, 'language': language, 'dpi': dpi,'psm':psm,'preprocess':preprocess}
            if selected is not None:request['pages']=selected
            return invoke_ocr(self.path, destination, request, cancel)
        def saved(result):
            self.result = result
            self.open_button.set_sensitive(True)
            missing = result['pages_without_text']
            notice = (' Sem texto detectado nas páginas: ' + ', '.join(map(str, missing)) + '.') if missing else ''
            self.status.set_text(f"Cópia criada: {result['pages']} página(s). Revise o texto reconhecido." + notice)
            self.status.set_tooltip_text(display_attachment_name(result['path']))
        self._submit(task, saved, 'Reconhecendo texto localmente…')

    def _submit(self, task, success, message):
        self.cancel = threading.Event()
        cancel = self.cancel
        self.busy = True
        for widget in self.controls:
            widget.set_sensitive(False)
        self.open_button.set_sensitive(False)
        self.status.set_tooltip_text(None)
        self.status.set_text(message)
        def finish():
            self.busy = False
            for widget in self.controls:
                widget.set_sensitive(True)
            self.open_button.set_sensitive(self.result is not None)
        def done(result):
            if self.closed or cancel.is_set():
                return
            finish()
            if result is not None:
                success(result)
        def failed(exc):
            if self.closed or cancel.is_set():
                return
            finish()
            self.status.set_text(str(exc))
        self.runner.submit('ocr', lambda: task(cancel), done, failed, priority='background')

    def _open(self, *_):
        if self.closed or self.busy or self.result is None:
            return
        result = dict(self.result)
        def check(_):
            try:
                with Path(result['path']).open('rb') as stream:
                    return hashlib.file_digest(stream, 'sha256').hexdigest() == result['output_sha256']
            except OSError:
                return False
        def opened(valid):
            if valid:
                self.open_result(result['path'])
            else:
                self.status.set_text('A cópia mudou ou não está disponível. Escolha o arquivo novamente em Abrir PDF.')
        self._submit(check, opened, 'Conferindo a cópia…')

    def _cancel(self, *_):
        if self.closed or not self.busy:
            return
        self.cancel.set()
        self.runner.invalidate('ocr')
        self.busy = False
        for widget in self.controls:
            widget.set_sensitive(True)
        self.open_button.set_sensitive(self.result is not None)
        self.status.set_text('Cancelado. Confira o destino antes de repetir o OCR.')

    def _destroy(self, *_):
        self.closed = True
        self.cancel.set()
        self.runner.shutdown()
