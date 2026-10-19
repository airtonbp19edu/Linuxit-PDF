"""Metadata panels for Linuxit PDF.

Uses pypdf in a background worker to expose document navigation structures
without touching GTK.  This module uses no external viewer assets.
"""
from pathlib import Path
import sys

VENDOR = Path(__file__).resolve().parent / 'vendor'
if str(VENDOR) not in sys.path:
    sys.path.insert(0, str(VENDOR))

from pypdf import PdfReader  # type: ignore  # noqa: E402
from pdf_comments import inspect_comments
from pdf_layers import inspect_layers


def _obj(value):
    try:
        return value.get_object()
    except Exception:
        return value


def _text(value):
    if value is None:
        return ''
    try:
        return str(value)
    except Exception:
        return ''


def inspect_document_panels(path, cancel=None):
    reader = PdfReader(path)
    if reader.is_encrypted:
        try:
            reader.decrypt('')
        except Exception:
            return {'bookmarks': [], 'comments': [], 'layers': []}

    bookmarks = []

    def walk_outline(items, level=0):
        for item in items or []:
            if cancel is not None and cancel.is_set():
                return
            if isinstance(item, list):
                walk_outline(item, level + 1)
                continue
            title = _text(getattr(item, 'title', '') or item)
            page = None
            try:
                page = reader.get_destination_page_number(item)
            except Exception:
                pass
            if title:
                bookmarks.append({'title': title, 'page': page, 'level': level,
                                  'item_id': 'bookmark:' + str(len(bookmarks))})

    try:
        walk_outline(reader.outline, 0)
    except Exception:
        pass

    comments, notices = inspect_comments(reader, cancel)

    layers = []
    try:
        layers=inspect_layers(reader)
    except Exception:
        notices.append('Camadas inválidas ou acima do limite; painel parcial.')

    return {'bookmarks': bookmarks, 'comments': comments, 'layers': layers, 'notices': notices}
