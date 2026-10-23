"""Extended API in the actual isolated QuickJS process, not a JS mock."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_form_javascript import run_form_javascript
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import NameObject, TextStringObject, NumberObject, DictionaryObject
from test_form_events import form_pdf


@unittest.skipUnless(importlib.util.find_spec('_quickjs'), 'QuickJS dependency absent')
class JavaScriptAPITests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'form.pdf'

    def fixture(self, script):
        return form_pdf(self.path, script, 'event.rc = true;')

    def test_printf_numeric_string_padding_and_percent_escape(self):
        writer,_=self.fixture('event.value=util.printf("%06d|%.2f|%-5s|%%",-12,1.25,"ok");')
        self.assertEqual(run_form_javascript(writer,{'a':'1'})[0]['total'], '-00012|1.25|ok   |%')

    def test_field_properties_reset_defaults_and_calculation_read_new_value(self):
        writer,raws=self.fixture('this.resetForm(["b"]);const f=this.getField("b"); event.value=[f.type,f.defaultValue,f.charLimit,f.getArray()[0].name,f.valueAsString].join("|");')
        raws['b'][NameObject('/DV')]=TextStringObject('17');raws['b'][NameObject('/MaxLen')]=NumberObject(4)
        values,_=run_form_javascript(writer,{'a':'2','b':'33'})
        self.assertEqual(values['b'],'17');self.assertEqual(values['total'],'text|17|4|b|17')

    def test_reset_readonly_or_unknown_field_refuses_entire_transaction(self):
        for script in ('this.resetForm(["total"]);','this.resetForm(["a","missing"]);'):
            writer,_=self.fixture(script)
            with self.subTest(script=script),self.assertRaises(ValueError):run_form_javascript(writer,{'a':'1'})

    def test_maximum_applies_to_script_setters_and_calculation_results(self):
        writer,raws=self.fixture('getField("b").value="12345";event.value=0;')
        raws['b'][NameObject('/MaxLen')]=NumberObject(3)
        with self.assertRaisesRegex(ValueError,'[Cc]aracteres'):run_form_javascript(writer,{'a':'1'})
        writer,raws=self.fixture('event.value="12345";');raws['total'][NameObject('/MaxLen')]=NumberObject(3)
        with self.assertRaisesRegex(ValueError,'caracteres'):run_form_javascript(writer,{'a':'1'})

    def test_percent_format_is_display_only_and_arithmetic_helper_is_finite(self):
        writer,raws=self.fixture('event.value=AFSimple("SUM",AFMakeNumber(getField("a").value),0.05);')
        raws['total']['/AA'][NameObject('/F')]=DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject('AFPercent_Format(1,0);')})
        values,display=run_form_javascript(writer,{'a':'0.2'})
        self.assertEqual(values['total'],'0.25');self.assertEqual(display['total'],'25.0%')

    def test_bad_formats_and_nonfinite_helpers_fail_without_external_capabilities(self):
        for script in ('event.value=util.printf("%999s","x");', 'event.value=util.printf("%n",1);',
                       'event.value=AFSimple("DIV",1,0);', 'event.value=AFMakeNumber("NaN");'):
            writer,_=self.fixture(script)
            with self.subTest(script=script),self.assertRaises(ValueError):run_form_javascript(writer,{'a':'1'})
