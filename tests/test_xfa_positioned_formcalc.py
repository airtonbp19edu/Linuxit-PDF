"""XFA positions and calculate-only FormCalc in real hybrid PDF roundtrips."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_xfa_flow import flow_model, create_xfa_flow_copy
from pdf_xfa import XFAError, inspect_xfa
from xfa_formcalc import expression
from test_pdf_xfa import xfa_pdf, datasets
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader

TEMPLATE = b'''<template xmlns="http://www.xfa.org/schema/xfa-template/3.3/">
<subform name="form" layout="position" x="10pt" y="20pt" w="500pt" h="700pt">
<field name="a" x="1in" y="1cm" w="180pt" h="30pt"><ui><numericEdit/></ui></field>
<field name="b" x="72pt" y="65pt" w="180pt" h="30pt"><ui><numericEdit/></ui></field>
<field name="total" x="72pt" y="105pt" w="180pt" h="30pt"><ui><numericEdit/></ui>
<calculate><script contentType="application/x-formcalc">Round(Sum(a, b) * 1.5, 2)</script></calculate></field>
</subform></template>'''


class PositionedFormCalcTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)

    def fixture(self, template=TEMPLATE, body='<form><a>2</a><b>3.5</b><total>old</total></form>'):
        return xfa_pdf(self.root/'source.pdf',[('template',template),('datasets',datasets(body))],fields=False,dynamic=True)

    def create(self, source, values=None):
        target=self.root/'copy.pdf'
        report=create_xfa_flow_copy(source,target,dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),values=values or {},instances=[]))
        return PdfReader(target), report

    def test_positions_units_parent_offsets_calculation_and_dataset_roundtrip(self):
        source=self.fixture();before=source.read_bytes()
        reader,report=self.create(source,{'form[0].a[0]':'4'})
        widget=reader.pages[0]['/Annots'][0].get_object()
        self.assertAlmostEqual(float(widget['/Rect'][0]),82)
        self.assertAlmostEqual(float(widget['/Rect'][1]),842-20-72/2.54-30,places=5)
        self.assertEqual(reader.get_fields()['form[0].total[0]']['/V'],'11.25')
        self.assertTrue(int(reader.get_fields()['form[0].total[0]']['/Ff']) & 1)
        data={r['path']:r['value'] for r in inspect_xfa(reader)['fields']}
        self.assertEqual(data['form[0].total[0]'],'11.25')
        self.assertTrue(report['scripts_executed']);self.assertEqual(report['calculations'],1)
        self.assertEqual(report['layout'],'position');self.assertFalse(report['original_layout_preserved'])
        self.assertEqual(source.read_bytes(),before)

    def test_calculated_field_cannot_be_overridden_and_failure_publishes_nothing(self):
        with self.assertRaisesRegex(XFAError,'calculados'):
            self.create(self.fixture(),{'form[0].total[0]':'999'})
        self.assertFalse((self.root/'copy.pdf').exists())

    def test_dependency_order_is_resolved_and_cycles_missing_fields_or_division_fail(self):
        base=TEMPLATE.replace(b'Round(Sum(a, b) * 1.5, 2)',b'a + b')
        # a depends on total, which depends on a: detected before publication.
        cyclic=base.replace(b'<field name="a"',b'<field name="a"').replace(b'<ui><numericEdit/></ui></field>',b'<ui><numericEdit/></ui><calculate><script contentType="application/x-formcalc">total+1</script></calculate></field>',1)
        for template in (cyclic, base.replace(b'a + b',b'missing+1'),base.replace(b'a + b',b'1/0')):
            with self.subTest(template=template),self.assertRaises(XFAError):self.create(self.fixture(template))
            self.assertFalse((self.root/'copy.pdf').exists())

    def test_code_execution_attribute_access_loops_and_javascript_are_refused(self):
        for code in (b'__import__("os")',b'a.__class__',b'for x in a',b'2^99999',b'NaN',b'1e999'):
            with self.subTest(code=code),self.assertRaises(XFAError):self.create(self.fixture(TEMPLATE.replace(b'Round(Sum(a, b) * 1.5, 2)',code)))
        with self.assertRaises(XFAError):self.create(self.fixture(TEMPLATE.replace(b'application/x-formcalc',b'application/x-javascript')))
        self.assertFalse((self.root/'copy.pdf').exists())

    def test_invalid_units_bounds_mixed_layout_and_repetition_are_refused(self):
        for template in (TEMPLATE.replace(b'x="1in"',b'x="999in"'),TEMPLATE.replace(b'w="180pt"',b'w="1em"'),
                         TEMPLATE.replace(b'<field name="a"',b'<subform layout="tb"/><field name="a"'),
                         TEMPLATE.replace(b'<ui><numericEdit/></ui>',b'<caption><value><text>Importante</text></value></caption><ui><numericEdit/></ui>',1),
                         TEMPLATE.replace(b'<ui><numericEdit/></ui>',b'<occur min="1" max="2" initial="1"/><ui><numericEdit/></ui>',1)):
            with self.subTest(template=template),self.assertRaises(XFAError):self.create(self.fixture(template))

    def test_basic_formcalc_in_flow_layout_and_rounding(self):
        template=TEMPLATE.replace(b'layout="position"',b'layout="tb"').replace(b'Round(Sum(a, b) * 1.5, 2)',b'Round(Avg(a,b),1) + Count(a,b) + Abs(-1)')
        reader,report=self.create(self.fixture(template))
        self.assertEqual(reader.get_fields()['form[0].total[0]']['/V'],'5.8')
        self.assertEqual(report['layout'],'tb')

    def test_reverse_dependency_calculated_before_consumer(self):
        template=TEMPLATE.replace(b'Round(Sum(a, b) * 1.5, 2)',b'a + b')
        template=template.replace(b'<ui><numericEdit/></ui></field>',b'<ui><numericEdit/></ui><calculate><script contentType="application/x-formcalc">b*2</script></calculate></field>',1)
        reader,report=self.create(self.fixture(template))
        self.assertEqual(reader.get_fields()['form[0].a[0]']['/V'],'7')
        self.assertEqual(reader.get_fields()['form[0].total[0]']['/V'],'10.5')
        self.assertEqual(report['calculations'],2)

    def test_medium_content_area_and_nested_offsets_are_applied(self):
        template=TEMPLATE.replace(b'<subform name="form"',b'<pageSet><pageArea><medium short="8in" long="10in"/><contentArea x="25pt" y="30pt" w="540pt" h="680pt"/></pageArea></pageSet><subform name="form"')
        # Container is 680pt high, so the form must fit it explicitly.
        template=template.replace(b'h="700pt"',b'h="650pt"')
        reader,_=self.create(self.fixture(template))
        self.assertEqual(tuple(map(float,reader.pages[0].mediabox)),(0,0,576,720))
        rect=reader.pages[0]['/Annots'][0].get_object()['/Rect']
        self.assertAlmostEqual(float(rect[0]),107)
        self.assertAlmostEqual(float(rect[1]),720-30-20-72/2.54-30,places=5)

    def test_generic_form_edit_refused_but_explicit_xfa_reopen_recalculates(self):
        from pdf_changes import save_edited_copy
        source=self.fixture();self.create(source)
        copy=self.root/'copy.pdf';before=copy.read_bytes();target=self.root/'edited.pdf'
        with self.assertRaisesRegex(NotImplementedError,'recalcular'):
            save_edited_copy(copy,target,source_sha256=hashlib.sha256(before).hexdigest(),
                             operations=[dict(kind='fill-text-fields',values={'form[0].a[0]':'99'})])
        self.assertFalse(target.exists());self.assertEqual(copy.read_bytes(),before)
        create_xfa_flow_copy(copy,target,dict(source_sha256=hashlib.sha256(before).hexdigest(),values={'form[0].a[0]':'4'},instances=[]))
        self.assertEqual(PdfReader(target).get_fields()['form[0].total[0]']['/V'],'11.25')
