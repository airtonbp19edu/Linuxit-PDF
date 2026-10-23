"""Own DOCX/ODT export: real Poppler text, valid packages, page starts and source safety."""
import hashlib,os,shutil,sys,tempfile,unittest,zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_conversion import convert_copy
from office_export import paragraphs_from_bbox,write_docx,write_odt,verify_office
from test_attachment_search import text_pdf

W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
T='{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
SAMPLE='''<html><body><doc><page width="200" height="200"><flow><block xMin="1" yMin="10" xMax="90" yMax="40">
<line xMin="1" yMin="10" xMax="90" yMax="22"><word xMin="1" yMin="10" xMax="20" yMax="22">Ol&amp;á</word><word xMin="1" yMin="10" xMax="20" yMax="22">exem-</word></line>
<line xMin="1" yMin="24" xMax="90" yMax="36"><word xMin="1" yMin="24" xMax="20" yMax="36">plo</word><word xMin="1" yMin="24" xMax="20" yMax="36">&lt;b&gt;</word></line>
</block></flow></page><page width="200" height="200"></page></doc></body></html>'''


class OfficeExportUnitTests(unittest.TestCase):
    def test_blocks_become_paragraphs_with_unescaped_text_joined_hyphens_and_empty_pages(self):
        pages=paragraphs_from_bbox(SAMPLE)
        self.assertEqual(len(pages),2);self.assertEqual(pages[1],[])
        self.assertEqual(pages[0][0]['text'],'Ol&á exemplo <b>');self.assertEqual(pages[0][0]['size'],10.0)

    def test_docx_and_odt_packages_parse_and_keep_one_start_per_pdf_page(self):
        pages=paragraphs_from_bbox(SAMPLE)
        with tempfile.TemporaryDirectory() as folder:
            docx=Path(folder)/'a.docx';odt=Path(folder)/'a.odt'
            write_docx(pages,docx);write_odt(pages,odt)
            self.assertEqual(verify_office(docx,'docx',2),2);self.assertEqual(verify_office(odt,'odt',2),2)
            with zipfile.ZipFile(docx) as archive:
                self.assertIn('[Content_Types].xml',archive.namelist())
                texts=[t.text for t in ET.fromstring(archive.read('word/document.xml')).iter(W+'t')]
            self.assertEqual(texts[0],'Ol&á exemplo <b>')
            with zipfile.ZipFile(odt) as archive:
                first=archive.infolist()[0]
                self.assertEqual((first.filename,first.compress_type,archive.read('mimetype')),('mimetype',zipfile.ZIP_STORED,b'application/vnd.oasis.opendocument.text'))
                body=[''.join(p.itertext()) for p in ET.fromstring(archive.read('content.xml')).iter(T+'p')]
            self.assertEqual(body[0],'Ol&á exemplo <b>')

    def test_control_characters_never_reach_the_xml(self):
        pages=paragraphs_from_bbox(SAMPLE.replace('plo','pl\x01o'))
        self.assertNotIn('\x01',pages[0][0]['text'])

    def test_page_count_mismatch_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            docx=Path(folder)/'a.docx';write_docx(paragraphs_from_bbox(SAMPLE),docx)
            with self.assertRaises(ValueError):verify_office(docx,'docx',3)


@unittest.skipUnless(shutil.which('pdftotext'),'Requires Poppler pdftotext')
class OfficeExportPopplerTests(unittest.TestCase):
    def test_real_pdf_exports_editable_text_per_page_without_touching_source(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';source.write_bytes(text_pdf(['Primeira pagina','Segunda pagina']));before=source.read_bytes()
            identity=hashlib.sha256(before).hexdigest()
            for kind in ('docx','odt'):
                with self.subTest(kind=kind):
                    target=Path(folder)/('a.'+kind)
                    result=convert_copy(source,target,dict(source_sha256=identity,format=kind,dpi=150))
                    self.assertEqual((result['pages'],result['format'],result['layout_preserved']),(2,kind,False))
                    with zipfile.ZipFile(target) as archive:
                        xml=archive.read('word/document.xml' if kind=='docx' else 'content.xml').decode('utf-8')
                    self.assertIn('Primeira pagina',xml);self.assertIn('Segunda pagina',xml)
                    self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(),result['output_sha256'])
                    with self.assertRaises(FileExistsError):convert_copy(source,target,dict(source_sha256=identity,format=kind,dpi=150))
            self.assertEqual(source.read_bytes(),before)

    def test_wrong_extension_is_refused_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'a.pdf';source.write_bytes(text_pdf(['x']))
            target=Path(folder)/'a.odt'
            with self.assertRaises(ValueError):
                convert_copy(source,target,dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),format='docx',dpi=150))
            self.assertFalse(target.exists())


if __name__=='__main__':unittest.main()
