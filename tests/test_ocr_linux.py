"""Actual Poppler/Tesseract recognition and process-group cancellation on own scans."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from test_pdf_ocr import ocr, PdfReader, PdfWriter
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat
from pdf_creation import _image_page

TOOLS = all(shutil.which(name) for name in ('tesseract','pdftocairo','pdftotext'))


def scan(path, texts=('LINUXIT DOCUMENTO TESTE',), dpi=150):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',64)
    writer = PdfWriter()
    for text in texts:
        with Image.new('RGB',(1200,450),'white') as image:
            if text:
                draw=ImageDraw.Draw(image)
                draw.text((40,100),text,fill='black',font=font)
                draw.rectangle((1100,350,1160,410),fill='red')
            _image_page(writer,image,dpi)
    writer.write(path)


@unittest.skipUnless(TOOLS and sys.platform.startswith('linux'),'Requires actual Linux Poppler and Tesseract')
class OCRLinuxTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-ocr-real-')
        self.root=Path(self.temp.name)
        self.source,self.output=self.root/'scan.pdf',self.root/'searchable.pdf'
        scan(self.source)

    def tearDown(self):
        self.temp.cleanup()

    def create(self,language='eng',dpi=150):
        request={'source_sha256':ocr.source_identity(self.source),'language':language,'dpi':dpi}
        return ocr.invoke_ocr(self.source,self.output,request)

    def test_real_english_worker_adds_searchable_text_and_keeps_scan(self):
        original=self.source.read_bytes()
        self.assertEqual(PdfReader(self.source).pages[0].extract_text(),'')
        result=self.create()
        extracted=subprocess.check_output(['pdftotext',str(self.output),'-'],text=True)
        self.assertIn('LINUXIT',extracted)
        self.assertIn('DOCUMENTO',extracted)
        self.assertEqual(result['pages_without_text'],[])
        self.assertGreater(result['pages_info'][0]['recognized_characters'],15)
        self.assertEqual(self.source.read_bytes(),original)
        self.assertEqual(result['output_sha256'],hashlib.sha256(self.output.read_bytes()).hexdigest())

    def test_actual_portuguese_combined_models_and_300_dpi(self):
        for language in ('por','por+eng'):
            with self.subTest(language=language):
                self.output=self.root/(language+'.pdf')
                result=self.create(language,300)
                self.assertIn('LINUXIT',PdfReader(self.output).pages[0].extract_text())
                self.assertEqual(result['language'],language)
                self.assertEqual(result['dpi'],300)

    def test_blank_page_notice_and_page_order_are_real(self):
        scan(self.source,('LINUXIT DOCUMENTO TESTE',''))
        result=self.create()
        pages=PdfReader(self.output).pages
        self.assertEqual(len(pages),2)
        self.assertIn('LINUXIT',pages[0].extract_text())
        self.assertEqual(pages[1].extract_text(),'')
        self.assertEqual(result['pages_without_text'],[2])

    def test_multipage_tiff_import_feeds_searchable_ocr_without_losing_blank_page(self):
        from pdf_creation import invoke_image_creation
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',64)
        tiff=self.root/'source.tiff';imported=self.root/'imported.pdf'
        with Image.new('RGB',(1200,450),'white') as first,Image.new('RGB',(1200,450),'white') as blank:
            ImageDraw.Draw(first).text((40,100),'LINUXIT DOCUMENTO TESTE',fill='black',font=font)
            first.save(tiff,save_all=True,append_images=[blank],compression='tiff_lzw')
        original=tiff.read_bytes()
        created=invoke_image_creation(imported,{'paths':[str(tiff)],'dpi':150})
        self.assertEqual((created['input_count'],created['pages']),(1,2))
        self.source=imported
        result=self.create()
        self.assertIn('LINUXIT',PdfReader(self.output).pages[0].extract_text())
        self.assertEqual(result['pages_without_text'],[2])
        self.assertEqual(tiff.read_bytes(),original)

    def test_crop_and_rotation_preserve_display_size_and_raster_appearance(self):
        writer=PdfWriter(clone_from=self.source)
        page=writer.pages[0]
        page.cropbox.lower_left=(24,12)
        page.cropbox.upper_right=(float(page.mediabox.width)-24,float(page.mediabox.height)-12)
        page.rotate(90)
        writer.write(self.root/'rotated.pdf')
        self.source=self.root/'rotated.pdf'
        size=ocr._page_sizes(PdfReader(self.source),150)[0]
        result=self.create()
        self.assertEqual(result['pages_info'][0]['page_points'],list(size))
        rendered=[]
        for index,path in enumerate((self.source,self.output)):
            prefix=self.root/('render-'+str(index))
            subprocess.run(['pdftocairo','-singlefile','-cropbox','-png','-r','72',str(path),str(prefix)],check=True,capture_output=True)
            with Image.open(prefix.with_suffix('.png')) as image:rendered.append(image.convert('RGB'))
        try:
            self.assertEqual(rendered[0].size,rendered[1].size)
            difference=ImageChops.difference(*rendered)
            self.assertLess(max(ImageStat.Stat(difference).mean),5)
        finally:
            for image in rendered:image.close()

    def test_cancel_stops_worker_and_its_actual_tesseract_child(self):
        import search_tasks
        # Observe the actual ELF child. Payload launchers intentionally prepend
        # bundled tools to PATH, so a PATH-injected stand-in is not a valid
        # synchronization mechanism across source/payload/sandbox environments.
        scan(self.source,('LINUXIT DOCUMENTO TESTE',)*3)
        cancel=threading.Event();results=[];errors=[];workers=[]
        request={'source_sha256':ocr.source_identity(self.source),'language':'eng','dpi':300}
        original=subprocess.Popen
        def started(*args,**kwargs):
            process=original(*args,**kwargs)
            if args and 'ocr-copy' in args[0]:workers.append(process)
            return process
        def work():
            try:results.append(ocr.invoke_ocr(self.source,self.output,request,cancel))
            except BaseException as error:errors.append(error)
        def find_tesseract(pid):
            queue=[pid];visited=set()
            while queue:
                current=queue.pop()
                if current in visited:continue
                visited.add(current)
                folder=Path('/proc')/str(current)
                try:
                    args=folder.joinpath('cmdline').read_bytes().split(b'\0')
                    if b'--list-langs' not in args and any(arg == b'tesseract' or arg.endswith((b'/libexec/tesseract',b'/usr/bin/tesseract')) for arg in args):
                        return current
                    queue.extend(map(int,folder.joinpath('task',str(current),'children').read_text().split()))
                except (FileNotFoundError,ProcessLookupError):pass
            return None
        pid=None
        with patch.object(search_tasks.subprocess,'Popen',side_effect=started):
            thread=threading.Thread(target=work)
            thread.start()
            try:
                deadline=time.monotonic()+10
                while pid is None and time.monotonic()<deadline:
                    if workers:pid=find_tesseract(workers[0].pid)
                    if pid is None:time.sleep(.003)
                self.assertIsNotNone(pid,'Actual Tesseract recognition process did not start')
            finally:
                cancel.set();thread.join(10)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors,[])
        self.assertEqual(results,[None])
        deadline=time.monotonic()+3
        def running():
            path=Path('/proc')/str(pid)/'stat'
            try:return path.read_text().split()[2] not in ('Z','X')
            except FileNotFoundError:return False
        while running() and time.monotonic()<deadline:time.sleep(.02)
        self.assertFalse(running(),'Tesseract child survived worker cancellation')
        self.assertFalse(self.output.exists())
