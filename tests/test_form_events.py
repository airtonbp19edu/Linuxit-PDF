import hashlib,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,DictionaryObject,NameObject,NumberObject,TextStringObject
from pdf_form_events import inspect_form_events,calculate_form_values,parse_calculation,parse_validation
from pdf_changes import save_edited_copy,inspect_editable_document


def form_pdf(path,calculation='AFSimple_Calculate("SUM", ["a", "b"]);',validation='AFRange_Validate(true, 0, true, 100);'):
    writer=PdfWriter();page=writer.add_blank_page(400,300)
    font=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    refs=[];raws={}
    for index,name in enumerate(['a','b','total']):
        raw=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Widget'),NameObject('/FT'):NameObject('/Tx'),NameObject('/T'):TextStringObject(name),NameObject('/V'):TextStringObject('0'),NameObject('/DA'):TextStringObject('/Helv 10 Tf 0 g'),NameObject('/Ff'):NumberObject(int(name=='total')),NameObject('/Rect'):ArrayObject(NumberObject(v) for v in [10,20+index*40,200,40+index*40])})
        refs.append(writer._add_object(raw));raws[name]=raw
    def action(script):return DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject(script)})
    raws['total'][NameObject('/AA')]=DictionaryObject({NameObject('/C'):action(calculation)})
    raws['a'][NameObject('/AA')]=DictionaryObject({NameObject('/V'):action(validation)})
    page[NameObject('/Annots')]=ArrayObject(refs)
    writer.root_object[NameObject('/AcroForm')]=writer._add_object(DictionaryObject({NameObject('/Fields'):ArrayObject(refs),NameObject('/DA'):TextStringObject('/Helv 10 Tf 0 g'),NameObject('/DR'):DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/Helv'):font})})}))
    writer.write(path);return writer,raws


class FormEventTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'form.pdf';form_pdf(self.path)

    def test_calculation_and_range_validation_roundtrip_with_appearances_and_readonly_preserved(self):
        before=self.path.read_bytes();out=self.path.with_name('copy.pdf')
        save_edited_copy(self.path,out,source_sha256=hashlib.sha256(before).hexdigest(),operations=[dict(kind='fill-form-events',values={'a':'2.5','b':'3.25'})])
        reader=PdfReader(out);fields=reader.get_fields()
        self.assertEqual(str(fields['total']['/V']),'5.75');self.assertEqual(int(fields['total']['/Ff']),1)
        self.assertIn('/AP',reader.pages[0]['/Annots'][2].get_object());self.assertEqual(self.path.read_bytes(),before)

    def test_invalid_input_rejects_entire_copy_without_partial_publication(self):
        out=self.path.with_name('invalid.pdf');before=self.path.read_bytes()
        for values in ({'a':'101'},{'a':'-1'},{'a':'1,2'},{'a':'nan'},{'total':'8'}):
            with self.assertRaises(ValueError):save_edited_copy(self.path,out,source_sha256=hashlib.sha256(before).hexdigest(),operations=[dict(kind='fill-form-events',values=values)])
            self.assertFalse(out.exists());self.assertEqual(self.path.read_bytes(),before)

    def test_dependency_order_and_cycle_detection(self):
        writer,raws=form_pdf(self.path,'AFSimple_Calculate("PRD", ["b", "b"]);')
        self.assertEqual(calculate_form_values(writer,{'a':'1','b':'3'})['total'],'9')
        raws['total']['/AA']['/C'][NameObject('/JS')]=TextStringObject('AFSimple_Calculate("SUM", ["total"]);')
        with self.assertRaisesRegex(ValueError,'circular'):calculate_form_values(writer,{'a':'2'})

    def test_unknown_javascript_is_recorded_and_never_executed(self):
        writer,_=form_pdf(self.path,'app.launchURL("https://example.invalid");')
        inspected=inspect_form_events(writer);self.assertFalse(inspected['javascript_executed']);self.assertEqual(len(inspected['unsupported']),1)
        with self.assertRaisesRegex(ValueError,'não suportados'):calculate_form_values(writer,{'a':'2'})

    def test_all_five_helpers_and_new_array_syntax(self):
        expected={'SUM':'6','AVG':'3','PRD':'8','MIN':'2','MAX':'4'}
        for function,value in expected.items():
            writer,_=form_pdf(self.path,'AFSimple_Calculate("'+function+'", new Array("a", "b"));')
            self.assertEqual(calculate_form_values(writer,{'a':'2','b':'4'})['total'],value)

    def test_parser_rejects_code_expressions_extra_statements_and_oversized_values(self):
        for script in ('AFSimple_Calculate("SUM", [getField("x")]);','AFSimple_Calculate("SUM", ["a"]); evil();','AFSimple_Calculate("SUM", []);'):
            with self.assertRaises(ValueError):parse_calculation(script)
        with self.assertRaises(ValueError):parse_validation('event.rc = true')
        with self.assertRaises(ValueError):calculate_form_values(PdfReader(self.path),{'a':'9'*129})

    def test_inspection_exposes_rules_to_editor_without_mutation(self):
        before=self.path.read_bytes();info=inspect_editable_document(self.path)
        self.assertEqual(len(info['form_events']['rules']),2);self.assertEqual(info['form_events']['unsupported'],[])
        self.assertEqual(self.path.read_bytes(),before)


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK and X display')
class FormEventGUITests(unittest.TestCase):
    def test_dialog_produces_input_values_and_keeps_calculated_field_out_of_entries(self):
        from main import Gtk,GLib
        from edit_dialogs import advanced_operation_dialog
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'form.pdf';form_pdf(path);info=inspect_editable_document(path)
            parent=Gtk.Window();seen=[]
            def accept():
                dialog=next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog)),None)
                if dialog is None:return True
                def collect(widget):
                    if isinstance(widget,Gtk.Entry):seen.append(widget.get_accessible().get_name());widget.set_text('3')
                    if isinstance(widget,Gtk.Container):
                        for child in widget.get_children():collect(child)
                collect(dialog);dialog.response(Gtk.ResponseType.OK);return False
            GLib.timeout_add(30,accept)
            try:operation=advanced_operation_dialog(parent,'fill-form-events',info,0)
            finally:parent.destroy()
            self.assertEqual(set(seen),{'a','b'});self.assertEqual(operation['values'],{'a':'3','b':'3'})
