"""Explicit embedded-media selection; never activates PDF multimedia actions."""
from pathlib import Path
import tempfile,threading
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from async_core import BackgroundRunner
from search_tasks import run_search_worker
from attachment_tasks import display_attachment_name
from local_playback import SUFFIXES


class MediaAssetsWindow(Gtk.Window):
    def __init__(self,parent,session):
        super().__init__(title='Mídia incorporada',transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(760,450)
        self.session=session;self.runner=BackgroundRunner(workers=1);self.cancel=threading.Event();self.closed=self.busy=False
        self.folder=tempfile.TemporaryDirectory(prefix='linuxit-media-view-');self.children=[];self.report=None
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8,margin=12);self.add(box)
        note=Gtk.Label(label='Selecione para salvar ou reproduzir. Ações e URLs do PDF não são executadas. Modelos3D podem ser extraídos; renderizador U3D/PRC ainda indisponível.',xalign=0);note.set_line_wrap(True);box.add(note)
        self.assets=Gtk.ComboBoxText();box.add(self.assets)
        row=Gtk.Box(spacing=8);box.add(row)
        self.controls=[]
        for name,callback in [('Atualizar',self._refresh),('Reproduzir selecionado',self._play),('Salvar selecionado…',self._save)]:
            button=Gtk.Button(label=name);button.connect('clicked',callback);row.add(button);self.controls.append(button)
        self.status=Gtk.Label(xalign=0);self.status.set_line_wrap(True);self.status.set_selectable(True);box.add(self.status)
        self.connect('destroy',self._destroy);self._refresh()

    def _submit(self,work,done):
        if self.closed or self.busy:return
        self.busy=True;self.cancel=threading.Event();cancel=self.cancel
        for control in [self.assets,*self.controls]:control.set_sensitive(False)
        self.status.set_text('Lendo mídia local…')
        def finish():
            self.busy=False
            for control in [self.assets,*self.controls]:control.set_sensitive(True)
        def loaded(result):
            if self.closed:return
            finish()
            if result:done(result)
        def failed(error):
            if not self.closed:finish();self.status.set_text(str(error))
        def task():
            try:return work(cancel)
            finally:
                if self.closed:self.folder.cleanup()
        self.runner.submit('media',task,loaded,failed,priority='background')

    def _refresh(self,*_):
        def loaded(report):
            if report.get('schema')!='linuxit-media-assets-v1':raise RuntimeError('Resposta de mídia inválida.')
            self.report=report;self.assets.remove_all()
            for item in report['assets']:self.assets.append(str(item['index']),f"Pág.{item['page']+1} · {display_attachment_name(item['name'])} · {item['kind']}")
            self.assets.set_active(0);self.status.set_text(f"{len(report['assets'])} recurso(s) incorporado(s). Referências externas são ignoradas.")
        self._submit(lambda cancel:self.session.call(lambda path:run_search_worker('media-info',path,{},cancel)),loaded)

    def _selected(self):
        selected=self.assets.get_active_id()
        return next((row for row in (self.report or {}).get('assets',[]) if str(row['index'])==selected),None)

    def _extract(self,item,destination,done):
        if not self.session.info['permissions']['copy']:self.status.set_text('Extração não autorizada pelas permissões do PDF.');return
        identity=self.report['source_sha256']
        self._submit(lambda cancel:self.session.call(lambda path:run_search_worker('media-extract',path,dict(index=item['index'],destination=str(destination),source_sha256=identity),cancel)),done)

    def _play(self,*_):
        if self.busy:return
        item=self._selected()
        if not item:return
        if item['kind']=='3d' or item['suffix'] not in SUFFIXES:self.status.set_text('Renderizador desse formato indisponível. É possível salvar o recurso.');return
        import uuid
        target=Path(self.folder.name)/(uuid.uuid4().hex+item['suffix'])
        def loaded(result):
            from media_window import MediaWindow
            window=MediaWindow(self,target,cleanup=lambda:target.unlink(missing_ok=True));self.children.append(window)
            window.connect('destroy',lambda w:self.children.remove(w) if w in self.children else None);window.show_all();window.player.play()
            self.status.set_text('Reprodução local iniciada por sua seleção.')
        self._extract(item,target,loaded)

    def _save(self,*_):
        if self.busy:return
        item=self._selected()
        if not item:return
        dialog=Gtk.FileChooserDialog(title='Salvar recurso em arquivo novo',transient_for=self,modal=True,action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Salvar',Gtk.ResponseType.OK);dialog.set_current_name('recurso'+item['suffix'])
        try:
            if dialog.run()!=Gtk.ResponseType.OK:return
            target=dialog.get_filename()
        finally:dialog.destroy()
        self._extract(item,target,lambda report:self.status.set_text('Recurso salvo: '+report['path']))

    def _destroy(self,*_):
        self.closed=True;self.cancel.set();self.runner.shutdown()
        for child in list(self.children):child.destroy()
        if not self.busy:self.folder.cleanup()
