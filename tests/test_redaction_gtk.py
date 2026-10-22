"""E15: the edit draft applies its redaction marks in a new copy; the confirmation dialog picks the DPI."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from test_copy_edit_gtk import Gtk, wait_for, descendants
from test_redaction_apply import SECRET, all_decoded, fixture


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class RedactionDraftGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow,load_css
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-redaction-gtk-');self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(fixture());self.original=self.source.read_bytes()
        self.callback_errors=[];self.hook=patch.object(sys,'excepthook',lambda *e:self.callback_errors.append(e));self.hook.start()
        self.quit=patch.object(Gtk,'main_quit');self.quit.start();load_css()
        self.parent=PDFWindow();self.parent.open_document(str(self.source))
        wait_for(lambda:self.parent.page_count==2 and self.parent.current_pixbuf is not None)
        self.parent._show_edit_draft();self.window=self.parent.edit_window
        wait_for(lambda:self.window.session is not None and not self.window.busy)

    def tearDown(self):
        if not self.window.closed:self.window.destroy()
        self.parent.destroy();self.quit.stop();self.hook.stop();self.temp.cleanup()
        self.assertEqual(self.callback_errors,[])

    def test_marks_in_the_draft_are_applied_to_a_new_copy(self):
        self.assertFalse(self.window.redact_button.get_sensitive())
        operation={'kind':'add-redaction','page':0,'rect':[30,185,240,225],'text':'CPF'}
        with patch.object(self.parent,'_copy_edit_operation_dialog',return_value=operation):self.window.add_button.clicked()
        wait_for(lambda:not self.window.busy and self.window.session.cursor==1)
        self.assertTrue(self.window.redact_button.get_sensitive())
        target=self.root/'redigido.pdf'
        with patch('edit_dialogs.redaction_apply_dialog',return_value=150),\
             patch.object(self.window,'_choose_destination',return_value=str(target)):
            self.window.redact_button.clicked()
        wait_for(lambda:not self.window.busy and target.exists(),timeout=60)
        self.assertIn('Redação aplicada',self.window.status.get_text())
        self.assertNotIn(SECRET,all_decoded(target))
        self.assertEqual(self.source.read_bytes(),self.original);self.assertEqual(self.window.session.cursor,1)

    def test_confirmation_dialog_returns_the_chosen_resolution(self):
        from edit_dialogs import redaction_apply_dialog
        seen={}
        def run(dialog):
            combo=next(w for w in descendants(dialog) if isinstance(w,Gtk.ComboBoxText) and w.get_accessible().get_name()=='Resolução das páginas redigidas')
            seen['text']=' '.join(w.get_text() for w in descendants(dialog) if isinstance(w,Gtk.Label))
            combo.set_active_id('300');return Gtk.ResponseType.OK
        with patch.object(Gtk.Dialog,'run',run):self.assertEqual(redaction_apply_dialog(self.window,2),300)
        self.assertIn('2 área(s) marcada(s)',seen['text']);self.assertIn('vira uma imagem',seen['text'])
        with patch.object(Gtk.Dialog,'run',lambda dialog:Gtk.ResponseType.CANCEL):
            self.assertIsNone(redaction_apply_dialog(self.window,1))


    def test_confirmation_explicit_vector_method_disables_raster_resolution(self):
        from edit_dialogs import redaction_apply_dialog
        def run(dialog):
            controls={w.get_accessible().get_name():w for w in descendants(dialog) if isinstance(w,Gtk.ComboBoxText)}
            controls['Método de redação'].set_active_id('vector')
            self.assertFalse(controls['Resolução das páginas redigidas'].get_sensitive())
            return Gtk.ResponseType.OK
        with patch.object(Gtk.Dialog,'run',run):self.assertEqual(redaction_apply_dialog(self.window,1),{'mode':'vector','dpi':150})


if __name__=='__main__':unittest.main()
