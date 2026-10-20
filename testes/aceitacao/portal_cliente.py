#!/usr/bin/env python3
"""Child program for S12-25: the real 'open with system chooser' action of PDFWindow.

argv: <app folder> <current pdf>. Opens the current document, then calls
PDFWindow._choose_open_native, which blocks in the portal dialog that the
parent case drives. Prints one LINUXIT_PORTAL_CASE line with the outcome.
"""
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch

app, current = Path(sys.argv[1]), sys.argv[2]
sys.path.insert(0, str(app))
import rendering  # noqa: E402,F401 - activates the vendored pypdf as the application does
import gi  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk  # noqa: E402
from main import PDFWindow, load_css  # noqa: E402


def pump(predicate, timeout=20):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        context = GLib.MainContext.default()
        while context.pending():
            context.iteration(False)
        if predicate():
            return True
        time.sleep(.02)
    return False


with patch.object(Gtk, 'main_quit'):
    load_css()
    window, errors = PDFWindow(), []
    window._error = errors.append
    window.open_document(current)
    pump(lambda: window.page_count > 0 and window.current_pixbuf is not None)
    before = window.filepath
    print('LINUXIT_CHOOSER_READY', flush=True)
    window._choose_open_native()
    pump(lambda: window.filepath != before and window.page_count > 0 and window.current_pixbuf is not None, 15)
    pump(lambda: False, .5)
    result = dict(before=before, after=window.filepath, pages=window.page_count, errors=errors,
                  status=window.status_file.get_text())
    print('LINUXIT_PORTAL_CASE ' + json.dumps(result, ensure_ascii=False), flush=True)
    window.destroy()
