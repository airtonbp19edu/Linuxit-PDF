"""Adversarial checks from an independent review of the vector profile."""
from io import BytesIO
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
from test_redaction_apply import fixture
from vector_redaction import redact_page


class VectorReviewTests(unittest.TestCase):
    def page(self, body):
        writer = PdfWriter(clone_from=PdfReader(BytesIO(fixture())))
        page = writer.pages[0]
        stream = DecodedStreamObject()
        stream.set_data(body)
        page[NameObject('/Contents')] = writer._add_object(stream)
        return writer, page

    def redact(self, writer, page):
        return redact_page(writer, page, [(None, [(30, 185, 240, 225)], (0, 0, 0))])

    def test_wide_text_stroke_is_refused_instead_of_preserving_secret(self):
        # The baseline is outside the mark, but a 1000pt outline reaches it.
        for mode in (1, 2):
            with self.subTest(mode=mode):
                writer, page = self.page(f'1000 w BT /F1 14 Tf {mode} Tr 40 60 Td (SEGREDO) Tj ET'.encode())
                with self.assertRaisesRegex(ValueError, 'contorno'):
                    self.redact(writer, page)

    def test_repeated_finite_transforms_cannot_overflow_into_unsafe_geometry(self):
        body = b'1000000 0 0 1000000 0 0 cm ' * 60 + b'40 190 100 20 re f'
        writer, page = self.page(body)
        with self.assertRaisesRegex(ValueError, 'limite numérico'):
            self.redact(writer, page)

    def test_thumbnail_and_private_page_payloads_are_removed(self):
        writer, page = self.page(b'BT /F1 14 Tf 40 200 Td (SEGREDO) Tj ET')
        thumbnail = DecodedStreamObject()
        thumbnail.set_data(b'SECRET_PRE_REDACTION_THUMBNAIL')
        page[NameObject('/Thumb')] = writer._add_object(thumbnail)
        page[NameObject('/PieceInfo')] = DictionaryObject({NameObject('/Application'): writer._add_object(thumbnail)})
        page[NameObject('/SeparationInfo')] = DictionaryObject()
        self.redact(writer, page)
        for key in ('/Thumb', '/PieceInfo', '/SeparationInfo'):
            self.assertNotIn(key, page)
        writer.compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)
        result = BytesIO()
        writer.write(result)
        reopened = PdfReader(BytesIO(result.getvalue()))
        decoded = [obj.get_object().get_data() for obj in writer._objects if hasattr(obj, 'get_data')]
        self.assertFalse(any(b'SECRET_PRE_REDACTION_THUMBNAIL' in value for value in decoded))
        self.assertNotIn('SEGREDO', reopened.pages[0].extract_text())


if __name__ == '__main__':
    unittest.main()
