"""Content removal and fail-closed controls for the non-raster path."""
import hashlib
from io import BytesIO
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_redaction import redact_copy
from pdf_changes import save_edited_copy
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.generic import DecodedStreamObject,NameObject
from test_redaction_apply import fixture,all_decoded


class VectorRedactionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def marked(self,body=None,rotate=0):
        data=fixture(rotate=rotate)
        if body:
            w=PdfWriter(clone_from=PdfReader(BytesIO(data)))
            stream=DecodedStreamObject();stream.set_data(body)
            w.pages[0][NameObject('/Contents')]=w._add_object(stream)
            out=BytesIO();w.write(out);data=out.getvalue()
        source=self.root/'plain.pdf';source.write_bytes(data);marked=self.root/'marked.pdf'
        save_edited_copy(source,marked,source_sha256=hashlib.sha256(data).hexdigest(),
            operations=[dict(kind='add-redaction',page=0,rect=[30,185,240,225],text='remover')])
        return marked

    def apply(self,path):
        return redact_copy(path,self.root/'result.pdf',dict(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),dpi=150,mode='vector'))

    def test_secret_bytes_and_image_removed_public_text_stays_selectable(self):
        source=self.marked();before=source.read_bytes();result=self.apply(source)
        target=self.root/'result.pdf';reader=PdfReader(target)
        self.assertFalse(result['rasterized']);self.assertEqual(result['mode'],'vector')
        self.assertNotIn(b'SEGREDO',all_decoded(target))
        self.assertIn('publico',reader.pages[0].extract_text())
        self.assertEqual(reader.pages[1].get_contents().get_data(),PdfReader(source).pages[1].get_contents().get_data())
        self.assertNotIn('/XObject',reader.pages[0]['/Resources'])
        self.assertEqual(source.read_bytes(),before)

    def test_rotation_does_not_change_page_space_selection(self):
        source=self.marked(rotate=90);self.apply(source)
        page=PdfReader(self.root/'result.pdf').pages[0]
        self.assertEqual(page.rotation,90);self.assertIn('publico',page.extract_text());self.assertNotIn('SEGREDO',page.extract_text())

    def test_tj_arrays_and_quote_strings_are_really_removed(self):
        body=b'BT /F1 14 Tf 40 200 Td [(SEG) 25 (REDO)] TJ 12 TL (SECOND) \' ET BT /F1 14 Tf 40 60 Td (publico) Tj ET'
        self.apply(self.marked(body))
        data=all_decoded(self.root/'result.pdf');self.assertNotIn(b'SEG',data);self.assertNotIn(b'SECOND',data)
        self.assertIn('publico',PdfReader(self.root/'result.pdf').pages[0].extract_text())

    def test_complex_content_is_refused_without_publishing(self):
        for operator in (b'/GS1 gs',b'0 0 300 300 re W n',b'/ActualText (SECRET) BDC EMC',b'/Form1 Do'):
            with self.subTest(operator=operator):
                for name in ('plain.pdf','marked.pdf'):(self.root/name).unlink(missing_ok=True)
                source=self.marked(operator)
                with self.assertRaises(ValueError):self.apply(source)
                self.assertFalse((self.root/'result.pdf').exists())

    def test_paths_are_removed_by_intersection_and_public_vectors_remain(self):
        source=self.marked(b'1 0 0 rg 40 190 100 20 re f 0 1 0 rg 40 30 20 20 re f')
        result=self.apply(source);ops=PdfReader(self.root/'result.pdf').pages[0].get_contents().operations
        rectangles=[list(map(float,a)) for a,op in ops if op==b're']
        self.assertNotIn([40.,190.,100.,20.],rectangles);self.assertIn([40.,30.,20.,20.],rectangles)
        self.assertEqual(result['objects_removed']['paths_removed'],1)

    def test_no_overwrite_and_changed_source_guard(self):
        source=self.marked();target=self.root/'result.pdf';target.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):self.apply(source)
        self.assertEqual(target.read_bytes(),b'keep');target.unlink()
        with self.assertRaises(ValueError):redact_copy(source,target,dict(source_sha256='0'*64,dpi=150,mode='vector'))
        self.assertFalse(target.exists())
