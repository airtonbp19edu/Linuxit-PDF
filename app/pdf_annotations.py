"""Bounded, font-free annotation appearances authored by Linuxit PDF."""
import math

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,
                           FloatObject, NameObject, NumberObject, TextStringObject)

AREA_KINDS = {'add-underline': '/Underline', 'add-strikeout': '/StrikeOut',
              'add-squiggly': '/Squiggly', 'add-ellipse': '/Circle'}
ANNOTATION_KINDS = frozenset(AREA_KINDS) | {'add-line'}
MAX_COORDINATE = 10_000_000
MIN_SPAN = .25
MAX_TEXT_BYTES = 64 * 1024


def _require(value, message):
    if not value:
        raise ValueError(message)


def _coordinates(value):
    _require(isinstance(value, list) and len(value) == 4
             and all(type(v) in (int, float) and math.isfinite(v)
                     and abs(v) <= MAX_COORDINATE for v in value),
             'Coordenadas inválidas ou acima do limite de 10 milhões de pontos.')
    return list(map(float, value))


def _numbers(values):
    return ArrayObject(FloatObject(v) for v in values)


def _command(values, operator):
    # PDF numbers cannot use exponent notation. The minimum span keeps this
    # six-decimal representation well above the rounding threshold.
    return ' '.join(f'{v:.6f}' for v in values) + ' ' + operator


def create_annotation(kind, cropbox, geometry, text):
    """Create one red area mark or line; coordinates precede page rotation.

    Areas are [left,bottom,right,top]; lines are [x1,y1,x2,y2] in either
    direction, including horizontal/vertical. No text selection is inferred.
    """
    _require(isinstance(kind, str) and kind in ANNOTATION_KINDS, 'Tipo de anotação não suportado.')
    _require(isinstance(text, str) and len(text.encode('utf-8')) <= MAX_TEXT_BYTES,
             'Comentário inválido ou acima do limite de 64 KiB.')
    left, bottom, right, top = _coordinates(cropbox)
    _require(right-left >= MIN_SPAN and top-bottom >= MIN_SPAN, 'CropBox inválido ou pequeno demais para anotação.')
    a, b, c, d = _coordinates(geometry)
    _require(left <= a <= right and left <= c <= right
             and bottom <= b <= top and bottom <= d <= top,
             'A anotação deve ficar dentro do CropBox, em coordenadas PDF.')
    if kind == 'add-line':
        _require(math.hypot(c-a, d-b) >= MIN_SPAN,
                 'A linha deve medir ao menos 0,25 ponto.')
        stroke = min(1.25, (right-left)/8, (top-bottom)/8)
        rect = [max(left, min(a,c)-stroke/2), max(bottom, min(b,d)-stroke/2),
                min(right, max(a,c)+stroke/2), min(top, max(b,d)+stroke/2)]
        x0, y0, x1, y1 = rect
        path = [_command([a-x0,b-y0], 'm'), _command([c-x0,d-y0], 'l')]
        subtype = '/Line'
    else:
        _require(c-a >= MIN_SPAN and d-b >= MIN_SPAN,
                 'A área deve ter largura e altura de ao menos 0,25 ponto.')
        rect = [a,b,c,d];x0,y0,x1,y1 = rect
        width, height = x1-x0, y1-y0
        stroke = min(1.25, width/8, height/8);pad = stroke/2
        if kind in ('add-underline','add-strikeout'):
            y = pad if kind == 'add-underline' else height/2
            path = [_command([pad,y], 'm'), _command([width-pad,y], 'l')]
        elif kind == 'add-squiggly':
            amplitude = min(1.5, (height-stroke)/3)
            baseline = pad+amplitude
            segments = 4 * max(1, min(128, math.ceil(width/6)))
            path = [_command([pad,baseline], 'm')]
            for i in range(1,segments+1):
                y = baseline + (amplitude if i % 4 == 1 else -amplitude if i % 4 == 3 else 0)
                path.append(_command([pad+(width-stroke)*i/segments,y], 'l'))
        else:
            cx,cy = width/2,height/2;rx,ry = cx-pad,cy-pad;k = .5522847498307936
            path = [_command([cx+rx,cy], 'm'),
                    _command([cx+rx,cy+k*ry,cx+k*rx,cy+ry,cx,cy+ry], 'c'),
                    _command([cx-k*rx,cy+ry,cx-rx,cy+k*ry,cx-rx,cy], 'c'),
                    _command([cx-rx,cy-k*ry,cx-k*rx,cy-ry,cx,cy-ry], 'c'),
                    _command([cx+k*rx,cy-ry,cx+rx,cy-k*ry,cx+rx,cy], 'c'), 'h']
        subtype = AREA_KINDS[kind]
    appearance = DecodedStreamObject()
    appearance.set_data(('q\n1 0 0 RG\n'+_command([stroke], 'w')+'\n1 J\n1 j\n'
                         +'\n'.join(path)+'\nS\nQ\n').encode('ascii'))
    appearance.update({NameObject('/Type'):NameObject('/XObject'), NameObject('/Subtype'):NameObject('/Form'),
                       NameObject('/FormType'):NumberObject(1), NameObject('/BBox'):_numbers([0,0,x1-x0,y1-y0]),
                       NameObject('/Resources'):DictionaryObject()})
    note = DictionaryObject({NameObject('/Type'):NameObject('/Annot'), NameObject('/Subtype'):NameObject(subtype),
        NameObject('/Rect'):_numbers(rect), NameObject('/Contents'):TextStringObject(text),
        NameObject('/F'):NumberObject(4), NameObject('/C'):_numbers([1,0,0]),
        NameObject('/BS'):DictionaryObject({NameObject('/W'):FloatObject(stroke), NameObject('/S'):NameObject('/S')}),
        NameObject('/AP'):DictionaryObject({NameObject('/N'):appearance})})
    if kind == 'add-line':
        note[NameObject('/L')] = _numbers([a,b,c,d])
        note[NameObject('/LE')] = ArrayObject([NameObject('/None'),NameObject('/None')])
    elif kind != 'add-ellipse':
        # ISO 32000-1 table179: counterclockwise vertices; first edge is the
        # bottom of the horizontal text area. The explicit /AP is authoritative.
        note[NameObject('/QuadPoints')] = _numbers([a,b,c,b,c,d,a,d])
    return note
