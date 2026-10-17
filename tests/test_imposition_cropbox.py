"""Measure real output PDF placement; no GTK, Poppler or original is required."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import json

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))
sys.path.insert(0, str(APP))
import imposition
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject, RectangleObject


def fixture(path, *, offsets=((0, 0),), rotation=0):
    writer = PdfWriter()
    for number, (left, bottom) in enumerate(offsets, 1):
        page = writer.add_blank_page(width=800, height=1000)
        page.mediabox = RectangleObject((-200, -200, 600, 800))
        page.cropbox = RectangleObject((left, bottom, left + 200, bottom + 300))
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                                 NameObject('/Subtype'): NameObject('/Type1'),
                                 NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        content = DecodedStreamObject()
        content.set_data((f'BT /F1 12 Tf 1 0 0 1 {left + 20} {bottom + 30} Tm '
                          f'(MARK {number:03d}) Tj ET\n').encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(content)
        if rotation:
            page.rotate(rotation)
    writer.write(path)


def text_positions(path):
    """Read text baselines in final PDF coordinates, including nested CTMs."""
    pages = []
    for page in PdfReader(path).pages:
        items = []
        def visit(text, cm, tm, _font, _size):
            if text.strip().startswith('MARK'):
                x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
                y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                items.append((text.strip(), x, y))
        page.extract_text(visitor_text=visit)
        pages.append(items)
    return pages


class CropBoxImpositionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-cropbox-')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.plain, self.shifted = self.root / 'plain.pdf', self.root / 'shifted.pdf'
        self.sequence = 0

    def tearDown(self):
        self.temp.cleanup()

    def outputs(self, job, *, offsets=((70, 80),), rotation=0, worker=False):
        fixture(self.plain, offsets=((0, 0),) * len(offsets), rotation=rotation)
        fixture(self.shifted, offsets=offsets, rotation=rotation)
        before = (self.plain.read_bytes(), self.shifted.read_bytes())
        self.sequence += 1
        outputs = []
        for label, source in [('plain', self.plain), ('shifted', self.shifted)]:
            target = self.root / f'{self.sequence}-{label}-output.pdf'
            if worker:
                result = subprocess.run([sys.executable, '-X', 'utf8', str(APP / 'worker_cli.py'),
                    'prepare', str(source), str(target)], input=json.dumps(job),
                    capture_output=True, text=True, encoding='utf-8', timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr)
            else:
                imposition.prepare_output(str(source), str(target), job)
            outputs.append(target)
        self.assertEqual((self.plain.read_bytes(), self.shifted.read_bytes()), before)
        return outputs

    def assert_equivalent(self, outputs):
        reference, actual = (text_positions(path) for path in outputs)
        self.assertTrue(any(reference), 'Output must contain measurable content')
        self.assertEqual([len(p) for p in actual], [len(p) for p in reference])
        for page_a, page_b in zip(reference, actual):
            for (label_a, x_a, y_a), (label_b, x_b, y_b) in zip(page_a, page_b):
                self.assertEqual(label_a, label_b)
                self.assertAlmostEqual(x_a, x_b, delta=0.001)
                self.assertAlmostEqual(y_a, y_b, delta=0.001)

    def test_actual_size_centers_the_visible_crop_not_the_media_origin(self):
        outputs = self.outputs({'print_mode': 'size', 'scale_mode': 'actual'})
        page = PdfReader(outputs[1]).pages[0]
        label, x, y = text_positions(outputs[1])[0][0]
        self.assertEqual(label, 'MARK 001')
        self.assertAlmostEqual(x, (float(page.mediabox.width) - 200) / 2 + 20, delta=0.001)
        self.assertAlmostEqual(y, (float(page.mediabox.height) - 300) / 2 + 30, delta=0.001)

    def test_fit_handles_negative_crop_origin(self):
        self.assert_equivalent(self.outputs({'scale_mode': 'fit'}, offsets=((-80, -60),)))

    def test_intrinsic_rotation_keeps_shifted_crop_aligned(self):
        for rotation in (0, 90, 180, 270):
            with self.subTest(rotation=rotation):
                self.assert_equivalent(self.outputs({'scale_mode': 'fit'}, rotation=rotation))

    def test_nup_orders_place_shifted_pages_in_same_cells(self):
        offsets = ((70, 80), (-80, -60), (30, 100), (10, -90), (90, 20), (-40, 50))
        for layout in ('lrtb', 'lrbt', 'rltb', 'rlbt'):
            with self.subTest(layout=layout):
                self.assert_equivalent(self.outputs({'print_mode': 'multiple', 'pages_per_sheet': 6,
                    'number_up_layout': layout}, offsets=offsets))

    def test_booklet_bindings_and_sides_keep_crop_placement(self):
        offsets = ((70, 80), (-80, -60), (30, 100), (10, -90), (90, 20))
        for binding in ('left', 'right'):
            for sides in ('both', 'front', 'back'):
                with self.subTest(binding=binding, sides=sides):
                    self.assert_equivalent(self.outputs({'print_mode': 'booklet',
                        'booklet_binding': binding, 'booklet_sides': sides}, offsets=offsets))

    def test_real_worker_prepares_shifted_crop_in_each_mode(self):
        for mode in ('size', 'multiple', 'booklet'):
            with self.subTest(mode=mode):
                self.assert_equivalent(self.outputs({'print_mode': mode}, worker=True))

    def test_poster_single_sheet_and_tiles_keep_crop_placement_without_marks(self):
        for scale, rotation, large_only in ((100, 0, True), (400, 0, False), (400, 90, False)):
            with self.subTest(scale=scale, rotation=rotation, large_only=large_only):
                self.assert_equivalent(self.outputs({'print_mode': 'poster', 'poster_scale': scale,
                    'poster_large_only': large_only, 'poster_overlap_mm': 5,
                    'poster_cut_marks': False, 'poster_labels': False}, rotation=rotation))

    def test_inputs_and_in_memory_page_geometry_are_preserved(self):
        fixture(self.shifted, offsets=((70, 80),), rotation=90)
        data = self.shifted.read_bytes()
        source = PdfReader(self.shifted).pages[0]
        geometry = (tuple(source.cropbox), tuple(source.mediabox), source.rotation)
        stream = source.get_contents().get_data()
        imposition._place(imposition._blank(600, 800), source, 10, 20, 200, 300)
        self.assertEqual((tuple(source.cropbox), tuple(source.mediabox), source.rotation), geometry)
        self.assertEqual(source.get_contents().get_data(), stream)
        self.assertEqual(self.shifted.read_bytes(), data)

    def test_zero_origin_keeps_known_actual_size_position(self):
        outputs = self.outputs({'scale_mode': 'actual'}, offsets=((0, 0),))
        self.assert_equivalent(outputs)
        _, x, y = text_positions(outputs[0])[0][0]
        page = PdfReader(outputs[0]).pages[0]
        self.assertAlmostEqual(x, (float(page.mediabox.width) - 200) / 2 + 20, delta=0.001)
        self.assertAlmostEqual(y, (float(page.mediabox.height) - 300) / 2 + 30, delta=0.001)


if __name__ == '__main__':
    unittest.main()
