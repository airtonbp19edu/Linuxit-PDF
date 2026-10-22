"""Adversarial transaction tests for opt-in PDF field scripts, with a real engine."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
from pdf_form_javascript import run_form_javascript
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import NameObject, NumberObject, DictionaryObject, TextStringObject
from test_form_events import form_pdf


@unittest.skipUnless(importlib.util.find_spec('_quickjs'), 'real QuickJS required')
class JavaScriptSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'form.pdf'

    def test_prototype_tojson_cannot_forge_readonly_transaction_result(self):
        code = '''Object.prototype.toJSON = function() {
          if (this.ok === true) return {ok:true,values:{b:"forged"},display:{}};
          return this;
        }; event.value = 5;'''
        document, fields = form_pdf(self.path, code)
        fields['b'][NameObject('/Ff')] = NumberObject(1)
        with self.assertRaises(ValueError):
            run_form_javascript(document, {'a': '1'})

    def test_global_intrinsic_replacement_cannot_skip_validation_or_calculation(self):
        for code in ('Object.keys = function(){return []}; event.value=5;',
                     'globalThis.Object = {keys:()=>[]}; event.value=5;',
                     'Set.prototype.add = function(){return this}; event.value=5;',
                     'Array.prototype["/C"] = "event.value=99"; event.value=5;'):
            document, _ = form_pdf(self.path, code)
            with self.subTest(code=code), self.assertRaises(ValueError):
                run_form_javascript(document, {'a': '1'})

    def test_chained_action_is_refused_before_engine_and_original_is_preserved(self):
        document, fields = form_pdf(self.path, 'event.value=5;')
        fields['total']['/AA']['/C'][NameObject('/Next')] = DictionaryObject({
            NameObject('/S'): NameObject('/JavaScript'), NameObject('/JS'): TextStringObject('event.value=666;')})
        with self.assertRaisesRegex(ValueError, 'composta'):
            run_form_javascript(document, {'a': '1'})


if __name__ == '__main__':unittest.main()
