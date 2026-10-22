"""Own vector polygon/polyline/caret and shaped text annotation appearances."""
import base64,io,math
from pdf_annotations import _coordinates,_numbers,_command,MIN_SPAN
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from pypdf.generic import ArrayObject,BooleanObject,DecodedStreamObject,DictionaryObject,FloatObject,NameObject,NumberObject,TextStringObject
from measurement import points,measure

EXTRA_KINDS={'add-polygon','add-polyline','add-caret','add-freetext','add-stamp'}
RESIZABLE=('/Square','/Circle','/FreeText','/Redact')


def _require(condition,message):
    if not condition:raise ValueError(message)


def _text_appearance(writer,text,width,height,stamp):
    """Shaped Unicode text with embedded fonts, laid out by the worker for a width x height box."""
    _require(isinstance(text,str) and text.strip() and len(text)<=4096,'Texto deve ter de 1 a 4096 caracteres.')
    from search_tasks import run_search_worker
    from cancel_state import get_event
    payload=run_search_worker('annotation-appearance','appearance',dict(text=text,width=width,height=height,stamp=stamp),get_event(),timeout=120)
    if payload is None:raise ValueError('Preparação da anotação cancelada.')
    raw=base64.b64decode(payload['pdf'],validate=True)
    _require(len(raw)<=4*1024**2,'Aparência acima de 4MiB.')
    document=PdfReader(io.BytesIO(raw));page=document.pages[0]
    appearance=DecodedStreamObject();appearance.set_data(page.get_contents().get_data())
    return appearance,page['/Resources'].clone(writer)


def resize_annotation(writer,note,rect):
    """E13: new /Rect for Square, Circle or FreeText with a regenerated, coherent appearance."""
    from annotation_style import current_style,restyle_annotation
    subtype=note.get('/Subtype')
    _require(subtype in RESIZABLE,'Só retângulos, elipses, texto livre e marcas de redação podem ser redimensionados.')
    x0,y0,x1,y1=map(float,rect)
    _require(min(x1-x0,y1-y0)>=MIN_SPAN,'A nova área deve ter ao menos 0,25 ponto de lado.')
    note[NameObject('/Rect')]=_numbers([x0,y0,x1,y1])
    note.pop('/RD',None)  # Inner margins referred to the old rectangle.
    if subtype=='/FreeText':
        appearance,resources=_text_appearance(writer,str(note.get('/Contents','')),x1-x0,y1-y0,False)
        appearance.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),
            NameObject('/FormType'):NumberObject(1),NameObject('/BBox'):_numbers([0,0,x1-x0,y1-y0]),NameObject('/Resources'):resources})
        note[NameObject('/AP')]=DictionaryObject({NameObject('/N'):writer._add_object(appearance)})
        return note
    if subtype=='/Redact':
        from annotation_style import set_quad_to_rect
        set_quad_to_rect(note)
    color,opacity=current_style(note)
    # Without /C viewers draw the border black; keep that look explicitly.
    return restyle_annotation(writer,note,color or [0.0,0.0,0.0],max(opacity,0.1))


def create_extra_annotation(writer,cropbox,operation):
    kind=operation['kind'];left,bottom,right,top=_coordinates(cropbox)
    text=operation['text']
    _require(isinstance(text,str) and len(text.encode('utf-8'))<=65536,'Comentário inválido.')
    if kind in ('add-polygon','add-polyline'):
        vertices=points(operation['points'],3 if kind=='add-polygon' else 2)
        if kind=='add-polygon':measure(vertices,'area')
        _require(all(left<=x<=right and bottom<=y<=top for x,y in vertices),'Vértice fora do CropBox.')
        x0=max(left,min(x for x,y in vertices)-.625);y0=max(bottom,min(y for x,y in vertices)-.625)
        x1=min(right,max(x for x,y in vertices)+.625);y1=min(top,max(y for x,y in vertices)+.625)
        _require(x1-x0>=MIN_SPAN and y1-y0>=MIN_SPAN,'Geometria pequena demais.')
        path=[_command([vertices[0][0]-x0,vertices[0][1]-y0],'m')]
        path.extend(_command([x-x0,y-y0],'l') for x,y in vertices[1:])
        if kind=='add-polygon':path.append('h')
        subtype='/Polygon' if kind=='add-polygon' else '/PolyLine'
    else:
        x0,y0,x1,y1=_coordinates(operation['rect'])
        _require(left<=x0<x1<=right and bottom<=y0<y1<=top and min(x1-x0,y1-y0)>=MIN_SPAN,'Área inválida ou fora do CropBox.')
        subtype={'add-caret':'/Caret','add-freetext':'/FreeText','add-stamp':'/Stamp'}[kind]
        w,h=x1-x0,y1-y0
        path=[_command([w*.1,h*.1],'m'),_command([w*.5,h*.9],'l'),_command([w*.9,h*.1],'l')]
    note=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject(subtype),
        NameObject('/Rect'):_numbers([x0,y0,x1,y1]),NameObject('/Contents'):TextStringObject(text),
        NameObject('/F'):NumberObject(4),NameObject('/C'):_numbers([.85,.1,.1])})
    appearance=DecodedStreamObject()
    if kind in ('add-freetext','add-stamp'):
        appearance,resources=_text_appearance(writer,text,x1-x0,y1-y0,kind=='add-stamp')
        if kind=='add-freetext':note[NameObject('/DA')]=TextStringObject('/Helv 12 Tf 0.85 0.1 0.1 rg')
        else:note[NameObject('/Name')]=NameObject('/LinuxitCustom')
    else:
        appearance.set_data(('q\n0.85 0.1 0.1 RG\n1.25 w\n1 J\n1 j\n'+'\n'.join(path)+'\nS\nQ\n').encode())
        resources=DictionaryObject()
    appearance.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),
        NameObject('/FormType'):NumberObject(1),NameObject('/BBox'):_numbers([0,0,x1-x0,y1-y0]),NameObject('/Resources'):resources})
    note[NameObject('/AP')]=DictionaryObject({NameObject('/N'):writer._add_object(appearance)})
    if kind in ('add-polygon','add-polyline'):note[NameObject('/Vertices')]=_numbers([v for p in vertices for v in p])
    if kind=='add-caret':note[NameObject('/Sy')]=NameObject('/P')
    return note


def move_annotation(page,note,dx,dy):
    _require(all(type(v) in (int,float) and math.isfinite(v) for v in (dx,dy)),'Deslocamento inválido.')
    rect=_coordinates(list(map(float,note['/Rect'])));shifted=[rect[0]+dx,rect[1]+dy,rect[2]+dx,rect[3]+dy]
    left,bottom,right,top=map(float,page.cropbox)
    _require(left<=shifted[0]<shifted[2]<=right and bottom<=shifted[1]<shifted[3]<=top,'Anotação deslocada para fora do CropBox.')
    for name in ('/Vertices','/QuadPoints','/L'):
        if name in note:
            values=list(note[name]);_require(len(values)%2==0 and len(values)<=8192,'Coordenadas da anotação inválidas.')
            _require(all(math.isfinite(float(v)) and abs(float(v))<=10000000 for v in values),'Coordenadas da anotação inválidas.')
            note[NameObject(name)]=_numbers([float(v)+(dx if i%2==0 else dy) for i,v in enumerate(values)])
    if '/InkList' in note:
        _require(len(note['/InkList'])<=32 and sum(len(p) for p in note['/InkList'])<=8192 and all(len(p)%2==0 and all(math.isfinite(float(v)) for v in p) for p in note['/InkList']),'Traços de anotação inválidos.')
        note[NameObject('/InkList')]=ArrayObject(_numbers([float(v)+(dx if i%2==0 else dy) for i,v in enumerate(path)]) for path in note['/InkList'])
    note[NameObject('/Rect')]=_numbers(shifted)


def conversation_members(document,page,index):
    from annotation_editing import conversation_members as validated_members
    return validated_members(document,page,index)
