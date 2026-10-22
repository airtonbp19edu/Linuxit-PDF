"""Conservative content-stream redaction without rasterization.

Admitted pages use standard fonts and simple paths/images. Text objects and
painted objects are indivisible: an intersecting object is removed completely.
Unsupported rendering constructs are rejected, never covered with an overlay.
"""
import math
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import (ArrayObject, ContentStream, DecodedStreamObject,
                          DictionaryObject, FloatObject, NameObject)

IDENTITY = (1., 0., 0., 1., 0., 0.)
STANDARD = {'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
            'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
            'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic', 'Symbol', 'ZapfDingbats'}
PAINT = {b'S', b's', b'f', b'F', b'f*', b'B', b'B*', b'b', b'b*', b'n'}
PATH = {b'm', b'l', b'c', b'v', b'y', b'h', b're'}
SAFE = {b'RG', b'rg', b'G', b'g', b'K', b'k', b'J', b'j', b'd', b'ri', b'i'}
TEXT_STATE = {b'Tf', b'Tc', b'Tw', b'Tz', b'TL', b'Tr', b'Ts'}
SHOW = {b'Tj', b'TJ', b"'", b'"'}


def require(ok, message='Conteúdo não suportado pela redação vetorial; use o modo rasterizado.'):
    if not ok:
        raise ValueError(message)


def numbers(values):
    result = [float(v) for v in values]
    require(all(math.isfinite(v) and abs(v) <= 1_000_000 for v in result))
    return result


def point(matrix, x, y):
    a, b, c, d, e, f = matrix
    result = a*x+c*y+e, b*x+d*y+f
    require(all(math.isfinite(value) for value in result),
            'Transformação gráfica excede o limite numérico da redação vetorial.')
    return result


def compose(a, b):
    # apply b first, then a
    x, y = point(a, b[4], b[5])
    result = (a[0]*b[0]+a[2]*b[1], a[1]*b[0]+a[3]*b[1],
              a[0]*b[2]+a[2]*b[3], a[1]*b[2]+a[3]*b[3], x, y)
    require(all(math.isfinite(value) for value in result),
            'Transformação gráfica excede o limite numérico da redação vetorial.')
    return result


def bbox(points, padding=0):
    require(math.isfinite(padding) and padding >= 0 and
            all(math.isfinite(value) for pair in points for value in pair),
            'Geometria derivada inválida para redação vetorial.')
    xs, ys = zip(*points)
    return min(xs)-padding, min(ys)-padding, max(xs)+padding, max(ys)+padding


def intersects(rect, areas):
    return any(rect[0] <= a[2] and rect[2] >= a[0] and rect[1] <= a[3] and rect[3] >= a[1] for a in areas)


def _font(resources, name):
    fonts = resources.get('/Font', {})
    fonts = fonts.get_object() if hasattr(fonts, 'get_object') else fonts
    require(name in fonts)
    font = fonts[name].get_object()
    require(font.get('/Subtype') == '/Type1' and str(font.get('/BaseFont', ''))[1:] in STANDARD,
            'O modo vetorial aceita fontes padrão Type1; este PDF requer o modo rasterizado.')
    require(not any(k in font for k in ('/FontDescriptor', '/Widths', '/CharProcs', '/ToUnicode')))
    require(font.get('/Encoding') in (None, '/WinAnsiEncoding', '/MacRomanEncoding', '/StandardEncoding'))


def redact_page(writer, page, marks):
    """Mutate only the writer page, return counts; source reader remains untouched."""
    areas = [area for _, boxes, _ in marks for area in boxes]
    resources = page.get('/Resources', {})
    resources = resources.get_object() if hasattr(resources, 'get_object') else resources
    require(isinstance(resources, dict))
    stream = page.get_contents()
    operations = list(stream.operations) if stream is not None else []
    require(len(operations) <= 200_000, 'Página excede o limite de operações vetoriais.')
    ctm, width, miter, stack = IDENTITY, 1., 10., []
    path, path_ops, output, used_images = [], [], [], set()
    text = None
    state = {'size': 12., 'font': None, 'Tc': 0., 'Tw': 0., 'Tz': 100., 'TL': 0., 'Ts': 0., 'Tr': 0.}
    removed_text = removed_paths = removed_images = 0
    for args, op in operations:
        if text is not None:
            if op == b'ET':
                if text['hit']:
                    removed_text += 1
                    for a, code in text['ops']:
                        if code == b'"':
                            output.extend([([a[0]], b'Tw'), ([a[1]], b'Tc')])
                        elif code not in SHOW:
                            output.append((a, code))
                else:
                    output.extend(text['ops'])
                output.append((args, op)); text = None; continue
            require(op in TEXT_STATE | SHOW | {b'Tm', b'Td', b'TD', b'T*'})
            text['ops'].append((args, op))
            if op == b'Tf':
                require(len(args) == 2);_font(resources, args[0])
                state['font'], state['size'] = args[0], abs(numbers(args[1:])[0])
                require(0 < state['size'] <= 10000)
            elif op in TEXT_STATE:
                require(len(args) == 1); state[op.decode()] = numbers(args)[0]
                if op == b'Tr':require(state['Tr'] in (0, 3),
                    'Texto com contorno ou usado como recorte requer redação rasterizada.')
            elif op == b'Tm':
                require(len(args) == 6);text['line'] = tuple(numbers(args));text['advance'] = 0.
            elif op in (b'Td', b'TD', b'T*', b"'", b'"'):
                if op in (b'Td', b'TD'):
                    require(len(args) == 2);dx, dy = numbers(args)
                    if op == b'TD': state['TL'] = -dy
                else:
                    dx, dy = 0., -state['TL']
                    if op == b'"':
                        require(len(args) == 3);state['Tw'], state['Tc'] = numbers(args[:2])
                text['line'] = compose(text['line'], (1,0,0,1,dx,dy));text['advance'] = 0.
            if op in SHOW:
                require(state['font'] is not None)
                values = args[0] if op == b'TJ' else [args[-1]]
                require(isinstance(values, (list, ArrayObject)))
                count, offsets = 0, 0.
                for value in values:
                    if isinstance(value, (str, bytes)):
                        count += len(value.original_bytes) if hasattr(value, 'original_bytes') else len(value)
                    else:
                        offsets += abs(numbers([value])[0])*state['size']/1000
                require(count <= 1_000_000)
                # Bounding interval, deliberately wider than all Standard14 glyphs.
                # No guessed exact widths: this also covers accumulated positioning.
                expansion = (count*(3*state['size']+abs(state['Tc'])+abs(state['Tw']))+offsets)*abs(state['Tz'])/100
                previous = text['advance']; text['advance'] += expansion
                radius = text['advance'] + 3*state['size']*max(1,abs(state['Tz'])/100)
                transform = compose(ctm, text['line'])
                bounds = bbox([point(transform,x,y) for x in (-radius,radius)
                               for y in (state['Ts']-3*state['size'],state['Ts']+3*state['size'])])
                text['hit'] |= intersects(bounds, areas)
            continue
        if op == b'BT':
            require(not path_ops);text={'ops':[(args,op)], 'hit':False, 'line':IDENTITY, 'advance':0.};continue
        if op == b'q':
            require(not path_ops); stack.append((ctm,width,miter,dict(state))); require(len(stack) <= 64)
        elif op == b'Q':
            require(not path_ops and stack); ctm,width,miter,state=stack.pop()
        elif op == b'cm':
            require(not path_ops and len(args)==6);ctm=compose(ctm,tuple(numbers(args)))
        elif op in (b'w', b'M'):
            require(len(args)==1);value=numbers(args)[0];require(value>=0)
            if op==b'w':width=value
            else:miter=max(1,value)
        elif op in PATH:
            path_ops.append((args,op));values=numbers(args)
            if op == b're':
                require(len(values)==4);x,y,w,h=values;path.extend(point(ctm,a,b) for a,b in ((x,y),(x+w,y),(x,y+h),(x+w,y+h)))
            elif op != b'h':
                require(len(values)%2==0);path.extend(point(ctm,values[i],values[i+1]) for i in range(0,len(values),2))
            continue
        elif op in PAINT:
            require(path or op==b'n')
            padding=width*miter*(abs(ctm[0])+abs(ctm[1])+abs(ctm[2])+abs(ctm[3]))
            if op!=b'n' and path and intersects(bbox(path,padding),areas):removed_paths+=1
            else:output.extend(path_ops);output.append((args,op))
            path=[];path_ops=[];continue
        elif op == b'Do':
            require(not path_ops and len(args)==1)
            objects=resources.get('/XObject',{});objects=objects.get_object() if hasattr(objects,'get_object') else objects
            require(args[0] in objects);image=objects[args[0]].get_object()
            require(image.get('/Subtype')=='/Image', 'Form XObject e conteúdo aninhado requerem redação rasterizada.')
            require(not any(k in image for k in ('/SMask','/Mask','/Alternates','/OPI')))
            rect=bbox([point(ctm,x,y) for x,y in ((0,0),(1,0),(0,1),(1,1))])
            if intersects(rect,areas):removed_images+=1;continue
            used_images.add(args[0])
        elif op not in SAFE:
            raise ValueError('A página usa operadores não suportados pela redação vetorial; escolha o modo rasterizado.')
        output.append((args,op))
    require(text is None and not stack and not path_ops, 'Fluxo gráfico incompleto para redação vetorial.')
    # Drop unused XObjects so removed image bytes cannot survive as orphan resources.
    copied=DictionaryObject(resources)
    objects=resources.get('/XObject',{});objects=objects.get_object() if hasattr(objects,'get_object') else objects
    if objects:
        retained=DictionaryObject({k:v for k,v in objects.items() if k in used_images})
        if retained:copied[NameObject('/XObject')]=retained
        else:copied.pop('/XObject',None)
    page[NameObject('/Resources')]=copied
    # A page thumbnail may contain the pre-redaction pixels, even after the
    # displayed content stream and its image resources have been removed.
    for key in ('/Thumb', '/PieceInfo', '/StructParents', '/SeparationInfo'):
        page.pop(key, None)
    final=ContentStream(None,writer)
    final.operations=[([],b'q'),*output,([],b'Q')]
    for _, boxes, colour in marks:
        final.operations.append(([],b'q'))
        final.operations.append(([FloatObject(c/255) for c in colour],b'rg'))
        for x0,y0,x1,y1 in boxes:
            final.operations.extend([([FloatObject(v) for v in (x0,y0,x1-x0,y1-y0)],b're'),([],b'f')])
        final.operations.append(([],b'Q'))
    page[NameObject('/Contents')]=writer._add_object(final)
    return {'text_objects_removed':removed_text,'paths_removed':removed_paths,'images_removed':removed_images}
