"""Hidden-data redaction: real PDF objects, geometry and atomic refusal."""
from io import BytesIO
import hashlib
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT/'app'))))
from redaction_hidden import sanitise, words_from_bbox, options
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject, DecodedStreamObject, DictionaryObject, ArrayObject, RectangleObject


class HiddenRedactionTests(unittest.TestCase):
    def writer(self):
        writer = PdfWriter();writer.add_blank_page(300, 300)
        return writer

    def test_only_words_intersecting_marks_are_selected_with_nonzero_media_origin(self):
        writer = self.writer();page = writer.pages[0]
        page.mediabox = RectangleObject([10, 20, 310, 320])
        raw = b'<html><page width="300" height="300"><word xMin="20" yMin="40" xMax="70" yMax="60">SEGREDO</word><word xMin="90" yMin="40" xMax="120" yMax="60">PUBLICO</word></page></html>'
        self.assertEqual(words_from_bbox(raw, page, [(25, 250, 90, 290)]), {'SEGREDO'})
        self.assertEqual(words_from_bbox(raw, page, [(200, 200, 220, 220)]), set())

    def test_bad_geometry_and_entities_are_refused(self):
        for raw in (b'<!DOCTYPE x [<!ENTITY a "oops">]><page/>', b'<page width="300" height="300"><word xMin="nan" yMin="0" xMax="1" yMax="1">x</word></page>'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                words_from_bbox(raw, self.writer().pages[0], [(0, 0, 1, 1)])

    def test_metadata_and_recursive_bookmark_titles_removed_after_roundtrip(self):
        writer = self.writer();writer.add_metadata({'/Title':'SEGREDO', '/Custom':'outro'})
        stream = DecodedStreamObject();stream.set_data(b'<x>SEGREDO</x>')
        writer.root_object[NameObject('/Metadata')] = writer._add_object(stream)
        parent = writer.add_outline_item('SEGREDO chefe', 0)
        writer.add_outline_item('filho segredo', 0, parent=parent)
        report = sanitise(writer, {'SEGREDO'}, dict(metadata=True, bookmarks=True))
        output = BytesIO();writer.compress_identical_objects(remove_duplicates=False,remove_unreferenced=True);writer.write(output)
        reader = PdfReader(output)
        self.assertIsNone(reader.metadata);self.assertNotIn('/Metadata', reader.root_object)
        self.assertEqual(reader.outline[0].title, '[REDACTED] chefe')
        self.assertEqual(reader.outline[1][0].title, 'filho [REDACTED]')
        self.assertEqual(report['bookmark_titles_changed'], 2)

    def test_utf8_attachment_content_names_description_and_catalog_are_consistent(self):
        writer = self.writer()
        entry = writer.add_attachment('segredo.txt', 'Olá SEGREDO público'.encode())
        entry.pdf_object[NameObject('/UF')] = TextStringObject('SEGREDO.txt')
        entry.pdf_object[NameObject('/Desc')] = TextStringObject('um segredo')
        report = sanitise(writer, {'SEGREDO'}, dict(attachments=True))
        output = BytesIO();writer.compress_identical_objects(remove_duplicates=False,remove_unreferenced=True);writer.write(output)
        reader = PdfReader(output)
        self.assertEqual(reader.attachments['[REDACTED].txt'], ['Olá [REDACTED] público'.encode()])
        self.assertEqual(report['attachments_checked'], 1)
        self.assertEqual(report['attachment_contents_changed'], 1)
        self.assertEqual(report['attachment_strings_changed'], 3)

    def test_binary_or_non_utf8_attachments_and_associated_graph_are_refused(self):
        for name, data in (('x.pdf', b'%PDF-1.7'), ('x.txt', b'\xff'), ('x.txt', b'a\x00b')):
            writer = self.writer();writer.add_attachment(name, data)
            with self.subTest(name=name,data=data),self.assertRaises(ValueError):
                sanitise(writer, {'segredo'}, dict(attachments=True))
        writer = self.writer();writer.root_object[NameObject('/AF')] = ArrayObject()
        with self.assertRaisesRegex(ValueError, '/AF'):
            sanitise(writer, {'segredo'}, dict(attachments=True))

    def test_colliding_redacted_names_are_refused(self):
        writer = self.writer();writer.add_attachment('a.txt', b'a');writer.add_attachment('b.txt', b'b')
        with self.assertRaisesRegex(ValueError, 'duplicados'):
            sanitise(writer, {'a', 'b'}, dict(attachments=True))

    def test_disabled_options_preserve_data_and_invalid_flags_are_refused(self):
        writer = self.writer();writer.add_metadata({'/Title':'segredo'})
        sanitise(writer, {'segredo'}, {})
        self.assertEqual(writer.metadata.title, 'segredo')
        for flags in ({'metadata':1}, {'all':True}, []):
            with self.subTest(flags=flags),self.assertRaises(ValueError):options({'hidden':flags})


@unittest.skipUnless(shutil.which('pdftotext'), 'Real Poppler word geometry required')
class HiddenRedactionPopplerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def source(self, attachment='segredo.txt', rotate=0):
        from test_redaction_apply import fixture
        from pdf_changes import save_edited_copy
        writer=PdfWriter(clone_from=PdfReader(BytesIO(fixture(rotate=rotate))))
        writer.add_metadata({'/Title':'SEGREDO 123'});writer.add_outline_item('SEGREDO público',0)
        writer.add_attachment(attachment,b'SEGREDO em anexo, texto publico')
        source=self.root/'plain.pdf';writer.write(source)
        marked=self.root/'marked.pdf'
        save_edited_copy(source,marked,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                         operations=[dict(kind='add-redaction',page=0,rect=[30,185,240,225],text='marcar')])
        return marked

    def test_complete_vector_copy_uses_actual_poppler_words_without_hidden_leftovers(self):
        from pdf_redaction import redact_copy
        from test_redaction_apply import all_decoded
        for rotate in (0,90,270):
            with self.subTest(rotate=rotate):
                source=self.source(rotate=rotate);before=source.read_bytes();target=self.root/f'out-{rotate}.pdf'
                request=dict(source_sha256=hashlib.sha256(before).hexdigest(),dpi=150,mode='vector',
                             hidden=dict(metadata=True,bookmarks=True,attachments=True))
                result=redact_copy(source,target,request)
                self.assertNotIn(b'SEGREDO',all_decoded(target))
                reader=PdfReader(target)
                self.assertEqual(reader.outline[0].title,'[REDACTED] público')
                self.assertEqual(reader.attachments['[REDACTED].txt'],[b'[REDACTED] em anexo, texto publico'])
                self.assertTrue(result['hidden_data']['metadata_removed']);self.assertEqual(source.read_bytes(),before)

    def test_unsupported_attachment_aborts_without_publishing_or_changing_source(self):
        from pdf_redaction import redact_copy
        source=self.source(attachment='segredo.pdf');before=source.read_bytes();target=self.root/'out.pdf'
        with self.assertRaisesRegex(ValueError,'anexos txt'):
            redact_copy(source,target,dict(source_sha256=hashlib.sha256(before).hexdigest(),dpi=150,mode='vector',hidden=dict(attachments=True)))
        self.assertFalse(target.exists());self.assertEqual(source.read_bytes(),before)
