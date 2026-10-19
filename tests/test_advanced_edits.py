"""Roundtrip real AcroForm states, linked outlines and annotation copies."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
import pdf_changes as edits
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text
from pypdf.generic import (ArrayObject, DictionaryObject, NameObject, NumberObject,
                           TextStringObject, DecodedStreamObject)


def make_controls(path):
    writer = PdfWriter()
    for _ in range(2):writer.add_blank_page(200,300)
    parent = writer.add_outline_item('Parent',0)
    writer.add_outline_item('Child',1,parent=parent)
    writer.add_outline_item('Sibling',1)
    writer.add_annotation(0,Text(rect=(5,5,20,20),text='Original note'))
    writer.add_attachment('keep.txt',b'unchanged attachment')
    font = writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'),
        NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')}))
    resources = DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/Helv'):font})})
    fields = []
    def appearance(on):
        stream = DecodedStreamObject();stream.set_data(b'0 0 16 16 re f' if on else b'')
        stream.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),
                       NameObject('/BBox'):ArrayObject(NumberObject(v) for v in (0,0,16,16))})
        return writer._add_object(stream)
    def widget(y):
        return DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Widget'),
            NameObject('/Rect'):ArrayObject(NumberObject(v) for v in (25,y,175,y+18)),NameObject('/F'):NumberObject(4),
            NameObject('/DA'):TextStringObject('/Helv 10 Tf 0 g')})
    def add(raw):
        ref = writer._add_object(raw);fields.append(ref);writer.pages[0]['/Annots'].append(ref);return raw
    checkbox = widget(30);checkbox.update({NameObject('/FT'):NameObject('/Btn'),NameObject('/T'):TextStringObject('check'),
        NameObject('/V'):NameObject('/Off'),NameObject('/AS'):NameObject('/Off'),NameObject('/AP'):DictionaryObject({
            NameObject('/N'):DictionaryObject({NameObject('/Off'):appearance(False),NameObject('/Yes'):appearance(True)})})})
    add(checkbox)
    radio = DictionaryObject({NameObject('/FT'):NameObject('/Btn'),NameObject('/T'):TextStringObject('radio'),
        NameObject('/Ff'):NumberObject(1<<15),NameObject('/V'):NameObject('/Off')})
    radio_ref = writer._add_object(radio);fields.append(radio_ref);kids = ArrayObject()
    for n,state in enumerate(('/Left','/Right')):
        raw = widget(60+n*25);raw.update({NameObject('/Parent'):radio_ref,NameObject('/AS'):NameObject('/Off'),
            NameObject('/AP'):DictionaryObject({NameObject('/N'):DictionaryObject({NameObject('/Off'):appearance(False),NameObject(state):appearance(True)})})})
        ref = writer._add_object(raw);kids.append(ref);writer.pages[0]['/Annots'].append(ref)
    radio[NameObject('/Kids')] = kids
    choices = {}
    for n,(name,flags) in enumerate((('choice',0),('combo',1<<17),('multi',1<<21))):
        raw = widget(120+n*30);raw.update({NameObject('/FT'):NameObject('/Ch'),NameObject('/T'):TextStringObject(name),
            NameObject('/Ff'):NumberObject(flags),NameObject('/Opt'):ArrayObject([
                ArrayObject([TextStringObject(value),TextStringObject(label)]) for value,label in (('A','Alpha'),('B','Beta'),('C','Gamma'))]),
            NameObject('/V'):ArrayObject([TextStringObject('A')]) if name == 'multi' else TextStringObject('A')})
        choices[name] = add(raw)
    writer.root_object[NameObject('/AcroForm')] = writer._add_object(DictionaryObject({NameObject('/Fields'):ArrayObject(fields),
        NameObject('/DR'):resources,NameObject('/DA'):TextStringObject('/Helv 10 Tf 0 g')}))
    writer.write(path)
    return writer, checkbox, radio, choices


class AdvancedEditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-advanced-');self.root = Path(self.temp.name)
        self.source,self.output = self.root/'source.pdf',self.root/'output.pdf'
        self.writer,self.check,self.radio,self.choices = make_controls(self.source)
        self._record()
    def _record(self):self.original = self.source.read_bytes();self.identity = hashlib.sha256(self.original).hexdigest()
    def tearDown(self):self.temp.cleanup()
    def save(self,*operations):
        edits.save_edited_copy(self.source,self.output,source_sha256=self.identity,operations=list(operations))
        self.assertEqual(self.source.read_bytes(),self.original)
        return PdfReader(self.output)
    def fill(self,values):return self.save({'kind':'fill-form-controls','values':values})
    def assert_rejected(self,operation):
        with self.assertRaises((ValueError,NotImplementedError)):self.save(operation)
        self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-copy-*')),[])

    def test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect(self):
        info = edits.inspect_editable_document(self.source);controls = {r['name']:r for r in info['form_controls']}
        self.assertEqual(len(controls),5);self.assertEqual(controls['check']['kind'],'checkbox')
        self.assertEqual(controls['radio']['options'],['/Left','/Right'])
        self.assertTrue(controls['combo']['combo']);self.assertTrue(controls['multi']['multiple'])
        self.assertEqual(controls['choice']['options'][1],{'value':'B','label':'Beta'})
        self.assertEqual(info['page_boxes'][0],[0,0,200,300]);self.assertEqual(info['unsupported_controls'],[])

    def test_checkbox_sets_and_clears_value_and_visible_appearance(self):
        for value in (True,False):
            reader = self.fill({'check':value});raw = reader.get_fields()['check'].indirect_reference.get_object()
            self.assertEqual((raw['/V'],raw['/AS']),('/Yes','/Yes') if value else ('/Off','/Off'));self.output.unlink()

    def test_radio_activates_only_the_selected_widget_and_can_clear(self):
        for value,expected in (('/Right',['/Off','/Right']),('/Left',['/Left','/Off']),('/Off',['/Off','/Off'])):
            reader = self.fill({'radio':value});raw = reader.get_fields()['radio'].indirect_reference.get_object()
            self.assertEqual(raw['/V'],value);self.assertEqual([k.get_object()['/AS'] for k in raw['/Kids']],expected)
            self.output.unlink()

    def test_radio_no_toggle_off_is_enforced(self):
        self.radio[NameObject('/Ff')] = NumberObject((1<<15)|(1<<14));self.writer.write(self.source);self._record()
        self.assert_rejected({'kind':'fill-form-controls','values':{'radio':'/Off'}})

    def test_single_and_combo_values_indices_and_generated_appearances_roundtrip(self):
        reader = self.fill({'choice':['B'],'combo':['C']})
        fields = reader.get_fields()
        for name,value,index in (('choice','B',1),('combo','C',2)):
            raw = fields[name].indirect_reference.get_object()
            self.assertEqual(raw['/V'],value);self.assertEqual(list(raw['/I']),[index])
            self.assertTrue(raw['/AP']['/N'].get_data());self.assertIn(b'Tf',raw['/AP']['/N'].get_data())

    def test_multiselect_uses_export_values_and_canonical_indices(self):
        reader = self.fill({'multi':['C','A']});raw = reader.get_fields()['multi'].indirect_reference.get_object()
        self.assertEqual(list(raw['/V']),['A','C']);self.assertEqual(list(raw['/I']),[0,2])
        self.assertIn(b'Gamma',raw['/AP']['/N'].get_data())

    def test_choice_selection_can_be_cleared(self):
        reader = self.fill({'multi':[],'choice':[]})
        self.assertEqual(reader.get_fields()['choice']['/V'],'');self.assertEqual(list(reader.get_fields()['multi']['/V']),[])

    def test_invalid_values_do_not_publish_partial_batch(self):
        for values in ({'check':1},{'radio':'/Unknown'},{'choice':['Alpha']},{'choice':['A','B']},
                       {'multi':['A','A']},{'choice':'B'},{'missing':True}):
            with self.subTest(values=values):self.assert_rejected({'kind':'fill-form-controls','values':values})

    def test_read_only_and_unsupported_button_appearance_are_explicit(self):
        self.check[NameObject('/Ff')] = NumberObject(1);self.writer.write(self.source);self._record()
        self.assert_rejected({'kind':'fill-form-controls','values':{'check':True}})
        self.check.pop('/Ff');self.check.pop('/AP');self.writer.write(self.source);self._record()
        info = edits.inspect_editable_document(self.source)
        self.assertEqual(info['unsupported_controls'][0]['name'],'check')
        self.assert_rejected({'kind':'fill-form-controls','values':{'check':True}})

    def test_editable_combo_and_duplicate_exports_are_rejected(self):
        # Edit without Combo is an invalid choice field, unlike a valid editable combo.
        self.choices['combo'][NameObject('/Ff')] = NumberObject(1<<18)
        self.choices['choice']['/Opt'].append(self.choices['choice']['/Opt'][0]);self.writer.write(self.source);self._record()
        for name in ('combo','choice'):self.assert_rejected({'kind':'fill-form-controls','values':{name:['A']}})

    def test_inherited_checkbox_flags_and_type_are_respected(self):
        form = self.writer.root_object['/AcroForm'];raw = self.check
        parent = DictionaryObject({NameObject('/FT'):raw.pop('/FT'),NameObject('/T'):TextStringObject('group'),
            NameObject('/Ff'):NumberObject(1),NameObject('/Kids'):ArrayObject([raw.indirect_reference])})
        ref = self.writer._add_object(parent);raw[NameObject('/Parent')]=ref
        form['/Fields'][0]=ref;self.writer.write(self.source);self._record()
        record=next(x for x in edits.inspect_editable_document(self.source)['form_controls'] if x['name']=='group.check')
        self.assertTrue(record['read_only'])
        self.assert_rejected({'kind':'fill-form-controls','values':{'group.check':True}})

    def test_checkbox_widget_absent_from_pages_is_unsupported(self):
        self.writer.pages[0]['/Annots'].remove(self.check.indirect_reference);self.writer.write(self.source);self._record()
        self.assert_rejected({'kind':'fill-form-controls','values':{'check':True}})

    def test_closed_outline_counts_remain_closed_after_move(self):
        parent=self.writer.root_object['/Outlines']['/First'];parent[NameObject('/Count')]=NumberObject(-1)
        self.writer.write(self.source);self._record()
        reader=self.save({'kind':'move-bookmark','path':[1],'parent':[0],'position':0})
        parent=reader.root_object['/Outlines']['/First']
        self.assertEqual(parent['/Count'],-2);self.assertEqual(reader.root_object['/Outlines']['/Count'],1)

    def test_move_preserves_subtree_destinations_and_sibling_links(self):
        reader = self.save({'kind':'move-bookmark','path':[0],'parent':[1],'position':0})
        self.assertEqual(reader.outline[0].title,'Sibling')
        nested = reader.outline[1];self.assertEqual(nested[0].title,'Parent');self.assertEqual(nested[1][0].title,'Child')
        self.assertEqual(reader.get_destination_page_number(nested[1][0]),1)
        self.assertEqual(edits.inspect_editable_document(self.output)['bookmarks'][2]['path'],[0,0,0])
        root = reader.root_object['/Outlines'];self.assertEqual(root['/Count'],3)
        self.assertEqual(root['/First'].indirect_reference,root['/Last'].indirect_reference)
        self.assertEqual(next(reader.attachment_list).content,b'unchanged attachment')

    def test_move_child_to_root_and_reorder_same_parent(self):
        reader = self.save({'kind':'move-bookmark','path':[0,0],'parent':[],'position':1},
                           {'kind':'move-bookmark','path':[2],'parent':[],'position':0})
        self.assertEqual([n.title for n in reader.outline],['Sibling','Parent','Child'])
        root = reader.root_object['/Outlines'];first = root['/First']
        self.assertNotIn('/Prev',first);self.assertEqual(first['/Next']['/Prev'].indirect_reference,first.indirect_reference)

    def test_delete_bookmark_removes_subtree_and_last_root(self):
        reader = self.save({'kind':'delete-bookmark','path':[0]},{'kind':'delete-bookmark','path':[0]})
        self.assertEqual(reader.outline,[]);self.assertEqual(reader.root_object['/Outlines']['/Count'],0)
        self.assertEqual(len(reader.pages),2)

    def test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused(self):
        for operation in ({'kind':'move-bookmark','path':[0],'parent':[0,0],'position':0},
                          {'kind':'move-bookmark','path':[1],'parent':[],'position':True},
                          {'kind':'move-bookmark','path':[1],'parent':[],'position':2},
                          {'kind':'delete-bookmark','path':[True]}):self.assert_rejected(operation)

    def test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text(self):
        reader = self.save({'kind':'add-highlight','page':0,'rect':[20,30,120,50],'text':'mark'},
                           {'kind':'add-rectangle','page':1,'rect':[5,6,100,80],'text':'box'})
        highlight = reader.pages[0]['/Annots'][-1].get_object();rectangle = reader.pages[1]['/Annots'][-1].get_object()
        self.assertEqual(highlight['/Subtype'],'/Highlight');self.assertEqual(list(highlight['/QuadPoints']),[20,50,120,50,20,30,120,30])
        self.assertEqual(highlight['/F'],4);self.assertEqual(highlight['/Contents'],'mark')
        self.assertEqual(rectangle['/Subtype'],'/Square');self.assertEqual(list(rectangle['/Rect']),[5,6,100,80])

    def test_delete_supported_annotation_preserves_widgets_and_other_pages(self):
        reader = self.save({'kind':'add-rectangle','page':1,'rect':[5,6,100,80],'text':'keep'},
                           {'kind':'delete-annotation','page':0,'index':0})
        self.assertTrue(all(a.get_object()['/Subtype']=='/Widget' for a in reader.pages[0]['/Annots']))
        self.assertEqual(reader.pages[1]['/Annots'][0].get_object()['/Contents'],'keep')
        self.assertEqual(len(reader.get_fields()),5)

    def test_locked_notes_widgets_and_replies_are_not_deleted(self):
        self.assert_rejected({'kind':'delete-annotation','page':0,'index':1})
        note = self.writer.pages[0]['/Annots'][0].get_object();note[NameObject('/F')]=NumberObject(128)
        self.writer.write(self.source);self._record();self.assert_rejected({'kind':'delete-annotation','page':0,'index':0})
        note[NameObject('/F')]=NumberObject(4)
        reply = Text(rect=(5,5,20,20),text='reply');reply[NameObject('/IRT')]=note.indirect_reference
        self.writer.add_annotation(0,reply);self.writer.write(self.source);self._record()
        self.assert_rejected({'kind':'delete-annotation','page':0,'index':0})

    def test_invalid_annotation_geometry_and_extra_parameters_are_rejected(self):
        for rect in ([0,0,201,40],[10,10,5,50],[0,0,float('inf'),50],[True,0,10,20]):
            self.assert_rejected({'kind':'add-highlight','page':0,'rect':rect,'text':''})
        self.assert_rejected({'kind':'delete-annotation','page':0,'index':0,'unexpected':True})


if __name__ == '__main__':unittest.main()
