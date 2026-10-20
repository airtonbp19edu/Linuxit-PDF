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
from pdf_changes import inspect_editable_document,save_edited_copy
from pypdf.generic import NumberObject

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


TEMPLATE=b'<template xmlns="http://www.xfa.org/schema/xfa-template/3.3/"><subform name="form1"><subform><field name="nome"/></subform></subform></template>'


def hybrid_pdf(path,body,names,*,single=False,calculate=None,encoding='UTF-8'):
    """Hybrid form: AcroForm text widgets named like form1[0].#subform[0].x[0] and a datasets packet."""
    writer=PdfWriter();page=writer.add_blank_page(300,60+40*len(names))
    font=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    refs=[]
    for index,(name,value) in enumerate(names):
        widget=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Widget'),NameObject('/FT'):NameObject('/Tx'),
            NameObject('/T'):TextStringObject(name),NameObject('/V'):TextStringObject(value),NameObject('/DA'):TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/Rect'):ArrayObject([NumberObject(v) for v in (10,20+40*index,280,40+40*index)])})
        if calculate and name==calculate[0]:
            widget[NameObject('/AA')]=DictionaryObject({NameObject('/C'):DictionaryObject({NameObject('/S'):NameObject('/JavaScript'),NameObject('/JS'):TextStringObject(calculate[1])})})
        refs.append(writer._add_object(widget))
    page[NameObject('/Annots')]=ArrayObject(refs)
    data=(f'<?xml version="1.0" encoding="{encoding}"?>'.encode()+datasets(body))
    def stream(raw):
        value=DecodedStreamObject();value.set_data(raw);return writer._add_object(value.flate_encode())
    if single:xfa=stream(b'<xdp:xdp xmlns:xdp="http://ns.adobe.com/xdp/">'+TEMPLATE+data.split(b'?>',1)[1]+b'</xdp:xdp>')
    else:xfa=ArrayObject([TextStringObject('template'),stream(TEMPLATE),TextStringObject('datasets'),stream(data)])
    form=DictionaryObject({NameObject('/Fields'):ArrayObject(refs),NameObject('/XFA'):xfa,NameObject('/DA'):TextStringObject('/Helv 10 Tf 0 g'),
        NameObject('/DR'):DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/Helv'):font})})})
    if calculate:form[NameObject('/CO')]=ArrayObject([refs[[n for n,_ in names].index(calculate[0])]])
    writer.root_object[NameObject('/AcroForm')]=writer._add_object(form)
    with open(path,'wb') as handle:writer.write(handle)
    return path


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def xfa_values(path):
    return {f['path']:f['value'] for f in inspect_xfa(PdfReader(path))['fields']}


class HybridFillTests(unittest.TestCase):
    """E07: filling a hybrid form keeps AcroForm and datasets equal in the new copy."""
    NAME='form1[0].#subform[0].nome[0]'

    def setUp(self):
        self.folder=tempfile.TemporaryDirectory();self.addCleanup(self.folder.cleanup);self.dir=Path(self.folder.name)

    def fill(self,source,values,kind='fill-text-fields',name='copia.pdf'):
        output=self.dir/name
        return output,save_edited_copy(source,output,source_sha256=sha(source),operations=[{'kind':kind,'values':values}])

    def test_text_fill_updates_acroform_and_datasets_and_preserves_the_rest(self):
        source=hybrid_pdf(self.dir/'h.pdf','<form1><nome>Ana</nome><outro>fixo</outro></form1>',[(self.NAME,'Ana')])
        before=sha(source);template=PdfReader(source).root_object['/AcroForm']['/XFA'][1].get_object().get_data()
        output,result=self.fill(source,{self.NAME:'Bia & Cia <ç>'})
        reader=PdfReader(output)
        self.assertEqual(reader.get_fields()[self.NAME]['/V'],'Bia & Cia <ç>')
        self.assertEqual(xfa_values(output),{'form1[0].nome[0]':'Bia & Cia <ç>','form1[0].outro[0]':'fixo'})
        self.assertEqual(reader.root_object['/AcroForm']['/XFA'][1].get_object().get_data(),template)
        self.assertEqual(result['xfa_synced_fields'],[self.NAME]);self.assertEqual(sha(source),before)

    def test_empty_element_single_stream_and_ascii_declaration(self):
        source=hybrid_pdf(self.dir/'s.pdf','<form1><nome/></form1>',[(self.NAME,'')],single=True)
        output,_=self.fill(source,{self.NAME:'José'})
        self.assertEqual(xfa_values(output),{'form1[0].nome[0]':'José'})
        raw=PdfReader(output).root_object['/AcroForm']['/XFA'].get_object().get_data()
        self.assertIn('<nome>José</nome>'.encode(),raw)
        ascii_source=hybrid_pdf(self.dir/'a.pdf','<form1><nome/></form1>',[(self.NAME,'')],encoding='US-ASCII')
        output,_=self.fill(ascii_source,{self.NAME:'José'},name='a-out.pdf')
        self.assertEqual(xfa_values(output),{'form1[0].nome[0]':'José'})
        self.assertIn(b'<nome>Jos&#233;</nome>',PdfReader(output).root_object['/AcroForm']['/XFA'][3].get_object().get_data())

    def test_calculated_values_are_mirrored_too(self):
        names=[('form1[0].a[0]','1'),('form1[0].b[0]','2'),('form1[0].total[0]','3')]
        source=hybrid_pdf(self.dir/'c.pdf','<form1><a>1</a><b>2</b><total>3</total></form1>',names,
                          calculate=('form1[0].total[0]','AFSimple_Calculate("SUM", ["form1[0].a[0]", "form1[0].b[0]"]);'))
        output,result=self.fill(source,{'form1[0].a[0]':'10'},kind='fill-form-events')
        self.assertEqual(xfa_values(output),{'form1[0].a[0]':'10','form1[0].b[0]':'2','form1[0].total[0]':'12'})
        self.assertEqual(result['xfa_synced_fields'],['form1[0].a[0]','form1[0].total[0]'])

    def test_unbound_field_other_operations_and_xfa_only_are_refused_without_output(self):
        source=hybrid_pdf(self.dir/'u.pdf','<form1><outro>x</outro></form1>',[(self.NAME,'')])
        with self.assertRaisesRegex(ValueError,'sem dado XFA'):self.fill(source,{self.NAME:'novo'})
        bookmark={'kind':'add-bookmark','title':'x','page':0}
        with self.assertRaisesRegex(NotImplementedError,'só o preenchimento'):
            save_edited_copy(source,self.dir/'m.pdf',source_sha256=sha(source),operations=[bookmark])
        rich=hybrid_pdf(self.dir/'r.pdf','<form1><nome xfa:contentType="text/html"><b>x</b></nome></form1>',[(self.NAME,'x')])
        with self.assertRaisesRegex(ValueError,'sem dado XFA'):self.fill(rich,{self.NAME:'y'},name='r-out.pdf')
        only=xfa_pdf(self.dir/'o.pdf',[('datasets',datasets('<f><a>1</a></f>'))],fields=False)
        with self.assertRaisesRegex(NotImplementedError,'somente XFA'):inspect_editable_document(only)
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()),['o.pdf','r.pdf','u.pdf'])

    def test_edit_info_lists_bound_text_fields(self):
        source=hybrid_pdf(self.dir/'i.pdf','<form1><nome>Ana</nome></form1>',[(self.NAME,'Ana'),('form1[0].solto[0]','')])
        info=inspect_editable_document(source)
        self.assertEqual(info['xfa']['bound_text_fields'],[self.NAME]);self.assertTrue(info['xfa']['hybrid'])


if __name__=='__main__':unittest.main()
