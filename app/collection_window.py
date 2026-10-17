"""GTK entrypoint for an explicit local PDF collection and its saved text index."""
from pathlib import Path
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

from async_core import BackgroundRunner
from attachment_tasks import display_attachment_name
from collection_index import invoke_collection, verify_document


class CollectionWindow(Gtk.Window):
    def __init__(self, parent, open_result):
        super().__init__(title='Pesquisar em coleção', transient_for=parent)
        self.set_destroy_with_parent(True)
        self.set_default_size(760, 500)
        self.open_result = open_result
        self.runner = BackgroundRunner()
        self.cancel = threading.Event()
        self.closed = self.busy = False
        self.hits = []
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8, margin=12)
        self.add(box)
        hint = Gtk.Label(label='Escolha PDFs para indexar seu texto, sem OCR. Nenhuma pasta será varrida automaticamente.', xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint, False, False, 0)
        row = Gtk.Box(spacing=6)
        self.index_entry = Gtk.Entry();self.index_entry.set_placeholder_text('Arquivo .linuxit-index.json')
        self.index_entry.get_accessible().set_name('Arquivo de índice da coleção')
        row.pack_start(self.index_entry, True, True, 0)
        browse = Gtk.Button(label='Abrir índice…');browse.connect('clicked', self._browse)
        row.pack_start(browse, False, False, 0)
        build = Gtk.Button(label='Criar/atualizar…');build.connect('clicked', self._build)
        row.pack_start(build, False, False, 0);box.pack_start(row, False, False, 0)
        row = Gtk.Box(spacing=6)
        self.query = Gtk.Entry();self.query.set_placeholder_text('Consulta')
        self.query.get_accessible().set_name('Consulta da coleção')
        self.query.connect('activate', self._search)
        row.pack_start(self.query, True, True, 0)
        find = Gtk.Button(label='Pesquisar');find.connect('clicked', self._search)
        row.pack_start(find, False, False, 0)
        stop = Gtk.Button(label='Cancelar');stop.connect('clicked', self._cancel)
        row.pack_start(stop, False, False, 0);box.pack_start(row, False, False, 0)
        row = Gtk.Box(spacing=6)
        self.mode = Gtk.ComboBoxText()
        for key, name in [('literal', 'Literal'), ('wildcard', 'Coringas por palavra'), ('proximity', 'Proximidade ordenada')]:
            self.mode.append(key, name)
        self.mode.set_active_id('literal');row.pack_start(self.mode, False, False, 0)
        row.pack_start(Gtk.Label(label='Distância:'), False, False, 0)
        self.distance = Gtk.SpinButton.new_with_range(0, 50, 1)
        self.distance.set_sensitive(False)
        self.distance.get_accessible().set_name('Distância da consulta da coleção')
        def mode_changed(*_):
            self.distance.set_sensitive(self.mode.get_active_id() == 'proximity')
            self.flags['whole_words'].set_sensitive(self.mode.get_active_id() == 'literal')
        self.mode.connect('changed', mode_changed)
        row.pack_start(self.distance, False, False, 0)
        self.flags = {}
        for key, name in [('match_case', 'Maiúsc./minúsc.'), ('whole_words', 'Palavra inteira'), ('ignore_accents', 'Ignorar acentos')]:
            button = Gtk.CheckButton(label=name);self.flags[key] = button;row.pack_start(button, False, False, 0)
        box.pack_start(row, False, False, 0)
        self.status = Gtk.Label(xalign=0);self.status.set_line_wrap(True)
        box.pack_start(self.status, False, False, 0)
        self.results = Gtk.ListBox();self.results.connect('row-activated', self._activate)
        scroll = Gtk.ScrolledWindow();scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.results);box.pack_start(scroll, True, True, 0)
        self.controls = [self.index_entry, browse, build, self.query, find, self.mode, *self.flags.values()]
        self.connect('destroy', self._destroy)

    def _choose(self, title, action, multiple=False, default=None):
        dialog = Gtk.FileChooserDialog(title=title, transient_for=self, modal=True, action=action)
        dialog.set_destroy_with_parent(True)
        dialog.add_buttons('Cancelar', Gtk.ResponseType.CANCEL, 'Selecionar', Gtk.ResponseType.OK)
        if multiple:dialog.set_select_multiple(True)
        if default:dialog.set_current_name(default)
        try:
            if dialog.run() != Gtk.ResponseType.OK:return None
            return dialog.get_filenames() if multiple else dialog.get_filename()
        finally:dialog.destroy()

    def _browse(self, *_):
        path = self._choose('Abrir índice Linuxit', Gtk.FileChooserAction.OPEN)
        if path and not self.closed:self.index_entry.set_text(path)

    def _build(self, *_):
        if self.busy or self.closed:return
        paths = self._choose('Escolher PDFs da coleção', Gtk.FileChooserAction.OPEN, multiple=True)
        if not paths or self.closed:return
        path = self._choose('Salvar índice Linuxit', Gtk.FileChooserAction.SAVE, default='colecao.linuxit-index.json')
        if not path or self.closed:return
        self.index_entry.set_text(path)
        self._clear_hits()
        self._submit(lambda cancel: invoke_collection('index-build', path, {'paths': paths}, cancel),
                     lambda result: self.status.set_text(f"Índice salvo: {result['documents']} PDFs, {result['pages']} páginas."))

    def _clear_hits(self):
        self.hits = []
        for row in self.results.get_children():self.results.remove(row)

    def _search(self, *_):
        if self.busy or self.closed:return
        path, query = self.index_entry.get_text().strip(), self.query.get_text().strip()
        if not path or not query:
            self.status.set_text('Escolha um índice e informe a consulta.');return
        request = {key: button.get_active() for key, button in self.flags.items()}
        request.update(query=query, mode=self.mode.get_active_id(), proximity_distance=self.distance.get_value_as_int(), max_hits=5000)
        self._clear_hits()
        def loaded(result):
            self.hits = result['hits']
            for hit in self.hits[:350]:
                row = Gtk.ListBoxRow();row.hit = hit
                name = display_attachment_name(Path(hit['path']).name)
                label = Gtk.Label(label=f"{name} · pág. {hit['page'] + 1} · {hit['snippet']}", xalign=0)
                label.set_ellipsize(Pango.EllipsizeMode.END);label.set_margin_top(5);label.set_margin_bottom(5)
                label.set_tooltip_text(display_attachment_name(hit['path']) + '\n' + hit['snippet'])
                row.add(label);self.results.add(row)
            self.results.show_all()
            text = f"{len(self.hits)} ocorrência(s); {len(result['stale'])} PDF(s) desatualizado(s) excluído(s)."
            if result['limit_reached']:text += ' Limite de resultados atingido.'
            if len(self.hits) > 350:text += ' A lista exibe os primeiros 350; refine a consulta.'
            self.status.set_text(text)
            self.status.set_tooltip_text('\n'.join(display_attachment_name(item['path']) for item in result['stale'][:20]) or None)
        self._submit(lambda cancel: invoke_collection('index-search', path, request, cancel), loaded)

    def _submit(self, task, success):
        if self.closed or self.busy:return
        self.cancel = threading.Event();cancel = self.cancel
        self.busy = True
        for widget in self.controls:widget.set_sensitive(False)
        self.distance.set_sensitive(False)
        self.status.set_text('Processando coleção…')
        def finish():
            self.busy = False
            for widget in self.controls:widget.set_sensitive(True)
            self.distance.set_sensitive(self.mode.get_active_id() == 'proximity')
            self.flags['whole_words'].set_sensitive(self.mode.get_active_id() == 'literal')
        def done(result):
            if self.closed or cancel.is_set():return
            finish()
            if result is not None:success(result)
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('index-operation', lambda: task(cancel), done, failed, priority='background')

    def _activate(self, _, row):
        if self.busy or self.closed or not hasattr(row, 'hit'):return
        hit = dict(row.hit)
        def checked(valid):
            if valid:self.open_result(hit['path'], hit['page'])
            else:self.status.set_text('Este PDF mudou ou não está disponível. Atualize o índice antes de abrir este resultado.')
        self._submit(lambda cancel: verify_document(hit['path'], hit['source_sha256']), checked)

    def _cancel(self, *_):
        self.cancel.set();self.runner.invalidate('index-operation');self.busy = False
        for widget in self.controls:widget.set_sensitive(True)
        self.distance.set_sensitive(self.mode.get_active_id() == 'proximity')
        self.flags['whole_words'].set_sensitive(self.mode.get_active_id() == 'literal')
        self.status.set_text('Cancelado. Confira o índice antes de repetir uma gravação.')

    def _destroy(self, *_):
        self.closed = True;self.cancel.set();self.runner.shutdown()
