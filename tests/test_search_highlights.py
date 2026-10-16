"""Real GTK/Cairo rendering checks for the independent highlight preference."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_regressions import APP, make_pdf
sys.path.insert(0, str(APP))


@unittest.skipUnless(os.environ.get('DISPLAY'), 'Requires an X display')
class SearchHighlightGUITests(unittest.TestCase):
    def test_queued_navigation_does_not_touch_destroyed_widgets(self):
        from main import PDFWindow, Gtk, GLib
        from test_gui import wait_for

        with tempfile.TemporaryDirectory() as directory, patch.object(Gtk, 'main_quit'):
            path = Path(directory) / 'closed.pdf'
            make_pdf(path, ['alvo primeiro alvo segundo'])
            window = PDFWindow(str(path))
            try:
                wait_for(lambda: window.displayed_page == 0 and window.current_pixbuf)
                window.find_entry.set_text('alvo')
                wait_for(lambda: not window.search_running and len(window.search_hits) == 2)
                window._select_search_hit(1)
            finally:
                window.destroy()
            errors = []
            with patch.object(sys, 'excepthook', side_effect=lambda *error: errors.append(error)):
                context = GLib.MainContext.default()
                while context.pending():
                    context.iteration(False)
            self.assertEqual(errors, [])

    def test_closing_window_removes_pending_search(self):
        from main import PDFWindow, Gtk, GLib
        from test_gui import wait_for

        with tempfile.TemporaryDirectory() as directory, patch.object(Gtk, 'main_quit'):
            path = Path(directory) / 'pending.pdf'
            make_pdf(path, ['alvo'])
            window = PDFWindow(str(path))
            try:
                wait_for(lambda: window.displayed_page == 0 and window.current_pixbuf)
                window.find_entry.set_text('alvo')
                pending = window.search_timer
                self.assertIsNotNone(pending)
            finally:
                window.destroy()
            self.assertIsNone(GLib.MainContext.default().find_source_by_id(pending))

    def test_highlight_preference_and_navigation_change_pixels_without_new_search(self):
        import cairo
        from main import PDFWindow, Gtk
        from test_gui import wait_for

        with tempfile.TemporaryDirectory() as directory, patch.object(Gtk, 'main_quit'):
            path = Path(directory) / 'highlights.pdf'
            make_pdf(path, ['alvo primeiro alvo segundo'])
            window = PDFWindow(str(path))
            try:
                wait_for(lambda: window.displayed_page == 0 and window.current_pixbuf)
                window.find_entry.set_text('alvo')
                wait_for(lambda: not window.search_running and len(window.search_hits) == 2)
                hits = window.search_hits
                cancel = window.search_cancel

                def alphas():
                    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                                 window.current_pixbuf.get_width(),
                                                 window.current_pixbuf.get_height())
                    window._interaction_draw(window.interaction_layer, cairo.Context(surface))
                    surface.flush()
                    data = surface.get_data()
                    values = []
                    for hit in hits:
                        x0, y0, x1, y1 = window._pdf_rect_to_display(hit['rects'][0], hit)
                        offset = int((y0 + y1) / 2) * surface.get_stride() + int((x0 + x1) / 2) * 4
                        values.append(int.from_bytes(data[offset:offset + 4], sys.byteorder) >> 24)
                    return values

                self.assertTrue(window.find_highlight_all.get_active())
                self.assertTrue(all(alpha > 0 for alpha in alphas()))
                window.find_highlight_all.set_active(False)
                self.assertGreater(alphas()[0], 0)
                self.assertEqual(alphas()[1], 0)
                window._find_next()
                self.assertEqual(alphas()[0], 0)
                self.assertGreater(alphas()[1], 0)
                window.find_highlight_all.set_active(True)
                self.assertTrue(all(alpha > 0 for alpha in alphas()))
                self.assertIs(window.search_hits, hits)
                self.assertIs(window.search_cancel, cancel)
                self.assertIsNone(window.search_timer)
                self.assertFalse(window.search_running)
            finally:
                window.destroy()
