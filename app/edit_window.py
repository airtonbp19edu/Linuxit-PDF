"""Copy-edit draft UI with real worker validation and undo/redo before saving."""
from pathlib import Path
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from async_core import BackgroundRunner
from edit_history import EditSession
from folder_dialogs import prepare_chooser, remember_selection

ACTIONS = [('add-bookmark','Adicionar marcador'),('rename-bookmark','Renomear marcador'),
           ('move-bookmark','Mover marcador'),('delete-bookmark','Excluir marcador e descendentes'),
           ('add-note','Adicionar nota'),('update-note','Editar nota'),('add-highlight','Destacar área'),
           ('add-rectangle','Adicionar retângulo'),('add-underline','Sublinhar área'),
           ('add-strikeout','Tachar área'),('add-squiggly','Sublinhar área com ondulado'),
           ('add-ellipse','Adicionar elipse'),('add-line','Adicionar linha'),
           ('add-ink','Desenhar à mão livre'),('add-reply','Responder comentário'),
           ('add-polygon','Adicionar polígono'),('add-polyline','Adicionar polilinha'),
           ('add-caret','Marcar inserção'),('add-freetext','Adicionar texto livre'),('add-stamp','Adicionar carimbo textual'),
           ('move-annotation','Mover anotação'),('update-comment','Editar comentário ou resposta'),
           ('set-popup','Configurar popup'),('delete-conversation','Excluir conversa e popups'),
           ('update-annotation','Editar comentário da anotação'),('style-annotation','Cor e opacidade da anotação'),('resize-annotation','Redimensionar anotação'),('add-redaction','Marcar área para redação'),('delete-annotation','Excluir anotação'),
           ('fill-text-fields','Preencher campo de texto'),('fill-form-controls','Preencher caixas e listas'),
           ('fill-form-events','Preencher com cálculos e validação'),
           ('rotate-page','Girar página')]
NAMES = dict(ACTIONS)


class EditWindow(Gtk.Window):
    def __init__(self, parent, path, page=0, auth=None):
        super().__init__(title='Editar cópia — '+Path(path).name, transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(680, 480)
        self.parent_view, self.path = parent, str(path)
        self.cancel = threading.Event();self.runner = BackgroundRunner(workers=1)
        self.session = None;self.closed = False;self.busy = True
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10);box.set_border_width(14);self.add(box)
        hint = Gtk.Label(label='Prepare alterações e salve em um arquivo novo. Desfazer/refazer atua neste rascunho; cópias já salvas são preservadas.',xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint,False,False,0)
        bar = Gtk.Box(spacing=6);box.pack_start(bar,False,False,0)
        self.kind = Gtk.ComboBoxText();self.kind.get_accessible().set_name('Tipo de alteração')
        for key,label in ACTIONS:self.kind.append(key,label)
        self.kind.set_active(0);bar.pack_start(self.kind,True,True,0)
        self.page = Gtk.SpinButton.new_with_range(1,1,1);self.page.get_accessible().set_name('Página a alterar')
        bar.pack_start(Gtk.Label(label='Página:'),False,False,0);bar.pack_start(self.page,False,False,0)
        self.add_button = Gtk.Button(label='Preparar alteração…');self.add_button.connect('clicked',self._add)
        box.pack_start(self.add_button,False,False,0)
        self.entries = Gtk.ListBox();self.entries.set_selection_mode(Gtk.SelectionMode.NONE)
        scroll = Gtk.ScrolledWindow();scroll.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC);scroll.add(self.entries)
        box.pack_start(scroll,True,True,0)
        bar = Gtk.Box(spacing=6);box.pack_start(bar,False,False,0)
        self.undo_button = Gtk.Button(label='Desfazer');self.undo_button.connect('clicked',lambda *_:self._history(False))
        self.redo_button = Gtk.Button(label='Refazer');self.redo_button.connect('clicked',lambda *_:self._history(True))
        self.save_button = Gtk.Button(label='Salvar cópia nova…');self.save_button.connect('clicked',self._save)
        for button in (self.undo_button,self.redo_button,self.save_button):bar.pack_start(button,False,False,0)
        self.status = Gtk.Label(label='Lendo documento…',xalign=0);self.status.set_line_wrap(True);self.status.set_selectable(True)
        box.pack_start(self.status,False,False,0)
        self.connect('destroy',self._destroy);self.connect('key-press-event',self._key)
        self._refresh()
        def load():
            session = EditSession(self.path,cancel=self.cancel,auth=auth)
            self.session = session
            if self.cancel.is_set():session.close()
            return session
        def loaded(session):
            self.page.set_range(1,session.info['pages']);self.page.set_value(min(max(1,page+1),session.info['pages']))
            self.busy = False;self.status.set_text('Escolha uma alteração para preparar.');self._refresh()
        self.runner.submit('draft',load,loaded,self._failed)

    def _refresh(self):
        ready = self.session is not None and not self.busy and not self.closed
        for widget in (self.kind,self.page,self.add_button):widget.set_sensitive(ready)
        self.undo_button.set_sensitive(ready and self.session.can_undo)
        self.redo_button.set_sensitive(ready and self.session.can_redo)
        self.save_button.set_sensitive(ready and self.session.can_undo)
        for row in self.entries.get_children():self.entries.remove(row);row.destroy()
        if self.session is not None:
            for index,operation in enumerate(self.session.operations):
                label = Gtk.Label(label=f"{index+1}. {NAMES[operation['kind']]}",xalign=0)
                label.set_margin_start(8);label.set_margin_end(8);label.set_margin_top(4);label.set_margin_bottom(4)
                self.entries.add(label)
        self.entries.show_all()

    def _failed(self, error):
        if self.closed:return
        self.busy = False;self.status.set_text(str(error));self._refresh()

    def _run(self, task, message):
        if self.closed or self.busy or self.session is None:return
        self.busy = True;self.status.set_text(message);self._refresh()
        def done(result):
            if self.closed:return
            self.busy = False
            if isinstance(result,dict) and 'output_sha256' in result:
                self.status.set_text('Cópia salva: '+Path(result['path']).name+'. As cópias salvas permanecem intactas ao desfazer o rascunho.')
            else:self.status.set_text(f'{self.session.cursor} alteração(ões) preparada(s). Ctrl+Z desfaz; Ctrl+Shift+Z refaz.')
            self._refresh()
        self.runner.submit('draft',task,done,self._failed)

    def _add(self,*_):
        if self.closed or self.busy or self.session is None:return
        self.busy = True;self._refresh()
        try:operation = self.parent_view._copy_edit_operation_dialog(self.kind.get_active_id(),self.session.info,self.page.get_value_as_int()-1)
        finally:
            self.busy = False
            if not self.closed:self._refresh()
        if operation is not None and not self.closed:self._run(lambda:self.session.add(operation),'Verificando alteração…')

    def _history(self,redo):
        if self.session is None:return
        if not (self.session.can_redo if redo else self.session.can_undo):return
        self._run(self.session.redo if redo else self.session.undo,'Reconstituindo rascunho…')

    def _choose_destination(self):
        dialog = Gtk.FileChooserDialog(title='Salvar cópia nova',transient_for=self,modal=True,action=Gtk.FileChooserAction.SAVE)
        dialog.set_destroy_with_parent(True);dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Salvar',Gtk.ResponseType.OK)
        dialog.set_current_name(Path(self.path).stem+'-editado.pdf');prepare_chooser(dialog,'save',self.path)
        try:
            target = dialog.get_filename() if dialog.run() == Gtk.ResponseType.OK else None
            remember_selection(target,'save');return target
        finally:dialog.destroy()

    def _save(self,*_):
        if self.closed or self.busy or self.session is None or not self.session.can_undo:return
        self.busy = True;self._refresh()
        try:target = self._choose_destination()
        finally:
            self.busy = False
            if not self.closed:self._refresh()
        if target and not self.closed:self._run(lambda:self.session.save(target),'Salvando cópia nova… Se interromper, confira o destino antes de repetir.')

    def _key(self,_widget,event):
        if not event.state & Gdk.ModifierType.CONTROL_MASK:return False
        if isinstance(self.get_focus(),(Gtk.Entry,Gtk.TextView)):return False
        key = (Gdk.keyval_name(event.keyval) or '').lower()
        if key not in ('z','y'):return False
        self._history(key == 'y' or bool(event.state & Gdk.ModifierType.SHIFT_MASK));return True

    def _destroy(self,*_):
        if self.closed:return
        self.closed = True;self.cancel.set();self.runner.shutdown()
        if self.session is not None:self.session.close()
