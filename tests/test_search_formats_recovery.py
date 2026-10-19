"""Source preservation, passive formats, native OCR and explicit lock recovery."""
import hashlib,json,os,socket,sys,tempfile,unittest,zipfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))

from attachment_formats import extract_passive_text
from attachment_rtf import extract_rtf
from attachment_images import image_text
from search_languages import LANGUAGES,python_stemmer
from search_matching import query_spans
from test_attachment_search import text_pdf,request
import collection_index as index
import collection_recovery as recovery


def archive(parts):
    stream=BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as target:
        for name,value in parts.items():target.writestr(name,value)
    return stream.getvalue()


class PassiveSearchTests(unittest.TestCase):
    def test_all_pinned_language_algorithms_and_german_span(self):
        self.assertEqual(len(LANGUAGES),36)
        for language in LANGUAGES:
            with self.subTest(language=language):
                stemmer=python_stemmer('stem-'+language)
                self.assertIsInstance(stemmer.stemWord('testing'),str)
        self.assertTrue(list(query_spans('häuser haus','haus',False,'stem-de',0)))
        self.assertTrue(list(query_spans('hablando hablar','hablar',False,'stem-es',0)))
        with self.assertRaises(ValueError):python_stemmer('stem-../../evil')

    def test_docx_header_footnotes_and_odt_styles_are_included_without_objects(self):
        raw=archive({'word/document.xml':'<body><p>corpo<object>segredo</object></p></body>',
                     'word/header1.xml':'<hdr><p>cabeçalho</p></hdr>',
                     'word/footnotes.xml':'<notes><p>rodapé</p></notes>'})
        text,notice=extract_passive_text(raw,'.docx')
        self.assertIn('cabeçalho',text);self.assertIn('rodapé',text);self.assertNotIn('segredo',text);self.assertIn('objetos',notice)
        self.assertIn('estilo',extract_passive_text(archive({'content.xml':'<body>corpo</body>','styles.xml':'<body>estilo</body>'}),'.odt')[0])

    def test_xlsx_shared_inline_cached_formula_and_pptx_notes(self):
        raw=archive({'xl/sharedStrings.xml':'<sst><si><t>texto comum</t></si></sst>',
                     'xl/worksheets/sheet1.xml':'<sheet><c t="s"><v>0</v></c><c t="inlineStr"><is><t>direto</t></is></c><c><f>EXECUTE()</f><v>42</v></c></sheet>'})
        text,notice=extract_passive_text(raw,'.xlsx')
        self.assertIn('texto comum direto 42',text);self.assertNotIn('EXECUTE',text);self.assertIn('fórmulas',notice)
        raw=archive({'ppt/slides/slide1.xml':'<slide><p><t>slide</t></p></slide>','ppt/notesSlides/notesSlide1.xml':'<note><p><t>orador</t></p></note>'})
        self.assertIn('orador',extract_passive_text(raw,'.pptx')[0])
        with self.assertRaises(ValueError):extract_passive_text(archive({'xl/worksheets/sheet1.xml':'<s><c t="s"><v>99</v></c></s>'}),'.xlsx')

    def test_rtf_unicode_surrogate_pairs_hidden_and_passive_destinations(self):
        raw=br'{\rtf1\ansi\ansicpg1252 Ol\u225? \u-10179?\u-8704?{\v oculto}{\object executavel}{\*\unknown segredo}\par fim}'
        text,notice=extract_rtf(raw)
        self.assertEqual(text,'Olá 😀\nfim');self.assertIn('passivo',notice)
        for bad in [b'{\\rtf1 x}trailing',b'{\\rtf1 x',br'{\rtf1\bin999 x}',br'{\rtf1\u-10179?}']:
            with self.subTest(bad=bad),self.assertRaises(ValueError):extract_rtf(bad)

    def test_office_dtd_and_output_expansion_are_refused(self):
        with self.assertRaises(ValueError):extract_passive_text(archive({'word/document.xml':'<!DOCTYPE a [<!ENTITY e "x">]><a>&e;</a>'}),'.docx')
        with patch('attachment_formats.MAX_EXPANDED',150):
            with self.assertRaises(ValueError):extract_passive_text(archive({'xl/sharedStrings.xml':'<sst><si><t>'+('x'*80)+'</t></si></sst>','xl/worksheets/sheet1.xml':'<s>'+('<c t="s"><v>0</v></c>'*10)+'</s>'}),'.xlsx')

    def test_image_multiframe_refusal_precedes_any_ocr_process(self):
        from PIL import Image
        stream=BytesIO();first=Image.new('RGB',(10,10),'white');second=Image.new('RGB',(10,10),'black')
        first.save(stream,'TIFF',save_all=True,append_images=[second]);first.close();second.close()
        with patch('attachment_images.subprocess.run') as run,self.assertRaises(ValueError):image_text(stream.getvalue())
        run.assert_not_called()

    @unittest.skipUnless(os.name!='nt','Native Linux Tesseract integration')
    def test_actual_offline_attachment_ocr_recognizes_synthetic_image(self):
        from PIL import Image,ImageDraw,ImageFont
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',48)
        with Image.new('RGB',(1000,160),'white') as image:
            ImageDraw.Draw(image).text((30,40),'LINUXIT ALPHA 2048',font=font,fill='black')
            stream=BytesIO();image.save(stream,'PNG')
        self.assertIn('ALPHA',image_text(stream.getvalue()))


class IndexRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(text_pdf(['alpha']))
        self.index=self.root/'source.linuxit-index.json';index.build_index(self.index,{'paths':[str(self.source)]})

    def test_backup_restore_preserves_corrupt_destination_and_source_pdf(self):
        before=self.source.read_bytes();backup=self.root/'backup.json';recovery.snapshot_index(self.index,backup)
        self.index.write_bytes(b'corrupt');identity=hashlib.sha256(b'corrupt').hexdigest()
        report=recovery.restore_index(backup,self.index,identity)
        self.assertEqual(Path(report['preserved_previous']).read_bytes(),b'corrupt')
        self.assertEqual(index.load_index(self.index)[1],index.load_index(backup)[1]);self.assertEqual(before,self.source.read_bytes())

    def test_changed_destination_failed_restore_and_backup_collision_preserve_files(self):
        backup=self.root/'backup.json';recovery.snapshot_index(self.index,backup);before=self.index.read_bytes()
        with self.assertRaises(ValueError):recovery.restore_index(backup,self.index,'0'*64)
        with self.assertRaises(ValueError):recovery.snapshot_index(self.index,backup)
        with patch.object(recovery.os,'replace',side_effect=OSError('disk full')),self.assertRaises(OSError):
            recovery.restore_index(backup,self.index,hashlib.sha256(before).hexdigest())
        self.assertEqual(self.index.read_bytes(),before);self.assertFalse(list(self.root.glob('.linuxit-recovery-*')))

    def test_new_recovery_stale_sources_stay_excluded(self):
        target=self.root/'new.linuxit-index.json';recovery.restore_index(self.index,target)
        self.source.write_bytes(text_pdf(['changed alpha']))
        self.assertEqual(index.search_index(target,request('alpha'))['hits'],[])

    def test_only_dead_same_host_unchanged_lock_may_be_explicitly_removed(self):
        lock=self.index.with_name(self.index.name+'.lock')
        lock.write_text(json.dumps(dict(host=socket.gethostname(),pid=os.getpid(),token='a'*32)))
        self.assertFalse(recovery.inspect_lock(self.index)['removable'])
        with self.assertRaises(ValueError):recovery.remove_dead_lock(self.index,hashlib.sha256(lock.read_bytes()).hexdigest())
        with patch.object(recovery,'_alive',return_value=False):
            record=recovery.inspect_lock(self.index)
            lock.write_text('{}')
            with self.assertRaises(ValueError):recovery.remove_dead_lock(self.index,record['sha256'])
            lock.write_text(json.dumps(dict(host=socket.gethostname(),pid=123,token='b'*32)))
            recovery.remove_dead_lock(self.index,recovery.inspect_lock(self.index)['sha256'])
            self.assertFalse(lock.exists())

    def test_writer_preserves_a_replacement_lock(self):
        lock=self.index.with_name(self.index.name+'.lock')
        with index.index_writer_lock(self.index):lock.write_text('{"other_writer":true}')
        self.assertEqual(lock.read_text(),'{"other_writer":true}')
