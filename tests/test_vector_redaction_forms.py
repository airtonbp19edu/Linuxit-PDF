"""Remove whole bounded forms, retaining no orphan secret resource graph."""
import hashlib
from io import BytesIO
from pathlib import Path
import os
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
from pypdf.generic import ArrayObject,DecodedStreamObject,DictionaryObject,FloatObject,NameObject
from test_redaction_apply import fixture,all_decoded


class VectorFormRedactionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def source(self,placements=((40,195),),matrix=None,bounds=(0,0,80,20)):
        writer=PdfWriter(clone_from=PdfReader(BytesIO(fixture())))
        page=writer.pages[0]
        form=DecodedStreamObject()
        form.set_data(b'0 0 80 20 re W n BT /F1 10 Tf 0 5 Td (NESTED_SECRET) Tj ET')
        form[NameObject('/Subtype')]=NameObject('/Form')
        form[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):page['/Resources']['/Font']})
        if bounds is not None:form[NameObject('/BBox')]=ArrayObject(FloatObject(v) for v in bounds)
        if matrix is not None:form[NameObject('/Matrix')]=ArrayObject(FloatObject(v) for v in matrix)
        objects=DictionaryObject({NameObject('/Complex'):writer._add_object(form)})
        page['/Resources'][NameObject('/XObject')]=objects
        body=b'BT /F1 14 Tf 40 30 Td (publico) Tj ET '
        for x,y in placements:body+=f'q 1 0 0 1 {x} {y} cm /Complex Do Q '.encode()
        content=DecodedStreamObject();content.set_data(body)
        page[NameObject('/Contents')]=writer._add_object(content)
        data=BytesIO();writer.write(data)
        plain=self.root/'plain.pdf';plain.write_bytes(data.getvalue())
        marked=self.root/'marked.pdf'
        save_edited_copy(plain,marked,source_sha256=hashlib.sha256(plain.read_bytes()).hexdigest(),
                         operations=[dict(kind='add-redaction',page=0,rect=[30,185,240,225],text='remover')])
        return marked

    def apply(self,source):
        return redact_copy(source,self.root/'result.pdf',dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),dpi=150,mode='vector'))

    def test_nested_clipping_text_removed_whole_without_raster_or_orphans(self):
        source=self.source();before=source.read_bytes();result=self.apply(source)
        output=self.root/'result.pdf'
        self.assertEqual(result['objects_removed']['forms_removed'],1)
        self.assertFalse(result['rasterized'])
        self.assertNotIn(b'NESTED_SECRET',all_decoded(output))
        self.assertNotIn('/XObject',PdfReader(output).pages[0]['/Resources'])
        self.assertIn('publico',PdfReader(output).pages[0].extract_text())
        self.assertEqual(source.read_bytes(),before)

    def test_form_matrix_and_page_transform_are_composed(self):
        source=self.source(placements=((40,20),),matrix=(1,0,0,1,0,175))
        self.apply(source)
        self.assertNotIn(b'NESTED_SECRET',all_decoded(self.root/'result.pdf'))

    def test_same_resource_kept_only_for_nonintersecting_invocation(self):
        source=self.source(placements=((40,195),(40,60)))
        result=self.apply(source);page=PdfReader(self.root/'result.pdf').pages[0]
        self.assertEqual(result['objects_removed']['forms_removed'],1)
        self.assertEqual(sum(op==b'Do' for args,op in page.get_contents().operations),1)
        self.assertIn('NESTED_SECRET',page.extract_text())

    def test_missing_or_reversed_bbox_refused_before_publication(self):
        for bounds in (None,(80,0,0,20),(0,0,0,20)):
            with self.subTest(bounds=bounds):
                for name in ('plain.pdf','marked.pdf'):(self.root/name).unlink(missing_ok=True)
                source=self.source(bounds=bounds)
                with self.assertRaises(ValueError):self.apply(source)
                self.assertFalse((self.root/'result.pdf').exists())
