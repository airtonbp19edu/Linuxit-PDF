"""E14: areas marked for redaction are /Redact annotations; nothing is removed until applied."""
import hashlib,os,shutil,subprocess,sys,tempfile,unittest
from io import BytesIO
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.generic import DecodedStreamObject,DictionaryObject,NameObject
from pdf_changes import inspect_editable_document,save_edited_copy

SECRET='SEGREDO 123'


def text_pdf():
    writer=PdfWriter();page=writer.add_blank_page(300,300)
    font=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),
        NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):font})})
    stream=DecodedStreamObject()
    stream.set_data(f'BT /F1 14 Tf 40 200 Td ({SECRET}) Tj ET BT /F1 14 Tf 40 60 Td (publico) Tj ET'.encode('ascii'))
    page[NameObject('/Contents')]=writer._add_object(stream)
    output=BytesIO();writer.write(output);return output.getvalue()


class RedactionMarkTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(text_pdf());self.count=0

    def save(self,source,operations):
        self.count+=1;target=self.root/f'out-{self.count}.pdf'
        save_edited_copy(source,target,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=operations)
        return target

    def marked(self):
        return self.save(self.source,[{'kind':'add-redaction','page':0,'rect':[30,190,160,222],'text':'CPF do cliente'}])

    def annotation(self,path):
        return PdfReader(str(path)).pages[0]['/Annots'][0].get_object()

    def test_mark_is_a_pending_redact_annotation_and_content_is_untouched(self):
        path=self.marked();note=self.annotation(path)
        self.assertEqual(note['/Subtype'],'/Redact');self.assertEqual(note['/Contents'],'CPF do cliente')
        self.assertEqual([float(v) for v in note['/QuadPoints']],[30,222,160,222,30,190,160,190])
        self.assertEqual([float(v) for v in note['/IC']],[0,0,0])
        self.assertNotIn('/OverlayText',note);self.assertNotIn('/RO',note)
        self.assertIn(b'[3 2] 0 d',note['/AP']['/N'].get_object().get_data())
        # Marking alone removes nothing: the text is still in the page content.
        self.assertIn(SECRET,PdfReader(str(path)).pages[0].extract_text())
        self.assertEqual(PdfReader(str(path)).pages[0]['/Contents'].get_object().get_data(),
                         PdfReader(str(self.source)).pages[0]['/Contents'].get_object().get_data())

    def test_mark_is_listed_as_editable(self):
        info=inspect_editable_document(self.marked())
        record=[r for r in info['annotations'] if r['subtype']=='/Redact'][0]
        self.assertTrue(record['styleable']);self.assertTrue(record['resizable'])
        self.assertEqual(record['text'],'CPF do cliente');self.assertEqual(record['rect'],[30,190,160,222])

    def test_mark_can_be_resized_commented_restyled_and_deleted(self):
        marked=self.marked()
        resized=self.save(marked,[{'kind':'resize-annotation','page':0,'index':0,'rect':[20,180,200,230]}])
        note=self.annotation(resized)
        self.assertEqual([float(v) for v in note['/QuadPoints']],[20,230,200,230,20,180,200,180])
        self.assertEqual(note['/Subtype'],'/Redact')
        commented=self.save(resized,[{'kind':'update-annotation','page':0,'index':0,'text':'Nome','author':'Revisor'}])
        self.assertEqual(self.annotation(commented)['/Contents'],'Nome');self.assertEqual(self.annotation(commented)['/T'],'Revisor')
        styled=self.save(commented,[{'kind':'style-annotation','page':0,'index':0,'color':[0,0,1],'opacity':.5}])
        self.assertEqual([float(v) for v in self.annotation(styled)['/C']],[0,0,1])
        deleted=self.save(styled,[{'kind':'delete-annotation','page':0,'index':0}])
        self.assertFalse(PdfReader(str(deleted)).pages[0].get('/Annots'))

    def test_invalid_marks_are_refused(self):
        for rect in ([30,190,30.1,222],[-5,190,160,222],[30,190,400,222],[160,190,30,222],[30,190,160,'x']):
            with self.subTest(rect=rect),self.assertRaises(ValueError):
                self.save(self.source,[{'kind':'add-redaction','page':0,'rect':rect,'text':''}])
        with self.assertRaises(ValueError):
            self.save(self.source,[{'kind':'add-redaction','page':0,'rect':[30,190,160,222],'text':'','overlay':'X'}])
        with self.assertRaises(ValueError):
            self.save(self.source,[{'kind':'add-redaction','page':0,'rect':[30,190,160,222],'text':'x'*70000}])

    def test_poppler_draws_the_outline_and_keeps_the_marked_text_visible(self):
        if not shutil.which('pdftocairo'):self.skipTest('Poppler pdftocairo required')
        from PIL import Image
        path=self.marked();base=self.root/'render'
        subprocess.run(['pdftocairo','-png','-r','144','-singlefile',str(path),str(base)],check=True,timeout=60)
        image=Image.open(str(base)+'.png').convert('RGB')
        border=[image.getpixel((x*2,int((300-221.5)*2))) for x in range(34,156,2)]
        self.assertTrue(any(p[0]>150 and p[1]<80 and p[2]<80 for p in border),border)
        inside=[image.getpixel((x,y)) for x in range(80,320) for y in range(2*(300-215),2*(300-195))]
        self.assertTrue(any(sum(p)<200 for p in inside),'texto marcado deveria continuar visível')


if __name__=='__main__':unittest.main()
