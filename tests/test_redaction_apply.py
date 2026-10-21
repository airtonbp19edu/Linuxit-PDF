"""E15: applying redaction marks removes text and images under them in a new copy."""
import hashlib,os,shutil,subprocess,sys,tempfile,unittest
from io import BytesIO
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.generic import (ArrayObject,DecodedStreamObject,DictionaryObject,FloatObject,NameObject,NumberObject,
                           TextStringObject)
from pdf_changes import save_edited_copy

SECRET=b'SEGREDO 123'


def fixture(rotate=0,structure=False):
    """Page 1: secret text, a red image inside the future mark, public text. Page 2: other text."""
    writer=PdfWriter()
    font=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),
        NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    image=DecodedStreamObject();image.set_data(bytes([255,0,0])*100)
    image.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Image'),
                  NameObject('/Width'):NumberObject(10),NameObject('/Height'):NumberObject(10),
                  NameObject('/ColorSpace'):NameObject('/DeviceRGB'),NameObject('/BitsPerComponent'):NumberObject(8)})
    image=writer._add_object(image)
    for body in (b'BT /F1 14 Tf 40 200 Td (SEGREDO 123) Tj ET q 30 0 0 30 200 190 cm /Im1 Do Q BT /F1 14 Tf 40 60 Td (publico) Tj ET',
                 b'BT /F1 14 Tf 40 200 Td (PAGINA DOIS) Tj ET'):
        page=writer.add_blank_page(300,300)
        resources=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):font})})
        if b'/Im1' in body:resources[NameObject('/XObject')]=DictionaryObject({NameObject('/Im1'):image})
        page[NameObject('/Resources')]=resources
        stream=DecodedStreamObject();stream.set_data(body);page[NameObject('/Contents')]=writer._add_object(stream)
    if rotate:writer.pages[0][NameObject('/Rotate')]=NumberObject(rotate)
    if structure:
        writer._root_object[NameObject('/StructTreeRoot')]=writer._add_object(DictionaryObject({
            NameObject('/Type'):NameObject('/StructTreeRoot'),NameObject('/K'):DictionaryObject({
                NameObject('/S'):NameObject('/P'),NameObject('/ActualText'):TextStringObject('SEGREDO 123')})}))
        writer._root_object[NameObject('/MarkInfo')]=DictionaryObject({NameObject('/Marked'):NameObject('/true')})
    output=BytesIO();writer.write(output);return output.getvalue()


def all_decoded(path):
    """Raw bytes plus every object of the file decoded, so compressed leftovers are found too."""
    import logging
    reader=PdfReader(str(path));chunks=[Path(path).read_bytes()]
    logging.getLogger('pypdf').setLevel(logging.CRITICAL)
    for number in range(1,int(reader.trailer['/Size'])):
        try:item=reader.get_object(number)
        except Exception:continue
        if item is None:continue
        if hasattr(item,'get_data'):
            try:chunks.append(item.get_data())
            except Exception:pass
        chunks.append(repr(item).encode('utf-8','replace'))
    return b'\n'.join(chunks)


class RedactionApplyTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which('pdftocairo'):self.skipTest('Poppler pdftocairo required')
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.count=0

    def source(self,data=None,operations=None,**kwargs):
        self.count+=1;plain=self.root/f'plain-{self.count}.pdf';plain.write_bytes(data or fixture(**kwargs))
        marked=self.root/f'marked-{self.count}.pdf'
        operations=operations or [{'kind':'add-redaction','page':0,'rect':[30,185,240,225],'text':'CPF'}]
        save_edited_copy(plain,marked,source_sha256=hashlib.sha256(plain.read_bytes()).hexdigest(),operations=operations)
        return marked

    def apply(self,source,dpi=150):
        from pdf_redaction import redact_copy
        target=self.root/f'redigido-{self.count}.pdf'
        result=redact_copy(source,target,{'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dpi':dpi})
        return target,result

    def render(self,path,page=1):
        from PIL import Image
        base=self.root/f'render-{path.stem}-{page}'
        subprocess.run(['pdftocairo','-png','-r','144','-singlefile','-f',str(page),'-l',str(page),str(path),str(base)],check=True,timeout=60)
        return Image.open(str(base)+'.png').convert('RGB')

    def test_text_and_image_under_the_mark_are_gone_and_other_pages_are_intact(self):
        source=self.source();before=hashlib.sha256(source.read_bytes()).hexdigest()
        target,result=self.apply(source)
        self.assertEqual(result['redacted_pages'],[1]);self.assertEqual(result['marks_applied'],1)
        self.assertTrue(result['rasterized']);self.assertFalse(result['structure_tree_removed'])
        reader=PdfReader(str(target));original=PdfReader(str(source))
        self.assertEqual(len(reader.pages),2)
        self.assertEqual(reader.pages[0].extract_text().strip(),'')
        self.assertNotIn('/Annots',reader.pages[0])
        self.assertNotIn(SECRET,all_decoded(target))
        self.assertNotIn(b'\xff\x00\x00'*10,all_decoded(target))
        self.assertEqual(reader.pages[1].get_contents().get_data(),original.pages[1].get_contents().get_data())
        self.assertIn('PAGINA DOIS',reader.pages[1].extract_text())
        image=self.render(target)
        self.assertEqual(image.getpixel((2*60,2*(300-205))),(0,0,0))       # secret text area
        self.assertEqual(image.getpixel((2*215,2*(300-205))),(0,0,0))      # red image area
        self.assertTrue(any(sum(image.getpixel((x,y)))<300 for x in range(80,200) for y in range(2*(300-75),2*(300-55))),
                        'texto fora da marca deveria continuar visível')
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),before)

    def test_overlapping_annotations_go_and_others_stay(self):
        source=self.source(operations=[{'kind':'add-redaction','page':0,'rect':[30,185,240,225],'text':''},
            {'kind':'add-freetext','page':0,'rect':[40,190,180,215],'text':'SEGREDO 123'},
            {'kind':'add-rectangle','page':0,'rect':[20,20,100,50],'text':'fica'}])
        target,result=self.apply(source)
        self.assertEqual(result['annotations_removed'],2)
        notes=[n.get_object() for n in PdfReader(str(target)).pages[0]['/Annots']]
        self.assertEqual([n['/Subtype'] for n in notes],['/Square'])
        self.assertNotIn(SECRET,all_decoded(target))

    def test_rotated_page_is_painted_in_page_space(self):
        target,_=self.apply(self.source(rotate=90))
        reader=PdfReader(str(target));self.assertEqual(reader.pages[0].rotation,90)
        unrotated=PdfWriter(clone_from=reader);unrotated.pages[0][NameObject('/Rotate')]=NumberObject(0)
        check=self.root/'sem-rotacao.pdf'
        with check.open('wb') as handle:unrotated.write(handle)
        image=self.render(check)
        self.assertEqual(image.getpixel((2*60,2*(300-205))),(0,0,0))
        self.assertTrue(any(sum(image.getpixel((x,y)))<300 for x in range(80,200) for y in range(2*(300-75),2*(300-55))))

    def test_structure_tree_is_dropped(self):
        target,result=self.apply(self.source(structure=True))
        self.assertTrue(result['structure_tree_removed'])
        self.assertNotIn('/StructTreeRoot',PdfReader(str(target)).root_object)
        self.assertNotIn(SECRET,all_decoded(target))

    def test_refusals_create_nothing(self):
        from pdf_redaction import redact_copy
        plain=self.root/'plain.pdf';plain.write_bytes(fixture());identity=hashlib.sha256(plain.read_bytes()).hexdigest()
        cases={'sem_marcas':(plain,{'source_sha256':identity,'dpi':150},'Não há áreas marcadas'),
               'dpi':(plain,{'source_sha256':identity,'dpi':200},'150 ou 300'),
               'chave_extra':(plain,{'source_sha256':identity,'dpi':150,'overlay':'x'},'inválido'),
               'identidade':(plain,{'source_sha256':'0'*64,'dpi':150},'mudou')}
        for label,(path,request,message) in cases.items():
            target=self.root/f'{label}.pdf'
            with self.subTest(label),self.assertRaisesRegex(ValueError,message):redact_copy(path,target,request)
            self.assertFalse(target.exists())
        # Form field under a mark.
        writer=PdfWriter(clone_from=str(self.source()))
        widget=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Widget'),
            NameObject('/FT'):NameObject('/Tx'),NameObject('/T'):TextStringObject('cpf'),
            NameObject('/Rect'):ArrayObject(FloatObject(v) for v in (50,195,150,215))})
        writer.add_annotation(0,widget)
        field=writer.pages[0]['/Annots'][-1]
        writer._root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject([field])})
        form=self.root/'form.pdf'
        with form.open('wb') as handle:writer.write(handle)
        with self.assertRaisesRegex(ValueError,'campo de formulário'):self.apply(form)
        # Signed or permission-locked document.
        writer=PdfWriter(clone_from=str(self.source()))
        writer._root_object[NameObject('/Perms')]=DictionaryObject()
        locked=self.root/'locked.pdf'
        with locked.open('wb') as handle:writer.write(handle)
        with self.assertRaisesRegex(NotImplementedError,'assinaturas'):self.apply(locked)
        # Existing destination is never replaced.
        source=self.source();target=self.root/'existe.pdf';target.write_bytes(b'x')
        from pdf_redaction import redact_copy as again
        with self.assertRaises(FileExistsError):
            again(source,target,{'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dpi':150})
        self.assertEqual(target.read_bytes(),b'x')

    def test_worker_round_trip_and_confirmation(self):
        from pdf_redaction import invoke_redaction
        source=self.source();target=self.root/'via-worker.pdf'
        result=invoke_redaction(source,target,{'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'dpi':300})
        self.assertEqual(result['dpi'],300);self.assertEqual(result['redacted_pages'],[1])
        self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(),result['output_sha256'])
        self.assertNotIn(SECRET,all_decoded(target))
        with self.assertRaisesRegex(RuntimeError,'Não há áreas marcadas'):
            plain=self.root/'p.pdf';plain.write_bytes(fixture())
            invoke_redaction(plain,self.root/'nada.pdf',{'source_sha256':hashlib.sha256(plain.read_bytes()).hexdigest(),'dpi':150})


if __name__=='__main__':unittest.main()
