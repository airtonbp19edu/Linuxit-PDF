#!/usr/bin/env python3
"""Measure own GTK sidebar geometry; observation mode never claims a passing layout."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))


def settle(seconds=.15):
    from gi.repository import GLib
    until = time.monotonic() + seconds
    while time.monotonic() < until:
        context = GLib.MainContext.default()
        for _ in range(100):
            if not context.pending():
                break
            context.iteration(False)
        time.sleep(.01)


def rect(widget, window):
    point = widget.translate_coordinates(window, 0, 0)
    if point is None:
        raise ValueError('Unrealized widget')
    x, y = point[-2:]
    return [x, y, widget.get_allocated_width(), widget.get_allocated_height()]


def contained(inner, outer):
    x, y, w, h = inner
    a, b, width, height = outer
    return x >= a - 1 and y >= b - 1 and x + w <= a + width + 1 and y + h <= b + height + 1


def snapshot(window):
    page = window.sidebar_notebook.get_current_page()
    wrapper = window.sidebar_notebook.get_nth_page(page)
    header = wrapper.get_children()[0]
    label, close = header.get_children()
    sidebar = rect(window.sidebar_container, window)
    notebook = rect(window.sidebar_notebook, window)
    title = rect(label, window)
    title_pixels = label.get_layout().get_pixel_size()
    buttons = [rect(button, window) for button in window.sidebar_rail_buttons]
    checks = {'sidebar_meets_minimum_width': sidebar[2] >= window.sidebar_container.get_preferred_width()[0],
              'rail_buttons_visible': all(contained(button, sidebar) for button in buttons),
              'title_visible_in_sidebar': contained(title, sidebar),
              'title_visible_in_notebook': contained(title, notebook),
              'title_text_fits': title_pixels[0] <= title[2],
              'close_button_visible': contained(rect(close, window), sidebar),
              'viewer_has_space': window.viewer_scroll.get_allocated_width() >= 180}
    return {'panel': label.get_text(), 'window_size': list(window.get_size()),
            'sidebar': sidebar, 'notebook': notebook, 'title': title, 'title_pixels': list(title_pixels),
            'rail_buttons': buttons, 'sidebar_minimum': window.sidebar_container.get_preferred_width()[0],
            'paned_position': window.body_paned.get_position(), 'checks': checks, 'passed': all(checks.values())}


def show_panel(window, index):
    # Select through the same application method, preserving click-to-hide semantics.
    if not window.sidebar_visible or window.sidebar_notebook.get_current_page() != index:
        window._show_side_panel(index)
    settle()
    return snapshot(window)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--screenshots', required=True, type=Path)
    parser.add_argument('--observe-only', action='store_true')
    args = parser.parse_args()
    if args.output.exists() or args.screenshots.exists():
        parser.error('Use new paths to preserve prior measurements')
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    sys.path.insert(0, str(APP))
    from main import PDFWindow, load_css
    errors, scenarios, images = [], [], []
    args.screenshots.mkdir(parents=True)
    with patch.object(Gtk, 'main_quit'), patch.object(sys, 'excepthook', lambda *error: errors.append(str(error[1]))):
        load_css()
        window = PDFWindow()
        try:
            window.open_document(str(ROOT / 'testes/fixtures/busca-escopos.pdf'))
            deadline = time.monotonic() + 15
            while (window.current_pixbuf is None or window.page_count != 2) and time.monotonic() < deadline:
                settle(.05)
            if window.current_pixbuf is None:
                raise RuntimeError('Own PDF did not render')
            for width in (1180, 760):
                window.resize(width, 780 if width == 1180 else 500)
                settle(.3)
                for index in range(5):
                    scenarios.append(show_panel(window, index))
                    if width == 1180 and index in (0, 4):
                        pixbuf = Gdk.pixbuf_get_from_window(window.get_window(), 0, 0, window.get_allocated_width(), window.get_allocated_height())
                        path = args.screenshots / ('sidebar-' + str(index) + '.png')
                        pixbuf.savev(str(path), 'png', [], [])
                        images.append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        finally:
            window.destroy()
            settle(.05)
    result = {'schema': 'linuxit-sidebar-layout-v1', 'date_local': datetime.now(timezone(timedelta(hours=-3))).isoformat(),
              'app_main_sha256': hashlib.sha256((APP / 'main.py').read_bytes()).hexdigest(),
              'observation_only': args.observe_only, 'scenarios': scenarios, 'screenshots': images,
              'errors': errors, 'passed': len(scenarios) == 10 and all(s['passed'] for s in scenarios) and not errors,
              'original_executed': False, 'foxit_differential_test': False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': result['passed'], 'scenarios_passed': sum(s['passed'] for s in scenarios), 'errors': errors}))
    return 0 if args.observe_only or result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
