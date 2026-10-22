"""Own dynamic XFA dataset repetition, pagination, widgets and refusal checks."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from pdf_xfa_flow import flow_model,create_xfa_flow_copy,inspect_xfa_flow
from pdf_xfa import inspect_xfa,XFAError
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from test_pdf_xfa import xfa_pdf,datasets

TEMPLATE=b'''<template xmlns="http://www.xfa.org/schema/xfa-template/3.3/">
<subform name="form1" layout="tb"><draw><value><text>Pedido</text></value></draw>
<field name="cliente"><caption><value><text>Cliente</text></value></caption><ui><textEdit/></ui></field>
<subform name="item" layout="tb"><occur min="0" max="100" initial="0"/>
<field name="produto"><ui><textEdit/></ui><value><text>Novo</text></value></field>
<field name="quantidade"><ui><numericEdit/></ui><value><decimal>1</decimal></value></field>
</subform></subform></template>'''


class XFAFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.dir=Path(self.temp.name)

    def fixture(self,template=TEMPLATE,body='<form1><cliente>José</cliente><item><produto>A</produto><quantidade>2</quantidade></item></form1>'):
        return xfa_pdf(self.dir/'source.pdf',[('template',template),('datasets',datasets(body))],fields=False,dynamic=True)

    def create(self,path,values=None,instances=None):
        output=self.dir/'output.pdf'
        result=create_xfa_flow_copy(path,output,dict(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),values=values or {},instances=instances or []))
        return output,result

    def test_dynamic_form_becomes_coherent_hybrid_copy_with_real_widget_appearances(self):
        path=self.fixture();before=path.read_bytes();output,result=self.create(path,{'form1[0].cliente[0]':'André & Cia'})
        reader=PdfReader(output);fields=reader.get_fields();info=inspect_xfa(reader)
        self.assertEqual(fields['form1[0].cliente[0]']['/V'],'André & Cia')
        self.assertEqual(info['fields'][0]['value'],'André & Cia');self.assertTrue(info['hybrid'])
        self.assertFalse(result['original_layout_preserved']);self.assertFalse(result['scripts_executed'])
        widget=reader.pages[0]['/Annots'][0].get_object();self.assertIn(b'416e6472e9',widget['/AP']['/N'].get_data())
        self.assertEqual(before,path.read_bytes())

    def test_repeat_insertion_creates_defaults_and_values_are_bound_after_insertion(self):
        path=self.fixture();output,_=self.create(path,{'form1[0].item[1].produto[0]':'B'},[dict(action='add',path='form1[0].item',index=1)])
        data={row['path']:row['value'] for row in inspect_xfa(PdfReader(output))['fields']}
        self.assertEqual(data['form1[0].item[0].produto[0]'],'A')
        self.assertEqual(data['form1[0].item[1].produto[0]'],'B')
        self.assertEqual(data['form1[0].item[1].quantidade[0]'],'1')

    def test_repeat_removal_to_zero_preserves_minimum_zero_without_respawning(self):
        path=self.fixture();output,_=self.create(path,instances=[dict(action='remove',path='form1[0].item',index=0)])
        self.assertEqual(list(PdfReader(output).get_fields()),['form1[0].cliente[0]'])

    def test_many_repeated_rows_paginate_and_each_widget_is_on_exactly_one_page(self):
        body='<form1><cliente>A</cliente>'+''.join('<item><produto>Produto '+str(i)+'</produto><quantidade>1</quantidade></item>' for i in range(40))+'</form1>'
        path=self.fixture(body=body);output,result=self.create(path)
        reader=PdfReader(output);self.assertGreater(result['pages'],1);self.assertEqual(len(reader.get_fields()),81)
        widgets=[str(ref.get_object()['/T']) for page in reader.pages for ref in page.get('/Annots',[])]
        self.assertEqual(len(widgets),len(set(widgets)));self.assertEqual(set(widgets),set(reader.get_fields()))

    def test_instance_minimum_maximum_and_missing_paths_are_refused_atomically(self):
        path=self.fixture(TEMPLATE.replace(b'min="0" max="100" initial="0"',b'min="1" max="1" initial="1"'))
        for op in (dict(action='remove',path='form1[0].item',index=0),dict(action='add',path='form1[0].item',index=1),dict(action='add',path='missing',index=0)):
            with self.subTest(op=op),self.assertRaises(XFAError):self.create(path,instances=[op])
            self.assertFalse((self.dir/'output.pdf').exists())

    def test_scripts_bindings_positioned_layout_and_other_controls_are_never_silently_accepted(self):
        for extra in (b'<script>app.alert(1)</script>',b'<bind match="dataRef" ref="secret"/>',b'<event/>'):
            path=self.fixture(TEMPLATE.replace(b'<ui><textEdit/></ui>',b'<ui><textEdit/></ui>'+extra))
            with self.subTest(extra=extra),self.assertRaises(XFAError):self.create(path)
        for template in (TEMPLATE.replace(b'layout="tb"',b'layout="position"'),TEMPLATE.replace(b'<textEdit/>',b'<choiceList/>')):
            path=self.fixture(template)
            with self.assertRaises(XFAError):self.create(path)
        self.assertFalse((self.dir/'output.pdf').exists())

    def test_document_entities_duplicate_binding_and_unknown_fields_are_refused(self):
        for template in (b'<!DOCTYPE a [<!ENTITY x "expanded">]>'+TEMPLATE,
                         TEMPLATE.replace(b'<field name="cliente">',b'<field name="cliente"/><field name="cliente">')):
            path=self.fixture(template)
            with self.assertRaises(XFAError):self.create(path)
        path=self.fixture()
        with self.assertRaises(XFAError):self.create(path,{'form1[0].secret[0]':'x'})

    def test_no_overwrite_hash_guard_unicode_limit_and_source_preservation(self):
        path=self.fixture();before=path.read_bytes()
        with self.assertRaisesRegex(XFAError,'mudou'):
            create_xfa_flow_copy(path,self.dir/'output.pdf',dict(source_sha256='0'*64,values={},instances=[]))
        with self.assertRaisesRegex(XFAError,'Unicode'):
            self.create(path,{'form1[0].cliente[0]':'漢字'})
        output,_=self.create(path);saved=output.read_bytes()
        with self.assertRaises(FileExistsError):self.create(path)
        self.assertEqual(output.read_bytes(),saved);self.assertEqual(path.read_bytes(),before)

    def test_info_lists_groups_and_default_template_nodes_without_writing_source(self):
        path=self.fixture(body='<form1><cliente>A</cliente></form1>');before=path.read_bytes()
        info=inspect_xfa_flow(path)
        self.assertEqual(info['groups'],[dict(path='form1[0].item',count=0,minimum=0,maximum=100)])
        self.assertEqual(len(info['fields']),1);self.assertEqual(before,path.read_bytes())


if __name__=='__main__':unittest.main()
