"""Passive enumeration/extraction of embedded Movie/RichMedia/Sound/3D assets."""
from io import BytesIO
from pathlib import Path
import array,hashlib,sys,tempfile,wave
from types import SimpleNamespace
from pdf_changes import _sha
from pdf_attachments import _document,_catalog_entries
from pypdf.generic import DictionaryObject,NameObject
from local_files import publish_copy

MAX_BYTES=64*1024**2


def _entries(reader):
    count=0
    for page_no,page in enumerate(reader.pages):
        if page_no>=5000:raise ValueError('Inspeção de mídia limitada a5000 páginas.')
        annotations=page.get('/Annots',[]).get_object() if hasattr(page.get('/Annots'),'get_object') else page.get('/Annots',[])
        if len(annotations)>10000:raise ValueError('Página acima de10000 anotações.')
        for reference in annotations:
            annotation=reference.get_object();kind=annotation.get('/Subtype')
            assets=[]
            if kind=='/Movie':
                movie=annotation.get('/Movie')
                if movie is not None:
                    spec=movie.get_object().get('/F')
                    if spec is not None:
                        spec=spec.get_object()
                        if isinstance(spec,DictionaryObject):assets=[(str(spec.get('/UF') or spec.get('/F') or 'movie'),spec,'file')]
            elif kind=='/RichMedia':
                content=annotation.get('/RichMediaContent')
                if content is not None:
                    tree=content.get_object().get('/Assets')
                    if tree is not None:
                        proxy=SimpleNamespace(root_object=DictionaryObject({NameObject('/Names'):DictionaryObject({NameObject('/EmbeddedFiles'):tree})}))
                        assets=[(entry.name,entry.pdf_object,'file') for entry,_,_ in _catalog_entries(proxy)]
            elif kind in ('/Sound','/3D'):
                value=annotation.get('/Sound' if kind=='/Sound' else '/3DD')
                if value is not None:
                    stream=value.get_object()
                    suffix='.wav' if kind=='/Sound' else '.u3d' if stream.get('/Subtype')=='/U3D' else '.prc' if stream.get('/Subtype')=='/PRC' else '.bin'
                    assets=[('som'+suffix if kind=='/Sound' else 'modelo'+suffix,stream,'sound' if kind=='/Sound' else '3d')]
            for name,value,encoding in assets:
                if count>=256:raise ValueError('PDF acima de256 recursos de mídia.')
                stream=value
                if encoding=='file':
                    embedded=value.get('/EF')
                    embedded=embedded.get_object() if embedded is not None else {}
                    stream=embedded.get('/UF') or embedded.get('/F')
                    if stream is None:continue  # External references are never loaded.
                    stream=stream.get_object()
                if not hasattr(stream,'get_data'):continue
                yield count,dict(name=str(name)[:1024],page=page_no,kind=encoding,suffix=Path(str(name)).suffix.lower()[:16]),stream
                count+=1


def _sound(raw,stream):
    rate=stream.get('/R');channels=stream.get('/C',1);bits=stream.get('/B',8);encoding=stream.get('/E','/Raw')
    if type(rate).__name__ not in ('NumberObject','FloatObject','int','float') or float(rate)!=int(rate) or not 8000<=int(rate)<=192000 or channels not in (1,2) or bits not in (8,16) or encoding not in ('/Raw','/Signed','/Unsigned'):
        raise ValueError('Som PDF suportado:PCM8/16bits,1–2canais,8000–192000Hz.')
    width=bits//8
    if not raw or len(raw)%(channels*width):raise ValueError('Quadros PCM incompletos.')
    if bits==8:
        if encoding=='/Signed':raw=bytes((v+128)%256 for v in raw)
    else:
        values=array.array('H');values.frombytes(raw)
        if sys.byteorder=='little':values.byteswap()
        if encoding=='/Unsigned':values=array.array('H',((v+32768)%65536 for v in values))
        if sys.byteorder=='big':values.byteswap()
        raw=values.tobytes()
    output=BytesIO()
    with wave.open(output,'wb') as target:
        target.setnchannels(int(channels));target.setsampwidth(width);target.setframerate(int(rate));target.writeframes(raw)
    return output.getvalue()


def inspect_media(path,request):
    if request!={}:raise ValueError('Pedido de mídia inválido.')
    if Path(path).stat().st_size>MAX_BYTES:raise ValueError('Mídia em PDF limitada a64MiB.')
    with _document(path) as (reader,identity):rows=[dict(index=index,**info) for index,info,stream in _entries(reader)]
    return dict(schema='linuxit-media-assets-v1',source_sha256=identity,assets=rows,network_used=False,actions_executed=False,three_d_renderer_available=False)


def extract_media(path,request):
    if not isinstance(request,dict) or set(request)!={'index','destination','source_sha256'} or type(request['index']) is not int or not 0<=request['index']<256:
        raise ValueError('Pedido de extração de mídia inválido.')
    if Path(path).stat().st_size>MAX_BYTES:raise ValueError('Mídia em PDF limitada a64MiB.')
    destination=Path(request['destination'])
    with _document(path,request['source_sha256'],enforce_copy=True) as (reader,identity):
        selected=next((entry for entry in _entries(reader) if entry[0]==request['index']),None)
        if selected is None:raise ValueError('Recurso de mídia não existe mais.')
        _,info,stream=selected
        if destination.suffix.lower()!=info['suffix']:raise ValueError('Mantenha a extensão declarada do recurso de mídia.')
        raw=stream.get_data()
        if len(raw)>MAX_BYTES:raise ValueError('Recurso de mídia acima de64MiB.')
        if info['kind']=='sound':raw=_sound(raw,stream)
        with tempfile.TemporaryDirectory(prefix='linuxit-media-extract-') as folder:
            staged=Path(folder)/'asset';staged.write_bytes(raw)
            def unchanged():
                if _sha(path)!=identity:raise ValueError('PDF alterado durante a extração de mídia.')
            publish_copy(staged,destination,unchanged)
    return dict(schema='linuxit-media-extracted-v1',path=str(destination),sha256=hashlib.sha256(raw).hexdigest(),kind=info['kind'])
