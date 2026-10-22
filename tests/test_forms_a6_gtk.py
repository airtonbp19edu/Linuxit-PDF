"""Real GTK controls for explicit JavaScript authorization and own XFA layout."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))


@unittest.skipUnless(os.environ.get('DISPLAY') or os.name=='nt' and os.environ.get('LINUXIT_WINDOWS_GUI_TESTS'),'Requires GTK display')
class AdvancedFormsGTKTests(unittest.TestCase):
    def setUp(self):
        import gi
        gi.require_version('Gtk','3.0')
        from gi.repository import Gtk
        self.Gtk=Gtk
        self.parent=Gtk.Window();self.addCleanup(self.parent.destroy)

    def test_javascript_dialog_is_explicit_and_accepts_custom_script_configuration(self):
        from edit_dialogs import advanced_operation_dialog
        info=dict(text_fields=[dict(name='entry',value='1',read_only=False),dict(name='total',value='2',read_only=False)],
                  form_events=dict(rules=[],unsupported=[dict(field='total',event='/C',reason='Custom JavaScript')]))
        seen=[]
        def run(dialog):
            queue=[dialog]
            while queue:
                widget=queue.pop()
                if isinstance(widget,self.Gtk.Container):queue.extend(widget.get_children())
                if isinstance(widget,self.Gtk.Label):seen.append(widget.get_text())
                if isinstance(widget,self.Gtk.Entry):widget.set_text('5')
            return self.Gtk.ResponseType.OK
        with patch('pdf_form_javascript.available',return_value=True),patch.object(self.Gtk.Dialog,'run',run):
            operation=advanced_operation_dialog(self.parent,'fill-form-javascript',info,0)
        self.assertEqual(operation,dict(kind='fill-form-javascript',values={'entry':'5'}))
        self.assertTrue(any('autoriza' in text and 'QuickJS' in text for text in seen))

    def test_xfa_flow_window_loads_fields_and_disables_value_changes_during_instance_operation(self):
        from xfa_window import XFAFlowWindow
        with patch.object(XFAFlowWindow,'_submit'):
            window=XFAFlowWindow(self.parent,'sample.pdf',lambda _:None)
        self.addCleanup(window.destroy)
        window.busy=False
        window._loaded(dict(source_sha256='a'*64,fields=[dict(path='form1[0].nome[0]',value='Ana')],
                            groups=[dict(path='form1[0].item',count=2,minimum=0,maximum=10)]))
        self.assertEqual(window.entries[0][1].get_text(),'Ana')
        window.action.set_active_id('add')
        self.assertFalse(window.grid.get_sensitive());self.assertTrue(window.group.get_sensitive())
        self.assertEqual(window.index.get_adjustment().get_upper(),3)
        window.action.set_active_id('values');self.assertTrue(window.grid.get_sensitive())

    def test_missing_quickjs_dependency_refuses_before_any_dialog_is_run(self):
        from edit_dialogs import advanced_operation_dialog
        with patch('pdf_form_javascript.available',return_value=False),patch.object(self.Gtk.Dialog,'run',side_effect=AssertionError('opened')):
            with self.assertRaisesRegex(ValueError,'quickjs'):
                advanced_operation_dialog(self.parent,'fill-form-javascript',dict(text_fields=[],form_events={}),0)


if __name__=='__main__':unittest.main()
