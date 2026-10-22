import os,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_ocr import preprocess_image,validate_request

class OCRCleanupTests(unittest.TestCase):
    def test_contrast_and_otsu_are_explicit_geometry_preserving_options(self):
        with tempfile.TemporaryDirectory() as folder:
            image=Image.new('RGB',(100,100),(210,210,210))
            for x in range(20,70):
                for y in range(30,70):image.putpixel((x,y),(150,150,150))
            for mode in ('contrast','threshold'):
                path=Path(folder)/(mode+'.png');image.save(path);preprocess_image(path,mode)
                with Image.open(path) as result:
                    self.assertEqual(result.size,(100,100));self.assertEqual(result.getextrema(),(0,255))
                    if mode=='threshold':self.assertEqual(set(result.getdata()),{0,255})

    def test_unknown_cleanup_is_refused(self):
        with self.assertRaises(ValueError):validate_request(dict(source_sha256='0'*64,language='por',dpi=300,preprocess='execute'))
