"""Passive enumeration/extraction of embedded Movie/RichMedia/Sound/3D assets.

3D annotations: the model (U3D/PRC) can be saved, and the annotation's own
normal appearance (its poster image) can be shown as a still picture (E16).
No 3D scene is rendered or made interactive.
"""
from io import BytesIO
from pathlib import Path
import array,hashlib,math,subprocess,sys,tempfile,wave
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
                elif kind=='/3D' and _poster(annotation) is not None:
                    # 3D annotation without an embedded model: still listed for its poster.
                    assets=[('modelo-sem-dados.3d',None,'3d')]
            for name,value,encoding in assets:
                if count>=256:raise ValueError('PDF acima de256 recursos de mídia.')
                stream=value
                if encoding=='file':
                    embedded=value.get('/EF')
                    embedded=embedded.get_object() if embedded is not None else {}
                    stream=embedded.get('/UF') or embedded.get('/F')
                    if stream is None:continue  # External references are never loaded.
                    stream=stream.get_object()
                if stream is not None and not hasattr(stream,'get_data'):continue
                if stream is None and encoding!='3d':continue
                info=dict(name=str(name)[:1024],page=page_no,kind=encoding,suffix=Path(str(name)).suffix.lower()[:16])
                if encoding=='3d':
                    views=annotation.get('/3DD').get_object().get('/VA') if annotation.get('/3DD') is not None else None
                    info.update(poster=_poster(annotation) is not None,model_embedded=stream is not None,
                                views=len(views.get_object()) if views is not None and hasattr(views.get_object(),'__len__') else 0)
                yield count,info,stream,annotation
                count+=1


def _poster(annotation):
    """The annotation's normal appearance (/AP /N) when it is a single form XObject."""
    appearance=annotation.get('/AP')
    appearance=appearance.get_object() if appearance is not None else None
    if not isinstance(appearance,DictionaryObject) or appearance.get('/N') is None:return None
    normal=appearance['/N'].get_object()
    if isinstance(normal,DictionaryObject) and not hasattr(normal,'get_data'):
        state=annotation.get('/AS')
        normal=normal.get(state).get_object() if state is not None and normal.get(state) is not None else None
    return normal if normal is not None and hasattr(normal,'get_data') else None


def _numbers(value,count):
    value=value.get_object() if value is not None else None
    if value is None or len(value)!=count:raise ValueError('Geometria da anotação 3D inválida.')
    numbers=[float(v) for v in value]
    if not all(math.isfinite(v) and abs(v)<=1_000_000 for v in numbers):raise ValueError('Geometria da anotação 3D inválida.')
    return numbers


def render_poster(path,request):
    """E16: the 3D annotation's poster (its own appearance) as a PNG, never an interactive scene."""
    if not isinstance(request,dict) or set(request)!={'index','destination','source_sha256'} or type(request['index']) is not int or not 0<=request['index']<256:
        raise ValueError('Pedido de imagem 3D inválido.')
    if Path(path).stat().st_size>MAX_BYTES:raise ValueError('Mídia em PDF limitada a64MiB.')
    destination=Path(request['destination'])
    if destination.suffix.lower()!='.png':raise ValueError('A imagem de apresentação é salva como PNG.')
    from pypdf import PdfWriter
    from pypdf.generic import ArrayObject,DecodedStreamObject,FloatObject
    with _document(path,request['source_sha256']) as (reader,identity):
        selected=next((entry for entry in _entries(reader) if entry[0]==request['index']),None)
        if selected is None or selected[1]['kind']!='3d':raise ValueError('O recurso escolhido não é uma anotação 3D.')
        annotation=selected[3];poster=_poster(annotation)
        if poster is None:raise ValueError('Esta anotação 3D não tem imagem de apresentação.')
        x0,y0,x1,y1=_numbers(annotation.get('/Rect'),4);x0,x1=sorted((x0,x1));y0,y1=sorted((y0,y1))
        width,height=x1-x0,y1-y0
        if not (1<=width<=14400 and 1<=height<=14400):raise ValueError('Área da anotação 3D inválida.')
        bx0,by0,bx1,by1=_numbers(poster.get('/BBox'),4)
        a,b,c,d,e,f=_numbers(poster.get('/Matrix',ArrayObject([FloatObject(v) for v in (1,0,0,1,0,0)])),6)
        corners=[(a*x+c*y+e,b*x+d*y+f) for x in (bx0,bx1) for y in (by0,by1)]
        tx0,tx1=min(p[0] for p in corners),max(p[0] for p in corners);ty0,ty1=min(p[1] for p in corners),max(p[1] for p in corners)
        if tx1-tx0<=0 or ty1-ty0<=0:raise ValueError('Imagem de apresentação sem área.')
        # Same mapping a viewer uses: the transformed BBox fills the annotation rectangle.
        sx,sy=width/(tx1-tx0),height/(ty1-ty0)
        writer=PdfWriter();page=writer.add_blank_page(width,height)
        form=writer._add_object(poster.clone(writer))
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/XObject'):DictionaryObject({NameObject('/Poster'):form})})
        content=DecodedStreamObject();content.set_data(f'q {sx:.6f} 0 0 {sy:.6f} {-tx0*sx:.6f} {-ty0*sy:.6f} cm /Poster Do Q'.encode('ascii'))
        page[NameObject('/Contents')]=writer._add_object(content)
        model=selected[1]['suffix'].lstrip('.') if selected[1]['model_embedded'] else None
        with tempfile.TemporaryDirectory(prefix='linuxit-3d-poster-') as folder:
            single=Path(folder)/'poster.pdf'
            with single.open('wb') as stream:writer.write(stream)
            scale=1600 if max(width,height)*2>1600 else int(max(width,height)*2)
            prefix=Path(folder)/'poster'
            try:
                result=subprocess.run(['pdftocairo','-png','-singlefile','-scale-to',str(max(scale,64)),str(single),str(prefix)],
                                      stdin=subprocess.DEVNULL,capture_output=True,timeout=120)
            except FileNotFoundError as exc:raise ValueError('A imagem de apresentação requer o Poppler (pdftocairo).') from exc
            image=prefix.with_suffix('.png')
            if result.returncode or not image.is_file():raise ValueError('Falha ao desenhar a imagem de apresentação.')
            from PIL import Image
            with Image.open(image) as picture:size=list(picture.size)
            def unchanged():
                if _sha(path)!=identity:raise ValueError('PDF alterado durante a leitura da imagem 3D.')
            publish_copy(image,destination,unchanged)
    return dict(schema='linuxit-3d-poster-v1',path=str(destination),page=selected[1]['page'],size=size,
                model_format=model,interactive=False,renderer_3d_available=False)


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
    with _document(path) as (reader,identity):rows=[dict(index=index,**info) for index,info,stream,_ in _entries(reader)]
    return dict(schema='linuxit-media-assets-v1',source_sha256=identity,assets=rows,network_used=False,actions_executed=False,three_d_renderer_available=False)


def extract_media(path,request):
    if not isinstance(request,dict) or set(request)!={'index','destination','source_sha256'} or type(request['index']) is not int or not 0<=request['index']<256:
        raise ValueError('Pedido de extração de mídia inválido.')
    if Path(path).stat().st_size>MAX_BYTES:raise ValueError('Mídia em PDF limitada a64MiB.')
    destination=Path(request['destination'])
    with _document(path,request['source_sha256'],enforce_copy=True) as (reader,identity):
        selected=next((entry for entry in _entries(reader) if entry[0]==request['index']),None)
        if selected is None:raise ValueError('Recurso de mídia não existe mais.')
        _,info,stream,_=selected
        if stream is None:raise ValueError('Este recurso 3D não tem modelo incorporado; só a imagem de apresentação existe.')
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
