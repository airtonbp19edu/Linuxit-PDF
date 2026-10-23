"""Actual concurrent cache publication and Windows reader-lock regression."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
import os
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from PIL import Image
import rendering


class RenderCachePublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        encoded=BytesIO();Image.new('RGB',(30,30),(10,30,50)).save(encoded,format='JPEG');self.raw=encoded.getvalue()

    def test_existing_valid_entry_is_reused_while_reader_holds_file(self):
        output=self.root/'cached.jpg';output.write_bytes(self.raw)
        temporary=self.root/'new.jpg';temporary.write_bytes(self.raw)
        with output.open('rb') as reader,patch('rendering.os.replace') as replace,patch('rendering.os.rename') as rename:
            rendering._publish_render_cache(temporary,output,rendering._valid_jpeg)
            self.assertEqual(reader.read(),self.raw)
            replace.assert_not_called();rename.assert_not_called()
        self.assertTrue(temporary.exists())

    def test_two_renderers_publish_same_key_without_overwriting_open_result(self):
        source=self.root/'source.pdf';source.write_bytes(b'synthetic identity; Poppler is replaced only in this test')
        cache=self.root/'cache';barrier=threading.Barrier(2)
        def run(command,timeout=120):
            if command[0]=='pdfinfo':return type('Result',(),{'stdout':b'Page 1 size: 300 x 300 pts'})()
            Path(command[-1]+'.jpg').write_bytes(self.raw)
            barrier.wait(timeout=10)
        real_replace=os.replace
        def exclusive_replace(temporary,output):
            if Path(output).exists():raise PermissionError('simulated Windows reader denies replacement')
            return real_replace(temporary,output)
        with patch('rendering._run',side_effect=run),patch('rendering.shutil.which',return_value='synthetic-poppler'), \
                patch('rendering.os.replace',side_effect=exclusive_replace):
            with ThreadPoolExecutor(max_workers=2) as workers:
                futures=[workers.submit(rendering.render_page,str(source),0,300,str(cache),'race','jpeg') for _ in range(2)]
                paths=[future.result(timeout=15) for future in futures]
        self.assertEqual(paths[0],paths[1]);self.assertEqual(Path(paths[0]).read_bytes(),self.raw)
        self.assertFalse(any(p.name.startswith('.') for p in cache.iterdir()))

    def test_invalid_cache_is_replaced_by_complete_image(self):
        output=self.root/'cached.jpg';output.write_bytes(b'broken')
        temporary=self.root/'new.jpg';temporary.write_bytes(self.raw)
        rendering._publish_render_cache(temporary,output,rendering._valid_jpeg)
        self.assertEqual(output.read_bytes(),self.raw);self.assertFalse(temporary.exists())
