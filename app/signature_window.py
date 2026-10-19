"""Offline signature integrity, explicitly separate from certificate trust."""
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from async_core import BackgroundRunner
from attachment_tasks import display_attachment_name
from pdf_signatures import invoke_signature_inspection
from pdf_signing import invoke_sign_copy
from pdf_changes import _sha
from pathlib import Path


class SignatureWindow(Gtk.Window):
    def __init__(self,parent,path=None):
        super().__init__(title='Integridade de assinaturas PDF',transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(780,420)
        self.runner=BackgroundRunner(workers=1);self.cancel=threading.Event();self.closed=self.busy=False;self.result=None
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10);box.set_border_width(14);self.add(box)
        self.path=Gtk.Entry();self.path.set_text(str(path or ''));self.path.get_accessible().set_name('PDF para verificar assinaturas')
        box.pack_start(self.path,False,False,0)
        note=Gtk.Label(label='Integridade CMS offline. A validação com CA usa somente raízes/CRL locais selecionadas; carimbos RFC3161 são verificados quando presentes. Não determina validade legal nem PAdES-LTV.',xalign=0)
        note.set_line_wrap(True);box.pack_start(note,False,False,0)
        actions=Gtk.Box(spacing=8);box.pack_start(actions,False,False,0)
        self.verify=Gtk.Button(label='Verificar');self.verify.connect('clicked',self._verify);actions.pack_start(self.verify,False,False,0)
        self.trust=Gtk.Button(label='Validar com CA/CRL…');self.trust.connect('clicked',self._verify_trust);actions.pack_start(self.trust,False,False,0)
        self.sign=Gtk.Button(label='Assinar cópia com PEM…');self.sign.connect('clicked',self._sign);actions.pack_start(self.sign,False,False,0)
        cancel=Gtk.Button(label='Cancelar');cancel.connect('clicked',self._cancel);actions.pack_start(cancel,False,False,0)
        self.rows=Gtk.ListBox();scroll=Gtk.ScrolledWindow();scroll.add(self.rows);box.pack_start(scroll,True,True,0)
        self.status=Gtk.Label(label='Informe um PDF local de até 64 MiB.',xalign=0);self.status.set_line_wrap(True);box.pack_start(self.status,False,False,0)
        self.path.connect('changed',self._changed);self.connect('destroy',self._destroy)

    def _changed(self,*_):
        self._cancel();self.result=None
        for row in self.rows.get_children():self.rows.remove(row)
        self.status.set_text('Verifique o arquivo selecionado.')

    def _identity_file(self,title,save=False,default=None):
        dialog=Gtk.FileChooserDialog(title=title,transient_for=self,modal=True,
                    action=Gtk.FileChooserAction.SAVE if save else Gtk.FileChooserAction.OPEN)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Selecionar',Gtk.ResponseType.OK)
        if default:dialog.set_current_name(default)
        try:return dialog.get_filename() if dialog.run()==Gtk.ResponseType.OK else None
        finally:dialog.destroy()

    def _sign(self,*_):
        if self.busy or self.closed:return
        source=self.path.get_text().strip()
        if not source:self.status.set_text('Informe o PDF que receberá uma assinatura na cópia.');return
        cert=self._identity_file('Escolher certificado PEM')
        if not cert:return
        key=self._identity_file('Escolher chave privada PEM correspondente')
        if not key:return
        dialog=Gtk.Dialog(title='Senha da chave privada',transient_for=self,modal=True)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Continuar',Gtk.ResponseType.OK)
        password=Gtk.Entry();password.set_visibility(False);password.set_max_length(1024)
        password.get_accessible().set_name('Senha da chave privada PEM')
        label=Gtk.Label(label='Deixe em branco se a chave PEM não tiver senha.',margin=10)
        dialog.get_content_area().add(label);dialog.get_content_area().add(password);dialog.show_all()
        try:
            if dialog.run()!=Gtk.ResponseType.OK:return
            secret=password.get_text()
        finally:password.set_text('');dialog.destroy()
        destination=self._identity_file('Salvar cópia assinada em arquivo novo',True,Path(source).stem+'-assinado.pdf')
        if not destination:return
        self.cancel=threading.Event();cancel=self.cancel;self.busy=True
        self.verify.set_sensitive(False);self.sign.set_sensitive(False);self.path.set_sensitive(False)
        self.status.set_text('Assinando cópia local…')
        def work():
            request=dict(destination=destination,source_sha256=_sha(source),certificate=cert,private_key=key,password=secret)
            return invoke_sign_copy(source,request,cancel)
        def finish():
            self.busy=False;self.verify.set_sensitive(True);self.sign.set_sensitive(True);self.path.set_sensitive(True)
        def done(result):
            if self.closed or cancel.is_set():return
            finish()
            if result:self.path.set_text(result['path']);self.status.set_text('Cópia assinada. Verifique a integridade; confiança e carimbo de tempo não foram avaliados.')
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('signature-info',work,done,failed,priority='background')

    def _verify_trust(self,*_):
        if self.busy or self.closed:return
        root=self._identity_file('Escolher CA confiável PEM para esta validação')
        if not root:return
        dialog=Gtk.MessageDialog(transient_for=self,modal=True,message_type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.YES_NO,text='Exigir revogação offline com uma CRL local? Sem CRL, a confiança da cadeia pode ser verificada, mas a revogação fica desconhecida.')
        try:require=dialog.run()==Gtk.ResponseType.YES
        finally:dialog.destroy()
        crl=self._identity_file('Escolher lista de revogação CRL local') if require else None
        if require and not crl:return
        self._verify(policy=dict(roots=[root],crls=[crl] if crl else [],require_revocation=require,at_time=None))

    def _verify(self,*_,policy=None):
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
                trust=item.get('trust')
                if trust:
                    text+=' · cadeia '+('confiável na CA selecionada' if trust['chain_verified'] else 'não validada')
                    text+=' · revogação '+('verificada offline' if trust['revocation_verified'] else 'desconhecida/não validada')
                    if trust['timestamps']:text+=' · carimbos '+str(sum(t['verified'] for t in trust['timestamps']))+'/'+str(len(trust['timestamps']))+' verificados'
                label=Gtk.Label(label=text,xalign=0);label.set_line_wrap(True);label.set_selectable(True)
                label.set_margin_top(5);label.set_margin_bottom(5);self.rows.add(label)
            self.rows.show_all()
            self.status.set_text(f"{len(result['signatures'])} campo(s), {result['omitted_signatures']} omitido(s) pelo limite. "+('Política de CA local aplicada por assinatura; sem decisão legal/LTV.' if policy else 'Confiança dos certificados não avaliada.'))
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('signature-info',lambda:invoke_signature_inspection(path,cancel,policy),loaded,failed,priority='background')

    def _cancel(self,*_):
        if not self.busy:return
        self.cancel.set();self.runner.invalidate('signature-info');self.busy=False
        self.path.set_sensitive(True);self.verify.set_sensitive(True);self.sign.set_sensitive(True);self.status.set_text('Operação cancelada. Confira o destino antes de repetir uma gravação.')

    def _destroy(self,*_):self.closed=True;self.cancel.set();self.runner.shutdown()
