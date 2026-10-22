import hashlib,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from test_attachment_search import text_pdf

@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK display')
class ConversionGTKTests(unittest.TestCase):
    def test_window_pins_identity_before_document_replacement_and_shuts_down(self):
        import gi
        gi.require_version('Gtk','3.0')
        from gi.repository import Gtk
        from conversion_window import ConversionWindow
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';data=text_pdf(['original']);source.write_bytes(data)
            parent=Gtk.Window();window=ConversionWindow(parent,source)
            source.write_bytes(text_pdf(['replacement']))
            self.assertEqual(window.source_sha256,hashlib.sha256(data).hexdigest())
            with patch.object(window.runner,'shutdown',wraps=window.runner.shutdown) as shutdown:
                parent.destroy();self.assertTrue(window.closed);self.assertTrue(window.cancel.is_set());shutdown.assert_called_once()

