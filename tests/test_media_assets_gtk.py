"""Actual own reader dialogs use workers, save copies and play embedded WAV."""
import os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from test_search_extensions_gtk import Gtk,GLib,wait_for,capture
import test_media_layer_persistence as media_fixture
from test_measurement_layers_speech import layer_pdf
from pdf_layers import inspect_layers
from pypdf import PdfReader


@unittest.skipUnless(Gtk is not None and os.environ.get('DISPLAY'),'Native Linux GTK3')
class MediaAssetGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.quit=patch.object(Gtk,'main_quit');self.quit.start();self.addCleanup(self.quit.stop)
        self.window=PDFWindow();self.addCleanup(self.window.destroy);self.errors=[];self.window._error=self.errors.append

    def test_layer_panel_save_action_uses_original_auth_and_worker_publishes_selected_visibility(self):
        source=self.root/'layers.pdf';layer_pdf(source);before=source.read_bytes();target=self.root/'saved.pdf'
        self.window.open_document(str(source));wait_for(lambda:self.window.displayed_page==0 and len(getattr(self.window,'layer_checks',[]))==2)
        self.window.layer_checks[0].set_active(False);wait_for(lambda:not self.window._layer_busy)
        with patch.object(Gtk.FileChooserDialog,'run',return_value=Gtk.ResponseType.OK),patch.object(Gtk.FileChooserDialog,'get_filename',return_value=str(target)):
            self.window._save_layer_visibility()
        wait_for(target.exists);wait_for(lambda:'visibilidade salva' in self.window.status_file.get_text())
        self.assertEqual([r['visible'] for r in inspect_layers(PdfReader(target))],[False,True]);self.assertEqual(before,source.read_bytes());self.assertFalse(self.errors)

    def test_media_asset_list_and_explicit_extraction_roundtrip_through_actual_workers(self):
        from media_assets_window import MediaAssetsWindow
        fixture=media_fixture.MediaLayerPersistenceTests('test_pdf_sound_big_endian_pcm_is_converted_to_little_endian_wave');fixture.setUp()
        try:
            fixture.fixture();self.window.open_document(str(fixture.source));wait_for(lambda:self.window.displayed_page==0)
            dialog=MediaAssetsWindow(self.window,self.window.document_session);self.addCleanup(dialog.destroy);dialog.show_all()
            wait_for(lambda:dialog.report is not None and not dialog.busy)
            self.assertEqual(len(dialog.report['assets']),3);dialog.assets.set_active_id('1')
            target=self.root/'sound.wav'
            with patch.object(Gtk.FileChooserDialog,'run',return_value=Gtk.ResponseType.OK),patch.object(Gtk.FileChooserDialog,'get_filename',return_value=str(target)):
                dialog._save()
            wait_for(lambda:target.exists() and not dialog.busy);self.assertTrue(target.read_bytes().startswith(b'RIFF'))
            capture(dialog,'embedded-media-assets')
        finally:fixture.doCleanups()
