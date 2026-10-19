"""Real GTK attachment workflow tests; explicitly skipped without GTK/display."""
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))
sys.path.insert(0, str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, RectangleObject

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
except (ImportError, ValueError):
    Gtk = GLib = None

GUI_AVAILABLE = Gtk is not None and bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))


def wait_for(predicate, timeout=15):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        context = GLib.MainContext.default()
        while context.pending():
            context.iteration(False)
        if predicate():
            return
        time.sleep(.02)
    raise AssertionError('GTK attachment workflow timeout')


class FolderChoice:
    def __init__(self, response, folder, during_dialog=None):
        self.response, self.folder, self.during_dialog = response, folder, during_dialog
        self.destroyed = False
    def add_buttons(self, *args):
        pass
    def set_modal(self, value):
        pass
    def set_destroy_with_parent(self, value):
        pass
    def set_current_folder(self, folder):
        self.initial_folder = folder
        return True
    def add_shortcut_folder(self, folder):
        self.shortcut_folder = folder
        return True
    def run(self):
        if self.during_dialog:
            self.during_dialog()
        return self.response
    def get_filename(self):
        return str(self.folder)
    def destroy(self):
        self.destroyed = True


@unittest.skipUnless(GUI_AVAILABLE, 'Requires GTK 3 and a real X11/Wayland display')
class AttachmentGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-attachment-gtk-')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.pdf = self.root / 'attached.pdf'
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.add_attachment('note.txt', b'GTK attachment bytes')
        writer.add_attachment('../unsafe.txt', b'not extracted')
        writer.write(self.pdf)
        self.output = self.root / 'output'
        self.output.mkdir()
        self.quit_patch = patch.object(Gtk, 'main_quit')
        self.quit_patch.start()
        self.callback_errors = []
        self.hook_patch = patch.object(sys, 'excepthook',
                                      lambda *error: self.callback_errors.append(error))
        self.hook_patch.start()
        self.addCleanup(self.hook_patch.stop)
        load_css()
        self.errors = []
        self.window = PDFWindow()
        self.window._error = self.errors.append
        self.window.open_document(str(self.pdf))
        wait_for(lambda: self.window.page_count == 1 and self.window.current_pixbuf is not None)
        self.assertFalse(self.window.attachment_controller.requested)
        self.window._show_side_panel(4)
        wait_for(lambda: self.window.attachment_controller.source_sha256 is not None)
        self.assertTrue(self.window.sidebar_visible)
        self.assertEqual(self.window.sidebar_notebook.get_current_page(), 4)

    def tearDown(self):
        self.window.destroy()
        self.quit_patch.stop()
        self.temp.cleanup()
        self.assertEqual(self.callback_errors, [], 'Unhandled exception in GTK signal callback')

    def test_sidebar_buttons_switch_hide_and_restore_without_recursive_callbacks(self):
        window = self.window
        for index in (1, 0, 4):
            window.sidebar_rail_buttons[index].clicked()
            self.assertTrue(window.sidebar_visible)
            self.assertEqual(window.sidebar_notebook.get_current_page(), index)
            self.assertEqual([button.get_active() for button in window.sidebar_rail_buttons],
                             [i == index for i in range(5)])
        window.sidebar_rail_buttons[4].clicked()
        self.assertFalse(window.sidebar_visible)
        self.assertFalse(any(button.get_active() for button in window.sidebar_rail_buttons))
        window._toggle_sidebar()
        self.assertTrue(window.sidebar_visible)
        self.assertTrue(window.sidebar_rail_buttons[4].get_active())

    def test_panel_saves_selected_file_and_shows_conflict_without_overwrite(self):
        self.assertEqual(len(self.window.attachment_list.get_children()), 2)
        self.assertTrue(self.window.attachment_save.get_sensitive())
        for _ in range(2):
            chooser = FolderChoice(Gtk.ResponseType.OK, self.output)
            with patch('main.Gtk.FileChooserDialog', return_value=chooser):
                self.window._save_selected_attachment()
            wait_for(lambda: not self.window.attachment_controller.extracting)
            self.assertTrue(chooser.destroyed)
            self.assertEqual((self.output / 'note.txt').read_bytes(), b'GTK attachment bytes')
        self.assertIn('Escolha outra pasta', self.window.attachment_status.get_text())
        self.assertEqual(self.errors, [])

    def test_cancelled_folder_dialog_writes_nothing(self):
        chooser = FolderChoice(Gtk.ResponseType.CANCEL, self.output)
        with patch('main.Gtk.FileChooserDialog', return_value=chooser):
            self.window._save_selected_attachment()
        self.assertFalse(self.window.attachment_controller.extracting)
        self.assertEqual(list(self.output.iterdir()), [])
        self.assertTrue(chooser.destroyed)

    def test_document_change_during_folder_dialog_invalidates_selection(self):
        other = self.root / 'other.pdf'
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.write(other)
        chooser = FolderChoice(Gtk.ResponseType.OK, self.output,
                               during_dialog=lambda: self.window.open_document(str(other)))
        with patch('main.Gtk.FileChooserDialog', return_value=chooser):
            self.window._save_selected_attachment()
        wait_for(lambda: self.window.filepath == str(other) and self.window.page_count == 1)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_unsafe_selected_row_disables_saving(self):
        entry = next(item for item in self.window.attachment_controller.items if not item['filename_allowed'])
        self.window.attachment_list.select_row(self.window._attachment_rows[entry['index']])
        self.assertFalse(self.window.attachment_save.get_sensitive())
        self.assertIsNone(self.window.attachment_controller.selection_token())

    def test_nested_catalog_and_annotation_attachment_save_through_real_worker(self):
        writer = PdfWriter()
        writer.add_blank_page(100, 100)
        writer.add_attachment('nested.txt', b'nested catalog')
        writer.add_attachment('page-note.txt', b'page attachment')
        tree = writer.root_object['/Names']['/EmbeddedFiles']
        pairs = tree.pop('/Names')
        leaf = writer._add_object(DictionaryObject({NameObject('/Names'): ArrayObject(pairs[:2])}))
        tree[NameObject('/Kids')] = ArrayObject([DictionaryObject({NameObject('/Kids'): ArrayObject([leaf])})])
        writer.pages[0][NameObject('/Annots')] = ArrayObject([DictionaryObject({
            NameObject('/Subtype'): NameObject('/FileAttachment'), NameObject('/FS'): pairs[3],
            NameObject('/Rect'): RectangleObject([0, 0, 10, 10])})])
        target = self.root / 'nested.pdf'
        writer.write(target)
        self.window.open_document(str(target))
        # The panel is already visible from setUp; clicking it again hides it.
        # Opening the next document must refresh that visible panel automatically.
        wait_for(lambda: self.window.filepath == str(target)
                 and self.window.attachment_controller.source_sha256 is not None
                 and len(self.window.attachment_controller.items) == 2)
        self.assertEqual(self.window.filepath, str(target))
        self.assertTrue(self.window.sidebar_visible)
        items = self.window.attachment_controller.items
        self.assertEqual([i['name'] for i in items], ['nested.txt', 'page-note.txt'])
        self.assertEqual([(i['origin'], i['page']) for i in items], [('catalog', None), ('annotation', 0)])
        self.window.attachment_list.select_row(self.window._attachment_rows[1])
        chooser = FolderChoice(Gtk.ResponseType.OK, self.output)
        with patch('main.Gtk.FileChooserDialog', return_value=chooser):
            self.window._save_selected_attachment()
        wait_for(lambda: not self.window.attachment_controller.extracting)
        self.assertEqual((self.output / 'page-note.txt').read_bytes(), b'page attachment')


if __name__ == '__main__':
    unittest.main()
