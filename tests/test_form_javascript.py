"""Real QuickJS field calculations and transactional/adversarial boundaries."""
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_form_javascript import run_form_javascript
from pdf_changes import save_edited_copy
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from pypdf.generic import DictionaryObject,NameObject,TextStringObject,ArrayObject
from test_form_events import form_pdf


@unittest.skipUnless(importlib.util.find_spec('_quickjs'),'python-quickjs-ng not installed')
class JavaScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'form.pdf'

    def fixture(self,code,validation='event.rc = Number(event.value) >= 0;'):
        return form_pdf(self.path,code,validation)

    def save(self,values):
        output=self.path.with_name('out.pdf')
        return output,save_edited_copy(self.path,output,source_sha256=hashlib.sha256(self.path.read_bytes()).hexdigest(),
                                     operations=[dict(kind='fill-form-javascript',values=values)])

    def test_real_language_functions_arrays_conditions_and_calculated_field_roundtrip(self):
        code='const nums = ["a", "b"].map(n => Number(this.getField(n).value)); function total(x) { return x.reduce((a,b)=>a+b,0); } event.value = total(nums) > 5 ? total(nums) * 2 : 0;'
        self.fixture(code);before=self.path.read_bytes();output,_=self.save({'a':'2.5','b':'3.25'})
        fields=PdfReader(output).get_fields()
        self.assertEqual(str(fields['total']['/V']),'11.5');self.assertEqual(int(fields['total']['/Ff']),1)
        self.assertEqual(self.path.read_bytes(),before)

    def test_validation_failure_is_atomic_and_no_output_is_published(self):
        self.fixture('event.value = 20;')
        with self.assertRaisesRegex(ValueError,'Validação'):self.save({'a':'-1'})
        self.assertFalse(self.path.with_name('out.pdf').exists())

    def test_format_display_is_distinct_from_raw_field_value(self):
        writer,raws=self.fixture('event.value = Number(getField("a").value) * 2;')
        raws['total']['/AA'][NameObject('/F')]=DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject('event.value = "R$ " + Number(event.value).toFixed(2);')})
        writer.write(self.path);output,_=self.save({'a':'2.5'})
        reader=PdfReader(output)
        self.assertEqual(reader.get_fields()['total']['/V'],'5')
        self.assertIn(b'R$ 5.00',reader.pages[0]['/Annots'][2].get_object()['/AP']['/N'].get_data())

    def test_getfield_value_setter_updates_other_writable_fields(self):
        writer,_=self.fixture('this.getField("b").value = 12; event.value = Number(this.getField("b").value) + 1;')
        values,_=run_form_javascript(writer,{'a':'1'})
        self.assertEqual((values['b'],values['total']),('12','13'))

    def test_external_api_and_python_bridge_are_absent_even_through_function_constructor(self):
        writer,_=self.fixture('event.value = [typeof process,typeof require,typeof std,typeof os,typeof fetch,typeof XMLHttpRequest,typeof Python].join(",");')
        values,_=run_form_javascript(writer,{'a':'1'})
        self.assertEqual(values['total'],','.join(['undefined']*7))
        for script in ('event.value = this.getField.constructor("return process")().env;',
                       'event.value = std.loadFile("/etc/passwd");',
                       'event.value = app.launchURL("https://example.invalid");'):
            writer,_=self.fixture(script)
            with self.subTest(script=script),self.assertRaises(ValueError):run_form_javascript(writer,{'a':'1'})

    def test_endless_loop_cpu_limit_stops_transaction(self):
        writer,_=self.fixture('while (true) {}')
        start=time.monotonic()
        with self.assertRaisesRegex(ValueError,'interrupted|tempo|falhou'):run_form_javascript(writer,{'a':'1'})
        self.assertLess(time.monotonic()-start,8)

    def test_heap_and_recursion_budgets_fail_without_crashing_parent(self):
        for code in ('let a=[];for(;;)a.push(new Array(10000).fill("abcdefgh"));',
                     'function recurse(){return recurse()+1;} event.value=recurse();'):
            writer,_=self.fixture(code)
            with self.subTest(code=code),self.assertRaises(ValueError):run_form_javascript(writer,{'a':'1'})
        writer,_=self.fixture('event.value = 7;')
        self.assertEqual(run_form_javascript(writer,{'a':'1'})[0]['total'],'7')

    def test_calculation_order_and_helper_compatibility(self):
        writer,raws=self.fixture('AFSimple_Calculate("SUM", ["a", "b"]);','AFRange_Validate(true,0,true,100);')
        self.assertEqual(run_form_javascript(writer,{'a':'2','b':'3'})[0]['total'],'5')
        raws['b'][NameObject('/AA')]=DictionaryObject({NameObject('/C'):DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject('event.value = Number(getField("a").value) * 2;')})})
        writer.root_object['/AcroForm'][NameObject('/CO')]=ArrayObject([raws['b'].indirect_reference,raws['total'].indirect_reference])
        self.assertEqual(run_form_javascript(writer,{'a':'2'})[0]['total'],'6')

    def test_open_actions_and_document_scripts_are_not_executed(self):
        writer,_=self.fixture('event.value = 4;')
        writer.root_object[NameObject('/OpenAction')]=DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject('throw Error("OPEN ACTION RAN");')})
        self.assertEqual(run_form_javascript(writer,{'a':'1'})[0]['total'],'4')

    def test_invalid_targets_and_non_finite_values_are_refused(self):
        for code in ('event.value = NaN;','event.value = Infinity;','event.value = {};','event.value = "x".repeat(70000);'):
            writer,_=self.fixture(code)
            with self.subTest(code=code),self.assertRaises(ValueError):run_form_javascript(writer,{'a':'1'})
        writer,_=self.fixture('event.value = 5;')
        for values in ({'total':'1'},{'missing':'2'}):
            with self.assertRaises(ValueError):run_form_javascript(writer,values)


if __name__=='__main__':unittest.main()
