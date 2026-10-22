"""Bound allocation while creating default XFA instances, before rendering them."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
import pdf_xfa_flow as flow
from pdf_xfa import XFAError
from test_xfa_flow import TEMPLATE
from test_pdf_xfa import xfa_pdf,datasets


class XFAFlowSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_exponential_default_instantiation_stops_during_allocation(self):
        tree=ET.fromstring('''<subform name="a"><subform name="b"><occur min="1" max="1000" initial="1000"/>
          <subform name="c"><occur min="1" max="1000" initial="1000"/><field name="d"/></subform></subform></subform>''')
        budget=[25];created=[];original=flow.ET.Element
        def record(*args,**kwargs):
            created.append(1);return original(*args,**kwargs)
        with patch.object(flow.ET,'Element',side_effect=record),self.assertRaisesRegex(XFAError,'orçamento'):
            flow._blank(tree,budget)
        self.assertLessEqual(len(created),25)

    def test_many_tiny_xml_nodes_are_refused_before_elementtree_allocation(self):
        raw=b'<root>'+b'<x/>'*101+b'</root>'
        with patch.object(flow,'MAX_NODES',100),patch.object(flow.ET,'fromstring') as allocate:
            with self.assertRaisesRegex(XFAError,'nós'):flow._xml(raw)
            allocate.assert_not_called()

    def test_readonly_xfa_is_refused_before_publishing_editable_widgets(self):
        template=TEMPLATE.replace(b'<field name="cliente">',b'<field name="cliente" access="readOnly">')
        source=xfa_pdf(self.root/'source.pdf',[('template',template),('datasets',datasets('<form1><cliente>A</cliente></form1>'))],fields=False,dynamic=True)
        with self.assertRaisesRegex(XFAError,'somente leitura'):flow.inspect_xfa_flow(source)

    def test_repeated_draw_rows_share_the_global_row_budget(self):
        template=b'''<template xmlns="http://www.xfa.org/schema/xfa-template/3.3/"><subform name="form1" layout="tb">
          <subform name="item" layout="tb"><occur min="0" max="100" initial="0"/><draw><value><text>x</text></value></draw>
          <draw><value><text>y</text></value></draw></subform></subform></template>'''
        source=xfa_pdf(self.root/'source.pdf',[('template',template),('datasets',datasets('<form1>'+'<item/>'*10+'</form1>'))],fields=False,dynamic=True)
        with patch.object(flow,'MAX_FIELDS',10),self.assertRaisesRegex(XFAError,'linhas'):
            flow.inspect_xfa_flow(source)


if __name__=='__main__':unittest.main()
