"""Reading transactions, geometry and presentation through actual GTK/Poppler."""
from io import BytesIO
import os
from pathlib import Path
import re
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_document_session import PdfReader, PdfWriter, text_pdf, DocumentSession
from test_search_extensions_gtk import Gtk, GLib, Gdk, wait_for, capture


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')), 'Requires GTK3 and X11')
class ReadingWorkflowsGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-reading-ui-')
        self.root = Path(self.temp.name)
        self.pdf = self.root / 'reading.pdf'; self.pdf.write_bytes(text_pdf(['alpha first page', 'beta second page']))
        self.quit = patch.object(Gtk, 'main_quit'); self.quit.start()
        self.errors = []
        self.excepthook = patch('sys.excepthook', lambda *args:self.errors.append(str(args[1]))); self.excepthook.start()
        self.w = PDFWindow(); self.w._error = self.errors.append
        self.w.open_document(str(self.pdf))
        wait_for(lambda:self.w.displayed_page == 0)
        self.children = []

    def tearDown(self):
        for child in self.children:child.destroy()
        self.w.destroy(); self.quit.stop(); self.excepthook.stop(); self.temp.cleanup()

    def encrypted(self):
        path = self.root / 'protected.pdf'
        writer = PdfWriter(clone_from=self.pdf)
        writer.encrypt('reading-secret', 'separate-owner', algorithm='AES-256')
        writer.write(path)
        return path

    def presentation(self, **kwargs):
        from presentation import PresentationWindow
        p = PresentationWindow(self.w, self.w.runner, self.w.filepath, self.w.page_sizes,
            self.w.page, self.w.cache_dir, session=self.w.document_session,
            rotation=self.w.rotation, **kwargs)
        self.children.append(p)
        wait_for(lambda:p.pixbuf is not None and not p._loading)
        return p

    def event(self, name, ctrl=False, shift=False):
        flags = (Gdk.ModifierType.CONTROL_MASK if ctrl else 0) | (Gdk.ModifierType.SHIFT_MASK if shift else 0)
        return SimpleNamespace(keyval=Gdk.keyval_from_name(name), state=flags)

    def test_failed_open_preserves_document_page_and_image(self):
        self.w.goto_page(1); wait_for(lambda:self.w.displayed_page == 1)
        old = self.w.current_pixbuf
        path = self.root / 'empty.pdf'; path.write_bytes(b'')
        self.w.open_document(str(path))
        wait_for(lambda:bool(self.errors))
        self.assertEqual(self.w.filepath, str(self.pdf))
        self.assertEqual((self.w.page, self.w.displayed_page), (1, 1))
        self.assertIs(self.w.current_pixbuf, old)

    def test_cancel_password_and_wrong_password_preserve_previous_document(self):
        path = self.encrypted(); before = path.read_bytes()
        answers = iter(('wrong', None)); prompts = []
        def prompt(_path, wrong):prompts.append(wrong); return next(answers)
        with patch.object(self.w, '_ask_document_password', side_effect=prompt):
            self.w.open_document(str(path))
            wait_for(lambda:len(prompts) == 2 and self.w._pending_document is None)
        self.assertEqual(prompts, [False, True])
        self.assertEqual(self.w.filepath, str(self.pdf)); self.assertEqual(before, path.read_bytes())
        self.assertEqual(self.errors, [])

    def test_authenticated_open_renders_searches_and_presents_without_mutating_source(self):
        path = self.encrypted(); before = path.read_bytes()
        with patch.object(self.w, '_ask_document_password', return_value='reading-secret'):
            self.w.open_document(str(path))
            wait_for(lambda:self.w.filepath == str(path) and self.w.displayed_page == 0)
        self.w.find_entry.set_text('beta')
        wait_for(lambda:not self.w.search_running and len(self.w.search_hits) == 1)
        self.assertEqual(self.w.search_hits[0]['page'], 1)
        self.w.goto_page(1); wait_for(lambda:self.w.displayed_page == 1)
        p = self.presentation(); self.assertEqual(p.page, 1)
        capture(self.w, 'reading-authenticated')
        self.assertEqual(before, path.read_bytes()); self.assertTrue(PdfReader(path).is_encrypted)
        self.assertEqual(self.errors, [])

    def test_recovery_decline_then_accept_preserves_original_and_content(self):
        path = self.root / 'broken-xref.pdf'
        path.write_bytes(re.sub(rb'(startxref\s+)\d+', rb'\g<1>1', self.pdf.read_bytes()))
        before = path.read_bytes()
        with patch.object(self.w, '_ask_document_recovery', return_value=False):
            self.w.open_document(str(path)); wait_for(lambda:self.w._pending_document is None)
        self.assertEqual(self.w.filepath, str(self.pdf))
        with patch.object(self.w, '_ask_document_recovery', return_value=True):
            self.w.open_document(str(path))
            wait_for(lambda:self.w.filepath == str(path) and self.w.displayed_page == 0)
        self.assertTrue(self.w.document_session.info['recovered'])
        self.assertEqual(before, path.read_bytes()); self.assertEqual(self.errors, [])

    def test_superseded_open_cannot_replace_newer_document_and_cleans_session(self):
        entered, release = threading.Event(), threading.Event(); sessions = []
        slow = self.root / 'slow.pdf'; slow.write_bytes(text_pdf(['slow candidate']))
        real = DocumentSession.prepare
        def prepare(session, *args):
            if session.source == str(slow):
                sessions.append(session); entered.set(); release.wait(8)
            return real(session, *args)
        try:
            with patch.object(DocumentSession, 'prepare', prepare):
                self.w.open_document(str(slow)); wait_for(entered.is_set)
                self.w.open_document(str(self.pdf)); release.set()
                wait_for(lambda:self.w._pending_document is None and self.w.filepath == str(self.pdf))
                wait_for(lambda:not sessions[0].root.exists())
            self.assertEqual(self.w.page_count, 2); self.assertEqual(self.errors, [])
        finally:release.set()

    def test_page_entries_clamp_and_restore_invalid_value_and_disable_edges(self):
        self.w.status_page_entry.set_text('999'); self.w.status_page_entry.emit('activate')
        wait_for(lambda:self.w.displayed_page == 1)
        self.assertEqual(self.w.status_page_entry.get_text(), '2')
        self.assertFalse(self.w._status_navigation[1].get_sensitive())
        self.w.status_page_entry.set_text('nan'); self.w.status_page_entry.emit('activate')
        self.assertEqual(self.w.status_page_entry.get_text(), '2')
        self.w.page_entry.set_text('-100'); self.w.page_entry.emit('activate')
        wait_for(lambda:self.w.displayed_page == 0)
        self.assertFalse(self.w._status_navigation[0].get_sensitive())

    def test_zoom_extremes_use_logical_surface_and_reject_nonfinite_input(self):
        large = self.root / 'letter.pdf'; writer = PdfWriter(); writer.add_blank_page(612, 792); writer.write(large)
        self.w.open_document(str(large)); wait_for(lambda:self.w.filepath == str(large) and self.w.displayed_page == 0)
        for value, expected in [('0%', 1), ('99999%', 6400), ('37,5%', 37.5)]:
            self.w.zoom_entry.set_text(value); self.w.zoom_entry.emit('activate')
            wait_for(lambda:not self.w._render_pending)
            self.assertEqual(self.w.zoom_percent, expected)
            width = self.w.page_image.display_size[0]
            self.assertAlmostEqual(width, 612 / 72 * 96 * expected / 100, delta=1)
            self.assertLessEqual(self.w.current_pixbuf.get_width() * self.w.current_pixbuf.get_height(), 40_000_000)
            self.assertLess(self.w.page_image.get_allocated_width(), 3000)
            if expected == 6400:
                adjustment = self.w.viewer_scroll.get_vadjustment()
                self.assertGreater(adjustment.get_upper(), 60000)
                adjustment.set_value(adjustment.get_upper() - adjustment.get_page_size())
                self.assertLess(self.w.page_overlay.offset()[1], -60000)
        self.w.zoom_entry.set_text('nan'); self.w.zoom_entry.emit('activate')
        self.assertEqual(self.w.zoom_percent, 37.5)
        self.w._fit_page(); wait_for(lambda:not self.w._render_pending)
        capture(self.w, 'reading-fit-page')
        self.assertEqual(self.errors, [])

    def test_rotated_cropbox_geometry_matches_selection_and_presentation(self):
        from pypdf.generic import RectangleObject
        path = self.root / 'crop-rotate.pdf'; writer = PdfWriter(clone_from=self.pdf)
        writer.pages[0].cropbox = RectangleObject([5, 10, 195, 180]); writer.pages[0].rotate(90); writer.write(path)
        self.w.open_document(str(path)); wait_for(lambda:self.w.filepath == str(path) and self.w.displayed_page == 0)
        for rotation in (0, 90, 180, 270):
            self.w.rotation = rotation; self.w._fit_page(); wait_for(lambda:not self.w._render_pending)
            data = {'width':170, 'height':190}; rectangle = [12, 17, 48, 39]
            restored = self.w._display_rect_to_pdf(self.w._pdf_rect_to_display(rectangle, data), data)
            for expected, actual in zip(rectangle, restored):self.assertAlmostEqual(expected, actual)
        p = self.presentation()
        self.assertEqual(p.rotation, 270); self.assertEqual(self.errors, [])

    def test_presentation_keys_respect_control_focus_and_restore_parent_focus(self):
        self.w.interaction_layer.grab_focus(); focus = self.w.get_focus()
        p = self.presentation(); p.canvas.grab_focus()
        p._key(p, self.event('Right')); wait_for(lambda:p.page == 1 and not p._loading)
        p._key(p, self.event('F6'))
        self.assertIsNot(p.get_focus(), p.canvas)
        self.assertFalse(p._key(p, self.event('Left'))); self.assertEqual(p.page, 1)
        p._key(p, self.event('F6')); self.assertIs(p.get_focus(), p.canvas)
        p._key(p, self.event('Escape'))
        self.assertTrue(p._closed); self.assertIs(self.w.get_focus(), focus)

    def test_monitor_selection_removal_and_fullscreen_request(self):
        p = self.presentation()
        self.assertTrue(p.fullscreen_requested)
        def monitor(w, h):return SimpleNamespace(get_geometry=lambda:SimpleNamespace(width=w,height=h))
        monitors = [monitor(1280, 800), monitor(1920, 1080)]
        display = SimpleNamespace(get_n_monitors=lambda:len(monitors), get_monitor=lambda i:monitors[i],
            get_monitor_at_window=lambda _:monitors[0], get_primary_monitor=lambda:monitors[0])
        with patch.object(p, '_display', display), patch.object(p, 'fullscreen_on_monitor') as request, patch.object(p, 'unfullscreen'):
            p._refresh_monitors(preferred=1); p._fullscreen_on_selected_monitor()
            self.assertEqual(request.call_args.args[1], 1)
            self.assertTrue(p.monitor_combo.get_visible())
            monitors.pop(); p._monitors_changed()
            self.assertEqual(p.monitor_combo.get_active_id(), '0')
            self.assertEqual(request.call_args.args[1], 0)
            self.assertFalse(p.monitor_combo.get_visible())

    def test_document_close_cancels_open_and_resets_controls(self):
        session = self.w.document_session
        self.w._close_document()
        self.assertIsNone(self.w.filepath); self.assertFalse(self.w.zoom_entry.get_sensitive())
        self.assertTrue(session.closed); self.assertEqual(self.w.status_page_entry.get_text(), '0')
        self.assertFalse(any(button.get_sensitive() for button in self.w._status_navigation))

    def test_first_render_failure_does_not_commit_candidate(self):
        new = self.root / 'new.pdf'; new.write_bytes(text_pdf(['new candidate']))
        from main import render_page
        def broken(path, *args, **kwargs):
            if str(path) == str(new):raise RuntimeError('synthetic first-render failure')
            return render_page(path, *args, **kwargs)
        with patch('main.render_page', side_effect=broken):
            self.w.open_document(str(new)); wait_for(lambda:bool(self.errors))
        self.assertEqual(self.w.filepath, str(self.pdf))
        self.assertEqual(self.w.displayed_page, 0)
