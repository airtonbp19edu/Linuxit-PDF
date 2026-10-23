"""Offline signature integrity, explicitly separate from certificate trust."""
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from async_core import BackgroundRunner
from attachment_tasks import display_attachment_name
from pdf_signatures import invoke_signature_inspection
from pdf_signing import invoke_sign_copy
from pdf_preservation import invoke_preservation
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
        note=Gtk.Label(label='Integridade CMS offline. CA, CRL e OCSP locais; DSS incremental e carimbos RFC3161 com pedido/resposta de TSA. Nenhum serviço é contatado. Não determina validade legal nem PAdES-LTA universal.',xalign=0)
        note.set_line_wrap(True);box.pack_start(note,False,False,0)
        actions=Gtk.Box(spacing=8);box.pack_start(actions,False,False,0)
        self.verify=Gtk.Button(label='Verificar');self.verify.connect('clicked',self._verify);actions.pack_start(self.verify,False,False,0)
        self.trust=Gtk.Button(label='Validar com CA/CRL…');self.trust.connect('clicked',self._verify_trust);actions.pack_start(self.trust,False,False,0)
        self.sign=Gtk.Button(label='Assinar cópia com PEM…');self.sign.connect('clicked',self._sign);actions.pack_start(self.sign,False,False,0)
        cancel=Gtk.Button(label='Cancelar');cancel.connect('clicked',self._cancel);actions.pack_start(cancel,False,False,0)
        preservation=Gtk.Box(spacing=8);box.pack_start(preservation,False,False,0)
        for label,callback in (('Incorporar DSS em cópia…',self._add_dss),('Exportar pedido TSA…',self._prepare_timestamp),
                               ('Importar resposta TSA…',self._complete_timestamp)):
            button=Gtk.Button(label=label);button.connect('clicked',callback);preservation.pack_start(button,False,False,0)
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

    def _material_files(self,title):
        dialog=Gtk.FileChooserDialog(title=title,transient_for=self,modal=True,action=Gtk.FileChooserAction.OPEN)
        dialog.set_select_multiple(True)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Sem estes arquivos',Gtk.ResponseType.NO,'Selecionar',Gtk.ResponseType.OK)
        try:
            response=dialog.run()
            return dialog.get_filenames() if response==Gtk.ResponseType.OK else [] if response==Gtk.ResponseType.NO else None
        finally:dialog.destroy()

    def _preserve(self,command,source,request,message):
        self.cancel=threading.Event();cancel=self.cancel;self.busy=True
        self.path.set_sensitive(False);self.verify.set_sensitive(False);self.sign.set_sensitive(False);self.status.set_text(message)
        def work():
            return invoke_preservation(command,source,dict(request,source_sha256=request.get('source_sha256') or _sha(source)),cancel)
        def finish():
            self.busy=False;self.path.set_sensitive(True);self.verify.set_sensitive(True);self.sign.set_sensitive(True)
        def done(result):
            if self.closed or cancel.is_set():return
            finish()
            if not result:return
            if command=='timestamp-prepare':
                self.status.set_text('Pedido salvo em '+result['query']+'. A pasta contém uma revisão incompleta; obtenha uma resposta TSA e use Importar resposta TSA. Nenhuma conexão foi feita.')
            else:
                self.path.set_text(result['path'])
                self.status.set_text('Cópia incremental salva: '+result['path']+'. As revisões anteriores foram preservadas. Verifique com CA local; sem garantia PAdES-LTA universal.')
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('signature-info',work,done,failed,priority='background')

    def _add_dss(self,*_):
        if self.busy or self.closed:return
        source=self.path.get_text().strip()
        if not source:self.status.set_text('Informe um PDF assinado para preservar material DSS.');return
        request={}
        for key,title in (('certificates','Certificados locais PEM/DER para DSS'),('crls','CRLs locais PEM/DER para DSS'),
                          ('ocsps','Respostas OCSP locais DER para DSS')):
            values=self._material_files(title)
            if values is None:return
            request[key]=values
        if not any(request.values()):self.status.set_text('Selecione ao menos um certificado, CRL ou OCSP.');return
        dialog=Gtk.Dialog(title='Associar material às assinaturas',transient_for=self,modal=True)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Continuar',Gtk.ResponseType.OK)
        box=dialog.get_content_area();box.set_spacing(8);box.set_border_width(12)
        hint=Gtk.Label(label='O material será armazenado no DSS global. Opcionalmente, marque assinaturas verificadas para criar ou atualizar suas entradas VRI. A associação não comprova confiança nem completude; valide depois com CA/CRL. Se não houver assinaturas listadas, use Verificar primeiro.',xalign=0)
        hint.set_line_wrap(True);hint.set_max_width_chars(70);box.add(hint)
        choices=[]
        for item in (self.result or {}).get('signatures',[]):
            if item['status']=='verified':
                control=Gtk.CheckButton.new_with_label(display_attachment_name(item['field']));box.add(control);choices.append((item['field'],control))
        dialog.show_all()
        try:
            if dialog.run()!=Gtk.ResponseType.OK:return
            selected=[name for name,control in choices if control.get_active()]
        finally:dialog.destroy()
        if selected:
            request['vri_fields']=selected
            request['source_sha256']=self.result['source_sha256']
        destination=self._identity_file('Salvar cópia com DSS em arquivo novo',True,Path(source).stem+'-dss.pdf')
        if not destination:return
        self._preserve('signature-dss',source,dict(request,destination=destination),'Acrescentando material DSS em uma cópia incremental…')

    def _prepare_timestamp(self,*_):
        if self.busy or self.closed:return
        source=self.path.get_text().strip()
        if not source:self.status.set_text('Informe o PDF que receberá o carimbo de documento.');return
        folder=self._identity_file('Escolher nome de uma NOVA pasta para o pedido TSA',True,Path(source).stem+'-pedido-tsa')
        if not folder:return
        self._preserve('timestamp-prepare',source,dict(folder=folder),'Preparando revisão e pedido RFC3161 com nonce…')

    def _complete_timestamp(self,*_):
        if self.busy or self.closed:return
        source=self.path.get_text().strip()
        if not source:self.status.set_text('Informe o mesmo PDF usado para exportar o pedido TSA.');return
        dialog=Gtk.FileChooserDialog(title='Pasta do pedido TSA exportado',transient_for=self,modal=True,action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Selecionar',Gtk.ResponseType.OK)
        try:folder=dialog.get_filename() if dialog.run()==Gtk.ResponseType.OK else None
        finally:dialog.destroy()
        if not folder:return
        response=self._identity_file('Resposta TSA DER (TimeStampResp .tsr)')
        if not response:return
        ca=self._identity_file('CA confiável PEM da TSA, selecionada explicitamente')
        if not ca:return
        destination=self._identity_file('Salvar nova cópia com carimbo de documento',True,Path(source).stem+'-carimbado.pdf')
        if not destination:return
        policy=dict(roots=[ca],crls=[],require_revocation=False,at_time=None)
        self._preserve('timestamp-complete',source,dict(folder=folder,response=response,destination=destination,trust_policy=policy),
                       'Validando resposta, nonce, resumo e cadeia TSA antes de publicar a cópia…')

    def _verify_trust(self,*_):
        if self.busy or self.closed:return
        root=self._identity_file('Escolher CA confiável PEM para esta validação')
        if not root:return
        dialog=Gtk.MessageDialog(transient_for=self,modal=True,message_type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.YES_NO,text='Exigir revogação offline por CRL ou OCSP? O material DSS do PDF também será considerado. A seguir, cancele a seleção de CRL para usar somente o DSS.')
        try:require=dialog.run()==Gtk.ResponseType.YES
        finally:dialog.destroy()
        crl=self._identity_file('Escolher lista de revogação CRL local') if require else None
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
                if item.get('kind')=='document_timestamp':
                    # RFC 3161 document timestamp (E09): integrity is the token signature plus the imprint.
                    text=display_attachment_name(item['field'])+' · Carimbo de tempo do documento · '+labels[item['status']]
                    if item.get('timestamp_time'):text+=' · horário '+item['timestamp_time']
                if item['status']=='verified' and not item['current_file_covered']:text+=' · há dados posteriores à revisão assinada'
                trust=item.get('trust')
                if trust:
                    text+=' · cadeia '+('confiável na CA selecionada' if trust['chain_verified'] else 'não validada')
                    text+=' · revogação '+('verificada offline' if trust['revocation_verified'] else 'desconhecida/não validada')
                    if trust['timestamps']:text+=' · carimbos '+str(sum(t['verified'] for t in trust['timestamps']))+'/'+str(len(trust['timestamps']))+' verificados'
                    used=trust.get('dss_used') or {}
                    if used.get('certificates') or used.get('crls'):text+=f" · DSS usado: {used.get('certificates',0)} certificado(s), {used.get('crls',0)} CRL(s)"
                vri=item.get('vri')
                if vri:
                    text+=' · VRI '+('correspondente' if vri['matched'] else 'ausente; material global' if vri['scope']=='global_fallback' else 'ausente')
                    if vri['matched']:
                        complete=vri['validation_material_complete']
                        text+=' · material '+('validado na política offline' if complete is True else 'incompleto/não validado' if complete is False else 'não avaliado com CA/revogação')
                label=Gtk.Label(label=text,xalign=0);label.set_line_wrap(True);label.set_selectable(True)
                label.set_margin_top(5);label.set_margin_bottom(5);self.rows.add(label)
            self.rows.show_all()
            dss=result.get('dss')
            dss_text=(f"DSS no PDF: {dss['certificates']} certificado(s), {dss['crls']} CRL(s), {dss['ocsp_responses']} OCSP. " if dss
                      else (result.get('dss_error')+' ' if result.get('dss_error') else ''))
            self.status.set_text(dss_text+f"{len(result['signatures'])} campo(s), {result['omitted_signatures']} omitido(s) pelo limite. "+('Política de CA local aplicada por assinatura; sem decisão legal/LTV.' if policy else 'Confiança dos certificados não avaliada.'))
        def failed(exc):
            if self.closed or cancel.is_set():return
            finish();self.status.set_text(str(exc))
        self.runner.submit('signature-info',lambda:invoke_signature_inspection(path,cancel,policy),loaded,failed,priority='background')

    def _cancel(self,*_):
        if not self.busy:return
        self.cancel.set();self.runner.invalidate('signature-info');self.busy=False
        self.path.set_sensitive(True);self.verify.set_sensitive(True);self.sign.set_sensitive(True);self.status.set_text('Operação cancelada. Confira o destino antes de repetir uma gravação.')

    def _destroy(self,*_):self.closed=True;self.cancel.set();self.runner.shutdown()
