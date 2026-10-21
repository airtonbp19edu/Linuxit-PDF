"""E16: a 3D annotation's own appearance is shown as a still poster; the scene is never interactive."""
import hashlib,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter
from pypdf.generic import ArrayObject,DecodedStreamObject,DictionaryObject,FloatObject,NameObject,NumberObject
from pdf_media import inspect_media,extract_media,render_poster

BLUE=(0,0,255);RED=(255,0,0)


def numbers(*values):return ArrayObject(FloatObject(v) for v in values)


def poster_pdf(path):
    """Page 300x300. 3D #1: U3D model, two views, poster (blue box, red left half) drawn at 2x via BBox/Rect.
    3D #2: poster, no model. 3D #3: model, no poster."""
    writer=PdfWriter();page=writer.add_blank_page(300,300)
    def form(body,bbox,matrix=None):
        stream=DecodedStreamObject();stream.set_data(body)
        stream.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),NameObject('/BBox'):numbers(*bbox)})
        if matrix:stream[NameObject('/Matrix')]=numbers(*matrix)
        return writer._add_object(stream)
    def model():
        data=DecodedStreamObject();data.set_data(b'SYNTHETIC U3D fixture, not a renderable model')
        data[NameObject('/Subtype')]=NameObject('/U3D')
        views=ArrayObject(DictionaryObject({NameObject('/Type'):NameObject('/3DView'),NameObject('/XN'):NameObject('/V%d'%i)}) for i in (1,2))
        data[NameObject('/VA')]=views
        return writer._add_object(data)
    def annotation(rect,ap=None,model_ref=None):
        note=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/3D'),
                               NameObject('/Rect'):numbers(*rect),NameObject('/F'):NumberObject(4)})
        if ap is not None:note[NameObject('/AP')]=DictionaryObject({NameObject('/N'):ap})
        if model_ref is not None:note[NameObject('/3DD')]=model_ref
        return writer._add_object(note)
    # BBox 50x25 drawn into a 100x50 rectangle (scale 2): blue box, red left half.
    first=form(b'0 0 1 rg 0 0 50 25 re f 1 0 0 rg 0 0 25 25 re f',[0,0,50,25])
    second=form(b'0 1 0 rg 0 0 10 10 re f',[0,0,10,10])
    page[NameObject('/Annots')]=ArrayObject([annotation([20,200,120,250],first,model()),annotation([20,20,80,80],second),
                                            annotation([150,20,250,80],None,model())])
    with open(path,'wb') as handle:writer.write(handle)


class Poster3DTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which('pdftocairo'):self.skipTest('Poppler pdftocairo required')
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'3d.pdf';poster_pdf(self.source);self.identity=hashlib.sha256(self.source.read_bytes()).hexdigest()

    def request(self,index,name='poster.png',identity=None):
        return dict(index=index,destination=str(self.root/name),source_sha256=identity or self.identity)

    def test_listing_reports_poster_model_and_views_without_a_renderer(self):
        report=inspect_media(self.source,{})
        rows=[(r['kind'],r['poster'],r['model_embedded'],r['views'],r['suffix']) for r in report['assets']]
        self.assertEqual(rows,[('3d',True,True,2,'.u3d'),('3d',True,False,0,'.3d'),('3d',False,True,2,'.u3d')])
        self.assertFalse(report['three_d_renderer_available']);self.assertFalse(report['actions_executed'])

    def test_poster_is_the_annotation_appearance_scaled_to_its_rectangle(self):
        from PIL import Image
        result=render_poster(self.source,self.request(0))
        self.assertEqual(result['schema'],'linuxit-3d-poster-v1');self.assertFalse(result['interactive'])
        self.assertFalse(result['renderer_3d_available']);self.assertEqual(result['model_format'],'u3d');self.assertEqual(result['page'],0)
        image=Image.open(result['path']).convert('RGB');width,height=image.size
        self.assertEqual(result['size'],[width,height]);self.assertAlmostEqual(width/height,2,delta=.05)
        self.assertEqual(image.getpixel((width//4,height//2)),RED);self.assertEqual(image.getpixel((3*width//4,height//2)),BLUE)
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(),self.identity)

    def test_poster_without_model_and_page_rendering_show_the_same_appearance(self):
        from PIL import Image
        result=render_poster(self.source,self.request(1,'green.png'));self.assertIsNone(result['model_format'])
        image=Image.open(result['path']).convert('RGB');self.assertEqual(image.getpixel((image.size[0]//2,image.size[1]//2)),(0,255,0))
        base=self.root/'page'
        subprocess.run(['pdftocairo','-png','-r','72','-singlefile',str(self.source),str(base)],check=True,timeout=60)
        page=Image.open(str(base)+'.png').convert('RGB')
        self.assertEqual(page.getpixel((30,300-225)),RED);self.assertEqual(page.getpixel((100,300-225)),BLUE)
        with self.assertRaisesRegex(ValueError,'não tem modelo incorporado'):
            extract_media(self.source,dict(index=1,destination=str(self.root/'x.3d'),source_sha256=self.identity))

    def test_refusals_publish_nothing(self):
        cases=[(self.request(2,'none.png'),'não tem imagem de apresentação'),(self.request(0,'poster.jpg'),'PNG'),
               (self.request(9,'missing.png'),'não é uma anotação 3D'),(self.request(0,'changed.png','0'*64),'mudou|alterado'),
               (dict(self.request(0,'extra.png'),interactive=True),'inválido')]
        for request,message in cases:
            with self.subTest(message),self.assertRaisesRegex(ValueError,message):render_poster(self.source,request)
            self.assertFalse(Path(request['destination']).exists())
        existing=self.root/'exists.png';existing.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):render_poster(self.source,self.request(0,'exists.png'))
        self.assertEqual(existing.read_bytes(),b'keep')


if __name__=='__main__':unittest.main()
