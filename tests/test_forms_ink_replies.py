"""Roundtrip own editable combos, printable Ink and reply relationships."""
import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_advanced_edits import make_controls
from pypdf import PdfReader
from pypdf.generic import NameObject,NumberObject,TextStringObject
from pdf_changes import inspect_editable_document,save_edited_copy
from pdf_panels import inspect_document_panels
from pdf_annotations import create_ink
from edit_history import EditSession


class FormsInkRepliesTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.out=self.root/'copy.pdf'
        self.writer,self.check,self.radio,self.choices=make_controls(self.source)

    def tearDown(self):self.temp.cleanup()

    def save(self,operations):
        before=self.source.read_bytes()
        save_edited_copy(self.source,self.out,source_sha256=hashlib.sha256(before).hexdigest(),operations=operations)
        self.assertEqual(self.source.read_bytes(),before)
        return PdfReader(self.out)

    def editable(self,value=None):
        field=self.choices['combo'];field[NameObject('/Ff')]=NumberObject((1<<17)|(1<<18))
        if value is not None:field[NameObject('/V')]=TextStringObject(value)
        self.writer.write(self.source)

    def test_editable_combo_accepts_free_text_removes_stale_indices_and_embeds_appearance(self):
        self.editable('initial custom')
        record=next(c for c in inspect_editable_document(self.source)['form_controls'] if c['name']=='combo')
        self.assertTrue(record['editable']);self.assertEqual(record['value'],['initial custom'])
        reader=self.save([dict(kind='fill-form-controls',values={'combo':['custom text']})])
        field=reader.get_fields()['combo'].indirect_reference.get_object()
        self.assertEqual(field['/V'],'custom text');self.assertNotIn('/I',field)
        self.assertIn(b'custom text',field['/AP']['/N'].get_data())

    def test_editable_combo_preserves_export_label_schema_for_predefined_selection(self):
        self.editable()
        reader=self.save([dict(kind='fill-form-controls',values={'combo':['B']})])
        field=reader.get_fields()['combo'].indirect_reference.get_object()
        self.assertEqual(field['/V'],'B');self.assertEqual(list(field['/I']),[1])
        self.assertIn(b'Beta',field['/AP']['/N'].get_data())
        self.assertEqual(list(field['/Opt'][1]),['B','Beta'])

    def test_editable_combo_refuses_control_characters_and_retains_source(self):
        self.editable();before=self.source.read_bytes()
        with self.assertRaises(ValueError):self.save([dict(kind='fill-form-controls',values={'combo':['bad\nline']})])
        self.assertFalse(self.out.exists());self.assertEqual(self.source.read_bytes(),before)

    def test_ink_roundtrips_absolute_pdf_coordinates_and_vector_appearance(self):
        paths=[[10,20,30,60,70,25],[80,90,110,90]]
        reader=self.save([dict(kind='add-ink',page=0,paths=paths,text='hand drawn')])
        ink=reader.pages[0]['/Annots'][-1].get_object()
        self.assertEqual(ink['/Subtype'],'/Ink');self.assertEqual([list(p) for p in ink['/InkList']],paths)
        self.assertTrue(int(ink['/F'])&4);self.assertIn(b'1 0 0 RG',ink['/AP']['/N'].get_data())
        self.assertEqual(inspect_document_panels(self.out)['comments'][-1]['contents'],'hand drawn')

    def test_ink_limits_reject_unusable_paths_and_out_of_page_points(self):
        for paths in ([],[[1,2]],[[1,2,1,2]],[[-1,2,5,8]],[[1,2,3,float('nan')]],
                      [[1,2,3,4]]*33,[[1,2,3,4]*2100]):
            with self.subTest(length=len(paths)),self.assertRaises(ValueError):create_ink([0,0,200,300],paths,'')

    def test_reply_chain_is_same_page_searchable_and_original_parent_is_preserved(self):
        first_reply_index=len(PdfReader(self.source).pages[0]['/Annots'])
        reader=self.save([dict(kind='add-reply',page=0,index=0,text='first response',author='A'),
                          dict(kind='add-reply',page=0,index=first_reply_index,text='second response',author='B')])
        self.assertEqual(len(reader.pages[0]['/Annots']),first_reply_index+2)
        comments=inspect_document_panels(self.out)['comments']
        self.assertEqual([c['thread_depth'] for c in comments],[0,1,2])
        self.assertEqual(comments[0]['contents'],'Original note')
        self.assertEqual(comments[-1]['author'],'B')

    def test_undo_redo_ink_and_reply_are_real_worker_draft_operations(self):
        session=EditSession(self.source)
        try:
            session.add(dict(kind='add-ink',page=0,paths=[[10,20,50,60]],text='ink'))
            session.add(dict(kind='add-reply',page=0,index=0,text='response',author='Author'))
            self.assertEqual(len(inspect_document_panels(session.preview)['comments']),3)
            session.undo();self.assertEqual(len(inspect_document_panels(session.preview)['comments']),2)
            session.redo();session.save(self.out)
            self.assertEqual(len(inspect_document_panels(self.out)['comments']),3)
        finally:session.close()


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK and X display')
class FormsInkReplyGUITests(unittest.TestCase):
    def test_drawing_pad_captures_drag_and_returns_pdf_stroke(self):
        from main import Gtk,GLib,Gdk
        from edit_dialogs import ink_operation_dialog
        parent=Gtk.Window();parent.show_all();failures=[]
        def draw():
            try:
                dialog=next(w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog) and w.get_title()=='Desenhar à mão livre')
                def descend(widget):
                    if isinstance(widget,Gtk.DrawingArea):return widget
                    if isinstance(widget,Gtk.Container):
                        for child in widget.get_children():
                            found=descend(child)
                            if found:return found
                area=descend(dialog)
                for kind,x,y in [(Gdk.EventType.BUTTON_PRESS,40,40),(Gdk.EventType.MOTION_NOTIFY,70,90),(Gdk.EventType.BUTTON_RELEASE,100,80)]:
                    event=Gdk.Event.new(kind);event.x=x;event.y=y
                    if kind!=Gdk.EventType.MOTION_NOTIFY:event.button=1
                    area.emit({Gdk.EventType.BUTTON_PRESS:'button-press-event',Gdk.EventType.MOTION_NOTIFY:'motion-notify-event',
                               Gdk.EventType.BUTTON_RELEASE:'button-release-event'}[kind],event)
                dialog.response(Gtk.ResponseType.OK)
            except Exception as exc:
                failures.append(exc)
                for w in Gtk.Window.list_toplevels():
                    if isinstance(w,Gtk.Dialog):w.response(Gtk.ResponseType.CANCEL)
            return False
        GLib.timeout_add(150,draw)
        try:
            result=ink_operation_dialog(parent,{'page_boxes':[[0,0,200,300]]},0)
            if failures:raise failures[0]
            self.assertEqual(result['kind'],'add-ink');self.assertGreaterEqual(len(result['paths'][0]),4)
            create_ink([0,0,200,300],result['paths'],'')
        finally:parent.destroy()
