import hashlib,json,os,shutil,sys,tempfile,unittest,zipfile
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_conversion import convert_copy,source_snapshot
from test_attachment_search import text_pdf
from PIL import Image

class PDFConversionTests(unittest.TestCase):
    def test_captured_source_identity_refuses_replaced_file_before_export(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';source.write_bytes(text_pdf(['original']))
            identity=source_snapshot(source)[1];source.write_bytes(text_pdf(['replacement']))
            output=Path(folder)/'a.txt'
            with self.assertRaisesRegex(ValueError,'mudou'):
                convert_copy(source,output,dict(source_sha256=identity,format='text',dpi=150))
            self.assertFalse(output.exists())

    def test_source_changed_during_converter_never_publishes(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';source.write_bytes(text_pdf(['original']))
            identity=source_snapshot(source)[1];output=Path(folder)/'a.txt'
            def replace(argv):
                Path(argv[-1]).write_text('output',encoding='utf-8');source.write_bytes(text_pdf(['replacement']))
            with patch('pdf_conversion._run',side_effect=replace),self.assertRaisesRegex(ValueError,'mudou'):
                convert_copy(source,output,dict(source_sha256=identity,format='text',dpi=150))
            self.assertFalse(output.exists())

    def test_source_reader_enforces_budget_after_open(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';source.write_bytes(b'12345')
            with patch('pdf_conversion.MAX_SOURCE_BYTES',4),self.assertRaises(ValueError):source_snapshot(source)

    def test_bad_requests_and_overwrite_do_not_publish(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';source.write_bytes(text_pdf(['alpha']))
            with self.assertRaises(ValueError):convert_copy(source,Path(folder)/'b.txt',{'format':'execute'})
            target=Path(folder)/'keep.txt';target.write_text('keep')
            with self.assertRaises(FileExistsError):convert_copy(source,target,dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),format='text',dpi=150))
            self.assertEqual(target.read_text(),'keep')

    @unittest.skipUnless(shutil.which('pdftocairo') and shutil.which('pdftotext'),'Poppler tools required')
    def test_real_text_images_and_tiff_exports_preserve_original(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';before=text_pdf(['alpha first','beta second']);source.write_bytes(before)
            for kind,suffix in [('text','.txt'),('png','.zip'),('jpeg','.zip'),('tiff','.tiff')]:
                output=Path(folder)/(kind+suffix)
                result=convert_copy(source,output,dict(source_sha256=hashlib.sha256(before).hexdigest(),format=kind,dpi=72))
                self.assertEqual(result['pages'],2);self.assertEqual(source.read_bytes(),before)
                if kind=='text':self.assertIn('alpha',output.read_text())
                elif kind=='tiff':
                    with Image.open(output) as image:self.assertEqual(image.n_frames,2)
                else:
                    with zipfile.ZipFile(output) as archive:
                        manifest=json.loads(archive.read('manifest.json'));self.assertEqual(len(manifest['pages']),2)
                        for row in manifest['pages']:self.assertEqual(hashlib.sha256(archive.read(row['file'])).hexdigest(),row['sha256'])
