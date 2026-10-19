"""User-invoked local media player, reusable for temporary narrated WAV files."""
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib
from local_playback import LocalPlayback


class MediaWindow(Gtk.Window):
    def __init__(self,parent,path,cleanup=None,**sinks):
        super().__init__(title='Reprodução local',transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(720,450);self.cleanup=cleanup
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8,margin=10);self.add(box)
        self.status=Gtk.Label(label='Pronto para reproduzir; mídia local, sem carregar URLs.',xalign=0);self.status.set_line_wrap(True)
        self.player=LocalPlayback(path,self._event,**sinks)
        try:video=self.player.video.get_property('widget')
        except TypeError:video=None
        if video is not None:box.pack_start(video,True,True,0)
        row=Gtk.Box(spacing=8);box.pack_start(row,False,False,0)
        for name,callback in [('Reproduzir',self.player.play),('Pausar',self.player.pause),('Parar',self.player.stop)]:
            button=Gtk.Button(label=name);button.connect('clicked',lambda _,action=callback:self._action(action));row.add(button)
        self.volume=Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,0,1,.05);self.volume.set_value(1)
        self.volume.get_accessible().set_name('Volume da mídia');self.volume.connect('value-changed',lambda slider:self.player.volume.set_property('volume',slider.get_value()))
        row.pack_start(self.volume,True,True,0)
        box.pack_start(self.status,False,False,0);self.connect('destroy',self._destroy)
        self.timer=GLib.timeout_add(500,self._tick)

    def _event(self,state,detail):
        labels={'playing':'Reproduzindo','paused':'Pausado','stopped':'Parado','ended':'Fim da mídia','error':'Erro na mídia'}
        self.status.set_text(labels.get(state,state)+(' · '+detail if detail else ''))

    def _action(self,action):
        try:action()
        except (ValueError,RuntimeError) as exc:self.status.set_text(str(exc))

    def _tick(self):
        if self.player.closed:return False
        if self.player.state in ('playing','paused'):
            position,duration=self.player.position()
            if position is not None:self.status.set_text(('Pausado' if self.player.state=='paused' else 'Reproduzindo')+f' · {position:.1f}s'+(f' / {duration:.1f}s' if duration is not None else ''))
        return True

    def _destroy(self,*_):
        GLib.source_remove(self.timer);self.player.close()
        if self.cleanup:self.cleanup();self.cleanup=None
