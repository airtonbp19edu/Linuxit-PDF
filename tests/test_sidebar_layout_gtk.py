"""GTK allocation regressions for the sidebar; generated PDF fixtures only."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(APP))
from check_sidebar_layout import settle, show_panel, snapshot

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except (ImportError, ValueError):
    Gtk = None


@unittest.skipUnless(Gtk is not None and os.environ.get('DISPLAY'), 'Requires GTK 3 and X11')
class SidebarLayoutTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-sidebar-')
        self.addCleanup(self.temp.cleanup)
        self.quit_patch = patch.object(Gtk, 'main_quit')
        self.quit_patch.start()
        self.addCleanup(self.quit_patch.stop)
        self.callback_errors = []
        self.hook_patch = patch.object(sys, 'excepthook', lambda *error: self.callback_errors.append(str(error[1])))
        self.hook_patch.start()
        self.addCleanup(self.hook_patch.stop)
        load_css()
        self.window = PDFWindow()
        self.addCleanup(self.window.destroy)
        self.window.open_document(str(ROOT / 'testes/fixtures/busca-escopos.pdf'))
        self.wait_for(lambda: self.window.current_pixbuf is not None and self.window.page_count == 2)

    def wait_for(self, predicate):
        import time
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            settle(.03)
            if predicate():
                return
        self.fail('Sidebar GTK state did not settle')

    def assert_layout(self, state):
        self.assertGreaterEqual(state['sidebar'][0], 0)
        self.assertGreaterEqual(state['title'][0], 0)
        self.assertTrue(all(button[0] >= 0 for button in state['rail_buttons']))
        self.assertTrue(state['passed'], str(state))
        self.assertEqual(self.callback_errors, [])

    def test_five_panel_headers_fit_default_and_small_window(self):
        for width, height in ((1180, 780), (760, 500)):
            self.window.resize(width, height)
            settle(.2)
            for index in range(5):
                with self.subTest(width=width, panel=index):
                    self.assert_layout(show_panel(self.window, index))

    def test_divider_hide_show_and_reading_restore_keep_controls_visible(self):
        window = self.window
        window.body_paned.set_position(1)
        settle()
        self.assert_layout(snapshot(window))
        window._toggle_sidebar()
        settle()
        self.assertFalse(window.sidebar_container.get_visible())
        self.assertGreater(window.viewer_scroll.get_allocated_width(), 180)
        window._toggle_sidebar()
        settle()
        self.assert_layout(snapshot(window))
        window._reading_mode_toggle()
        settle()
        self.assertFalse(window.sidebar_container.get_visible())
        window._reading_mode_toggle()
        settle()
        self.assert_layout(snapshot(window))

    def test_long_attachment_name_keeps_header_and_save_button_inside_panel(self):
        from pdf_dependency import configure_pdf_library
        configure_pdf_library()
        from pypdf import PdfWriter
        from check_sidebar_layout import contained, rect
        path = Path(self.temp.name) / 'long-attachment.pdf'
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.add_attachment('a' * 160 + '.txt', b'Own geometry fixture')
        writer.write(path)
        window = self.window
        window.open_document(str(path))
        show_panel(window, 4)
        self.wait_for(lambda: window.attachment_controller.source_sha256 is not None)
        for width in (1180, 760):
            window.resize(width, 780)
            settle(.2)
            state = snapshot(window)
            self.assert_layout(state)
            self.assertTrue(contained(rect(window.attachment_save, window), state['notebook']))
            self.assertTrue(window.attachment_save.get_sensitive())


if __name__ == '__main__':
    unittest.main()
