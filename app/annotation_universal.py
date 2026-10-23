"""Own edits for every non-form annotation type, with one capability rule (A6).

The same `capabilities()` result is shown to the user (edit-info records) and
enforced when a copy is saved, so the interface never offers an edit that the
writer would refuse, and the writer never accepts one the interface hid.

Rules (ISO 32000-1, 12.5.3):
- ReadOnly (64): nothing changes.
- Locked (128): no move, resize, delete or colour/opacity change; contents may
  still be edited.
- LockedContents (512): contents and author cannot change; geometry may.
- Form widgets keep their own form flow; popups follow their owner.
- A note moves together with its popup. Replies stay where they are.
- Deleting removes the selected annotation and its popup only. An annotation
  with replies, linked to the structure tree, referenced from another page or
  targeted by a rendition action is refused instead of leaving dangling links.
- Resizing maps every coordinate array (/Rect, /QuadPoints, /Vertices, /L,
  /CL, /InkList, /RD) from the old to the new rectangle. Appearances drawn by
  Linuxit's own generator are redrawn; any other appearance is kept and scaled
  by the viewer through the standard BBox-to-Rect mapping, so producer fonts,
  arrowheads and pictures are not replaced by an approximation.
- Colour is changed only where the appearance can be redrawn faithfully from
  geometry, or where the annotation has no appearance and the viewer draws it
  from /C. Opacity works for any appearance: the existing drawing is wrapped,
  never rewritten.

Nothing here runs PDF actions, scripts or embedded files. Deleting a file
attachment annotation does not promise to erase the attached bytes.
"""
import math

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject, DictionaryObject,  # noqa: E402
                           FloatObject, IndirectObject, NameObject, NumberObject, StreamObject, TextStringObject)

from pdf_comments import COMMENT_TYPES  # noqa: E402

READ_ONLY, LOCKED, LOCKED_CONTENTS = 64, 128, 512
NO_ZOOM = 8
FORM_TYPES = frozenset({'/Widget'})
# Types whose /Contents is a comment and /T an author (markup annotations).
MARKUP_TYPES = frozenset(COMMENT_TYPES) | {'/Sound'}
# Types drawn by a viewer from /C when they carry no appearance stream.
ICON_TYPES = frozenset({'/Text', '/FileAttachment', '/Sound'})
FLAT_KEYS = ('/QuadPoints', '/Vertices', '/L', '/CL')
MAX_POINTS = 8192
MAX_COORDINATE = 10_000_000
MIN_SPAN = .25
WRAP_MARK = '/LinuxitOpacityWrap'
NAMES = {'/Text': 'Nota', '/FreeText': 'Texto livre', '/Highlight': 'Destaque', '/Underline': 'Sublinhado',
         '/StrikeOut': 'Tachado', '/Squiggly': 'Ondulado', '/Stamp': 'Carimbo', '/Ink': 'Desenho', '/Line': 'Linha',
         '/Square': 'Retângulo', '/Circle': 'Elipse', '/Polygon': 'Polígono', '/PolyLine': 'Polilinha',
         '/FileAttachment': 'Anexo', '/Caret': 'Inserção', '/Redact': 'Redação marcada', '/Link': 'Link',
         '/Sound': 'Som', '/Movie': 'Filme', '/Screen': 'Tela de mídia', '/RichMedia': 'Mídia rica', '/3D': '3D',
         '/Watermark': "Marca d'água", '/PrinterMark': 'Marca de impressão', '/TrapNet': 'Rede de trapping'}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _obj(value):
    return value.get_object() if value is not None and hasattr(value, 'get_object') else value


def _number(value):
    value = float(value)
    _require(math.isfinite(value) and abs(value) <= MAX_COORDINATE, 'Coordenadas da anotação inválidas.')
    return value


def _numbers(values):
    return ArrayObject(FloatObject(v) for v in values)


def _flags(note):
    try:
        return int(note.get('/F', 0))
    except (TypeError, ValueError):
        return READ_ONLY  # Unreadable flags are treated as the most restrictive.


def _rect(note):
    value = _obj(note.get('/Rect'))
    _require(isinstance(value, list) and len(value) == 4, 'Anotação sem retângulo utilizável.')
    x0, y0, x1, y1 = [_number(v) for v in value]
    return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]


def label(subtype):
    return NAMES.get(subtype, str(subtype).lstrip('/') or 'Anotação')


# ---------- relationships ----------

def _page_annots(page):
    annots = _obj(page.get('/Annots'))
    return annots if isinstance(annots, list) else []


def _relations(document, page_no, note):
    """Popup, replies, inbound references and their pages, bounded to 50000 annotations."""
    popup = _obj(note.get('/Popup'))
    replies, inbound_other_pages, popups_of_note, rendition_targets = [], False, [], False
    count = 0
    for other_no, other_page in enumerate(document.pages):
        for reference in _page_annots(other_page):
            count += 1
            _require(count <= 50000, 'Documento acima de 50000 anotações.')
            other = _obj(reference)
            if not isinstance(other, DictionaryObject) or other is note:
                continue
            for key in ('/IRT', '/Parent'):
                if _obj(other.get(key)) is note:
                    if other_no != page_no:
                        inbound_other_pages = True
                    if key == '/IRT':
                        replies.append(other)
                    elif other.get('/Subtype') == '/Popup':
                        popups_of_note.append(other)
                    else:
                        inbound_other_pages = True  # A non-popup child (e.g. a widget kid) is not ours to move.
            action = _obj(other.get('/A'))
            if isinstance(action, DictionaryObject) and _obj(action.get('/AN')) is note:
                rendition_targets = True
    if popup is not None:
        popups_of_note = [p for p in popups_of_note if p is not popup] + [popup]
    return popup, replies, inbound_other_pages, popups_of_note, rendition_targets


def _popup_is_reciprocal(note, popup, page):
    if popup is None:
        return True
    in_page = any(_obj(r) is popup for r in _page_annots(page))
    return (isinstance(popup, DictionaryObject) and popup.get('/Subtype') == '/Popup'
            and _obj(popup.get('/Parent')) is note and in_page)


# ---------- appearance helpers ----------

def _regenerable(note):
    """True when Linuxit's geometric redraw reproduces this annotation without losing features."""
    from annotation_style import STYLEABLE
    subtype = note.get('/Subtype')
    if subtype not in STYLEABLE | {'/Square', '/Circle'}:
        return False
    border_effect = _obj(note.get('/BE'))
    if isinstance(border_effect, DictionaryObject) and border_effect.get('/S') == '/C':
        return False  # Cloudy borders.
    border = _obj(note.get('/BS'))
    if isinstance(border, DictionaryObject) and border.get('/S') not in (None, '/S') and subtype != '/Redact':
        return False  # Dashed, bevelled, inset or underline borders.
    endings = _obj(note.get('/LE'))
    if isinstance(endings, list) and any(str(e) != '/None' for e in endings):
        return False  # Arrowheads and other line endings.
    if any(key in note for key in ('/IT', '/Measure', '/Cap', '/LL', '/LLE', '/LLO')):
        return False  # Measurement/dimension annotations with captions or leaders.
    return True


def _form_box(stream):
    box = _obj(stream.get('/BBox'))
    _require(isinstance(box, list) and len(box) == 4, 'Aparência sem BBox.')
    x0, y0, x1, y1 = [_number(v) for v in box]
    matrix = _obj(stream.get('/Matrix'))
    if not isinstance(matrix, list) or len(matrix) != 6:
        return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    a, b, c, d, e, f = [_number(v) for v in matrix]
    corners = [(a * x + c * y + e, b * x + d * y + f) for x in (x0, x1) for y in (y0, y1)]
    xs, ys = [p[0] for p in corners], [p[1] for p in corners]
    return [min(xs), min(ys), max(xs), max(ys)]


def _wrap(writer, reference, opacity):
    """A form drawing the original appearance under an opacity state; repeated changes reuse the wrapper."""
    stream = _obj(reference)
    _require(isinstance(stream, StreamObject), 'Aparência da anotação inválida.')
    if stream.get(WRAP_MARK) is True or stream.get(WRAP_MARK) == BooleanObject(True):
        state = _obj(_obj(_obj(stream['/Resources'])['/ExtGState'])['/LinuxitOpacity'])
        state[NameObject('/CA')] = FloatObject(opacity);state[NameObject('/ca')] = FloatObject(opacity)
        return reference
    if not isinstance(reference, IndirectObject):
        reference = writer._add_object(stream)
    wrapper = DecodedStreamObject()
    wrapper.set_data(b'q\n/LinuxitOpacity gs\n/LinuxitOriginal Do\nQ\n')
    wrapper.update({
        NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Form'),
        NameObject('/FormType'): NumberObject(1), NameObject('/BBox'): _numbers(_form_box(stream)),
        NameObject(WRAP_MARK): BooleanObject(True),
        NameObject('/Resources'): DictionaryObject({
            NameObject('/ExtGState'): DictionaryObject({NameObject('/LinuxitOpacity'): DictionaryObject({
                NameObject('/Type'): NameObject('/ExtGState'),
                NameObject('/CA'): FloatObject(opacity), NameObject('/ca'): FloatObject(opacity)})}),
            NameObject('/XObject'): DictionaryObject({NameObject('/LinuxitOriginal'): reference})})})
    return writer._add_object(wrapper)


def _set_opacity(writer, note, opacity):
    appearances = _obj(note.get('/AP'))
    if isinstance(appearances, DictionaryObject):
        for key in ('/N', '/R', '/D'):
            raw = appearances.raw_get(key) if key in appearances else None
            value = _obj(raw)
            if isinstance(value, StreamObject):
                appearances[NameObject(key)] = _wrap(writer, raw, opacity)
            elif isinstance(value, DictionaryObject):
                for state in list(value.keys()):
                    value[NameObject(state)] = _wrap(writer, value.raw_get(state), opacity)
    note[NameObject('/CA')] = FloatObject(opacity)


# ---------- capabilities ----------

def capabilities(document, page_no, page, index):
    annots = _page_annots(page)
    _require(type(index) is int and 0 <= index < len(annots), 'Índice de anotação inválido.')
    note = _obj(annots[index])
    _require(isinstance(note, DictionaryObject), 'Anotação inválida.')
    subtype = note.get('/Subtype')
    result = dict(subtype=str(subtype), label=label(subtype), movable=False, resizable=False, deletable=False,
                  text_editable=False, color_editable=False, opacity_editable=False, has_author=False,
                  rect=None, reasons={})
    reasons = result['reasons']
    if subtype in FORM_TYPES:
        reasons['all'] = 'Campo de formulário: use as operações de formulário.'
        return note, result
    if subtype == '/Popup':
        reasons['all'] = 'Popup acompanha a anotação dona.'
        return note, result
    flags = _flags(note)
    if flags & READ_ONLY:
        reasons['all'] = 'Anotação somente leitura.'
        return note, result
    try:
        rect = _rect(note)
    except ValueError as exc:
        rect = None;reasons['geometry'] = str(exc)
    irt = _obj(note.get('/IRT')) if '/IRT' in note else None
    malformed = (('/IRT' in note and not (isinstance(irt, DictionaryObject) and '/Subtype' in irt and irt is not note))
                 or ('/Popup' in note and not _popup_is_reciprocal(note, _obj(note.get('/Popup')), page))
                 or '/Parent' in note)
    if malformed:
        reasons['all'] = 'Vínculos de popup/resposta malformados; nada é alterado.'
        return note, result
    popup, replies, cross_page, popups, rendition = _relations(document, page_no, note)
    reciprocal = _popup_is_reciprocal(note, popup, page)
    group = note.get('/RT') == '/Group' or any(r.get('/RT') == '/Group' for r in replies)
    geometry_ok = rect is not None and reciprocal and not cross_page and not group
    if not reciprocal:reasons['geometry'] = 'Popup sem vínculo recíproco na mesma página.'
    elif cross_page:reasons['geometry'] = 'Anotação referenciada por outra página.'
    elif group:reasons['geometry'] = 'Grupos de anotação (/RT Group) não são editados separadamente.'
    if flags & LOCKED:
        reasons['locked'] = 'Anotação travada: posição, tamanho, estilo e exclusão bloqueados.'
    else:
        result['movable'] = geometry_ok
        if geometry_ok:
            if flags & NO_ZOOM:reasons['resize'] = 'Ícone de tamanho fixo (NoZoom).'
            else:result['resizable'] = True
        delete_reason = ('Tem respostas; exclua a conversa inteira.' if replies else
                         'Ligada à árvore de acessibilidade.' if '/StructParent' in note else
                         'Alvo de ação de mídia de outra anotação.' if rendition else
                         None if geometry_ok else reasons.get('geometry'))
        if delete_reason:reasons['delete'] = delete_reason
        else:result['deletable'] = True
        has_ap = isinstance(_obj(note.get('/AP')), DictionaryObject)
        result['opacity_editable'] = rect is not None and reciprocal
        if _regenerable(note):result['color_editable'] = result['opacity_editable']
        elif subtype in ICON_TYPES and not has_ap:result['color_editable'] = result['opacity_editable']
        else:reasons['color'] = 'Cor definida pela aparência própria do arquivo; só a opacidade muda.'
    if flags & LOCKED_CONTENTS:
        reasons['text'] = 'Conteúdo travado (LockedContents).'
    else:
        contents, author = note.get('/Contents', ''), note.get('/T', '')
        result['text_editable'] = isinstance(contents, str) and (isinstance(author, str) or subtype not in MARKUP_TYPES)
        if not result['text_editable']:reasons['text'] = 'Comentário ou autor em formato não textual.'
    result['has_author'] = subtype in MARKUP_TYPES
    result['rect'] = rect
    result['styleable'] = result['color_editable']
    return note, result


ACTIONS = {'move': 'movable', 'resize': 'resizable', 'delete': 'deletable', 'text': 'text_editable',
           'color': 'color_editable', 'opacity': 'opacity_editable'}


def _checked(document, page_no, page, index, action):
    note, caps = capabilities(document, page_no, page, index)
    if not caps[ACTIONS[action]]:
        reason = caps['reasons'].get(action) or caps['reasons'].get('locked') or caps['reasons'].get('geometry') \
            or caps['reasons'].get('all') or 'Operação não suportada para este tipo.'
        raise ValueError(f"{caps['label']}: {reason}")
    return note, caps


# ---------- operations ----------

def _inside(page, rect):
    left, bottom, right, top = [_number(v) for v in page.cropbox]
    _require(left <= rect[0] < rect[2] <= right and bottom <= rect[1] < rect[3] <= top,
             'A anotação deve ficar dentro do CropBox, em coordenadas PDF.')


def _map_flat(note, key, fx, fy):
    values = _obj(note[key])
    _require(isinstance(values, list) and len(values) % 2 == 0 and len(values) <= MAX_POINTS,
             'Coordenadas da anotação inválidas.')
    note[NameObject(key)] = _numbers([fx(_number(v)) if i % 2 == 0 else fy(_number(v)) for i, v in enumerate(values)])


def _map_geometry(note, fx, fy, sx=1.0, sy=1.0):
    for key in FLAT_KEYS:
        if key in note:_map_flat(note, key, fx, fy)
    if '/InkList' in note:
        paths = _obj(note['/InkList'])
        _require(isinstance(paths, list) and len(paths) <= 256, 'Traços de anotação inválidos.')
        total = sum(len(_obj(p)) for p in paths)
        _require(total <= MAX_POINTS, 'Traços de anotação inválidos.')
        mapped = []
        for path in paths:
            path = _obj(path)
            _require(isinstance(path, list) and len(path) % 2 == 0, 'Traços de anotação inválidos.')
            mapped.append(_numbers([fx(_number(v)) if i % 2 == 0 else fy(_number(v)) for i, v in enumerate(path)]))
        note[NameObject('/InkList')] = ArrayObject(mapped)
    if '/RD' in note:
        margins = _obj(note['/RD'])
        if isinstance(margins, list) and len(margins) == 4:
            l, b, r, t = [_number(v) for v in margins]
            note[NameObject('/RD')] = _numbers([l * sx, b * sy, r * sx, t * sy])


def move(document, page_no, page, index, dx, dy):
    _require(all(type(v) in (int, float) and math.isfinite(v) and abs(v) <= MAX_COORDINATE for v in (dx, dy)),
             'Deslocamento inválido.')
    note, caps = _checked(document, page_no, page, index, 'move')
    targets = [note]
    popup = _obj(note.get('/Popup'))
    if popup is not None and '/Rect' in popup:targets.append(popup)
    shifted = []
    for target in targets:
        rect = _rect(target);moved = [rect[0] + dx, rect[1] + dy, rect[2] + dx, rect[3] + dy]
        if target is note:_inside(page, moved)
        shifted.append(moved)
    # Validate every array before changing any object, so a refusal leaves the copy untouched.
    clones = [DictionaryObject(t) for t in targets]
    for clone in clones:
        _map_geometry(clone, lambda x: x + dx, lambda y: y + dy)
    if popup is not None and len(targets) == 2:
        left, bottom, right, top = [_number(v) for v in page.cropbox]
        x0, y0, x1, y1 = shifted[1]
        # Keep the popup visible on the page: clamp instead of refusing the owner's move.
        w, h = x1 - x0, y1 - y0
        x0 = min(max(x0, left), max(left, right - w));y0 = min(max(y0, bottom), max(bottom, top - h))
        shifted[1] = [x0, y0, x0 + w, y0 + h]
    for target, clone, rect in zip(targets, clones, shifted):
        for key in FLAT_KEYS + ('/InkList',):
            if key in clone:target[NameObject(key)] = clone[key]
        target[NameObject('/Rect')] = _numbers(rect)
    return caps


def resize(writer, page_no, page, index, rect):
    note, caps = _checked(writer, page_no, page, index, 'resize')
    _require(isinstance(rect, list) and len(rect) == 4 and all(type(v) in (int, float) for v in rect), 'Retângulo inválido.')
    x0, y0, x1, y1 = [_number(v) for v in rect]
    _require(x1 - x0 >= MIN_SPAN and y1 - y0 >= MIN_SPAN, 'A nova área deve ter ao menos 0,25 ponto de lado.')
    _inside(page, [x0, y0, x1, y1])
    ox0, oy0, ox1, oy1 = caps['rect']
    _require(ox1 - ox0 > 0 and oy1 - oy0 > 0, 'Retângulo original vazio; não há escala definida.')
    sx, sy = (x1 - x0) / (ox1 - ox0), (y1 - y0) / (oy1 - oy0)
    subtype = note.get('/Subtype')
    from annotation_geometry import RESIZABLE, resize_annotation
    own_redraw = subtype in RESIZABLE and (subtype != '/FreeText' or not any(k in note for k in ('/CL', '/IT')))
    if own_redraw and subtype != '/FreeText' and not _regenerable(note):own_redraw = False
    clone = DictionaryObject(note)
    _map_geometry(clone, lambda x: x0 + (x - ox0) * sx, lambda y: y0 + (y - oy0) * sy, sx, sy)
    for key in FLAT_KEYS + ('/InkList', '/RD'):
        if key in clone:note[NameObject(key)] = clone[key]
    if own_redraw:
        resize_annotation(writer, note, [x0, y0, x1, y1])
    else:
        note[NameObject('/Rect')] = _numbers([x0, y0, x1, y1])
        if _regenerable(note) and isinstance(_obj(note.get('/AP')), DictionaryObject):
            from annotation_style import current_style, restyle_annotation
            color, opacity = current_style(note)
            restyle_annotation(writer, note, color or [0.0, 0.0, 0.0], max(opacity, 0.1))
        # Otherwise the original appearance is kept; viewers map its BBox onto the new /Rect.
    return dict(caps, redrawn=own_redraw or _regenerable(note))


def style(writer, page_no, page, index, color, opacity):
    _require(type(opacity) in (int, float) and .1 <= opacity <= 1, 'Opacidade deve ficar entre 10% e 100%.')
    note, caps = _checked(writer, page_no, page, index, 'opacity')
    if color is None:
        _set_opacity(writer, note, float(opacity))
        return caps
    from annotation_style import validate_style, restyle_annotation
    rgb, alpha = validate_style(color, opacity)
    if not caps['color_editable']:
        raise ValueError(f"{caps['label']}: {caps['reasons'].get('color', 'cor não editável')}")
    if _regenerable(note):
        restyle_annotation(writer, note, rgb, alpha)
    else:  # Icon drawn by the viewer from /C (no appearance stream).
        note[NameObject('/C')] = _numbers(rgb);note[NameObject('/CA')] = FloatObject(alpha)
    return caps


def delete(writer, page_no, page, index):
    note, caps = _checked(writer, page_no, page, index, 'delete')
    annots = _page_annots(page)
    removed = {id(note)}
    popup = _obj(note.get('/Popup'))
    for reference in annots:
        other = _obj(reference)
        if other is popup or (isinstance(other, DictionaryObject) and other.get('/Subtype') == '/Popup'
                              and _obj(other.get('/Parent')) is note):
            removed.add(id(other))
    page[NameObject('/Annots')] = ArrayObject(r for r in annots if id(_obj(r)) not in removed)
    return caps


def update_text(writer, page_no, page, index, text, author):
    note, caps = _checked(writer, page_no, page, index, 'text')
    _require(isinstance(text, str) and len(text.encode('utf-8')) <= 65536, 'Comentário inválido ou acima do limite de 64 KiB.')
    _require(isinstance(author, str) and len(author.encode('utf-8')) <= 4096, 'Autor inválido.')
    _require(caps['has_author'] or not author, f"{caps['label']}: este tipo não tem autor; deixe o campo vazio.")
    note[NameObject('/Contents')] = TextStringObject(text)
    if caps['has_author']:
        if author:note[NameObject('/T')] = TextStringObject(author)
        else:note.pop('/T', None)
    note.pop('/RC', None)  # Rich text would contradict the new plain contents.
    return caps


def records(document, limit=2000, text_limit=65536):
    """Every annotation except widgets/popups, with what may be done to it."""
    rows, size, truncated = [], 0, False
    for page_no, page in enumerate(document.pages):
        for index, reference in enumerate(_page_annots(page)):
            note = _obj(reference)
            if not isinstance(note, DictionaryObject) or note.get('/Subtype') in FORM_TYPES | {'/Popup'}:
                continue
            try:
                note, caps = capabilities(document, page_no, page, index)
            except ValueError:
                continue
            text, author = note.get('/Contents', ''), note.get('/T', '')
            text = text if isinstance(text, str) else '';author = author if isinstance(author, str) else ''
            if len(text.encode('utf-8')) > text_limit or len(author.encode('utf-8')) > 4096:
                text, author = '', '';caps['text_editable'] = False;caps['reasons']['text'] = 'Comentário acima de 64 KiB.'
            cost = len(text.encode('utf-8')) + len(author.encode('utf-8'))
            if len(rows) >= limit or size + cost > 1024 ** 2:
                truncated = True;continue
            size += cost
            from annotation_style import current_style
            try:color, opacity = current_style(note)
            except (TypeError, ValueError):color, opacity = None, 1.0
            rows.append(dict(page=page_no, index=index, text=text, author=author, color=color, opacity=opacity, **caps))
    return rows, truncated
