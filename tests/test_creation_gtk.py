"""Actual GTK creation, worker cancellation and Poppler opening of new PDFs."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from test_pdf_creation import Image, PdfReader
from test_search_extensions_gtk import Gtk, wait_for, capture


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')), 'Requires GTK3 and X11')
class CreationGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-create-ui-');self.root = Path(self.temp.name)
        self.first, self.second = self.root/'first.png', self.root/'second.jpg'
        for path, size, color in [(self.first, (40, 20), 'red'), (self.second, (20, 40), 'blue')]:
            with Image.new('RGB', size, color) as image:image.save(path)
        self.output = self.root/'new.pdf';self.children = [];self.errors = []
        self.hook = patch.object(sys, 'excepthook', lambda *args: self.errors.append(args));self.hook.start()
        self.quit = patch.object(Gtk, 'main_quit');self.quit.start()
        load_css();self.parent = PDFWindow();self.parent.show_all();self.parent._show_creation()
        self.window = self.parent.creation_window
        wait_for(lambda: self.window.get_realized())

    def tearDown(self):
        if not self.window.closed:self.window.destroy()
        self.parent.destroy()
        for proc in self.children:
            if proc.poll() is None:proc.kill();proc.wait()
        self.quit.stop();self.hook.stop();self.temp.cleanup();self.assertEqual(self.errors, [])

    def choose_images(self):
        with patch.object(self.window, '_choose', return_value=[str(self.first), str(self.second)]):self.window._add()

    def create(self):
        with patch.object(self.window, '_choose', return_value=str(self.output)):self.window._create()

    def test_ordered_creation_opens_actual_pdf_and_poppler_renders_pixels(self):
        w = self.window;self.choose_images()
        w.images.select_row(w.images.get_row_at_index(1));w._move(-1)
        self.assertEqual(w.paths, [str(self.second), str(self.first)])
        w.dpi.set_value(72);self.create()
        wait_for(lambda: not w.busy and w.result is not None)
        self.assertIn('2 página(s)', w.status.get_text());capture(w, 'image-creation')
        pages = PdfReader(self.output).pages
        self.assertEqual((float(pages[0].mediabox.width), float(pages[0].mediabox.height)), (20, 40))
        w._open()
        wait_for(lambda: self.parent.filepath == str(self.output) and self.parent.current_pixbuf is not None)
        self.assertEqual(self.parent.page_count, 2)
        pixel = self.parent.current_pixbuf.get_pixels()[:3]
        self.assertGreater(pixel[2], 240);self.assertLess(pixel[0], 20)

    def test_bmp_webp_tiff_selection_worker_and_opening(self):
        sources=[]
        for name,options in (('new.bmp',{}),('new.webp',{'lossless':True}),('new.tiff',{'compression':'tiff_lzw'})):
            path=self.root/name
            with Image.new('RGB',(20,15),'green') as image:image.save(path,**options)
            sources.append(str(path))
        with patch.object(self.window,'_choose',return_value=sources):self.window._add()
        self.create();wait_for(lambda:not self.window.busy and self.window.result is not None)
        self.assertEqual([s['format'] for s in self.window.result['sources']],['BMP','WEBP','TIFF'])
        self.window._open();wait_for(lambda:self.parent.page_count==3 and self.parent.current_pixbuf is not None)
        pixel=self.parent.current_pixbuf.get_pixels()[:3]
        self.assertLess(pixel[0],20);self.assertGreater(pixel[1],100);self.assertLess(pixel[2],20)

    def test_tiff_block_order_expands_pages_and_poppler_renders_each_color(self):
        source=self.root/'multipage.tiff'
        with Image.new('RGB',(30,20),'red') as first,Image.new('RGB',(20,40),'blue') as second:
            first.save(source,save_all=True,append_images=[second],compression='tiff_lzw')
        with patch.object(self.window,'_choose',return_value=[str(self.first),str(source)]):self.window._add()
        w=self.window;w.images.select_row(w.images.get_row_at_index(1));w._move(-1)
        self.assertIn('2 arquivo(s)',w.status.get_text())
        w.dpi.set_value(72);self.create()
        wait_for(lambda:not w.busy and w.result is not None)
        self.assertEqual((w.result['input_count'],w.result['pages']),(2,3))
        self.assertEqual([s['frame'] for s in w.result['sources']],[1,2,1])
        capture(w,'tiff-creation')
        w._open();wait_for(lambda:self.parent.page_count==3 and self.parent.current_pixbuf is not None)
        for index,color in enumerate(((255,0,0),(0,0,255),(255,0,0))):
            self.parent.goto_page(index,force=True)
            wait_for(lambda:self.parent.displayed_page==index and self.parent.current_pixbuf is not None)
            pixel=self.parent.current_pixbuf.get_pixels()[:3]
            for actual,expected in zip(pixel,color):self.assertLess(abs(actual-expected),20)

    def test_total_tiff_page_limit_is_visible_and_no_partial_copy_is_opened(self):
        source=self.root/'hundred.tiff'
        with Image.new('RGB',(2,2),'blue') as first:
            first.save(source,save_all=True,append_images=[Image.new('RGB',(2,2),'red') for _ in range(99)])
        original=source.read_bytes()
        with patch.object(self.window,'_choose',return_value=[str(self.first),str(source)]):self.window._add()
        self.create();wait_for(lambda:not self.window.busy and '100 páginas' in self.window.status.get_text())
        self.assertIsNone(self.window.result)
        self.assertFalse(self.window.open_button.get_sensitive())
        self.assertTrue(self.window.create.get_sensitive())
        self.assertFalse(self.output.exists());self.assertEqual(source.read_bytes(),original)

    def test_dialog_cancellation_and_existing_destination_preserve_files(self):
        w = self.window;self.choose_images()
        with patch.object(w, '_choose', return_value=None):w._create()
        self.assertFalse(w.busy);self.assertFalse(self.output.exists())
        self.output.write_bytes(b'original destination');self.create()
        wait_for(lambda: not w.busy and 'nome novo' in w.status.get_text())
        self.assertIsNone(w.result);self.assertFalse(w.open_button.get_sensitive())
        self.assertEqual(self.output.read_bytes(), b'original destination')

    def test_changed_created_pdf_is_not_opened_as_verified_result(self):
        self.choose_images();self.create()
        wait_for(lambda: self.window.result is not None and not self.window.busy)
        self.output.write_bytes(b'changed by another writer');self.window._open()
        wait_for(lambda: not self.window.busy and 'mudou' in self.window.status.get_text())
        self.assertIsNone(self.parent.filepath)

    def test_selection_remove_duplicates_order_and_empty_request(self):
        w = self.window;w._create();self.assertIn('pelo menos', w.status.get_text())
        self.choose_images();self.choose_images();self.assertEqual(len(w.paths), 2)
        w.images.select_row(w.images.get_row_at_index(0));w._move(-1)
        self.assertEqual(w.paths[0], str(self.first));w._remove()
        self.assertEqual(w.paths, [str(self.second)])
        w._remove();self.assertEqual(w.paths, [])

    def test_cancel_and_destroy_kill_real_worker_without_stale_callbacks(self):
        import search_tasks
        original = subprocess.Popen
        def delayed(*args, **kwargs):
            proc = original([sys.executable, '-c', 'import time;time.sleep(30)'], **kwargs)
            self.children.append(proc);return proc
        self.choose_images()
        with patch.object(search_tasks.subprocess, 'Popen', side_effect=delayed):
            self.create();wait_for(lambda: len(self.children) == 1)
            self.assertFalse(self.window.create.get_sensitive());self.window._cancel()
            wait_for(lambda: self.children[0].poll() is not None)
            self.assertFalse(self.window.busy);self.assertFalse(self.output.exists())
            self.create();wait_for(lambda: len(self.children) == 2)
            self.window.destroy();wait_for(lambda: self.children[1].poll() is not None)
            self.assertTrue(self.window.closed);self.assertFalse(self.output.exists())
