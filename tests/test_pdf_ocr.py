"""Own OCR orchestration controls; synthetic tools do not validate recognition."""
from io import BytesIO
import hashlib
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
import pdf_ocr as ocr
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, FloatObject, NameObject, NumberObject


def text_page(path, width, height, text='SYNTHETIC OCR'):
    writer = PdfWriter()
    page = writer.add_blank_page(width, height)
    if text:
        font = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
            NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')}))
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        content = DecodedStreamObject()
        content.set_data(('BT /F1 12 Tf 10 40 Td (' + text + ') Tj ET').encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(content)
    writer.write(path)


class OCRControlsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-ocr-controls-')
        self.root = Path(self.temp.name)
        self.source, self.output = self.root/'source.pdf', self.root/'new.pdf'
        writer = PdfWriter()
        writer.add_blank_page(200, 150)
        writer.add_blank_page(150, 200)
        writer.add_outline_item('Original bookmark', 0)
        writer.add_metadata({'/Title': 'Private original metadata'})
        writer.write(self.source)
        self.original = self.source.read_bytes()
        self.request = {'source_sha256': hashlib.sha256(self.original).hexdigest(), 'language': 'por+eng', 'dpi': 150}
        self.calls = []

    def tearDown(self):
        self.temp.cleanup()

    def fake_run(self, args, **_):
        self.calls.append(args)
        if args == ['tesseract', '--list-langs']:
            return 'List of available languages (2):\neng\npor\n'
        if args[0] == 'pdftocairo':
            source = PdfReader(args[-2])
            index = int(args[args.index('-f')+1])
            size = ocr._page_sizes(source, self.request['dpi'])[index-1]
            pixels = tuple(math.ceil(v * self.request['dpi'] / 72) for v in size)
            with Image.new('RGB', pixels, 'white') as image:
                image.save(Path(args[-1]).with_suffix('.png'))
        else:
            with Image.open(args[1]) as image:
                size = [v*72/self.request['dpi'] for v in image.size]
            text_page(Path(args[2]).with_suffix('.pdf'), *size)
        return ''

    def create(self):
        with patch.object(ocr, '_run', side_effect=self.fake_run):
            return ocr.create_searchable_copy(self.source, self.output, self.request)

    def absent(self):
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.linuxit-publish-*')), [])

    def test_raster_copy_pipeline_preserves_order_dimensions_hashes_and_original(self):
        result = self.create()
        self.assertEqual(result['pages'], 2)
        self.assertEqual(result['pages_without_text'], [])
        self.assertTrue(result['rasterized'])
        self.assertEqual(result['source_sha256'], self.request['source_sha256'])
        self.assertEqual(result['output_sha256'], hashlib.sha256(self.output.read_bytes()).hexdigest())
        self.assertEqual(self.source.read_bytes(), self.original)
        reader = PdfReader(self.output, strict=True)
        self.assertEqual([(float(p.mediabox.width), float(p.mediabox.height)) for p in reader.pages], [(200,150),(150,200)])
        self.assertEqual([p.extract_text() for p in reader.pages], ['SYNTHETIC OCR']*2)
        self.assertEqual(reader.outline, [])
        self.assertNotIn(b'Private original metadata', self.output.read_bytes())
        self.assertIn('-cropbox', self.calls[1])
        self.assertEqual(self.calls[2][3:], ['-l','por+eng','--dpi','150','--oem','1','--psm','3','pdf'])

    def test_blank_text_is_reported_without_claiming_recognition(self):
        def blank(args, **kwargs):
            result = self.fake_run(args, **kwargs)
            if args[0] == 'tesseract' and '--list-langs' not in args:
                path = Path(args[2]).with_suffix('.pdf')
                page = PdfReader(path).pages[0]
                text_page(path, float(page.mediabox.width), float(page.mediabox.height), '')
            return result
        with patch.object(ocr, '_run', side_effect=blank):
            result = ocr.create_searchable_copy(self.source, self.output, self.request)
        self.assertEqual(result['pages_without_text'], [1,2])
        self.assertTrue(all(p['recognized_characters'] == 0 and not p['text_detected'] for p in result['pages_info']))

    def test_invalid_request_types_values_and_extra_keys_rejected(self):
        for value in ({}, {**self.request, 'extra': 1}, {**self.request, 'dpi': True}, {**self.request,'dpi': 600},
                      {**self.request,'language': 'eng;bad'}, {**self.request,'language': []},
                      {**self.request,'source_sha256': 'not-a-hash'}, {**self.request,'source_sha256': None}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                ocr.create_searchable_copy(self.source, self.output, value)
            self.absent()

    def test_source_identity_mismatch_prevents_external_tools(self):
        with patch.object(ocr,'_run') as tool, self.assertRaisesRegex(ValueError, 'mudou'):
            ocr.create_searchable_copy(self.source,self.output,{**self.request,'source_sha256':'0'*64})
        tool.assert_not_called()
        self.absent()

    def test_existing_destination_original_and_dangling_link_not_overwritten(self):
        self.output.write_bytes(b'keep')
        for target in (self.output, self.source):
            with self.assertRaises(FileExistsError):
                ocr.create_searchable_copy(self.source, target, self.request)
        self.assertEqual(self.output.read_bytes(), b'keep')
        self.assertEqual(self.source.read_bytes(), self.original)
        if os.name != 'nt':
            link = self.root/'link.pdf'
            link.symlink_to(self.root/'absent.pdf')
            with self.assertRaises(FileExistsError):
                ocr.create_searchable_copy(self.source,link,self.request)

    def test_wrong_extension_and_missing_parent_refused(self):
        for path in (self.root/'out.png', self.root/'missing'/'out.pdf'):
            with self.assertRaises(ValueError):
                ocr.create_searchable_copy(self.source,path,self.request)
        self.absent()

    def test_encrypted_input_is_rejected_without_attempting_empty_password(self):
        writer = PdfWriter()
        writer.add_blank_page(200,200)
        writer.encrypt('',owner_password='synthetic-owner')
        writer.write(self.source)
        self.request['source_sha256'] = ocr.source_identity(self.source)
        with patch.object(ocr,'_run') as tool, self.assertRaisesRegex(ValueError, 'criptografado'):
            ocr.create_searchable_copy(self.source,self.output,self.request)
        tool.assert_not_called()
        self.absent()

    def test_page_source_pixel_and_total_budgets_precede_external_tools(self):
        for key,value in [('MAX_SOURCE_BYTES',1),('MAX_PAGES',1),('MAX_PAGE_PIXELS',10),('MAX_TOTAL_PIXELS',150000)]:
            with self.subTest(key=key), patch.object(ocr,key,value), patch.object(ocr,'_run') as tool, self.assertRaises(ValueError):
                ocr.create_searchable_copy(self.source,self.output,self.request)
            tool.assert_not_called()
            self.absent()

    def test_cropbox_rotation_userunit_and_nonfinite_geometry_guarded(self):
        for key,value in [('/CropBox',ArrayObject([NumberObject(-1),NumberObject(0),NumberObject(200),NumberObject(100)])),
                          ('/Rotate',NumberObject(17)),('/UserUnit',NumberObject(2)),
                          ('/MediaBox',ArrayObject([NumberObject(0),NumberObject(0),FloatObject('nan'),NumberObject(150)]))]:
            with self.subTest(key=key):
                reader = PdfReader(BytesIO(self.original))
                reader.pages[0][NameObject(key)] = value
                with self.assertRaises(ValueError):
                    ocr._page_sizes(reader,150)

    def test_missing_language_stops_before_rendering(self):
        with patch.object(ocr,'_run',return_value='eng\n') as tool, self.assertRaisesRegex(ValueError,'idioma'):
            ocr.create_searchable_copy(self.source,self.output,self.request)
        self.assertEqual(tool.call_count,1)
        self.absent()

    def test_renderer_missing_or_wrong_size_is_not_accepted(self):
        for wrong in (False,True):
            def broken(args,**kwargs):
                result = self.fake_run(args,**kwargs)
                if args[0]=='pdftocairo':
                    path=Path(args[-1]).with_suffix('.png')
                    if wrong:
                        with Image.new('RGB',(2,3),'white') as image:image.save(path)
                    else:path.unlink()
                return result
            with self.subTest(wrong=wrong), patch.object(ocr,'_run',side_effect=broken), self.assertRaises(ValueError):
                ocr.create_searchable_copy(self.source,self.output,self.request)
            self.absent()

    def test_missing_wrong_geometry_and_multiple_ocr_pages_refused(self):
        for mode in ('missing','geometry','multiple'):
            def broken(args,**kwargs):
                result=self.fake_run(args,**kwargs)
                if args[0]=='tesseract' and '--list-langs' not in args:
                    path=Path(args[2]).with_suffix('.pdf')
                    if mode=='missing':path.unlink()
                    else:
                        writer=PdfWriter();writer.add_blank_page(10,10)
                        if mode=='multiple':writer.add_blank_page(10,10)
                        writer.write(path)
                return result
            with self.subTest(mode=mode), patch.object(ocr,'_run',side_effect=broken), self.assertRaises(ValueError):
                ocr.create_searchable_copy(self.source,self.output,self.request)
            self.absent()

    def test_output_budget_failure_leaves_no_destination(self):
        with patch.object(ocr,'MAX_OUTPUT_BYTES',1), self.assertRaisesRegex(ValueError,'128 MiB'):
            self.create()
        self.absent()

    def test_changed_source_is_not_published(self):
        original=ocr.source_identity
        def changed(path):
            if Path(path)==self.source:return '0'*64
            return original(path)
        with patch.object(ocr,'source_identity',side_effect=changed), self.assertRaisesRegex(ValueError,'mudou'):
            self.create()
        self.absent()

    def test_destination_appearing_at_publication_is_preserved(self):
        original=ocr.source_identity
        def race(path):
            if Path(path)==self.source:self.output.write_bytes(b'concurrent destination')
            return original(path)
        with patch.object(ocr,'source_identity',side_effect=race), self.assertRaises(FileExistsError):
            self.create()
        self.assertEqual(self.output.read_bytes(),b'concurrent destination')
        self.assertEqual(list(self.root.glob('.linuxit-publish-*')),[])

    def test_publication_copy_failure_cleans_staging(self):
        def broken(source,dest,*args):
            dest.write(b'partial');raise OSError('synthetic write failure')
        import local_files
        with patch.object(local_files.shutil,'copyfileobj',side_effect=broken),self.assertRaises(OSError):self.create()
        self.absent()

    def test_external_missing_failure_and_timeout_use_bounded_local_errors(self):
        for outcome in (FileNotFoundError(),subprocess.TimeoutExpired(['tesseract'],120),subprocess.CompletedProcess([],1)):
            with self.subTest(outcome=outcome):
                options={'side_effect':outcome} if isinstance(outcome,Exception) else {'return_value':outcome}
                with patch.object(ocr.subprocess,'run',**options),self.assertRaises(ValueError):
                    ocr._run(['tesseract','image name.png','out'])

    def test_tool_arguments_do_not_use_shell_and_thread_count_is_bounded(self):
        with patch.object(ocr.subprocess,'run',return_value=subprocess.CompletedProcess([],0)) as process:
            self.assertEqual(ocr._run(['tesseract','name; literal.png','output']), '')
        args,kwargs=process.call_args
        self.assertEqual(args[0][1],'name; literal.png')
        self.assertFalse(kwargs.get('shell',False))
        self.assertEqual(kwargs['env']['OMP_THREAD_LIMIT'],'1')
        self.assertEqual(kwargs['stdin'],subprocess.DEVNULL)

    def test_worker_reply_cannot_claim_a_different_destination_or_missing_page(self):
        result=self.create()
        for bad in ({}, {**result,'path':str(self.root/'other.pdf')}, {**result,'pages':True},
                    {**result,'pages_info':[]}, {**result,'pages_without_text':[1]},
                    {**result,'pages_info':[{**result['pages_info'][0],'page_points':[float('nan'),1]},result['pages_info'][1]]}):
            with self.subTest(bad=bad),patch.object(ocr,'run_search_worker',return_value=bad),self.assertRaises(RuntimeError):
                ocr.invoke_ocr(self.source,self.output,self.request)

    def test_cancelled_request_never_starts_child_and_command_requires_destination(self):
        import search_tasks
        cancel=threading.Event();cancel.set()
        with patch.object(search_tasks.subprocess,'Popen') as process:
            self.assertIsNone(ocr.invoke_ocr(self.source,self.output,self.request,cancel))
            with self.assertRaises(ValueError):search_tasks.run_search_worker('ocr-copy',self.source,self.request)
            process.assert_not_called()
        self.absent()
