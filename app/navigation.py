"""Own finite navigation domain and rotation-aware page geometry."""
import math
import re

MIN_ZOOM, MAX_ZOOM = 1, 6400


def page_index(value, count, one_based=False):
    if count <= 0:return 0
    text = str(value).strip()
    if not re.fullmatch(r'[+-]?\d{1,10}', text):raise ValueError('Informe um número inteiro de página.')
    return max(0, min(int(text) - int(one_based), count - 1))


def zoom_value(value):
    text = str(value).strip().removesuffix('%').strip().replace(',', '.')
    if len(text) > 24:raise ValueError('Informe um percentual de zoom válido.')
    try:result = float(text)
    except (TypeError, ValueError):raise ValueError('Informe um percentual de zoom válido.') from None
    if not math.isfinite(result):raise ValueError('Informe um percentual de zoom finito.')
    return max(MIN_ZOOM, min(MAX_ZOOM, result))


def rotated_size(size, rotation):
    width, height = size
    return (height, width) if rotation % 180 else (width, height)


def page_width(size, rotation, mode, percent, viewport):
    width, height = rotated_size(size, rotation)
    vw, vh = max(1, viewport[0]), max(1, viewport[1])
    if mode == 'fit-width':return max(1, int(vw * .92))
    if mode == 'fit-page':return max(1, int(min(vw, vh * width / height)))
    return max(1, int(width / 72 * 96 * zoom_value(percent) / 100))
