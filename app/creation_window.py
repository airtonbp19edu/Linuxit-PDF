"""GTK workflow for explicitly ordered images and a new PDF destination."""
import hashlib
from pathlib import Path
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

from async_core import BackgroundRunner
from attachment_tasks import display_attachment_name
from pdf_creation import invoke_image_creation, MAX_IMAGES


class CreationWindow(Gtk.Window):
    def __init__(self, parent, open_result):
        super().__init__(title='Criar PDF de imagens', transient_for=parent)
        self.set_destroy_with_parent(True)
        self.set_default_size(740, 480)
        self.paths = []
        self.runner = BackgroundRunner(workers=1)
        self.cancel = threading.Event()
        self.closed = self.busy = False
        self.result = None
        self.open_result = open_result
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_border_width(14);self.add(box)
        hint = Gtk.Label(label='PNG/JPEG · uma imagem por página · transparência branca · sem OCR', xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint, False, False, 0)
        bar = Gtk.Box(spacing=6);box.pack_start(bar, False, False, 0)
        self.controls = []
        for title, action in [('Adicionar imagens…', self._add), ('Remover', self._remove),
                              ('Subir', lambda *_: self._move(-1)), ('Descer', lambda *_: self._move(1))]:
            button = Gtk.Button(label=title);button.connect('clicked', action)
            bar.pack_start(button, False, False, 0);self.controls.append(button)
        self.images = Gtk.ListBox();self.images.set_selection_mode(Gtk.SelectionMode.SINGLE)
        scroll = Gtk.ScrolledWindow();scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.images);box.pack_start(scroll, True, True, 0)
        actions = Gtk.Box(spacing=8);box.pack_start(actions, False, False, 0)
        label = Gtk.Label(label='Resolução (DPI):');actions.pack_start(label, False, False, 0)
        self.dpi = Gtk.SpinButton.new_with_range(72, 600, 1);self.dpi.set_value(300)
        self.dpi.set_tooltip_text('O tamanho da página é calculado a partir dos pixels e desta resolução.')
        actions.pack_start(self.dpi, False, False, 0);self.controls.append(self.dpi)
        self.create = Gtk.Button(label='Criar PDF…');self.create.connect('clicked', self._create)
        actions.pack_start(self.create, False, False, 0);self.controls.append(self.create)
        self.open_button = Gtk.Button(label='Abrir PDF');self.open_button.connect('clicked', self._open)
        self.open_button.set_sensitive(False);actions.pack_start(self.open_button, False, False, 0)
        cancel = Gtk.Button(label='Cancelar');cancel.connect('clicked', self._cancel)
        actions.pack_end(cancel, False, False, 0)
        self.status = Gtk.Label(label='Adicione imagens e organize a ordem das páginas.', xalign=0)
        self.status.set_line_wrap(True);self.status.set_selectable(True)
        box.pack_start(self.status, False, False, 0)
        self.connect('destroy', self._destroy)

    def _choose(self, save=False):
        dialog = Gtk.FileChooserDialog(title='Salvar novo PDF' if save else 'Escolher imagens PNG/JPEG',
                                      transient_for=self, modal=True,
                                      action=Gtk.FileChooserAction.SAVE if save else Gtk.FileChooserAction.OPEN)
        dialog.set_destroy_with_parent(True)
        dialog.add_buttons('Cancelar', Gtk.ResponseType.CANCEL, 'Selecionar', Gtk.ResponseType.OK)
        if save:
            dialog.set_current_name('imagens.pdf')
        else:
            dialog.set_select_multiple(True)
            filter_ = Gtk.FileFilter();filter_.set_name('Imagens PNG/JPEG')
            for mime in ('image/png', 'image/jpeg'):filter_.add_mime_type(mime)
            dialog.add_filter(filter_)
        try:
            if dialog.run() != Gtk.ResponseType.OK:return None
            return dialog.get_filename() if save else dialog.get_filenames()
        finally:dialog.destroy()

    def _refresh(self, selected=None):
        for row in self.images.get_children():self.images.remove(row)
        for index, path in enumerate(self.paths):
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=f'{index + 1}. {display_attachment_name(Path(path).name)}', xalign=0)
            label.set_ellipsize(Pango.EllipsizeMode.END);label.set_margin_top(6);label.set_margin_bottom(6)
            label.set_tooltip_text(display_attachment_name(path));row.add(label);self.images.add(row)
        self.images.show_all()
        if selected is not None:self.images.select_row(self.images.get_row_at_index(selected))
        self.status.set_text(f'{len(self.paths)} imagem(ns). A lista define a ordem das páginas.')

    def _add(self, *_):
        if self.busy or self.closed:return
        chosen = self._choose()
        if not chosen or self.closed:return
        paths = list(self.paths)
        for path in chosen:
            path = str(Path(path).resolve())
            if path not in paths:paths.append(path)
        if len(paths) > MAX_IMAGES:
            self.status.set_text(f'Escolha no máximo {MAX_IMAGES} imagens. A lista anterior foi preservada.');return
        self.paths = paths;self._refresh()

    def _remove(self, *_):
        if self.busy or self.closed:return
        row = self.images.get_selected_row()
        if row is not None:
            index = row.get_index();self.paths.pop(index);self._refresh(min(index, len(self.paths)-1))

    def _move(self, distance):
        if self.busy or self.closed:return
        row = self.images.get_selected_row()
        if row is None:return
        index = row.get_index();target = index + distance
        if 0 <= target < len(self.paths):
            self.paths[index], self.paths[target] = self.paths[target], self.paths[index]
            self._refresh(target)

    def _create(self, *_):
        if self.busy or self.closed:return
        if not self.paths:
            self.status.set_text('Adicione pelo menos uma imagem PNG/JPEG.');return
        destination = self._choose(save=True)
        if not destination or self.closed:return
        self.result = None;self.open_button.set_sensitive(False)
        request = {'paths': list(self.paths), 'dpi': self.dpi.get_value_as_int()}
        def saved(result):
            self.result = result;self.open_button.set_sensitive(True)
            self.status.set_text(f"PDF criado: {result['pages']} página(s). Use Abrir PDF para conferir.")
            self.status.set_tooltip_text(display_attachment_name(result['path']))
        self._submit(lambda cancel: invoke_image_creation(destination, request, cancel), saved, 'Criando PDF…')

    def _submit(self, task, success, message):
        self.cancel = threading.Event();cancel = self.cancel
        self.busy = True
        for widget in self.controls:self._enable(widget, False)
        self.open_button.set_sensitive(False);self.status.set_tooltip_text(None);self.status.set_text(message)
        def finish():
            self.busy = False
            for widget in self.controls:self._enable(widget, True)
            self.open_button.set_sensitive(self.result is not None)
        def done(result):
            if self.closed or cancel.is_set():return
            finish()
            if result is not None:success(result)
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('image-creation', lambda: task(cancel), done, failed, priority='background')

    @staticmethod
    def _enable(widget, enabled):
        widget.set_sensitive(enabled)

    def _open(self, *_):
        if self.closed or self.busy or self.result is None:return
        result = dict(self.result)
        def unchanged(_):
            try:
                with Path(result['path']).open('rb') as stream:
                    return hashlib.file_digest(stream, 'sha256').hexdigest() == result['output_sha256']
            except OSError:return False
        def opened(valid):
            if valid:self.open_result(result['path'])
            else:self.status.set_text('O PDF criado mudou ou não está disponível. Escolha o arquivo novamente em Abrir PDF.')
        self._submit(unchanged, opened, 'Conferindo PDF criado…')

    def _cancel(self, *_):
        if self.closed or not self.busy:return
        self.cancel.set();self.runner.invalidate('image-creation');self.busy = False
        for widget in self.controls:self._enable(widget, True)
        self.open_button.set_sensitive(self.result is not None)
        self.status.set_text('Cancelado. Confira o destino antes de repetir a criação.')

    def _destroy(self, *_):
        self.closed = True;self.cancel.set();self.runner.shutdown()
