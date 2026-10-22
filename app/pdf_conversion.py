"""Export local PDF to text, image ZIP or multipage TIFF, atomically."""
from io import BytesIO
import hashlib,json,math
from pathlib import Path
import tempfile,zipfile
from PIL import Image
from local_files import publish_copy
from pdf_dependency import configure_pdf_library
from pdf_ocr import _run
configure_pdf_library()
from pypdf import PdfReader

FORMATS={'text':'.txt','png':'.zip','jpeg':'.zip','tiff':'.tiff'}

def convert_copy(source,destination,request):
    if (not isinstance(request,dict) or set(request)!={'source_sha256','format','dpi'}
        or request['format'] not in FORMATS or type(request['dpi']) is not int or request['dpi'] not in (72,150,300)):
        raise ValueError('Pedido de conversão inválido.')
    source=Path(source).resolve();destination=Path(destination)
    if destination.exists() or destination.is_symlink():raise FileExistsError('Escolha um destino novo.')
    if destination.suffix.lower()!=FORMATS[request['format']] or not destination.parent.is_dir():raise ValueError('Extensão ou pasta de destino inválida.')
    if not source.is_file() or not 0<source.stat().st_size<=128*1024**2:raise ValueError('Selecione PDF de até128MiB.')
    data=source.read_bytes()
    if not 0<len(data)<=128*1024**2 or hashlib.sha256(data).hexdigest()!=request['source_sha256']:raise ValueError('PDF mudou ou excede128MiB.')
    reader=PdfReader(BytesIO(data),strict=True)
    if reader.is_encrypted:raise ValueError('Exporte uma cópia sem senha antes de converter.')
    if not 1<=len(reader.pages)<=100:raise ValueError('Conversão aceita1–100 páginas.')
    with tempfile.TemporaryDirectory(prefix='linuxit-convert-') as folder:
        work=Path(folder);pinned=work/'source.pdf';pinned.write_bytes(data);output=work/destination.name
        if request['format']=='text':
            _run(['pdftotext','-layout','-enc','UTF-8',str(pinned),str(output)])
            if not output.exists() or output.stat().st_size>32*1024**2:raise ValueError('Texto exportado ausente ou acima de32MiB.')
            output.read_text(encoding='utf-8')
        else:
            if len(reader.pages)>20:raise ValueError('Exportação de imagens aceita até20 páginas.')
            total=0;images=[];manifest=[]
            for index,page in enumerate(reader.pages,1):
                box=page.cropbox;width,height=float(box.width),float(box.height)
                if int(page.rotation)%180:width,height=height,width
                pixels=math.ceil(width*request['dpi']/72)*math.ceil(height*request['dpi']/72)
                total+=pixels
                if not 0<pixels<=45_000_000 or total>150_000_000:raise ValueError('Imagens excedem o orçamento de pixels; reduza DPI.')
                prefix=work/f'page-{index:03d}';jpeg=request['format']=='jpeg';image=prefix.with_suffix('.jpg' if jpeg else '.png')
                _run(['pdftocairo','-f',str(index),'-l',str(index),'-singlefile','-cropbox',
                      '-jpeg' if jpeg else '-png','-r',str(request['dpi']),str(pinned),str(prefix)])
                with Image.open(image) as decoded:
                    if decoded.width*decoded.height>45_000_000:raise ValueError('Imagem gerada acima do limite.')
                    if request['format']=='tiff':images.append(decoded.convert('RGB'))
                manifest.append({'page':index,'file':image.name,'sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
            if request['format']=='tiff':
                try:images[0].save(output,'TIFF',save_all=True,append_images=images[1:],compression='tiff_deflate',dpi=(request['dpi'],request['dpi']))
                finally:
                    for image in images:image.close()
            else:
                with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
                    for item in manifest:archive.write(work/item['file'],item['file'])
                    archive.writestr('manifest.json',json.dumps({'source_sha256':request['source_sha256'],'dpi':request['dpi'],'pages':manifest}))
        if output.stat().st_size>256*1024**2:raise ValueError('Conversão acima de256MiB.')
        def unchanged():
            if hashlib.sha256(source.read_bytes()).hexdigest()!=request['source_sha256']:raise ValueError('PDF mudou durante a conversão.')
        digest=hashlib.sha256(output.read_bytes()).hexdigest();publish_copy(output,destination,unchanged)
    return {'schema':'linuxit-conversion-copy-v1','path':str(destination.resolve()),'source_sha256':request['source_sha256'],
            'output_sha256':digest,'format':request['format'],'pages':len(reader.pages)}
