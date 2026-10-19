"""Character/caret selection using extractor offsets and actual glyph boxes."""
import bisect
import math
import unicodedata

MAX_CHARACTERS = 100000


def boundaries(text):
    """Keep combining marks, variation selectors and joiner sequences together."""
    result = [0]
    regional = 0
    for index, char in enumerate(text):
        if not index:
            regional = int(0x1F1E6 <= ord(char) <= 0x1F1FF)
            continue
        previous = text[index - 1]
        is_regional = 0x1F1E6 <= ord(char) <= 0x1F1FF
        joined = (unicodedata.category(char).startswith('M') or char == '\u200d'
                  or previous == '\u200d' or 0xFE00 <= ord(char) <= 0xFE0F
                  or 0x1F3FB <= ord(char) <= 0x1F3FF
                  or (previous == '\r' and char == '\n')
                  or (is_regional and regional % 2 == 1))
        if not joined:
            result.append(index)
        regional = regional + 1 if is_regional else 0
    if result[-1] != len(text):
        result.append(len(text))
    return result


def validate_layout(data):
    text, boxes = data.get('text'), data.get('boxes')
    if (not isinstance(text, str) or len(text) > MAX_CHARACTERS
            or not isinstance(boxes, list) or len(boxes) != len(text)):
        raise ValueError('Mapa de caracteres inválido ou acima de 100000 caracteres.')
    if not all(isinstance(box, list) and len(box) == 4 and
               all(type(v) in (int, float) and math.isfinite(v) for v in box)
               and box[2] >= box[0] and box[3] >= box[1] for box in boxes):
        raise ValueError('Coordenadas de caracteres inválidas.')
    return text, boxes


def carets(data):
    text, boxes = validate_layout(data)
    stops = boundaries(text)
    result = [];last_strong = False
    for start, end in zip(stops, stops[1:]):
        rtl=last_strong
        for char in text[start:end]:
            direction=unicodedata.bidirectional(char)
            if direction in ('L','R','AL'):
                last_strong=direction!='L';rtl=last_strong
            elif direction in ('AN','EN'):rtl=False
        visible = [box for i, box in enumerate(boxes[start:end], start)
                   if not text[i].isspace() and box[3] > box[1]]
        if not visible:
            continue
        left = min(b[0] for b in visible);right = max(b[2] for b in visible)
        top = min(b[1] for b in visible);bottom = max(b[3] for b in visible)
        a, b = (right, left) if rtl else (left, right)
        result.extend([(start, a, top, bottom), (end, b, top, bottom)])
    return result


def nearest_caret(data, point):
    if len(point) != 2 or not all(math.isfinite(v) for v in point):
        raise ValueError('Ponto de seleção inválido.')
    x, y = point
    points = carets(data)
    if not points:
        return 0
    def distance(caret):
        _, cx, top, bottom = caret
        dy = max(top-y, 0, y-bottom)
        return dy*dy*4 + (x-cx)**2
    return min(points, key=distance)[0]


def select_range(data, anchor, focus):
    text, boxes = validate_layout(data)
    if any(type(v) is not int or not 0 <= v <= len(text) for v in (anchor, focus)):
        raise ValueError('Cursor fora do texto da página.')
    stops = boundaries(text)
    low, high = sorted((anchor, focus))
    start = stops[max(0, bisect.bisect_right(stops, low)-1)]
    end = stops[min(len(stops)-1, bisect.bisect_left(stops, high))]
    return dict(start=start, end=end, text=text[start:end],
                rects=[b for i,b in enumerate(boxes[start:end], start)
                       if not text[i].isspace() and b[2] > b[0] and b[3] > b[1]])


def caret_rectangle(data, offset):
    choices = [c for c in carets(data) if c[0] == offset]
    if not choices:
        return None
    _, x, top, bottom = choices[0]
    return [x, top, x, bottom]


def move_caret(data, offset, key, control=False):
    text, _ = validate_layout(data)
    points = carets(data)
    if control and key in ('Home', 'End'):
        return 0 if key == 'Home' else len(text)
    current = next((p for p in points if p[0] == offset), None)
    if current is None:
        stops = boundaries(text);index = bisect.bisect_left(stops, offset)
        return stops[min(len(stops)-1, max(0,index+(1 if key in ('Right','Down','End') else -1)))]
    _, x, top, bottom = current
    middle = (top+bottom)/2
    line = [p for p in points if p[2] <= middle <= p[3]]
    if key in ('Home','End'):
        return (min if key == 'Home' else max)(line, key=lambda p:p[1])[0]
    if key in ('Left','Right'):
        direction = 1 if key == 'Right' else -1
        candidates = [p for p in line if (p[1]-x)*direction > 1e-5]
        if candidates:
            return min(candidates,key=lambda p:abs(p[1]-x))[0]
        stops = boundaries(text);index = bisect.bisect_left(stops,offset)
        return stops[min(len(stops)-1,max(0,index+direction))]
    candidates = [p for p in points if (p[2] > bottom if key == 'Down' else p[3] < top)]
    return min(candidates,key=lambda p:abs((p[2]+p[3])/2-middle)*4+abs(p[1]-x))[0] if candidates else offset
