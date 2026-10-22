"""Explicit local export workflow; no external converter or network access."""
from pathlib import Path
import hashlib,threading
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from async_core import BackgroundRunner
from folder_dialogs import prepare_chooser,remember_selection
from search_tasks import run_search_worker
from pdf_conversion import FORMATS

class ConversionWindow(Gtk.Window):
    def __init__(self,parent,path):
        super().__init__(title='Exportar PDF',transient_for=parent)
        self.path=Path(path);self.closed=False;self.busy=False;self.runner=BackgroundRunner();self.cancel=threading.Event()
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10);box.set_border_width(14);self.add(box)
        self.format=Gtk.ComboBoxText()
        for value,label in [('text','Texto UTF-8 (até100 páginas)'),('png','PNG por página em ZIP'),('jpeg','JPEG por página em ZIP'),('tiff','TIFF multipágina')]:self.format.append(value,label)
        self.format.set_active_id('text');box.add(self.format)
        self.dpi=Gtk.ComboBoxText()
        for value in (72,150,300):self.dpi.append(str(value),f'{value}DPI')
        self.dpi.set_active_id('150');box.add(self.dpi)
        self.create=Gtk.Button(label='Salvar exportação nova…');self.create.connect('clicked',self._create);box.add(self.create)
        cancel=Gtk.Button(label='Cancelar operação');cancel.connect('clicked',lambda *_:self.cancel.set());box.add(cancel)
        self.status=Gtk.Label(label='Exportação visual não recria documentos Office editáveis.',xalign=0);self.status.set_line_wrap(True);box.add(self.status)
        self.connect('destroy',self._destroy)
    def _create(self,*_):
        if self.busy or self.closed:return
        kind=self.format.get_active_id();dpi=int(self.dpi.get_active_id())
        dialog=Gtk.FileChooserDialog(title='Exportar para arquivo novo',transient_for=self,action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Salvar',Gtk.ResponseType.OK)
        dialog.set_current_name(self.path.stem+'-exportado'+FORMATS[kind]);prepare_chooser(dialog,'save')
        try:target=dialog.get_filename() if dialog.run()==Gtk.ResponseType.OK else None
        finally:dialog.destroy()
        if not target:return
        remember_selection(target,'save');self.busy=True;self.create.set_sensitive(False);self.cancel=threading.Event()
        def task():
            request={'source_sha256':hashlib.sha256(self.path.read_bytes()).hexdigest(),'format':kind,'dpi':dpi}
            result=run_search_worker('convert-copy',str(self.path),request,self.cancel,600,destination=target)
            if result is not None and (result.get('schema')!='linuxit-conversion-copy-v1' or Path(result['path']).resolve()!=Path(target).resolve()):raise ValueError('Confirmação de conversão inválida.')
            return result
        def done(result):
            if not self.closed:self.busy=False;self.create.set_sensitive(True);self.status.set_text('Exportação salva.' if result else 'Operação cancelada; confira o destino antes de repetir.')
        def failed(error):
            if not self.closed:self.busy=False;self.create.set_sensitive(True);self.status.set_text(str(error))
        self.runner.submit('convert',task,done,failed)
    def _destroy(self,*_):
        self.closed=True;self.cancel.set();self.runner.close()
