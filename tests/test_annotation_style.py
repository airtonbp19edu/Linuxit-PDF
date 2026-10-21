"""E12: colour and opacity of existing simple annotations, appearance regenerated and rendered."""
import hashlib,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pdf_changes import inspect_editable_document,save_edited_copy

BLUE=[0,0,1]


class AnnotationStyleTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        writer=PdfWriter();writer.add_blank_page(300,300);self.blank=self.root/'blank.pdf'
        with open(self.blank,'wb') as handle:writer.write(handle)
        self.count=0

    def save(self,source,operations):
        self.count+=1;target=self.root/f'out-{self.count}.pdf'
        save_edited_copy(source,target,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=operations)
        return target

    def annotated(self):
        return self.save(self.blank,[
            {'kind':'add-rectangle','page':0,'rect':[20,200,120,280],'text':'r'},
            {'kind':'add-highlight','page':0,'rect':[150,200,280,280],'text':'h'},
            {'kind':'add-ellipse','page':0,'rect':[20,100,120,180],'text':'e'},
            {'kind':'add-line','page':0,'points':[150,140,280,140],'text':'l'},
            {'kind':'add-ink','page':0,'paths':[[20,40,120,40,120,80]],'text':'i'},
            {'kind':'add-note','page':0,'text':'nota','rect':None}])

    def pixel(self,path,x,y,scale=2):
        if not shutil.which('pdftocairo'):self.skipTest('Poppler pdftocairo required')
        from PIL import Image
        base=self.root/f'render-{path.stem}'
        subprocess.run(['pdftocairo','-png','-r',str(72*scale),'-singlefile',str(path),str(base)],check=True,timeout=60)
        image=Image.open(str(base)+'.png').convert('RGB')
        return image.getpixel((int(x*scale),int((300-y)*scale)))

    def test_every_supported_type_becomes_blue_and_half_transparent(self):
        source=self.annotated()
        info=inspect_editable_document(source)
        styleable=[r for r in info['annotations'] if r['styleable']]
        self.assertEqual(sorted(r['subtype'] for r in styleable),['/Circle','/Highlight','/Ink','/Line','/Square'])
        self.assertFalse(next(r for r in info['annotations'] if r['subtype']=='/Text')['styleable'])
        styled=self.save(source,[{'kind':'style-annotation','page':0,'index':r['index'],'color':BLUE,'opacity':.5} for r in styleable])
        reader=PdfReader(styled)
        for ref in reader.pages[0]['/Annots']:
            note=ref.get_object()
            if note['/Subtype']=='/Text':continue
            self.assertEqual([float(c) for c in note['/C']],[0,0,1]);self.assertEqual(float(note['/CA']),.5)
            stream=note['/AP']['/N'].get_object()
            self.assertIn(b'0.0000 0.0000 1.0000',stream.get_data())
            self.assertEqual(float(stream['/Resources']['/ExtGState']['/LinuxitStyle']['/CA']),.5)
        # Rendered by Poppler: half-transparent blue over white is light blue, not red.
        for x,y in ((20.6,240),(20.8,140),(215,140),(215,240),(70,40)):
            r,g,b=self.pixel(styled,x,y)
            with self.subTest(point=(x,y)):self.assertGreater(b,r+40);self.assertGreater(r,60)
        self.assertEqual(self.statuses(source,styled),'original preserved')

    def statuses(self,source,styled):
        self.assertNotEqual(source.read_bytes(),styled.read_bytes())
        return 'original preserved'

    def test_full_opacity_keeps_solid_colour_and_restyle_can_repeat(self):
        source=self.annotated();index=next(r['index'] for r in inspect_editable_document(source)['annotations'] if r['subtype']=='/Square')
        green=self.save(source,[{'kind':'style-annotation','page':0,'index':index,'color':[0,.6,0],'opacity':1}])
        again=self.save(green,[{'kind':'style-annotation','page':0,'index':index,'color':[0,0,1],'opacity':1}])
        record=next(r for r in inspect_editable_document(again)['annotations'] if r['index']==index)
        self.assertEqual((record['color'],record['opacity']),([0.0,0.0,1.0],1.0))
        r,g,b=self.pixel(again,20.6,240);self.assertGreater(b,200);self.assertLess(r,60)

    def test_notes_bad_colour_and_too_low_opacity_are_refused_without_output(self):
        source=self.annotated();records=inspect_editable_document(source)['annotations']
        note=next(r['index'] for r in records if r['subtype']=='/Text');square=next(r['index'] for r in records if r['subtype']=='/Square')
        cases=((note,BLUE,.5,'notas'),(square,[0,0,2],.5,'Cor'),(square,BLUE,.05,'Opacidade'),(square,[0,0],.5,'Cor'))
        before=sorted(self.root.iterdir())
        for index,color,opacity,message in cases:
            with self.subTest(message=message),self.assertRaisesRegex(ValueError,message):
                self.save(source,[{'kind':'style-annotation','page':0,'index':index,'color':color,'opacity':opacity}])
        self.assertEqual(sorted(self.root.iterdir()),before)


if __name__=='__main__':unittest.main()
