import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_changes import save_edited_copy
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader

class RecoveredEditTests(unittest.TestCase):
    def test_consented_corpus_edits_publish_new_strictly_readable_copies(self):
        base=ROOT/'testes/fixtures/danificados';manifest=json.loads((base/'corpus.json').read_text())
        with tempfile.TemporaryDirectory() as folder:
            for row in manifest['files']:
                if not row['expected'].get('recovered'):continue
                with self.subTest(row['file']):
                    source=base/row['file'];before=source.read_bytes();dest=Path(folder)/row['file']
                    save_edited_copy(source,dest,source_sha256=hashlib.sha256(before).hexdigest(),
                        operations=[dict(kind='add-note',page=0,rect=None,text='nota recuperada')],
                        auth={'password':None,'recover':True})
                    reader=PdfReader(dest,strict=True)
                    self.assertEqual(len(reader.pages),row['expected']['recovered']['pages'])
                    self.assertEqual(source.read_bytes(),before)

    def test_unrecoverable_input_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'broken.pdf';source.write_bytes(b'%PDF-1.7\nno usable catalog')
            dest=Path(folder)/'new.pdf'
            with self.assertRaises(Exception):save_edited_copy(source,dest,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=[dict(kind='rotate-page',page=0,rotation=90)],auth={'password':None,'recover':True})
            self.assertFalse(dest.exists())
