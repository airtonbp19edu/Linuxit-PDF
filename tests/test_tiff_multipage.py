"""Actual TIFF pages: order, orientation, modes, bounds and worker provenance."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_pdf_creation import creation,Image,PdfReader
from PIL import TiffImagePlugin


def save_tiff(path, frames, **options):
    frames[0].save(path,format='TIFF',save_all=True,append_images=frames[1:],**options)


class MultipageTIFFTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-tiff-')
        self.root=Path(self.temp.name);self.source=self.root/'scan.tiff';self.output=self.root/'new.pdf'
        with Image.new('RGB',(12,8),'red') as first,Image.new('RGB',(6,10),'blue') as second:
            save_tiff(self.source,[first,second])
        self.png=self.root/'third.png'
        with Image.new('RGB',(5,7),'green') as image:image.save(self.png)

    def tearDown(self):self.temp.cleanup()

    def create(self,paths=None,dpi=72):
        return creation.create_pdf_from_images(self.output,{'paths':[str(p) for p in (paths or [self.source])],'dpi':dpi})

    def absent(self):
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.linuxit-images-*')),[])
        self.assertEqual(list(self.root.glob('.linuxit-publish-*')),[])

    def fixture(self,name):
        folder=Path(__file__).resolve().parents[1]/'testes/fixtures/tiff-multipage'
        manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        record=next(item for item in manifest['files'] if item['file']==name)
        data=(folder/name).read_bytes()
        self.assertEqual((len(data),hashlib.sha256(data).hexdigest()),(record['bytes'],record['sha256']))
        self.source.write_bytes(data)
        return record

    def test_file_order_expands_all_tiff_pages_with_dimensions_and_provenance(self):
        original=self.source.read_bytes()
        result=self.create([self.png,self.source],144)
        self.assertEqual((result['input_count'],result['pages']),(2,3))
        self.assertEqual([(s['input'],s['frame'],s['frame_count']) for s in result['sources']],[(1,1,1),(2,1,2),(2,2,2)])
        self.assertEqual([s['pixels'] for s in result['sources']],[[5,7],[12,8],[6,10]])
        reader=PdfReader(self.output,strict=True)
        for page,size,color in zip(reader.pages,((2.5,3.5),(6,4),(3,5)),((0,128,0),(255,0,0),(0,0,255))):
            self.assertEqual((float(page.mediabox.width),float(page.mediabox.height)),size)
            self.assertEqual(page['/Resources']['/XObject']['/Im1'].get_data(),bytes(color)*int(size[0]*size[1]*4))
        self.assertEqual([s['sha256'] for s in result['sources'][1:]],[hashlib.sha256(original).hexdigest()]*2)
        self.assertEqual(self.source.read_bytes(),original)

    def test_each_frame_orientation_is_applied_once_without_leaking_tags(self):
        fixture=self.fixture('orientations.tiff')
        self.create()
        for page,expected in zip(PdfReader(self.output).pages,fixture['expected_pages']):
            self.assertEqual([float(page.mediabox.width),float(page.mediabox.height)],expected['pixels'])
            self.assertEqual(page['/Resources']['/XObject']['/Im1'].get_data(),bytes.fromhex(expected['rgb_hex']))
        self.assertNotIn(b'PRIVATE SCANNER TAG',self.output.read_bytes())

    def test_mixed_grayscale_rgba_and_palette_frames_become_rgb_on_white(self):
        with Image.new('L',(3,2),100) as gray,Image.new('RGBA',(2,3),(255,0,0,128)) as alpha,Image.new('P',(2,2),0) as palette:
            palette.putpalette([0,255,0]+[0]*765)
            save_tiff(self.source,[gray,alpha,palette])
        self.create()
        for page,color,count in zip(PdfReader(self.output).pages,((100,100,100),(255,127,127),(0,255,0)),(6,6,4)):
            image=page['/Resources']['/XObject']['/Im1']
            self.assertEqual(image['/ColorSpace'],'/DeviceRGB')
            self.assertEqual(image.get_data(),bytes(color)*count)

    def test_lzw_and_group4_pages_decode_in_their_original_order(self):
        for compression,mode,colors in [('tiff_lzw','RGB',('red','blue')),('group4','1',(0,1))]:
            with self.subTest(compression=compression):
                with Image.new(mode,(8,6),colors[0]) as first,Image.new(mode,(4,8),colors[1]) as second:
                    expected=[first.convert('RGB').tobytes(),second.convert('RGB').tobytes()]
                    save_tiff(self.source,[first,second],compression=compression)
                self.create()
                self.assertEqual([p['/Resources']['/XObject']['/Im1'].get_data() for p in PdfReader(self.output).pages],expected)
                self.output.unlink()

    def test_bigtiff_and_big_endian_sequences_are_accepted_by_content(self):
        for big,mode in [(True,'RGB'),(False,'I;16B')]:
            with self.subTest(big=big):
                if big:
                    fixture=self.fixture('bigtiff.tiff')
                else:
                    with Image.new(mode,(4,3),1) as first,Image.new(mode,(2,4),2) as second:
                        save_tiff(self.source,[first,second])
                data=self.source.read_bytes()
                self.assertEqual(data[:4],b'II+\x00' if big else b'MM\x00*')
                renamed=self.root/'renamed.jpg';renamed.write_bytes(data)
                result=self.create([renamed])
                self.assertEqual(result['pages'],2)
                self.assertTrue(all(s['format']=='TIFF' for s in result['sources']))
                if big:
                    for page,size,color in zip(PdfReader(self.output).pages,fixture['pixels'],fixture['colors']):
                        self.assertEqual(page['/Resources']['/XObject']['/Im1'].get_data(),bytes(color)*(size[0]*size[1]))
                self.output.unlink()

    def test_aggregate_page_limit_rejects_before_decoding_tiff_pixels(self):
        with patch.object(creation,'MAX_PAGES',2),patch.object(TiffImagePlugin.TiffImageFile,'load',side_effect=AssertionError('must not decode')) as decode:
            with self.assertRaisesRegex(ValueError,'páginas'):self.create([self.png,self.source])
            decode.assert_not_called()
        self.absent()

    def test_later_frame_pixel_budget_and_total_budget_leave_no_output(self):
        with Image.new('RGB',(5,5),'red') as first,Image.new('RGB',(20,20),'blue') as second:save_tiff(self.source,[first,second])
        for key,value in [('MAX_IMAGE_PIXELS',100),('MAX_TOTAL_PIXELS',400)]:
            with self.subTest(key=key),patch.object(creation,key,value),self.assertRaisesRegex(ValueError,'megapixels'):self.create()
            self.absent()

    def test_source_bytes_and_hash_work_are_counted_per_file_not_per_page(self):
        original=creation._sha;calls=[]
        def counted(path):calls.append(Path(path));return original(path)
        with patch.object(creation,'MAX_TOTAL_BYTES',self.source.stat().st_size),patch.object(creation,'_sha',side_effect=counted):
            result=self.create()
        self.assertEqual(result['pages'],2)
        self.assertEqual(calls.count(self.source),2)
        self.assertEqual(calls.count(self.output),1)

    def test_cyclic_out_of_range_and_truncated_ifd_chains_are_not_silently_shortened(self):
        original=self.source.read_bytes()
        first=int.from_bytes(original[4:8],'little')
        count=int.from_bytes(original[first:first+2],'little')
        pointer=first+2+12*count
        cases=[]
        for next_offset in (first,len(original)+1000):
            data=bytearray(original);data[pointer:pointer+4]=next_offset.to_bytes(4,'little');cases.append(data)
        cases.append(original[:pointer+2])
        for data in cases:
            self.source.write_bytes(data)
            with self.assertRaises(ValueError):self.create()
            self.absent()

    def test_truncated_last_frame_aborts_entire_batch(self):
        self.source.write_bytes(self.source.read_bytes()[:-10])
        with self.assertRaises(ValueError):self.create([self.png,self.source])
        self.absent()

    def test_invalid_bigtiff_header_and_huge_directory_counts_are_bounded(self):
        for data in (b'II+\x00\x04\x00\x00\x00'+bytes(8),b'II+\x00\x08\x00\x01\x00'+bytes(8),
                     b'MM\x00+\x00\x08\x00\x00'+(16).to_bytes(8,'big')+(2**63).to_bytes(8,'big')):
            with self.subTest(data=data),self.assertRaises(ValueError):creation._tiff_page_count(data,100)
        raw=bytearray(self.source.read_bytes());first=int.from_bytes(raw[4:8],'little');raw[first:first+2]=b'\xff\xff'
        with self.assertRaises(ValueError):creation._tiff_page_count(raw,100)

    def test_changed_tiff_and_concurrent_destination_are_preserved(self):
        original=creation._sha
        with patch.object(creation,'_sha',return_value='0'*64),self.assertRaisesRegex(ValueError,'mudou'):self.create()
        self.absent()
        def race(path):
            if Path(path)==self.source:self.output.write_bytes(b'other writer')
            return original(path)
        with patch.object(creation,'_sha',side_effect=race),self.assertRaises(FileExistsError):self.create()
        self.assertEqual(self.output.read_bytes(),b'other writer')

    def test_real_worker_reports_input_count_frame_mapping_and_page_count(self):
        result=creation.invoke_image_creation(self.output,{'paths':[str(self.source),str(self.png)],'dpi':150})
        self.assertEqual((result['input_count'],result['pages']),(2,3))
        self.assertEqual([s['frame'] for s in result['sources']],[1,2,1])
        self.assertEqual(len(PdfReader(self.output).pages),3)

    def test_worker_replies_with_missing_reordered_or_forged_frames_are_rejected(self):
        result=self.create();request={'paths':[str(self.source)],'dpi':72}
        variants=[]
        for key,value in [('pages',True),('input_count',2),('sources',result['sources'][:1])]:
            bad=deepcopy(result);bad[key]=value;variants.append(bad)
        for key,value in [('frame',1),('input',2),('frame_count',1),('sha256','0'*64),('pixels',[2,2]),('page_points',[float('nan'),8])]:
            bad=deepcopy(result);bad['sources'][1][key]=value;variants.append(bad)
        for bad in variants:
            with self.subTest(bad=bad),patch.object(creation,'run_search_worker',return_value=bad),self.assertRaises(RuntimeError):
                creation.invoke_image_creation(self.output,request)
