"""Opt-in offline OCR of one-frame attachment images; never execute objects."""
from io import BytesIO
import os,shutil,subprocess,tempfile
from pathlib import Path

IMAGE_SUFFIXES={'.png','.jpg','.jpeg','.bmp','.tif','.tiff','.webp','.gif'}


def image_text(payload,timeout=30):
    from PIL import Image,ImageOps
    if not isinstance(payload,bytes) or len(payload)>2*1024**2:raise ValueError('Imagem anexa acima de 2MiB.')
    if timeout<1:raise ValueError('Orçamento de tempo do OCR em anexos esgotado.')
    with Image.open(BytesIO(payload)) as source:
        if not 0<source.width*source.height<=10_000_000:raise ValueError('OCR de anexo limitado a 10MP.')
        try:source.seek(1)
        except EOFError:pass
        else:raise ValueError('OCR de anexos aceita uma imagem/quadro; converta o documento multipágina antes.')
        source.seek(0)
        with ImageOps.exif_transpose(source).convert('RGBA') as image:
            background=Image.new('RGB',image.size,'white');background.paste(image,mask=image.getchannel('A'))
            try:
                with tempfile.TemporaryDirectory(prefix='linuxit-attachment-ocr-') as directory,tempfile.TemporaryFile() as output:
                    target=Path(directory)/'image.png';background.save(target,'PNG')
                    command=['tesseract',str(target),'stdout','-l','por+eng','--psm','3']
                    if os.name!='nt' and shutil.which('prlimit'):command=['prlimit','--as=1073741824','--cpu=35','--fsize=4194304','--',*command]
                    try:result=subprocess.run(command,stdout=output,stderr=subprocess.PIPE,timeout=min(30,timeout),env={**os.environ,'OMP_THREAD_LIMIT':'1'})
                    except subprocess.TimeoutExpired as exc:raise ValueError('OCR da imagem excedeu o tempo disponível.') from exc
                    if result.returncode:raise ValueError('Não foi possível reconhecer a imagem com OCR local português/inglês.')
                    output.seek(0);raw=output.read(2*1024**2+1)
                    if len(raw)>2*1024**2:raise ValueError('Texto OCR acima de 2MiB.')
                    return raw.decode('utf-8',errors='strict').strip()
            finally:background.close()
