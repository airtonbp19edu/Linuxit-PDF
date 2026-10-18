"""Roundtrip generated images through own RGB PDF creation and real worker."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT/'app'))))
import pdf_creation as creation
from PIL import Image, PngImagePlugin
from pypdf import PdfReader


class PDFCreationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-create-')
        self.root = Path(self.temp.name);self.output = self.root/'new.pdf'
        self.first = self.image('one.png', (40, 20), 'red')
        self.second = self.image('two.jpg', (10, 30), 'blue')

    def tearDown(self):self.temp.cleanup()

    def image(self, name, size, color, mode='RGB', **options):
        path = self.root/name
        with Image.new(mode, size, color) as image:image.save(path, **options)
        return path

    def test_bmp_webp_and_single_tiff_preserve_pixels_dimensions_and_order(self):
        sources = [self.image('solid.bmp',(12,8),'red'),self.image('solid.webp',(9,6),'blue',lossless=True),
                   self.image('solid.tiff',(10,15),'green',compression='tiff_lzw')]
        before = [p.read_bytes() for p in sources]
        result = self.create(sources,dpi=72);reader = PdfReader(self.output)
        self.assertEqual([s['format'] for s in result['sources']],['BMP','WEBP','TIFF'])
        for page,size,color in zip(reader.pages,((12,8),(9,6),(10,15)),((255,0,0),(0,0,255),(0,128,0))):
            self.assertEqual([float(page.mediabox.width),float(page.mediabox.height)],list(size))
            pixels = page['/Resources']['/XObject']['/Im1'].get_data()
            self.assertEqual(pixels,bytes(color)*(size[0]*size[1]))
        self.assertEqual([p.read_bytes() for p in sources],before)

    def test_webp_alpha_is_composited_over_white(self):
        source = self.image('alpha.webp',(1,1),(255,0,0,128),mode='RGBA',lossless=True)
        self.create([source]);pixels = PdfReader(self.output).pages[0]['/Resources']['/XObject']['/Im1'].get_data()
        self.assertEqual(pixels,bytes((255,127,127)))

    def test_multiframe_tiff_is_imported_and_animated_webp_is_refused(self):
        for suffix,options in (('tiff',{}),('webp',{'lossless':True,'duration':100})):
            source = self.root/('multi.'+suffix)
            with Image.new('RGB',(4,4),'red') as first,Image.new('RGB',(4,4),'blue') as second:
                first.save(source,save_all=True,append_images=[second],**options)
            if suffix == 'tiff':
                result = self.create([source]);self.assertEqual(result['pages'],2)
                self.output.unlink()
            else:
                with self.assertRaisesRegex(ValueError,'quadros'):self.create([source])
                self.assertFalse(self.output.exists())

    def test_bmp_renamed_as_jpeg_is_identified_by_content(self):
        source = self.image('source.bmp',(4,3),'red');renamed = self.root/'source.jpg';source.rename(renamed)
        result = self.create([renamed]);self.assertEqual(result['sources'][0]['format'],'BMP')

    def test_real_worker_supports_compressed_tiff_without_external_conversion(self):
        source = self.image('worker.tiff',(5,7),'blue',compression='tiff_lzw')
        result = creation.invoke_image_creation(self.output,{'paths':[str(source)],'dpi':144})
        self.assertEqual(result['sources'][0]['format'],'TIFF');self.assertEqual(len(PdfReader(self.output).pages),1)

    def create(self, paths=None, dpi=144):
        return creation.create_pdf_from_images(self.output, {'paths': [str(p) for p in (paths or [self.first, self.second])], 'dpi': dpi})

    def absent(self):
        self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-images-*')), [])

    def test_order_dimensions_lossless_rgb_and_source_identity(self):
        original = [p.read_bytes() for p in (self.second, self.first)]
        result = self.create([self.second, self.first])
        self.assertEqual(result['pages'], 2)
        self.assertEqual(result['output_sha256'], hashlib.sha256(self.output.read_bytes()).hexdigest())
        reader = PdfReader(self.output, strict=True)
        self.assertEqual([(float(p.mediabox.width), float(p.mediabox.height)) for p in reader.pages], [(5, 15), (20, 10)])
        for page, path, identity in zip(reader.pages, (self.second, self.first), result['sources']):
            image = page['/Resources']['/XObject']['/Im1']
            with Image.open(path) as source:self.assertEqual(image.get_data(), source.convert('RGB').tobytes())
            self.assertEqual(image['/Filter'], '/FlateDecode')
            self.assertEqual(identity['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual([p.read_bytes() for p in (self.second, self.first)], original)

    def test_pinned_fixture_manifest_matches_sources_and_oriented_dimensions(self):
        folder = ROOT/'testes/fixtures/criacao-imagens'
        manifest = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        sources = [folder/item['file'] for item in manifest['images']]
        for path, item in zip(sources, manifest['images']):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item['sha256'])
            self.assertEqual(path.stat().st_size, item['bytes'])
        self.create(sources, dpi=72)
        for page, item in zip(PdfReader(self.output).pages, manifest['images']):
            self.assertEqual([float(page.mediabox.width), float(page.mediabox.height)], item['page_points_at_72_dpi'])

    def test_alpha_and_palette_transparency_are_composited_on_white(self):
        alpha = self.image('alpha.png', (2, 1), (255, 0, 0, 128), mode='RGBA')
        palette = self.root/'palette.png'
        with Image.new('P', (1, 1), 0) as image:
            image.putpalette([0, 255, 0] + [0]*765);image.save(palette, transparency=0)
        self.create([alpha, palette])
        reader = PdfReader(self.output)
        self.assertEqual(reader.pages[0]['/Resources']['/XObject']['/Im1'].get_data(), bytes([255, 127, 127])*2)
        self.assertEqual(reader.pages[1]['/Resources']['/XObject']['/Im1'].get_data(), b'\xff\xff\xff')

    def test_exif_orientation_applied_and_private_metadata_not_copied(self):
        exif = Image.Exif();exif[274] = 6;exif[270] = 'PRIVATE CAMERA DESCRIPTION'
        source = self.image('camera.jpg', (40, 20), 'red', exif=exif)
        self.create([source], dpi=72)
        page = PdfReader(self.output).pages[0]
        self.assertEqual((float(page.mediabox.width), float(page.mediabox.height)), (20, 40))
        self.assertNotIn(b'PRIVATE CAMERA DESCRIPTION', self.output.read_bytes())

    def test_grayscale_and_cmyk_inputs_become_rgb(self):
        gray = self.image('gray.png', (2, 3), 100, mode='L')
        cmyk = self.image('cmyk.jpg', (3, 2), (0, 255, 255, 0), mode='CMYK')
        self.create([gray, cmyk])
        for page in PdfReader(self.output).pages:
            image = page['/Resources']['/XObject']['/Im1']
            self.assertEqual(image['/ColorSpace'], '/DeviceRGB');self.assertEqual(len(image.get_data()), 18)

    def test_corrupt_unsupported_animated_and_truncated_inputs_leave_no_output(self):
        bad = self.root/'bad.png';bad.write_bytes(b'not an image')
        gif = self.image('one.gif', (2, 2), 'red')
        animated = self.root/'animated.png'
        with Image.new('RGB', (3, 3), 'red') as a, Image.new('RGB', (3, 3), 'blue') as b:
            a.save(animated, save_all=True, append_images=[b], duration=100)
        truncated = self.root/'truncated.png';truncated.write_bytes(self.first.read_bytes()[:45])
        for path in (bad, gif, animated, truncated):
            with self.subTest(path=path), self.assertRaises(ValueError):self.create([path])
            self.absent()

    def test_invalid_request_duplicates_paths_dpi_and_destination(self):
        base = {'paths':[str(self.first)], 'dpi':300}
        for request in ({}, {**base, 'extra':True}, {**base, 'paths':[]}, {**base, 'paths':[1]},
                        {**base, 'paths':[str(self.first)]*2}, {**base, 'dpi':True}, {**base, 'dpi':71},
                        {**base, 'dpi':601}, {**base, 'dpi':72.5}, {**base, 'paths':['bad\x00name']}):
            with self.subTest(request=request), self.assertRaises(ValueError):creation.create_pdf_from_images(self.output, request)
            self.absent()
        for destination in (self.root/'wrong.png', self.root/'missing'/'out.pdf'):
            with self.assertRaises(ValueError):creation.create_pdf_from_images(destination, base)

    def test_existing_destination_and_source_never_overwritten(self):
        self.output.write_bytes(b'existing bytes')
        with self.assertRaises(FileExistsError):self.create()
        self.assertEqual(self.output.read_bytes(), b'existing bytes')
        with self.assertRaises(FileExistsError):creation.create_pdf_from_images(self.first, {'paths':[str(self.first)], 'dpi':300})
        if os.name != 'nt':
            link = self.root/'link.pdf';target = self.root/'missing.pdf';link.symlink_to(target)
            with self.assertRaises(FileExistsError):creation.create_pdf_from_images(link, {'paths':[str(self.first)], 'dpi':300})
            self.assertFalse(target.exists())

    def test_pixel_and_image_count_budgets_checked_before_page_creation(self):
        for constant, value in [('MAX_IMAGES', 1), ('MAX_IMAGE_PIXELS', 799), ('MAX_TOTAL_PIXELS', 1000)]:
            with self.subTest(constant=constant), patch.object(creation, constant, value), self.assertRaises(ValueError):self.create()
            self.absent()

    def test_byte_and_output_budgets_leave_no_partial_file(self):
        for constant, value in [('MAX_SOURCE_BYTES', 1), ('MAX_TOTAL_BYTES', self.first.stat().st_size), ('MAX_OUTPUT_BYTES', 1)]:
            with self.subTest(constant=constant), patch.object(creation, constant, value), self.assertRaises(ValueError):self.create()
            self.absent()

    def test_changed_or_missing_source_refuses_publication(self):
        with patch.object(creation, '_sha', return_value='0'*64), self.assertRaisesRegex(ValueError, 'mudou'):self.create()
        self.absent()
        self.second.unlink()
        with self.assertRaises(ValueError):self.create()
        self.absent()

    def test_writer_failure_removes_staging(self):
        with patch.object(creation.PdfWriter, 'write', side_effect=OSError('synthetic write failure')), self.assertRaises(OSError):self.create()
        self.absent()

    def test_partial_final_write_removed_on_handled_failure(self):
        def fail(source, output, *args):output.write(b'partial');raise OSError('synthetic final write failure')
        with patch.object(creation.shutil, 'copyfileobj', side_effect=fail), self.assertRaises(OSError):self.create()
        self.absent()

    def test_destination_appearing_during_conversion_is_preserved(self):
        original = creation._sha
        def concurrent(path):
            self.output.write_bytes(b'concurrent destination');return original(path)
        with patch.object(creation, '_sha', side_effect=concurrent), self.assertRaises(FileExistsError):self.create()
        self.assertEqual(self.output.read_bytes(), b'concurrent destination')
        self.assertEqual(list(self.root.glob('.linuxit-images-*')), [])

    def test_real_worker_roundtrip_and_existing_destination_error(self):
        request = {'paths':[str(self.first), str(self.second)], 'dpi':300}
        result = creation.invoke_image_creation(self.output, request)
        self.assertEqual(result['pages'], 2);self.assertEqual(len(PdfReader(self.output).pages), 2)
        with self.assertRaisesRegex(RuntimeError, 'nome novo'):creation.invoke_image_creation(self.output, request)

    def test_cancelled_request_and_excessive_json_never_start_worker(self):
        cancel = threading.Event();cancel.set()
        self.assertIsNone(creation.invoke_image_creation(self.output, {'paths':[str(self.first)], 'dpi':300}, cancel))
        import search_tasks
        with patch.object(search_tasks.subprocess, 'Popen') as process:
            with self.assertRaises(ValueError):search_tasks.run_search_worker('images-to-pdf', self.output, {'paths':['x'*300000], 'dpi':300})
            process.assert_not_called()
        self.absent()

    def test_invalid_worker_protocol_not_presented_as_saved(self):
        request = {'paths':[str(self.first)], 'dpi':300}
        for result in ({}, {'schema':'other'}, {'schema':'linuxit-image-pdf-result-v1','dpi':600}):
            with self.subTest(result=result), patch.object(creation, 'run_search_worker', return_value=result), self.assertRaises(RuntimeError):
                creation.invoke_image_creation(self.output, request)
