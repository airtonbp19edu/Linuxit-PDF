"""Explicit own-layout XFA copy workflow; source is never modified."""
from pathlib import Path
import threading
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from async_core import BackgroundRunner
from folder_dialogs import prepare_chooser,remember_selection
from search_tasks import run_search_worker


class XFAFlowWindow(Gtk.Window):
    def __init__(self,parent,path,open_result):
        super().__init__(title='Cópia XFA com layout próprio',transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(660,520)
        self.path=str(path);self.open_result=open_result;self.closed=False;self.busy=False
        self.cancel=threading.Event();self.runner=BackgroundRunner(workers=1);self.info=None;self.result=None
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10);box.set_border_width(14);self.add(box)
        hint=Gtk.Label(label='Gera páginas novas em fluxo vertical ou uma página com posições x/y/w/h suportadas. A aparência original é substituída. '
            'Aceita texto Windows-1252, repetições no fluxo vertical e cálculos FormCalc numéricos entre campos irmãos. Outros scripts/controles são recusados. O original é preservado.',xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint,False,False,0)
        self.grid=Gtk.Grid(column_spacing=8,row_spacing=6)
        scroll=Gtk.ScrolledWindow();scroll.set_vexpand(True);scroll.add(self.grid);box.pack_start(scroll,True,True,0)
        bar=Gtk.Box(spacing=6);box.pack_start(bar,False,False,0)
        self.action=Gtk.ComboBoxText()
        for key,label in [('values','Preencher valores'),('add','Adicionar instância'),('remove','Remover instância')]:self.action.append(key,label)
        self.action.set_active_id('values');bar.pack_start(self.action,False,False,0)
        self.group=Gtk.ComboBoxText();self.group.get_accessible().set_name('Subformulário repetido');bar.pack_start(self.group,True,True,0)
        self.index=Gtk.SpinButton.new_with_range(1,1001,1);self.index.get_accessible().set_name('Posição da instância');bar.pack_start(self.index,False,False,0)
        self.action.connect('changed',self._mode);self.group.connect('changed',self._mode)
        buttons=Gtk.Box(spacing=6);box.pack_start(buttons,False,False,0)
        self.create=Gtk.Button(label='Salvar nova cópia XFA…');self.create.connect('clicked',self._create);buttons.pack_start(self.create,False,False,0)
        self.open=Gtk.Button(label='Abrir cópia');self.open.set_sensitive(False);self.open.connect('clicked',lambda *_:self.open_result(self.result['path']) if self.result else None);buttons.pack_start(self.open,False,False,0)
        cancel=Gtk.Button(label='Cancelar operação');cancel.connect('clicked',lambda *_:self.cancel.set());buttons.pack_end(cancel,False,False,0)
        self.status=Gtk.Label(label='Lendo template e dados…',xalign=0);self.status.set_line_wrap(True);self.status.set_selectable(True);box.pack_start(self.status,False,False,0)
        self.entries=[];self.controls=[self.create,self.action,self.group,self.index,self.grid]
        self.connect('destroy',self._destroy)
        self._submit(lambda cancel:run_search_worker('xfa-flow-info',self.path,{},cancel),self._loaded)

    def _loaded(self,info):
        self.info=info
        for row,record in enumerate(info['fields'][:256]):
            label=Gtk.Label(label=record['path'],xalign=0);label.set_line_wrap(True)
            entry=Gtk.Entry();entry.set_text(record['value']);entry.get_accessible().set_name(record['path'])
            if record.get('calculate') is not None:entry.set_editable(False);entry.set_tooltip_text('Valor calculado por FormCalc; altere os campos de entrada.')
            self.grid.attach(label,0,row,1,1);self.grid.attach(entry,1,row,1,1);self.entries.append((record,entry))
        for record in info['groups']:self.group.append(record['path'],record['path']+f" ({record['count']})")
        self.group.set_active(0);self.grid.show_all();self._mode()
        self.status.set_text(f"{len(info['fields'])} campos. Altere até 256 valores ou uma instância por cópia; depois abra o resultado para continuar.")

    def _mode(self,*_):
        mode=self.action.get_active_id();self.grid.set_sensitive(mode=='values' and not self.busy)
        self.group.set_sensitive(mode!='values' and not self.busy);self.index.set_sensitive(mode!='values' and not self.busy)
        if self.info and self.group.get_active_id():
            record=next(row for row in self.info['groups'] if row['path']==self.group.get_active_id())
            self.index.set_range(1,max(1,record['count']+(1 if mode=='add' else 0)))

    def _create(self,*_):
        if self.busy or not self.info:return
        mode=self.action.get_active_id();values={};instances=[]
        if mode=='values':values={r['path']:entry.get_text() for r,entry in self.entries if r['value']!=entry.get_text()}
        else:
            group=self.group.get_active_id()
            if not group:self.status.set_text('Não há subformulários repetidos disponíveis.');return
            instances=[dict(action=mode,path=group,index=self.index.get_value_as_int()-1)]
        request=dict(source_sha256=self.info['source_sha256'],values=values,instances=instances)
        dialog=Gtk.FileChooserDialog(title='Salvar nova cópia fluida XFA',transient_for=self,modal=True,action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Salvar cópia',Gtk.ResponseType.OK)
        dialog.set_current_name(Path(self.path).stem+'-fluido.pdf');prepare_chooser(dialog,'save',self.path)
        try:destination=dialog.get_filename() if dialog.run()==Gtk.ResponseType.OK else None
        finally:dialog.destroy()
        if not destination:return
        remember_selection(destination,'save')
        def saved(result):
            self.result=result;self.open.set_sensitive(True)
            self.status.set_text(f"Cópia criada: {result['pages']} páginas, {result['fields']} campos. Layout próprio; revise antes de usar.")
        self._submit(lambda cancel:run_search_worker('xfa-flow-copy',self.path,request,cancel,destination=destination),saved)

    def _submit(self,work,done):
        self.cancel=threading.Event();cancel=self.cancel;self.busy=True
        for control in self.controls:control.set_sensitive(False)
        def finish():
            self.busy=False
            for control in self.controls:control.set_sensitive(True)
            self._mode()
        def success(result):
            if self.closed:return
            finish()
            if cancel.is_set() or result is None:self.status.set_text('Operação cancelada. Confira o destino antes de repetir.');return
            done(result)
        def failure(exc):
            if self.closed:return
            finish();self.status.set_text(str(exc))
        self.runner.submit('xfa-flow',lambda:work(cancel),success,failure)

    def _destroy(self,*_):
        self.closed=True;self.cancel.set();self.runner.shutdown()
