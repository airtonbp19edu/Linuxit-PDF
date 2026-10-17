"""Offline signature integrity, explicitly separate from certificate trust."""
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from async_core import BackgroundRunner
from attachment_tasks import display_attachment_name
from pdf_signatures import invoke_signature_inspection


class SignatureWindow(Gtk.Window):
    def __init__(self,parent,path=None):
        super().__init__(title='Integridade de assinaturas PDF',transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(780,420)
        self.runner=BackgroundRunner(workers=1);self.cancel=threading.Event();self.closed=self.busy=False;self.result=None
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10);box.set_border_width(14);self.add(box)
        self.path=Gtk.Entry();self.path.set_text(str(path or ''));self.path.get_accessible().set_name('PDF para verificar assinaturas')
        box.pack_start(self.path,False,False,0)
        note=Gtk.Label(label='Verifica a integridade CMS offline. Confiança do certificado, revogação, carimbos de tempo e validade legal não são avaliados.',xalign=0)
        note.set_line_wrap(True);box.pack_start(note,False,False,0)
        actions=Gtk.Box(spacing=8);box.pack_start(actions,False,False,0)
        self.verify=Gtk.Button(label='Verificar');self.verify.connect('clicked',self._verify);actions.pack_start(self.verify,False,False,0)
        cancel=Gtk.Button(label='Cancelar');cancel.connect('clicked',self._cancel);actions.pack_start(cancel,False,False,0)
        self.rows=Gtk.ListBox();scroll=Gtk.ScrolledWindow();scroll.add(self.rows);box.pack_start(scroll,True,True,0)
        self.status=Gtk.Label(label='Informe um PDF local de até 64 MiB.',xalign=0);self.status.set_line_wrap(True);box.pack_start(self.status,False,False,0)
        self.path.connect('changed',self._changed);self.connect('destroy',self._destroy)

    def _changed(self,*_):
        self._cancel();self.result=None
        for row in self.rows.get_children():self.rows.remove(row)
        self.status.set_text('Verifique o arquivo selecionado.')

    def _verify(self,*_):
        if self.busy or self.closed:return
        self.cancel=threading.Event();cancel=self.cancel;self.busy=True;self.result=None;path=self.path.get_text()
        for row in self.rows.get_children():self.rows.remove(row)
        self.path.set_sensitive(False);self.verify.set_sensitive(False);self.status.set_text('Verificando integridade…')
        def finish():self.busy=False;self.path.set_sensitive(True);self.verify.set_sensitive(True)
        def loaded(result):
            if self.closed or cancel.is_set():return
            finish()
            if result is None:return
            self.result=result
            labels={'verified':'Integridade CMS verificada','not_verified':'Integridade não validada',
                    'unsupported_or_malformed':'Formato não suportado ou inválido','unsigned':'Campo sem assinatura','unavailable':'Verificador indisponível ou sem resultado'}
            for item in result['signatures']:
                text=display_attachment_name(item['field'])+' · '+labels[item['status']]
                if item['status']=='verified' and not item['current_file_covered']:text+=' · há dados posteriores à revisão assinada'
                label=Gtk.Label(label=text,xalign=0);label.set_line_wrap(True);label.set_selectable(True)
                label.set_margin_top(5);label.set_margin_bottom(5);self.rows.add(label)
            self.rows.show_all()
            self.status.set_text(f"{len(result['signatures'])} campo(s), {result['omitted_signatures']} omitido(s) pelo limite. Confiança dos certificados não avaliada.")
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('signature-info',lambda:invoke_signature_inspection(path,cancel),loaded,failed,priority='background')

    def _cancel(self,*_):
        if not self.busy:return
        self.cancel.set();self.runner.invalidate('signature-info');self.busy=False
        self.path.set_sensitive(True);self.verify.set_sensitive(True);self.status.set_text('Verificação cancelada.')

    def _destroy(self,*_):self.closed=True;self.cancel.set();self.runner.shutdown()
