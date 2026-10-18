"""Generate own tiny TIFF fixtures in a new directory; never run during tests."""
import argparse
import hashlib
import json
from pathlib import Path

import PIL
from PIL import Image


def generate(destination):
    destination.mkdir(parents=True,exist_ok=False)
    records=[]
    path=destination/'bigtiff.tiff'
    with Image.new('RGB',(4,3),'red') as first,Image.new('RGB',(2,4),'blue') as second:
        first.save(path,format='TIFF',save_all=True,append_images=[second],big_tiff=True)
    if path.read_bytes()[:4]!=b'II+\x00':
        raise RuntimeError('The fixture generator requires a working multi-page BigTIFF writer.')
    records.append({'file':path.name,'pages':2,'pixels':[[4,3],[2,4]],'colors':[[255,0,0],[0,0,255]]})
    path=destination/'orientations.tiff'
    expected=[]
    with Image.new('RGB',(2,3),'white') as first,Image.new('RGB',(4,5),'white') as second:
        for image,transpose in ((first,Image.Transpose.ROTATE_270),(second,Image.Transpose.ROTATE_180)):
            image.putpixel((0,0),(255,0,0));image.putpixel((image.width-1,image.height-1),(0,0,255))
            with image.transpose(transpose) as oriented:
                expected.append({'pixels':list(oriented.size),'rgb_hex':oriented.tobytes().hex()})
        first.save(path,format='TIFF',save_all=True,append_images=[second],tiffinfo={274:1,270:'PRIVATE SCANNER TAG'})
    # Change only the existing inline SHORT Orientation values. Pixel/strip
    # data and directory offsets remain those written by Pillow.
    data=bytearray(path.read_bytes());assert data[:4]==b'II*\x00'
    offset=int.from_bytes(data[4:8],'little')
    for orientation in (6,3):
        count=int.from_bytes(data[offset:offset+2],'little');found=False
        for number in range(count):
            entry=offset+2+number*12
            if int.from_bytes(data[entry:entry+2],'little')==274:
                assert int.from_bytes(data[entry+2:entry+4],'little')==3
                assert int.from_bytes(data[entry+4:entry+8],'little')==1
                data[entry+8:entry+10]=orientation.to_bytes(2,'little');found=True
        assert found
        offset=int.from_bytes(data[offset+2+count*12:offset+6+count*12],'little')
    assert offset==0
    path.write_bytes(data)
    records.append({'file':path.name,'pages':2,'orientation_tags':[6,3],'expected_pages':expected})
    for record in records:
        data=(destination/record['file']).read_bytes()
        record.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    manifest={'schema':'linuxit-own-tiff-fixtures-v1','provenance':'Own solid colors/corner patterns, no external documents or Foxit assets.',
              'generator':'scripts/generate_tiff_fixtures.py','pillow_version':PIL.__version__,
              'reason':'Pin inputs independently of Pillow11.1 multipage BigTIFF writer failure; tests only read fixtures.','files':records}
    (destination/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(manifest))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    generate(parser.parse_args().output)
