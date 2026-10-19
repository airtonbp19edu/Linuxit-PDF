"""Rectangular word selection in Poppler reading order, without bidi reversal."""
import math


def select_words(data, rect):
    if len(rect) != 4 or not all(math.isfinite(float(v)) for v in rect):
        raise ValueError('Retângulo de seleção inválido.')
    x0, x1 = sorted((rect[0], rect[2]));y0, y1 = sorted((rect[1], rect[3]))
    if x0 == x1 or y0 == y1:return []
    return [word for word in data.get('words', [])
            if min(word['x1'], x1) > max(word['x0'], x0)
            and min(word['y1'], y1) > max(word['y0'], y0)]


def selection_text(words):
    """Keep Unicode logical strings from the extractor; never reverse RTL text.

    A column/block boundary is a paragraph boundary, not a phrase join. Character
    caret selection and inference of damaged PDF reading order are not provided.
    """
    parts, line, previous = [], [], None
    for word in words:
        current = word['block'], word['line']
        if previous is not None and current != previous:
            parts.append(' '.join(line));line=[]
            if current[0] != previous[0]:parts.append('')
        line.append(word['text']);previous=current
    if line:parts.append(' '.join(line))
    return '\n'.join(parts).strip()
