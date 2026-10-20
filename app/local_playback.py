"""Explicit local-file GStreamer playback; no URI/playlist source is created."""
from pathlib import Path
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
Gst.init(None)

SUFFIXES={'.wav','.ogg','.oga','.ogv','.webm','.mp4','.m4a','.mp3','.avi','.mov','.mkv','.flac'}


class LocalPlayback:
    def __init__(self,path,on_event=lambda state,detail:None,*,audio_sink='autoaudiosink',video_sink='gtksink'):
        path=Path(path).resolve(strict=True)
        if not path.is_file() or not 0<path.stat().st_size<=64*1024**2 or path.suffix.lower() not in SUFFIXES:
            raise ValueError('Mídia local:WAV/OGG/WebM/MP4/MP3/AVI/MOV/MKV/FLAC de até64MiB.')
        if audio_sink not in {'autoaudiosink','fakesink'} or video_sink not in {'gtksink','fakesink'}:raise ValueError('Saída de mídia inválida.')
        self.event=on_event;self.closed=False;self.state='stopped';self.linked=set();self._play_after_preroll=False
        self.pipeline=Gst.Pipeline.new(None)
        self.source=self._element('filesrc');self.source.set_property('location',str(path))
        self.decoder=self._element('decodebin');self.source.link(self.decoder)
        self.audio_queue=self._element('queue');convert=self._element('audioconvert');resample=self._element('audioresample')
        self.volume=self._element('volume');self.audio=self._element(audio_sink)
        for a,b in zip([self.audio_queue,convert,resample,self.volume],[convert,resample,self.volume,self.audio]):
            if not a.link(b):raise RuntimeError('Não foi possível montar a saída de áudio.')
        self.video_queue=self._element('queue');vconvert=self._element('videoconvert');self.video=self._element(video_sink)
        self.video_queue.link(vconvert);vconvert.link(self.video)
        self.branches={'audio':[self.audio_queue,convert,resample,self.volume,self.audio],
                       'video':[self.video_queue,vconvert,self.video]}
        # Sinks keep async preroll: only discovered branches are in the pipeline,
        # so an unused sink never holds it, and PLAYING waits for real data.
        # With async disabled, PLAYING could start before the audio branch was
        # linked and a short file reached EOS at once (intermittent, 1 in 25).
        if audio_sink=='fakesink':self.audio.set_property('sync',True)
        if video_sink=='fakesink':self.video.set_property('sync',True)
        # Add only discovered streams; an unused sink would prevent pipeline EOS.
        for branch in self.branches.values():
            for element in branch:self.pipeline.remove(element)
        self.decoder.connect('pad-added',self._pad)
        self.bus=self.pipeline.get_bus();self.bus.add_signal_watch();self.handler=self.bus.connect('message',self._message)

    def _element(self,name):
        element=Gst.ElementFactory.make(name)
        if element is None:raise RuntimeError('Componente de mídia indisponível:'+name)
        self.pipeline.add(element);return element

    def _pad(self,decoder,pad):
        caps=pad.get_current_caps() or pad.query_caps(None);name=caps.get_structure(0).get_name() if caps and caps.get_size() else ''
        kind='audio' if name.startswith('audio/') else 'video' if name.startswith('video/') else None
        if kind and kind not in self.linked:
            branch=self.branches[kind]
            for element in branch:
                if element.get_parent() is None:self.pipeline.add(element)
            # Removing a GstBin child breaks its links; rebuild after reparenting.
            for a,b in zip(branch,branch[1:]):
                if not a.get_static_pad('src').is_linked():a.link(b)
            sink=(self.audio_queue if kind=='audio' else self.video_queue).get_static_pad('sink')
            if pad.link(sink)==Gst.PadLinkReturn.OK:
                self.linked.add(kind)
                for element in reversed(branch):element.sync_state_with_parent()

    def _message(self,bus,message):
        if self.closed:return
        if message.type==Gst.MessageType.ERROR:
            error,debug=message.parse_error();self.pipeline.set_state(Gst.State.NULL);self.state='error';self.event('error',error.message[:500])
        elif message.type==Gst.MessageType.ASYNC_DONE and message.src==self.pipeline and self._play_after_preroll:
            self._play_after_preroll=False
            if self.pipeline.set_state(Gst.State.PLAYING)==Gst.StateChangeReturn.FAILURE:
                self.state='error';self.event('error','Falha ao iniciar mídia local.')
        elif message.type==Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL);self.state='ended';self.event('ended','')
        elif message.type==Gst.MessageType.STATE_CHANGED and message.src==self.pipeline:
            old,new,pending=message.parse_state_changed()
            if new in (Gst.State.PLAYING,Gst.State.PAUSED):
                self.state='playing' if new==Gst.State.PLAYING else 'paused';self.event(self.state,'')

    def play(self):
        """From a prerolled pause, resume at once; otherwise preroll first, then play."""
        if self.closed:raise RuntimeError('Reprodutor encerrado.')
        prerolled=bool(self.linked) and self.state=='paused'
        self._play_after_preroll=not prerolled
        target=Gst.State.PLAYING if prerolled else Gst.State.PAUSED
        if self.pipeline.set_state(target)==Gst.StateChangeReturn.FAILURE:
            self._play_after_preroll=False;raise RuntimeError('Falha ao iniciar mídia local.')

    def pause(self):
        if not self.closed:self._play_after_preroll=False;self.pipeline.set_state(Gst.State.PAUSED)

    def stop(self):
        if self.closed:return
        self._play_after_preroll=False;self.pipeline.set_state(Gst.State.NULL);self.linked.clear();self.state='stopped';self.event('stopped','')

    def seek(self,seconds):
        import math
        if type(seconds) not in (int,float) or not math.isfinite(seconds) or not 0<=seconds<=86400:raise ValueError('Posição de mídia inválida.')
        return not self.closed and self.pipeline.seek_simple(Gst.Format.TIME,Gst.SeekFlags.FLUSH|Gst.SeekFlags.KEY_UNIT,int(seconds*Gst.SECOND))

    def position(self):
        ok,pos=self.pipeline.query_position(Gst.Format.TIME);known,duration=self.pipeline.query_duration(Gst.Format.TIME)
        return (pos/Gst.SECOND if ok else None,duration/Gst.SECOND if known else None)

    def close(self):
        if self.closed:return
        self.stop();self.closed=True;self.bus.disconnect(self.handler);self.bus.remove_signal_watch()
