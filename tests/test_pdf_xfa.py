"""Read-only XFA detection and bounded datasets listing (E06)."""
import hashlib,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,BooleanObject,DecodedStreamObject,DictionaryObject,NameObject,TextStringObject
import pdf_xfa
from pdf_xfa import XFAError,inspect_xfa,parse_datasets
from pdf_panels import inspect_document_panels

NS='xmlns:xfa="http://www.xfa.org/schema/xfa-data/1.0/"'


def datasets(body):
    return f'<xfa:datasets {NS}><xfa:data>{body}</xfa:data></xfa:datasets>'.encode('utf-8')


def xfa_pdf(path,xfa,*,fields=True,dynamic=False):
    """xfa: bytes for a single XDP stream, or a list of (name, bytes) packets."""
    writer=PdfWriter();writer.add_blank_page(200,200)
    def stream(data):
        value=DecodedStreamObject();value.set_data(data);return writer._add_object(value)
    if isinstance(xfa,bytes):value=stream(xfa)
    else:
        value=ArrayObject()
        for name,data in xfa:value+=[TextStringObject(name),stream(data)]
    form=DictionaryObject({NameObject('/XFA'):value,NameObject('/Fields'):ArrayObject()})
    if fields:
        widget=writer._add_object(DictionaryObject({NameObject('/FT'):NameObject('/Tx'),NameObject('/T'):TextStringObject('form1[0].nome[0]')}))
        form[NameObject('/Fields')]=ArrayObject([widget])
    writer.root_object[NameObject('/AcroForm')]=writer._add_object(form)
    if dynamic:writer.root_object[NameObject('/NeedsRendering')]=BooleanObject(True)
    with open(path,'wb') as handle:writer.write(handle)
    return path


class XFAParserTests(unittest.TestCase):
    def test_paths_follow_som_indices_and_skip_groups(self):
        found,fields,truncated=parse_datasets(datasets(
            '<form1><nome>Ana</nome><itens><item>A</item><item>B</item></itens><vazio/>'
            '<grupo xfa:dataNode="dataGroup"/></form1>'))
        self.assertTrue(found);self.assertFalse(truncated)
        self.assertEqual([(f['path'],f['value']) for f in fields],
            [('form1[0].nome[0]','Ana'),('form1[0].itens[0].item[0]','A'),('form1[0].itens[0].item[1]','B'),('form1[0].vazio[0]','')])

    def test_rich_text_and_data_value_are_single_values(self):
        _,fields,_=parse_datasets(datasets(
            '<f><obs xfa:contentType="text/html"><body xmlns="http://www.w3.org/1999/xhtml"><p>Oi <b>mundo</b></p></body></obs>'
            '<v xfa:dataNode="dataValue">x<sub>y</sub></v></f>'))
        self.assertEqual([(f['path'],f['value']) for f in fields],[('f[0].obs[0]','Oi mundo'),('f[0].v[0]','xy')])

    def test_template_and_text_outside_data_are_ignored(self):
        xdp=(b'<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/"><template><subform><field name="a"><event><script>app.alert(1)</script>'
             b'</event></field></subform></template>'+datasets('<f><a>1</a></f>')+b'</xdp:xdp>')
        found,fields,_=parse_datasets(xdp)
        self.assertTrue(found);self.assertEqual([(f['path'],f['value']) for f in fields],[('f[0].a[0]','1')])

    def test_doctype_entities_malformed_and_depth_are_refused(self):
        for data,message in ((b'<!DOCTYPE a [<!ENTITY x "y">]><a>&x;</a>','DOCTYPE'),
                             (b'<!DOCTYPE a SYSTEM "file:///etc/passwd"><a/>','DOCTYPE'),
                             (b'<a><b></a>','inválido'),
                             (b'<a>'+b'<b>'*70+b'</b>'*70+b'</a>','profundidade')):
            with self.subTest(message=message),self.assertRaisesRegex(XFAError,message):parse_datasets(data)

    def test_field_count_value_length_and_size_are_bounded(self):
        _,fields,truncated=parse_datasets(datasets('<f>'+'<c>1</c>'*(pdf_xfa.MAX_FIELDS+3)+'</f>'))
        self.assertEqual(len(fields),pdf_xfa.MAX_FIELDS);self.assertTrue(truncated)
        _,fields,_=parse_datasets(datasets('<f><c>'+'x'*(pdf_xfa.MAX_VALUE+10)+'</c></f>'))
        self.assertEqual(len(fields[0]['value']),pdf_xfa.MAX_VALUE);self.assertTrue(fields[0]['value_truncated'])
        with self.assertRaisesRegex(XFAError,'8 MiB'):parse_datasets(b' '*(pdf_xfa.MAX_BYTES+1))


class XFADocumentTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory();self.addCleanup(self.folder.cleanup);self.dir=Path(self.folder.name)

    def test_hybrid_packet_array_is_listed_without_changing_the_file(self):
        path=xfa_pdf(self.dir/'h.pdf',[('template',b'<template/>'),('datasets',datasets('<form1><nome>Ana</nome></form1>'))])
        before=hashlib.sha256(path.read_bytes()).hexdigest()
        info=inspect_document_panels(str(path))['xfa']
        self.assertEqual(info['packets'],['template','datasets']);self.assertTrue(info['hybrid']);self.assertFalse(info['dynamic'])
        self.assertEqual([(f['path'],f['value']) for f in info['fields']],[('form1[0].nome[0]','Ana')]);self.assertIsNone(info['error'])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),before)

    def test_elements_split_across_packets_use_the_joined_document(self):
        whole=b'<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/">'+datasets('<f><a>1</a></f>')+b'</xdp:xdp>'
        cut=whole.index(b'<a>')+3
        info=inspect_xfa(PdfReader(xfa_pdf(self.dir/'s.pdf',[('xdp:xdp',b''),('datasets',whole[:cut]),('postamble',whole[cut:])])))
        self.assertEqual([(f['path'],f['value']) for f in info['fields']],[('f[0].a[0]','1')])

    def test_single_stream_dynamic_form_without_acroform_fields(self):
        xdp=b'<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/">'+datasets('<f><a>1</a></f>')+b'</xdp:xdp>'
        info=inspect_xfa(PdfReader(xfa_pdf(self.dir/'d.pdf',xdp,fields=False,dynamic=True)))
        self.assertEqual(info['packets'],[]);self.assertFalse(info['hybrid']);self.assertTrue(info['dynamic'])
        self.assertEqual([f['value'] for f in info['fields']],['1'])

    def test_missing_datasets_and_bad_packets_are_reported_by_the_panel(self):
        info=inspect_document_panels(str(xfa_pdf(self.dir/'n.pdf',[('template',b'<template/>')])))['xfa']
        self.assertEqual(info['fields'],[]);self.assertIn('pacote de dados',info['error'])
        hostile=datasets('<f>&x;</f>').replace(b'<xfa:datasets',b'<!DOCTYPE z [<!ENTITY x "y">]><xfa:datasets')
        info=inspect_document_panels(str(xfa_pdf(self.dir/'e.pdf',[('datasets',hostile)])))['xfa']
        self.assertEqual(info['fields'],[]);self.assertIn('DOCTYPE',info['error'])

    def test_pdf_without_xfa_reports_none(self):
        writer=PdfWriter();writer.add_blank_page(100,100);path=self.dir/'plain.pdf'
        with open(path,'wb') as handle:writer.write(handle)
        self.assertIsNone(inspect_xfa(PdfReader(path)));self.assertIsNone(inspect_document_panels(str(path))['xfa'])


if __name__=='__main__':unittest.main()
