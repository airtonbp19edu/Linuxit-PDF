"""Poppler-GLib character geometry, executed only inside a limited worker."""
from pathlib import Path


def unicode_cursor_stops(text):
    """PangoLogAttr.is_cursor_position implements native UAX29 boundaries."""
    import ctypes,ctypes.util
    from character_selection import MAX_CHARACTERS
    if not isinstance(text,str) or len(text)>MAX_CHARACTERS:raise ValueError('Texto de cursor acima do limite.')
    library=ctypes.CDLL(ctypes.util.find_library('pango-1.0') or 'libpango-1.0.so.0')
    function=library.pango_get_log_attrs
    function.argtypes=[ctypes.c_char_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint),ctypes.c_int]
    function.restype=None
    raw=text.encode('utf-8');attributes=(ctypes.c_uint*(len(text)+1))()
    function(raw,len(raw),-1,None,attributes,len(attributes))
    # Public PangoLogAttr guint bitfields: is_cursor_position is the fifth bit.
    stops=[i for i,value in enumerate(attributes) if value & (1<<4)]
    if not stops or stops[0]!=0 or stops[-1]!=len(text):raise ValueError('Pango retornou limites de cursor inválidos.')
    return stops


def extract_characters(path, page_index):
    import gi
    gi.require_version('Poppler', '0.18')
    from gi.repository import Poppler
    from character_selection import MAX_CHARACTERS, validate_layout
    document = Poppler.Document.new_from_file(Path(path).resolve().as_uri(), None)
    if type(page_index) is not int or not 0 <= page_index < document.get_n_pages():
        raise ValueError('Página de texto inválida.')
    page = document.get_page(page_index)
    text = page.get_text() or ''
    if len(text) > MAX_CHARACTERS:
        raise ValueError('Página acima de 100000 caracteres para seleção.')
    success, layout = page.get_text_layout()
    if not success and not text:
        layout = []
    width, height = page.get_size()
    data = dict(schema='linuxit-character-layout-v1',width=width,height=height,text=text,
                boxes=[[r.x1,r.y1,r.x2,r.y2] for r in layout],logical_order='poppler-extracted',
                cursor_stops=unicode_cursor_stops(text))
    validate_layout(data)
    return data


def page_characters(path, page_index):
    from search_tasks import run_search_worker
    from cancel_state import get_event
    return run_search_worker('page-characters',str(path),{'page':page_index},get_event(),timeout=120)
