"""E17: each damaged-PDF fixture opens, recovers only with consent, or is refused without inventing pages."""
import hashlib,json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from document_session import DocumentSession,DocumentError,describe_repairs
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader

CORPUS=ROOT/'testes/fixtures/danificados'


def load():
    return json.loads((CORPUS/'corpus.json').read_text(encoding='utf-8'))


class DamagedCorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def test_fixtures_match_the_manifest_and_the_generator(self):
        manifest=load();self.assertEqual(manifest['schema'],'linuxit-damaged-corpus-v1');self.assertGreaterEqual(len(manifest['files']),12)
        for row in manifest['files']:
            data=(CORPUS/row['file']).read_bytes()
            self.assertEqual((len(data),hashlib.sha256(data).hexdigest()),(row['bytes'],row['sha256']),row['file'])
        script=ROOT/'scripts/gerar_corpus_danificado.py'
        if script.exists():  # payload/sandbox runs have no scripts/
            result=subprocess.run([sys.executable,str(script),'--check'],capture_output=True,text=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_every_fixture_follows_its_expected_outcome_through_the_real_worker(self):
        render=shutil.which('pdftocairo')  # shipped in the Flatpak; pdftoppm is not
        for row in load()['files']:
            with self.subTest(row['file']):
                source=self.root/row['file'];shutil.copyfile(CORPUS/row['file'],source);before=source.read_bytes()
                expected=row['expected'];session=DocumentSession(source);self.addCleanup(session.close)
                first=session.prepare()
                self.assertEqual(first['status'],expected['open'])
                if expected['open']=='ready':
                    self.assertFalse(first['recovered']);self.assertEqual(first['pages'],expected['pages'])
                    self.assertEqual(session.read_path,str(source.resolve()))
                    continue
                self.assertTrue(first['repairs'] and all(isinstance(r,str) for r in first['repairs']))
                self.assertFalse((session.root/'view.pdf').exists(),'nada é gravado antes do consentimento')
                if expected.get('refused'):
                    with self.assertRaises(RuntimeError):session.prepare(recover=True)
                    self.assertFalse((session.root/'view.pdf').exists())
                else:
                    info=session.prepare(recover=True);want=expected['recovered']
                    self.assertEqual(info['status'],'ready');self.assertTrue(info['recovered'])
                    self.assertEqual((info['pages'],info['repairs']),(want['pages'],want['repairs']))
                    self.assertEqual(len(info['sizes']),want['pages'])
                    view=PdfReader(session.read_path,strict=True)
                    self.assertEqual([(p.extract_text() or '').strip() for p in view.pages],want['text'])
                    if render:
                        out=self.root/(row['file']+'-r');out.mkdir()
                        subprocess.run([render,'-png','-r','20',session.read_path,str(out/'p')],check=True,timeout=60)
                        self.assertEqual(len(list(out.glob('p*.png'))),want['pages'],'nenhuma página inventada')
                    self.assertTrue(describe_repairs(info['repairs']))
                self.assertEqual(source.read_bytes(),before)

    def test_repair_labels_are_fixed_text_only(self):
        self.assertEqual(describe_repairs(['xref','<script>','pagina_ausente',3]),'tabela de referências danificada, página inexistente omitida')
        self.assertEqual(describe_repairs([]),'')


if __name__=='__main__':unittest.main()
