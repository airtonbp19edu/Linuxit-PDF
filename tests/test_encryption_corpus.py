"""E18: matrix of encryption profiles (RC4-40, RC4-128, AES-128, AES-256, clear metadata) × open, edit, print."""
import hashlib,json,os,shutil,subprocess,sys,tempfile,unittest
from io import BytesIO
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from document_session import DocumentSession
from pdf_changes import save_edited_copy

CORPUS=ROOT/'testes/fixtures/criptografia'
MANIFEST=json.loads((CORPUS/'corpus.json').read_text(encoding='utf-8'))
USER,OWNER=MANIFEST['user_password'],MANIFEST['owner_password']
TEXT=MANIFEST['content']['text']


def encryption_of(data):
    entry=PdfReader(BytesIO(data)).trailer['/Encrypt'].get_object()
    flag=entry.get('/EncryptMetadata',True)
    return dict(V=int(entry['/V']),R=int(entry['/R']),Length=int(entry.get('/Length',40)),P=int(entry['/P']),
                EncryptMetadata=getattr(flag,'value',flag) is not False)


def xmp_title(reader):
    data=reader.root_object['/Metadata'].get_object().get_data()
    return MANIFEST['content']['xmp_title'] if MANIFEST['content']['xmp_title'].encode() in data else None


class EncryptionCorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def profiles(self):
        for row in MANIFEST['files']:
            source=self.root/row['file'];shutil.copyfile(CORPUS/row['file'],source)
            yield row,source

    def test_fixtures_match_the_manifest_and_independent_readers(self):
        self.assertEqual([r['algorithm'] for r in MANIFEST['files']],['RC4-40','RC4-128','AES-128','AES-256','AES-128'])
        self.assertEqual([r['EncryptMetadata'] for r in MANIFEST['files']],[True,True,True,True,False])
        for row in MANIFEST['files']:
            data=(CORPUS/row['file']).read_bytes()
            self.assertEqual((len(data),hashlib.sha256(data).hexdigest()),(row['bytes'],row['sha256']),row['file'])
            self.assertEqual(encryption_of(data),{k:row[k] for k in ('V','R','Length','P','EncryptMetadata')})
            self.assertEqual(MANIFEST['content']['xmp_title'].encode() in data,not row['EncryptMetadata'])
            if shutil.which('pdftotext'):
                text=subprocess.run(['pdftotext','-upw',USER,str(CORPUS/row['file']),'-'],capture_output=True,text=True,timeout=60).stdout
                self.assertEqual(text.split(),' '.join(TEXT).split())
        script=ROOT/'scripts/gerar_corpus_criptografia.py'
        if script.exists():
            result=subprocess.run([sys.executable,str(script),'--check'],capture_output=True,text=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_open_with_user_owner_wrong_and_missing_password(self):
        for row,source in self.profiles():
            with self.subTest(row['file']):
                before=source.read_bytes();session=DocumentSession(source);self.addCleanup(session.close)
                self.assertEqual(session.prepare()['status'],'password_required')
                self.assertEqual(session.prepare('senha-errada')['status'],'password_invalid')
                info=session.prepare(USER)
                self.assertEqual((info['status'],info['encrypted'],info['recovered'],info['pages']),('ready',True,False,2))
                self.assertEqual(info['permissions'],MANIFEST['permissions_for_user'])
                self.assertEqual(info['metadata']['title'],MANIFEST['content']['info_title'])
                view=PdfReader(session.read_path,strict=True);self.assertFalse(view.is_encrypted)
                self.assertEqual([p.extract_text().strip() for p in view.pages],TEXT)
                self.assertEqual(xmp_title(view),MANIFEST['content']['xmp_title'],'XMP legível na leitura')
                owner=DocumentSession(source);self.addCleanup(owner.close)
                self.assertTrue(all(owner.prepare(OWNER)['permissions'].values()))
                self.assertEqual(source.read_bytes(),before)

    def test_edit_keeps_the_profile_and_follows_user_permissions(self):
        for row,source in self.profiles():
            with self.subTest(row['file']):
                identity=hashlib.sha256(source.read_bytes()).hexdigest()
                target=self.root/('editado-'+row['file'])
                save_edited_copy(source,target,source_sha256=identity,auth=dict(password=OWNER,recover=False),
                                 operations=[{'kind':'add-bookmark','title':'Marcador cifrado','page':1}])
                data=target.read_bytes()
                self.assertEqual(encryption_of(data),{k:row[k] for k in ('V','R','Length','P','EncryptMetadata')})
                self.assertEqual(MANIFEST['content']['xmp_title'].encode() in data,not row['EncryptMetadata'],'metadados claros só quando declarado')
                reader=PdfReader(BytesIO(data));self.assertTrue(reader.decrypt(USER))
                self.assertEqual([o.title for o in reader.outline],['Marcador cifrado'])
                self.assertEqual([p.extract_text().strip() for p in reader.pages],TEXT)
                self.assertEqual(xmp_title(reader),MANIFEST['content']['xmp_title'])
                if shutil.which('pdfinfo'):
                    meta=subprocess.run(['pdfinfo','-upw',USER,'-meta',str(target)],capture_output=True,text=True,timeout=60).stdout
                    self.assertIn(MANIFEST['content']['xmp_title'],meta)
                # User password: annotations allowed, modifying the outline denied.
                noted=self.root/('nota-'+row['file'])
                save_edited_copy(source,noted,source_sha256=identity,auth=dict(password=USER,recover=False),
                                 operations=[{'kind':'add-note','page':0,'text':'nota','rect':None}])
                self.assertTrue(noted.exists())
                denied=self.root/('negado-'+row['file'])
                with self.assertRaisesRegex(ValueError,'permissão'):
                    save_edited_copy(source,denied,source_sha256=identity,auth=dict(password=USER,recover=False),
                                     operations=[{'kind':'add-bookmark','title':'x','page':0}])
                self.assertFalse(denied.exists())

    def test_print_preparation_uses_the_reading_copy_and_low_quality_only(self):
        from print_tasks import prepare_print
        for row,source in self.profiles():
            with self.subTest(row['file']):
                session=DocumentSession(source);self.addCleanup(session.close);info=session.prepare(USER)
                self.assertTrue(info['permissions']['print']);self.assertFalse(info['permissions']['print_high_quality'])
                out=self.root/('impressao-'+row['file'])
                with session.lease() as path:
                    prepare_print(path,out,{'scale_mode':'fit','print_as_image':True,'image_dpi':150})
                printed=PdfReader(out);self.assertFalse(printed.is_encrypted);self.assertEqual(len(printed.pages),2)


if __name__=='__main__':unittest.main()
