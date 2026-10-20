"""E13: Square, Circle and FreeText get a new rectangle with a regenerated appearance."""
import hashlib,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pdf_changes import inspect_editable_document,save_edited_copy


class AnnotationResizeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        writer=PdfWriter();writer.add_blank_page(300,300);blank=self.root/'blank.pdf'
        with open(blank,'wb') as handle:writer.write(handle)
        self.count=0
        self.source=self.save(blank,[{'kind':'add-rectangle','page':0,'rect':[20,200,120,280],'text':'r'},
                                     {'kind':'add-ellipse','page':0,'rect':[150,200,280,280],'text':'e'},
                                     {'kind':'add-freetext','page':0,'rect':[20,20,140,60],'text':'Texto livre redimensionável'},
                                     {'kind':'add-line','page':0,'points':[150,100,280,100],'text':'l'}])
        self.records={r['subtype']:r for r in inspect_editable_document(self.source)['annotations']}

    def save(self,source,operations):
        self.count+=1;target=self.root/f'out-{self.count}.pdf'
        save_edited_copy(source,target,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=operations)
        return target

    def note(self,path,index):return PdfReader(path).pages[0]['/Annots'][index].get_object()

    def pixel(self,path,x,y):
        if not shutil.which('pdftoppm'):self.skipTest('Poppler pdftoppm required')
        from PIL import Image
        base=self.root/f'render-{path.stem}'
        subprocess.run(['pdftoppm','-r','144','-png','-singlefile',str(path),str(base)],check=True,timeout=60)
        return Image.open(str(base)+'.png').convert('RGB').getpixel((int(x*2),int((300-y)*2)))

    def test_square_and_circle_are_redrawn_in_the_new_rectangle(self):
        square,circle=self.records['/Square'],self.records['/Circle']
        self.assertTrue(square['resizable'] and circle['resizable'] and not self.records['/Line']['resizable'])
        self.assertEqual(square['rect'],[20.0,200.0,120.0,280.0])
        out=self.save(self.source,[{'kind':'resize-annotation','page':0,'index':square['index'],'rect':[40,150,200,290]},
                                   {'kind':'resize-annotation','page':0,'index':circle['index'],'rect':[210,120,290,200]}])
        for record,rect in ((square,[40,150,200,290]),(circle,[210,120,290,200])):
            note=self.note(out,record['index'])
            self.assertEqual([float(v) for v in note['/Rect']],rect)
            box=note['/AP']['/N'].get_object()['/BBox']
            self.assertEqual([float(v) for v in box],[0,0,rect[2]-rect[0],rect[3]-rect[1]])
        # Poppler draws the new border where the old rectangle was not, and nothing at the old left edge.
        self.assertLess(sum(self.pixel(out,40.5,220)),600);self.assertGreater(sum(self.pixel(out,20.5,250)),740)

    def test_freetext_is_laid_out_again_for_the_new_size(self):
        record=self.records['/FreeText'];old=self.note(self.source,record['index'])['/AP']['/N'].get_object().get_data()
        out=self.save(self.source,[{'kind':'resize-annotation','page':0,'index':record['index'],'rect':[20,20,280,60]}])
        note=self.note(out,record['index'])
        self.assertEqual([float(v) for v in note['/Rect']],[20,20,280,60])
        self.assertEqual([float(v) for v in note['/AP']['/N'].get_object()['/BBox']],[0,0,260,40])
        self.assertNotEqual(note['/AP']['/N'].get_object().get_data(),old)
        self.assertEqual(note['/Contents'],'Texto livre redimensionável')

    def test_line_outside_page_and_tiny_rectangles_are_refused(self):
        before=sorted(self.root.iterdir())
        for index,rect,message in ((self.records['/Line']['index'],[10,10,50,50],'redimensionad'),
                                   (self.records['/Square']['index'],[10,10,400,50],'CropBox'),
                                   (self.records['/Square']['index'],[10,10,10.1,50],'0,25')):
            with self.subTest(message=message),self.assertRaisesRegex(ValueError,message):
                self.save(self.source,[{'kind':'resize-annotation','page':0,'index':index,'rect':rect}])
        self.assertEqual(sorted(self.root.iterdir()),before)


if __name__=='__main__':unittest.main()
