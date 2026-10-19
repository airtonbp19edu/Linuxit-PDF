"""Actual OCR GTK/worker, copy opening, stale results and lifecycle controls."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_ocr_linux import TOOLS, scan
from test_pdf_ocr import PdfReader
from test_search_extensions_gtk import Gtk, wait_for, capture


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')) and TOOLS and sys.platform.startswith('linux'),
                     'Requires GTK/X11 and actual Linux OCR tools')
class OCRGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow,load_css
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-ocr-ui-');self.root=Path(self.temp.name)
        self.source,self.output=self.root/'scan.pdf',self.root/'new.pdf'
        scan(self.source)
        self.children=[];self.errors=[]
        self.hook=patch.object(sys,'excepthook',lambda *args:self.errors.append(args));self.hook.start()
        self.quit=patch.object(Gtk,'main_quit');self.quit.start()
        load_css();self.parent=PDFWindow(str(self.source));self.parent.show_all()
        wait_for(lambda:self.parent.current_pixbuf is not None)
        self.parent._show_ocr();self.window=self.parent.ocr_window
        wait_for(lambda:self.window.get_realized())
        self.window.language.set_active_id('eng');self.window.dpi.set_active_id('150')

    def tearDown(self):
        if not self.window.closed:self.window.destroy()
        self.parent.destroy()
        for child in self.children:
            if child.poll() is None:child.kill();child.wait()
        self.quit.stop();self.hook.stop();self.temp.cleanup()
        self.assertEqual(self.errors,[])

    def create(self):
        with patch.object(self.window,'_choose',return_value=str(self.output)):self.window._create()

    def complete(self):
        self.create();wait_for(lambda:not self.window.busy and self.window.result is not None,timeout=40)

    def test_menu_workflow_recognizes_opens_and_renders_actual_copy(self):
        original=self.source.read_bytes()
        self.complete();w=self.window
        self.assertIn('Cópia criada',w.status.get_text())
        self.assertIn('LINUXIT',PdfReader(self.output).pages[0].extract_text())
        capture(w,'ocr-copy')
        self.assertTrue(w.open_button.get_sensitive())
        w._open()
        wait_for(lambda:self.parent.filepath==str(self.output) and self.parent.current_pixbuf is not None)
        self.assertTrue(w.closed)
        self.assertEqual(self.source.read_bytes(),original)

    def test_cancelled_dialog_and_existing_destination_keep_files(self):
        with patch.object(self.window,'_choose',return_value=None):self.window._create()
        self.assertFalse(self.window.busy);self.assertFalse(self.output.exists())
        self.output.write_bytes(b'keep');self.create()
        wait_for(lambda:not self.window.busy and 'nome novo' in self.window.status.get_text())
        self.assertEqual(self.output.read_bytes(),b'keep')
        self.assertFalse(self.window.open_button.get_sensitive())

    def test_changed_source_and_changed_result_are_not_silently_opened(self):
        self.complete()
        self.output.write_bytes(b'changed copy');self.window._open()
        wait_for(lambda:not self.window.busy and 'mudou' in self.window.status.get_text())
        self.assertEqual(self.parent.filepath,str(self.source))
        self.output.unlink()
        self.source.write_bytes(b'changed source');self.create()
        wait_for(lambda:not self.window.busy and 'mudou' in self.window.status.get_text())
        self.assertIsNone(self.window.result);self.assertFalse(self.output.exists())

    def test_blank_page_has_explicit_no_text_notice(self):
        self.window.destroy()
        scan(self.source,('',))
        self.parent.open_document(str(self.source))
        # A transactional open deliberately retains the previous image until
        # the replacement has been validated; wait for the new blank document.
        wait_for(lambda:self.parent._pending_document is None and self.parent.current_pixbuf is not None)
        self.parent._show_ocr();self.window=self.parent.ocr_window
        self.window.dpi.set_active_id('150')
        self.complete()
        self.assertIn('Sem texto detectado nas páginas: 1',self.window.status.get_text())

    def test_cancel_and_document_close_stop_real_worker_and_ignore_stale_callbacks(self):
        import search_tasks
        original=subprocess.Popen
        def delayed(*args,**kwargs):
            process=original([sys.executable,'-c','import time;time.sleep(30)'],**kwargs)
            self.children.append(process);return process
        with patch.object(search_tasks.subprocess,'Popen',side_effect=delayed):
            self.create();wait_for(lambda:len(self.children)==1)
            self.assertFalse(self.window.create.get_sensitive())
            self.window._cancel();wait_for(lambda:self.children[0].poll() is not None)
            self.assertFalse(self.window.busy);self.assertFalse(self.output.exists())
            self.create();wait_for(lambda:len(self.children)==2)
            self.parent._close_document()
            wait_for(lambda:self.window.closed and self.children[1].poll() is not None)
            self.assertFalse(self.output.exists())
