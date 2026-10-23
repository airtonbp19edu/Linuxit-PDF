"""Native file decoding/play/pause/EOS on a virtual sink, plus calibrated snaps."""
import math,os,sys,tempfile,time,unittest,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from measurement import snap_point,measure
from ocr_runtime import gstreamer_available


class MeasurementSnapTests(unittest.TestCase):
    def test_grid_and_angle_constraints_have_explicit_priority_and_keep_length(self):
        self.assertEqual(snap_point((12.2,19.1),grid=5),(10,20))
        point=snap_point((10,8),(0,0),grid=5,angle_step=45)
        self.assertAlmostEqual(point[0],point[1]);self.assertAlmostEqual(math.hypot(*point),math.hypot(10,8))
        self.assertAlmostEqual(measure([(0,0),point],unit='in'),math.hypot(10,8)/72)
        with self.assertRaises(ValueError):snap_point((1,2),grid=float('nan'))


@unittest.skipUnless(gstreamer_available(),'Requires native GStreamer decoding elements')
class LocalPlaybackTests(unittest.TestCase):
    def setUp(self):
        from gi.repository import GLib
        self.context=GLib.MainContext.default();self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'synthetic.wav'
        with wave.open(str(self.path),'wb') as output:
            output.setnchannels(1);output.setsampwidth(2);output.setframerate(8000);output.writeframes(b'\0\0'*8000)

    def until(self,predicate,timeout=4):
        end=time.monotonic()+timeout
        while time.monotonic()<end:
            while self.context.pending():self.context.iteration(False)
            if predicate():return
            time.sleep(.01)
        self.fail('Native media state did not arrive')

    def test_real_decode_pause_resume_eos_and_close_release_pipeline(self):
        from local_playback import LocalPlayback
        events=[];player=LocalPlayback(self.path,lambda *args:events.append(args),audio_sink='fakesink',video_sink='fakesink');self.addCleanup(player.close)
        player.play();self.until(lambda:player.state=='playing' and bool(player.linked))
        self.assertEqual(player.linked,{'audio'});player.pause();self.until(lambda:player.state=='paused')
        position,duration=player.position();self.assertIsNotNone(duration);self.assertAlmostEqual(duration,1,places=2)
        player.play();self.until(lambda:player.state=='ended');self.assertTrue(any(e[0]=='ended' for e in events))
        player.close();self.assertTrue(player.closed)
        with self.assertRaises(RuntimeError):player.play()

    def test_short_file_plays_for_its_duration_instead_of_ending_at_once(self):
        # Regression: PLAYING before the audio branch was prerolled let a 1 s file
        # reach EOS within milliseconds (seen 1 in 25 runs before the fix).
        from local_playback import LocalPlayback
        for attempt in range(3):
            player=LocalPlayback(self.path,audio_sink='fakesink',video_sink='fakesink');self.addCleanup(player.close)
            started=time.monotonic();player.play();self.until(lambda:player.state=='ended')
            with self.subTest(attempt=attempt):self.assertGreaterEqual(time.monotonic()-started,.8)
            player.close()

    def test_stop_then_play_and_malformed_media_report_without_process_leak(self):
        from local_playback import LocalPlayback
        player=LocalPlayback(self.path,audio_sink='fakesink',video_sink='fakesink');self.addCleanup(player.close)
        player.play();self.until(lambda:player.state=='playing');player.stop();self.assertEqual(player.state,'stopped')
        player.play();self.until(lambda:player.state=='playing');player.stop()
        bad=Path(self.temp.name)/'bad.wav';bad.write_bytes(b'not an audio file')
        other=LocalPlayback(bad,audio_sink='fakesink',video_sink='fakesink');self.addCleanup(other.close)
        other.play();self.until(lambda:other.state=='error')

    def test_gtk_controls_and_embedded_video_widget_are_constructed(self):
        from gi.repository import Gtk
        from media_window import MediaWindow
        parent=Gtk.Window();self.addCleanup(parent.destroy)
        window=MediaWindow(parent,self.path,audio_sink='fakesink');self.addCleanup(window.destroy)
        window.show_all();self.assertIsNotNone(window.player.video.get_property('widget'))
        window.player.play();self.until(lambda:window.player.state=='playing');window.destroy();self.assertTrue(window.player.closed)
