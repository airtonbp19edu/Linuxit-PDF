"""Adversarial synthetic reply/popup topology and stamp appearance preservation."""
import os,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from annotation_editing import conversation_members,delete_annotation,move_related_annotation
from pdf_changes import _apply
from pypdf import PdfWriter
from pypdf.annotations import Text
from pypdf.generic import ArrayObject,DictionaryObject,NameObject,NumberObject,TextStringObject,DecodedStreamObject

class AnnotationEditingTests(unittest.TestCase):
    def fixture(self):
        w=PdfWriter();p=w.add_blank_page(200,200);w.add_blank_page(200,200)
        w.add_annotation(0,Text(rect=(10,10,30,30),text='root'))
        root=p['/Annots'][0];note=root.get_object()
        popup=DictionaryObject({NameObject('/Subtype'):NameObject('/Popup'),NameObject('/Rect'):ArrayObject(NumberObject(v) for v in (40,40,60,60)),NameObject('/Parent'):root})
        popupref=w._add_object(popup);note[NameObject('/Popup')]=popupref;p['/Annots'].append(popupref)
        return w,p,note,popup

    def test_metadata_keeps_graphical_stamp_appearance_and_clears_rich_text(self):
        w,p,note,_=self.fixture();note[NameObject('/Subtype')]=NameObject('/Stamp')
        stream=DecodedStreamObject();stream.set_data(b'0 1 0 rg 0 0 20 20 re f')
        appearance=DictionaryObject({NameObject('/N'):w._add_object(stream)})
        note[NameObject('/AP')]=appearance;note[NameObject('/RC')]=TextStringObject('<p>old</p>')
        _apply(w,dict(kind='update-comment',page=0,index=0,text='new',author='Ana'))
        self.assertIs(note['/AP'],appearance);self.assertEqual(note['/Contents'],'new');self.assertNotIn('/RC',note)

    def test_moving_popup_is_atomic_when_popup_would_leave_page(self):
        w,p,note,popup=self.fixture();old=list(note['/Rect'])
        with self.assertRaises(ValueError):move_related_annotation(w,p,0,160,0)
        self.assertEqual(list(note['/Rect']),old)
        move_related_annotation(w,p,0,5,7);self.assertEqual(list(note['/Rect']),[15,17,35,37]);self.assertEqual(list(popup['/Rect']),[45,47,65,67])

    def test_delete_leaf_removes_popup_but_not_attachment_payload_claim(self):
        w,p,note,popup=self.fixture();delete_annotation(w,p,0);self.assertEqual(len(p['/Annots']),0)

    def test_cross_page_inbound_reply_blocks_conversation_and_metadata(self):
        w,p,note,_=self.fixture();reply=Text(rect=(10,10,30,30),text='reply');reply[NameObject('/IRT')]=p['/Annots'][0]
        w.add_annotation(1,reply)
        with self.assertRaisesRegex(ValueError,'outra página'):conversation_members(w,p,0)
        with self.assertRaises(ValueError):_apply(w,dict(kind='update-comment',page=0,index=0,text='new',author=''))
        self.assertEqual(note['/Contents'],'root')

    def test_locked_popup_and_cyclic_reply_refused(self):
        w,p,note,popup=self.fixture();popup[NameObject('/F')]=NumberObject(128)
        with self.assertRaisesRegex(ValueError,'bloqueado'):conversation_members(w,p,0)
        popup.pop('/F');note[NameObject('/IRT')]=p['/Annots'][0]
        with self.assertRaisesRegex(ValueError,'cíclica'):conversation_members(w,p,0)

    def test_subtree_does_not_remove_reply_parent(self):
        w,p,note,_=self.fixture();reply=Text(rect=(70,70,90,90),text='reply');reply[NameObject('/IRT')]=p['/Annots'][0];w.add_annotation(0,reply)
        members=conversation_members(w,p,2);self.assertEqual(members,{id(p['/Annots'][2].get_object())})
        with self.assertRaisesRegex(ValueError,'respostas'):delete_annotation(w,p,0)

