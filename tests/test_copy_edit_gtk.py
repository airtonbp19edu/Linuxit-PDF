"""GTK dialogs and real worker writes; no original/reference PDF is executed."""
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter, PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
except (ImportError, ValueError):
    Gtk = GLib = None


def wait_for(predicate, timeout=20):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        context = GLib.MainContext.default()
        while context.pending():context.iteration(False)
        if predicate():return
        time.sleep(.02)
    raise AssertionError('GTK copy edit timeout')


def descendants(widget):
    yield widget
    if isinstance(widget, Gtk.Container):
        for child in widget.get_children():yield from descendants(child)


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')), 'Requires GTK3 and X11')
class CopyEditGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-copy-gtk-')
        self.root = Path(self.temp.name)
        self.source = self.root/'source.pdf'
        writer = PdfWriter()
        page = writer.add_blank_page(200, 200)
        writer.add_outline_item('Original', 0)
        font = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
            NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')}))
        field = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Annot'),
            NameObject('/Subtype'): NameObject('/Widget'), NameObject('/FT'): NameObject('/Tx'),
            NameObject('/T'): TextStringObject('name'), NameObject('/V'): TextStringObject('old'),
            NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/Rect'): ArrayObject([NumberObject(v) for v in (10, 20, 190, 40)])}))
        page[NameObject('/Annots')] = ArrayObject([field])
        writer.root_object[NameObject('/AcroForm')] = writer._add_object(DictionaryObject({
            NameObject('/Fields'): ArrayObject([field]), NameObject('/DR'): DictionaryObject({
                NameObject('/Font'): DictionaryObject({NameObject('/Helv'): font})})}))
        writer.write(self.source)
        self.original = self.source.read_bytes()
        self.callback_errors, self.errors = [], []
        self.hook = patch.object(sys, 'excepthook', lambda *error: self.callback_errors.append(error))
        self.hook.start()
        self.quit = patch.object(Gtk, 'main_quit')
        self.quit.start()
        load_css()
        self.window = PDFWindow()
        self.window._error = self.errors.append
        self.window.open_document(str(self.source))
        wait_for(lambda: self.window.page_count == 1 and self.window.current_pixbuf is not None)

    def tearDown(self):
        self.window.destroy()
        self.quit.stop()
        self.hook.stop()
        self.temp.cleanup()
        self.assertEqual(self.callback_errors, [])

    def test_real_dialogs_and_worker_create_bookmark_note_and_form_copies(self):
        cases = [('add-bookmark', 'Novo marcador'), ('add-note', 'Adicionar nota'),
                 ('fill-text-fields', 'Preencher campo de texto')]
        for kind, title in cases:
            with self.subTest(kind=kind):
                target = self.root/(kind+'.pdf')
                def respond(title=title, kind=kind):
                    dialog = next((w for w in Gtk.Window.list_toplevels() if isinstance(w, Gtk.Dialog) and w.get_title() == title), None)
                    if dialog is None:return True
                    for widget in descendants(dialog):
                        if isinstance(widget, Gtk.Entry):widget.set_text('New value')
                        if isinstance(widget, Gtk.TextView):widget.get_buffer().set_text('New note')
                    dialog.response(Gtk.ResponseType.OK)
                    return False
                idle = GLib.timeout_add(20, respond)
                try:
                    with patch.object(self.window, '_copy_edit_destination_dialog', return_value=str(target)):
                        self.window._begin_copy_edit(kind)
                        wait_for(lambda: not self.window._copy_edit_busy and target.exists())
                finally:
                    if GLib.MainContext.default().find_source_by_id(idle):GLib.source_remove(idle)
                reader = PdfReader(target)
                if kind == 'add-bookmark':self.assertEqual([x.title for x in reader.outline], ['Original', 'New value'])
                elif kind == 'add-note':self.assertEqual(reader.pages[0]['/Annots'][-1].get_object()['/Contents'], 'New note')
                else:self.assertEqual(reader.get_fields()['name']['/V'], 'New value')
                self.assertEqual(self.window.filepath, str(self.source))
                self.assertEqual(self.source.read_bytes(), self.original)
        self.assertEqual(self.errors, [])

    def test_canceling_either_dialog_creates_nothing(self):
        for cancel_operation in (True, False):
            with patch.object(self.window, '_copy_edit_operation_dialog', return_value=None if cancel_operation else {
                    'kind':'add-bookmark','title':'not saved','page':0}), \
                 patch.object(self.window, '_copy_edit_destination_dialog', return_value=None):
                self.window._begin_copy_edit('add-bookmark')
                wait_for(lambda: not self.window._copy_edit_busy)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['source.pdf'])

    def test_reopening_same_document_during_dialog_blocks_stale_save(self):
        def during_dialog(*args):
            self.window.open_document(str(self.source))
            return {'kind':'add-bookmark','title':'stale','page':0}
        with patch.object(self.window, '_copy_edit_operation_dialog', side_effect=during_dialog), \
             patch.object(self.window, '_copy_edit_destination_dialog') as destination:
            self.window._begin_copy_edit('add-bookmark')
            wait_for(lambda: self.window.page_count == 1 and not self.window._copy_edit_busy)
            destination.assert_not_called()
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['source.pdf'])

    def test_existing_destination_is_preserved_and_busy_state_is_released(self):
        target = self.root/'existing.pdf'
        target.write_bytes(b'keep')
        with patch.object(self.window, '_copy_edit_operation_dialog', return_value={
                'kind':'add-bookmark','title':'copy','page':0}), \
             patch.object(self.window, '_copy_edit_destination_dialog', return_value=str(target)):
            self.window._begin_copy_edit('add-bookmark')
            wait_for(lambda: not self.window._copy_edit_busy)
        self.assertEqual(target.read_bytes(), b'keep')
        self.assertIn('nome novo', self.errors[-1])

    def test_repeated_clicks_do_not_queue_multiple_writes(self):
        target = self.root/'once.pdf'
        with patch.object(self.window, '_copy_edit_operation_dialog', return_value={
                'kind':'add-bookmark','title':'once','page':0}) as operation, \
             patch.object(self.window, '_copy_edit_destination_dialog', return_value=str(target)):
            self.window._begin_copy_edit('add-bookmark')
            self.window._begin_copy_edit('add-bookmark')
            wait_for(lambda: not self.window._copy_edit_busy and target.exists())
            self.assertEqual(operation.call_count, 1)
        self.assertEqual(len(PdfReader(target).outline), 2)


if __name__ == '__main__':unittest.main()
