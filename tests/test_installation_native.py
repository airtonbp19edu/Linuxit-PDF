"""Installation identity and GTK native chooser handoff contracts."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from test_attachment_search import text_pdf
from installation_info import installation_info,APP_ID


class InstallationInfoTests(unittest.TestCase):
    def test_known_flatpak_identity_has_explicit_system_update_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            info=Path(directory)/'flatpak-info'
            info.write_text('[Application]\nname='+APP_ID+'\n[Instance]\nbranch=devel\n')
            result=installation_info(info)
            self.assertEqual(result['installation'],'flatpak');self.assertEqual(result['branch'],'devel')
            self.assertEqual(result['update_command'],'flatpak update '+APP_ID)
            self.assertFalse(result['remote_update_checked'])

    def test_unrelated_or_malformed_metadata_cannot_change_update_command(self):
        with tempfile.TemporaryDirectory() as directory:
            info=Path(directory)/'flatpak-info'
            for value in ('[Application]\nname=malicious;command\n','broken','x'*65537):
                info.write_text(value);result=installation_info(info)
                self.assertIsNone(result['update_command']);self.assertIsNone(result['app_id'])


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK and X display')
class NativeChooserGUITests(unittest.TestCase):
    def test_native_chooser_accept_opens_transactionally_and_cancel_keeps_document(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            first=Path(directory)/'first.pdf';second=Path(directory)/'second.pdf'
            first.write_bytes(text_pdf(['first']));second.write_bytes(text_pdf(['second']))
            window=PDFWindow(str(first))
            try:
                wait_for(lambda:window.filepath==str(first.resolve()) and window._pending_document is None)
                with patch('main.choose_pdf_native',return_value=None):window._choose_open_native()
                self.assertEqual(window.filepath,str(first.resolve()))
                with patch('main.choose_pdf_native',return_value=str(second)):window._choose_open_native()
                wait_for(lambda:window.filepath==str(second.resolve()) and window._pending_document is None)
                self.assertEqual(window.page_count,1)
            finally:window.destroy()
