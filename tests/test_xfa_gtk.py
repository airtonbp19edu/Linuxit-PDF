"""E07: the fill dialog of a hybrid XFA form offers only fields bound to datasets."""
import os,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
FIXTURE=ROOT/'testes'/'aceitacao'/'fixtures'/'formulario-xfa.pdf'


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK3 and a display')
class XFAFillDialogTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow,Gtk
        from pdf_changes import inspect_editable_document
        self.Gtk=Gtk;self.quit=patch.object(Gtk,'main_quit');self.quit.start();self.addCleanup(self.quit.stop)
        self.window=PDFWindow();self.addCleanup(self.window.destroy)
        self.errors=[];self.window._error=self.errors.append
        self.info=inspect_editable_document(FIXTURE)

    def test_only_bound_fields_are_offered_and_value_reaches_the_operation(self):
        seen=[]
        def run(dialog):
            widgets=[];stack=[dialog]
            while stack:
                widget=stack.pop();widgets.append(widget)
                if isinstance(widget,self.Gtk.Container):stack.extend(widget.get_children())
            combo=next(w for w in widgets if isinstance(w,self.Gtk.ComboBoxText))
            seen.extend(row[0] for row in combo.get_model())
            seen.append(next(w.get_text() for w in widgets if isinstance(w,self.Gtk.Label) and 'XFA' in w.get_text()))
            next(w for w in widgets if isinstance(w,self.Gtk.Entry) and w is not combo.get_child()).set_text('Bia Lima')
            return self.Gtk.ResponseType.OK
        with patch.object(self.Gtk.Dialog,'run',run):
            operation=self.window._copy_edit_operation_dialog('fill-text-fields',self.info,0)
        self.assertEqual(seen[:-1],['form1[0].nome[0]']);self.assertIn('dados XFA',seen[-1])
        self.assertEqual(operation,{'kind':'fill-text-fields','values':{'form1[0].nome[0]':'Bia Lima'}})

    def test_other_edits_of_an_xfa_document_are_refused_before_any_dialog(self):
        with patch.object(self.Gtk.Dialog,'run',side_effect=AssertionError('dialog opened')):
            self.assertIsNone(self.window._copy_edit_operation_dialog('add-bookmark',self.info,0))
        self.assertIn('XFA',self.errors[0])


if __name__=='__main__':unittest.main()
