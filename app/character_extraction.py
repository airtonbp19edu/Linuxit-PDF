"""Poppler-GLib character geometry, executed only inside a limited worker."""
from pathlib import Path


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
                boxes=[[r.x1,r.y1,r.x2,r.y2] for r in layout],logical_order='poppler-extracted')
    validate_layout(data)
    return data


def page_characters(path, page_index):
    from search_tasks import run_search_worker
    from cancel_state import get_event
    return run_search_worker('page-characters',str(path),{'page':page_index},get_event(),timeout=120)
