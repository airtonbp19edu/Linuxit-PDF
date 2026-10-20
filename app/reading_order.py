"""Own, bounded reading-order heuristic for accessible text (E19).

Input: the text lines of one page with their boxes (top-down coordinates, as
Poppler's -bbox-layout reports them). Lines that do not cross a vertical gutter
are split into a left and a right column and read column by column; lines that
cross the gutter (titles, full-width paragraphs, footers) stay in place and
separate the vertical bands. The split is applied again inside each column,
up to three levels, so three columns also come out in order. Without a clear
gutter the order is top-to-bottom, left-to-right.

Limits: tables, captions inside columns, rotated text and pages whose columns
change width inside the same band are not analysed; this is not a tagged-PDF
structure tree.
"""
MIN_GUTTER = 6.0          # points without any narrow line crossing
MIN_LINES_PER_SIDE = 2
MAX_LINES = 20000
MAX_DEPTH = 3


def _gutter(lines, width):
    """x of a vertical gap that splits the lines into two columns, or None.

    Candidate regions are the x ranges with no line edge inside (at least MIN_GUTTER
    wide, in the middle 60% of the text area). The region crossed by the fewest lines
    wins; those few crossing lines (titles, full-width paragraphs) are read in place.
    """
    if len(lines) < 2 * MIN_LINES_PER_SIDE:return None
    left_edge, right_edge = min(l[0] for l in lines), max(l[2] for l in lines)
    span = right_edge - left_edge
    if span <= 0:return None
    low, high = left_edge + 0.2 * span, left_edge + 0.8 * span
    edges = sorted({low, high, *(x for l in lines for x in (l[0], l[2]) if low < x < high)})
    best = None
    for start, end in zip(edges, edges[1:]):
        if end - start < MIN_GUTTER:continue
        middle = (start + end) / 2
        crossing = sum(1 for l in lines if l[0] < middle < l[2])
        key = (crossing, -(end - start))
        if best is None or key < best[0]:best = (key, middle)
    if best is None:return None
    split = best[1];crossing = best[0][0]
    left = sum(1 for l in lines if l[2] <= split);right = sum(1 for l in lines if l[0] >= split)
    if left < MIN_LINES_PER_SIDE or right < MIN_LINES_PER_SIDE:return None
    return split if crossing <= max(1, len(lines) // 4) else None


def order_lines(lines, width, depth=0):
    """lines: [(x0, y0, x1, y1, text)] with y growing downwards. Returns texts in reading order."""
    lines = sorted(lines, key=lambda l: (round(l[1], 1), l[0]))
    if depth >= MAX_DEPTH or len(lines) < 2:return [l[4] for l in lines]
    wide = [l for l in lines if (l[2] - l[0]) >= 0.6 * width]
    if wide and len(wide) < len(lines):
        # Full-width lines separate bands that may have different column layouts.
        ordered, band = [], []
        for line in lines:
            if (line[2] - line[0]) >= 0.6 * width:
                ordered.extend(_columns(band, width, depth));band = [];ordered.append(line[4])
            else:band.append(line)
        return ordered + _columns(band, width, depth)
    return _columns(lines, width, depth)


def _columns(lines, width, depth):
    if not lines:return []
    split = _gutter(lines, width)
    if split is None:return [l[4] for l in lines]
    ordered, band = [], []
    def flush():
        left = [l for l in band if l[2] <= split];right = [l for l in band if l[0] >= split]
        ordered.extend(order_lines(left, width, depth + 1));ordered.extend(order_lines(right, width, depth + 1))
        band.clear()
    for line in lines:
        if line[0] < split < line[2]:
            flush();ordered.append(line[4])
        else:band.append(line)
    flush()
    return ordered


def page_lines(xml_bytes):
    """Lines and page width from `pdftotext -bbox-layout` output for one page."""
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_bytes)
    tag = lambda el: el.tag.rsplit('}', 1)[-1]
    page = next((el for el in root.iter() if tag(el) == 'page'), None)
    if page is None:return [], 0.0
    width, lines = float(page.attrib.get('width') or 0), []
    for line in (el for el in page.iter() if tag(el) == 'line'):
        words = [w for w in line if tag(w) == 'word']
        text = ' '.join(''.join(w.itertext()).strip() for w in words).strip()
        if not text:continue
        box = tuple(float(line.attrib[k]) for k in ('xMin', 'yMin', 'xMax', 'yMax'))
        lines.append((*box, text))
        if len(lines) > MAX_LINES:raise ValueError('Página acima de 20000 linhas de texto.')
    return lines, width
