"""Change the colour and opacity of existing simple annotations (E12).

The normal appearance is regenerated from the annotation's own geometry
(/Rect, /QuadPoints, /L, /InkList, /Vertices), so the result does not depend
on a viewer's fallback drawing. Opacity goes to /CA and to an ExtGState in
the appearance. Rich or text-bearing types (notes, free text, stamps) are not
restyled here: their appearance carries fonts and layout that would be lost.
"""
import math

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,  # noqa: E402
                           FloatObject, NameObject, NumberObject)

STYLEABLE = {'/Square', '/Circle', '/Line', '/Underline', '/StrikeOut', '/Squiggly', '/Highlight',
             '/Ink', '/Polygon', '/PolyLine', '/Caret'}
MAX_POINTS = 4096
MIN_OPACITY = 0.1
MAX_COORDINATE = 10_000_000
K = .5522847498307936


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _number(value):
    value = float(value)
    _require(math.isfinite(value) and abs(value) <= MAX_COORDINATE, 'Geometria da anotação inválida.')
    return value


def _numbers(values):
    return ArrayObject(FloatObject(v) for v in values)


def _f(*values):
    return ' '.join(f'{v:.4f}' for v in values)


def _list(note, key, minimum=0):
    value = note.get(key)
    value = value.get_object() if value is not None else None
    _require(isinstance(value, list) and len(value) >= minimum, f'Anotação sem {key} utilizável.')
    return value


def validate_style(color, opacity):
    _require(isinstance(color, list) and len(color) == 3 and all(type(c) in (int, float) and 0 <= c <= 1 for c in color),
             'Cor deve ter três componentes entre 0 e 1.')
    _require(type(opacity) in (int, float) and MIN_OPACITY <= opacity <= 1, 'Opacidade deve ficar entre 10% e 100%.')
    return [float(c) for c in color], float(opacity)


def current_style(note):
    """Colour/opacity as recorded on the annotation, for dialog defaults."""
    color = note.get('/C')
    color = [float(c) for c in color.get_object()] if color is not None and len(color.get_object()) == 3 else None
    opacity = note.get('/CA')
    return color, float(opacity) if opacity is not None else 1.0


def _quads(note, x0, y0):
    values = [_number(v) for v in _list(note, '/QuadPoints', 8)]
    _require(len(values) % 8 == 0 and len(values) // 8 <= MAX_POINTS // 4, 'QuadPoints inválidos.')
    boxes = []
    for i in range(0, len(values), 8):
        xs, ys = values[i:i + 8:2], values[i + 1:i + 8:2]
        boxes.append((min(xs) - x0, min(ys) - y0, max(xs) - x0, max(ys) - y0))
    return boxes


def _paths(note, key, x0, y0, nested):
    raw = _list(note, key, 1)
    groups = [g.get_object() for g in raw] if nested else [raw]
    total, result = 0, []
    for group in groups:
        _require(isinstance(group, list) and len(group) >= 4 and len(group) % 2 == 0, f'{key} inválido.')
        total += len(group) // 2
        _require(total <= MAX_POINTS, 'Geometria acima de 4096 pontos.')
        values = [_number(v) for v in group]
        result.append([(values[i] - x0, values[i + 1] - y0) for i in range(0, len(values), 2)])
    return result


def _drawing(note, subtype, width, height, x0, y0, stroke, rgb):
    """Content stream (without the colour state) and whether it is filled."""
    pad = stroke / 2
    color_stroke, color_fill = _f(*rgb) + ' RG', _f(*rgb) + ' rg'
    lines = []
    if subtype == '/Square' or subtype == '/Circle':
        interior = note.get('/IC')
        fill = interior is not None and len(interior.get_object()) == 3
        if fill:lines.append(_f(*[float(c) for c in interior.get_object()]) + ' rg')
        if subtype == '/Square':
            lines.append(_f(pad, pad, max(width - stroke, 0), max(height - stroke, 0)) + ' re')
        else:
            cx, cy, rx, ry = width / 2, height / 2, max(width / 2 - pad, 0), max(height / 2 - pad, 0)
            lines += [_f(cx + rx, cy) + ' m',
                      _f(cx + rx, cy + K * ry, cx + K * rx, cy + ry, cx, cy + ry) + ' c',
                      _f(cx - K * rx, cy + ry, cx - rx, cy + K * ry, cx - rx, cy) + ' c',
                      _f(cx - rx, cy - K * ry, cx - K * rx, cy - ry, cx, cy - ry) + ' c',
                      _f(cx + K * rx, cy - ry, cx + rx, cy - K * ry, cx + rx, cy) + ' c', 'h']
        return [color_stroke] + lines + ['B' if fill else 'S']
    if subtype == '/Line':
        a, b, c, d = [_number(v) for v in _list(note, '/L', 4)[:4]]
        return [color_stroke, _f(a - x0, b - y0) + ' m', _f(c - x0, d - y0) + ' l', 'S']
    if subtype == '/Highlight':
        return [color_fill] + [_f(l, b, r - l, t - b) + ' re' for l, b, r, t in _quads(note, x0, y0)] + ['f']
    if subtype in ('/Underline', '/StrikeOut', '/Squiggly'):
        lines = [color_stroke]
        for l, b, r, t in _quads(note, x0, y0):
            if subtype == '/Underline':lines += [_f(l, b + pad) + ' m', _f(r, b + pad) + ' l']
            elif subtype == '/StrikeOut':lines += [_f(l, (b + t) / 2) + ' m', _f(r, (b + t) / 2) + ' l']
            else:
                amplitude = max(min(1.5, (t - b - stroke) / 3), 0);base = b + pad + amplitude
                segments = 4 * max(1, min(128, math.ceil((r - l) / 6)))
                lines.append(_f(l, base) + ' m')
                for i in range(1, segments + 1):
                    y = base + (amplitude if i % 4 == 1 else -amplitude if i % 4 == 3 else 0)
                    lines.append(_f(l + (r - l) * i / segments, y) + ' l')
        return lines + ['S']
    if subtype in ('/Ink', '/Polygon', '/PolyLine'):
        paths = _paths(note, '/InkList' if subtype == '/Ink' else '/Vertices', x0, y0, subtype == '/Ink')
        lines = [color_stroke]
        for path in paths:
            lines.append(_f(*path[0]) + ' m');lines += [_f(*p) + ' l' for p in path[1:]]
            if subtype == '/Polygon':lines.append('h')
        return lines + ['S']
    if subtype == '/Caret':
        return [color_stroke, _f(width * .1, height * .1) + ' m', _f(width * .5, height * .9) + ' l',
                _f(width * .9, height * .1) + ' l', 'S']
    raise ValueError('Tipo de anotação sem cor/opacidade editável.')


def restyle_annotation(writer, note, color, opacity):
    """Set /C, /CA and a regenerated /AP /N on `note` (an annotation dictionary in `writer`)."""
    rgb, alpha = validate_style(color, opacity)
    subtype = note.get('/Subtype')
    _require(subtype in STYLEABLE, 'Tipo de anotação sem cor/opacidade editável (notas, texto livre e carimbos ficam como estão).')
    x0, y0, x1, y1 = [_number(v) for v in note['/Rect']]
    x0, x1 = sorted((x0, x1));y0, y1 = sorted((y0, y1))
    width, height = x1 - x0, y1 - y0
    _require(width > 0 and height > 0, 'Retângulo da anotação vazio.')
    border = note.get('/BS');border = border.get_object() if border is not None else {}
    stroke = float(border.get('/W', 1)) if hasattr(border, 'get') else 1.0
    stroke = min(max(stroke, 0.0), min(width, height) / 2, 50.0)
    body = _drawing(note, subtype, width, height, x0, y0, stroke, rgb)
    state = DictionaryObject({NameObject('/Type'): NameObject('/ExtGState'),
                              NameObject('/CA'): FloatObject(alpha), NameObject('/ca'): FloatObject(alpha)})
    if subtype == '/Highlight':state[NameObject('/BM')] = NameObject('/Multiply')
    content = ['q', '/LinuxitStyle gs', _f(stroke) + ' w', '1 J', '1 j'] + body + ['Q']
    appearance = DecodedStreamObject()
    appearance.set_data(('\n'.join(content) + '\n').encode('ascii'))
    appearance.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Form'),
                       NameObject('/FormType'): NumberObject(1), NameObject('/BBox'): _numbers([0, 0, width, height]),
                       NameObject('/Resources'): DictionaryObject({NameObject('/ExtGState'): DictionaryObject(
                           {NameObject('/LinuxitStyle'): state})})})
    note[NameObject('/C')] = _numbers(rgb)
    note[NameObject('/CA')] = FloatObject(alpha)
    note[NameObject('/AP')] = DictionaryObject({NameObject('/N'): writer._add_object(appearance)})
    note[NameObject('/Rect')] = _numbers([x0, y0, x1, y1])
    return note
