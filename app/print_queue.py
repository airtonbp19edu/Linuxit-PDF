"""Manage only jobs whose submission receipts were captured by this process."""
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from async_core import BackgroundRunner
import cups_backend as cups


class PrintQueueWindow(Gtk.Window):
    def __init__(self,parent,jobs):
        super().__init__(title='Trabalhos enviados pelo Linuxit',transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(650,350)
        self.jobs=jobs;self.closed=False;self.busy=False;self.runner=BackgroundRunner(workers=1)
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8,margin=12);self.add(box)
        label=Gtk.Label(label='Esta lista acompanha os trabalhos enviados nesta execução do aplicativo. O CUPS decide o cancelamento; uma página já impressa não pode ser recuperada.',xalign=0)
        label.set_line_wrap(True);box.pack_start(label,False,False,0)
        self.rows=Gtk.ListBox();self.rows.set_selection_mode(Gtk.SelectionMode.SINGLE)
        scroll=Gtk.ScrolledWindow();scroll.add(self.rows);box.pack_start(scroll,True,True,0)
        bar=Gtk.Box(spacing=6);box.pack_start(bar,False,False,0)
        self.refresh=Gtk.Button(label='Atualizar');self.refresh.connect('clicked',self._refresh)
        self.cancel=Gtk.Button(label='Cancelar selecionado');self.cancel.connect('clicked',self._cancel)
        bar.add(self.refresh);bar.add(self.cancel)
        self.status=Gtk.Label(xalign=0);self.status.set_line_wrap(True);box.pack_start(self.status,False,False,0)
        self.connect('destroy',self._close);self._render()

    def _render(self):
        for row in self.rows.get_children():self.rows.remove(row);row.destroy()
        for job in self.jobs:
            row=Gtk.ListBoxRow();row.job=job
            label=Gtk.Label(label=f"{job['id']} · {job['document']} · {job['status']}",xalign=0);label.set_line_wrap(True);row.add(label);self.rows.add(row)
        self.rows.show_all()
        self.refresh.set_sensitive(not self.busy);self.cancel.set_sensitive(not self.busy and bool(self.jobs))

    def _run(self,task):
        if self.busy:return
        self.busy=True;self.status.set_text('Consultando o CUPS…');self._render()
        def done(message):self.busy=False;self.status.set_text(message);self._render()
        def failed(error):self.busy=False;self.status.set_text(str(error));self._render()
        self.runner.submit('queue',task,done,failed)

    def _refresh(self,*_):
        def task():
            pending=cups.pending_jobs()
            for job in self.jobs:
                job['status']='Na fila' if job['id'] in pending else 'Fora da fila ativa; consulte o histórico do sistema'
            return 'Fila consultada. Ausência na fila ativa não distingue impressão, exclusão ou cancelamento.'
        self._run(task)

    def _cancel(self,*_):
        row=self.rows.get_selected_row()
        if row is None or self.busy:return
        job=row.job
        def task():
            message=cups.cancel_job(job['id']);job['status']='Cancelamento aceito';return message
        self._run(task)

    def _close(self,*_):self.closed=True;self.runner.shutdown()
