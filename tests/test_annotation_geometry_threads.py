import hashlib,math,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.annotations import Text
from pypdf.generic import ArrayObject,DictionaryObject,NameObject,NumberObject,TextStringObject
from pdf_changes import save_edited_copy,inspect_editable_document


class AnnotationGeometryThreadTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';writer=PdfWriter();writer.add_blank_page(400,300);writer.add_blank_page(400,300)
        writer.add_annotation(0,Text(rect=(10,10,30,30),text='root'))
        writer.write(self.source);self.counter=0

    def save(self,operations,source=None):
        source=source or self.source;self.counter+=1;target=self.root/f'copy-{self.counter}.pdf'
        save_edited_copy(source,target,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=operations)
        return target

    def test_polygon_polyline_and_caret_have_explicit_printable_vector_appearances(self):
        before=self.source.read_bytes();out=self.save([dict(kind='add-polygon',page=0,points=[[50,50],[100,150],[150,50]],text='poly'),dict(kind='add-polyline',page=0,points=[[200,50],[250,50],[250,100]],text='line'),dict(kind='add-caret',page=0,rect=[50,200,80,240],text='insert')])
        notes=[x.get_object() for x in PdfReader(out).pages[0]['/Annots']][1:]
        self.assertEqual([n['/Subtype'] for n in notes],['/Polygon','/PolyLine','/Caret'])
        self.assertTrue(all(int(n['/F'])&4 and b'S' in n['/AP']['/N'].get_data() for n in notes))
        self.assertEqual(notes[0]['/Vertices'],[50,50,100,150,150,50]);self.assertEqual(self.source.read_bytes(),before)

    def test_move_keeps_all_polygon_geometry_and_appearance_relative(self):
        first=self.save([dict(kind='add-polygon',page=0,points=[[50,50],[100,150],[150,50]],text='poly')])
        original=PdfReader(first).pages[0]['/Annots'][1].get_object()
        out=self.save([dict(kind='move-annotation',page=0,index=1,dx=10,dy=-5)],first)
        moved=PdfReader(out).pages[0]['/Annots'][1].get_object()
        self.assertEqual(moved['/Vertices'],[60,45,110,145,160,45])
        self.assertEqual(moved['/AP']['/N'].get_data(),original['/AP']['/N'].get_data())

    def test_reply_edit_retains_parent_and_full_text_in_editor(self):
        first=self.save([dict(kind='add-reply',page=0,index=0,text='reply',author='first')])
        long='resposta ' * 80
        out=self.save([dict(kind='update-comment',page=0,index=1,text=long,author='second')],first)
        notes=PdfReader(out).pages[0]['/Annots']
        self.assertEqual(notes[1]['/IRT']['/Contents'],'root');self.assertEqual(notes[1]['/Contents'],long)
        info=inspect_editable_document(out)
        self.assertEqual(info['conversation_comments'][1]['text'],long)

    def test_popup_parent_toggle_and_whole_conversation_delete_preserve_other_notes(self):
        first=self.save([dict(kind='add-reply',page=0,index=0,text='reply',author=''),dict(kind='set-popup',page=0,index=0,rect=[150,150,300,250],open=True),dict(kind='add-note',page=1,rect=[10,10,30,30],text='keep')])
        notes=PdfReader(first).pages[0]['/Annots'];self.assertEqual(notes[2]['/Parent']['/Contents'],'root')
        second=self.save([dict(kind='set-popup',page=0,index=0,rect=[150,150,300,250],open=False)],first)
        self.assertFalse(PdfReader(second).pages[0]['/Annots'][2]['/Open'].value)
        out=self.save([dict(kind='delete-conversation',page=0,index=0)],second)
        reader=PdfReader(out);self.assertEqual(len(reader.pages[0]['/Annots']),0);self.assertEqual(reader.pages[1]['/Annots'][0]['/Contents'],'keep')

    def test_locked_descendant_refuses_entire_conversation(self):
        first=self.save([dict(kind='add-reply',page=0,index=0,text='reply',author='')])
        writer=PdfWriter(clone_from=first);writer.pages[0]['/Annots'][1].get_object()[NameObject('/F')]=NumberObject(128)
        locked=self.root/'locked.pdf';writer.write(locked)
        with self.assertRaisesRegex(ValueError,'bloqueado'):self.save([dict(kind='delete-conversation',page=0,index=0)],locked)
        self.assertFalse((self.root/f'copy-{self.counter}.pdf').exists())

    def test_cross_page_reply_refuses_deletion_without_leaving_orphan(self):
        writer=PdfWriter(clone_from=self.source);root=writer.pages[0]['/Annots'][0]
        note=Text(rect=(10,10,30,30),text='other-page');note[NameObject('/IRT')]=root
        writer.add_annotation(1,note);path=self.root/'cross-page.pdf';writer.write(path)
        with self.assertRaisesRegex(ValueError,'outra página'):self.save([dict(kind='delete-conversation',page=0,index=0)],path)

    def test_invalid_polygon_and_out_of_bounds_move_never_publish(self):
        for points in ([[50,50],[100,100],[50,100],[100,50]],[[1,2],[math.nan,3],[4,5]]):
            with self.assertRaises(ValueError):self.save([dict(kind='add-polygon',page=0,points=points,text='')])
            self.assertFalse((self.root/f'copy-{self.counter}.pdf').exists())
        with self.assertRaises(ValueError):self.save([dict(kind='move-annotation',page=0,index=0,dx=-50,dy=0)])


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires Pango/Cairo/Poppler and GTK')
class AnnotationAppearanceLinuxTests(unittest.TestCase):
    def test_unicode_freetext_and_stamp_embed_fonts_and_render_real_pixels(self):
        from rendering import render_page_to_png
        from PIL import Image
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'source.pdf';out=root/'out.pdf'
            w=PdfWriter();w.add_blank_page(400,300);w.write(source)
            save_edited_copy(source,out,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),operations=[dict(kind='add-freetext',page=0,rect=[20,150,350,250],text='Olá α שלום\nTexto próprio'),dict(kind='add-stamp',page=0,rect=[30,30,200,100],text='APROVADO')])
            reader=PdfReader(out);notes=reader.pages[0]['/Annots'];embedded=False
            for note in notes:
                fonts=note['/AP']['/N']['/Resources']['/Font']
                for ref in fonts.values():
                    font=ref.get_object();descendants=font.get('/DescendantFonts',[font])
                    for child in descendants:
                        descriptor=child.get_object().get('/FontDescriptor',{})
                        if hasattr(descriptor,'get_object'):descriptor=descriptor.get_object()
                        embedded=embedded or any(key in descriptor for key in ('/FontFile','/FontFile2','/FontFile3'))
            self.assertTrue(embedded);self.assertEqual(notes[0]['/Contents'],'Olá α שלום\nTexto próprio')
            png=root/'page.png';render_page_to_png(str(out),0,png,dpi=72)
            with Image.open(png) as image:
                red=sum(r>g*1.5 and r>b*1.5 and r>80 for r,g,b in image.convert('RGB').getdata())
            self.assertGreater(red,100)

    def test_polygon_dialog_returns_its_vertices(self):
        from main import Gtk,GLib
        from edit_dialogs import advanced_operation_dialog
        parent=Gtk.Window();info=dict(page_boxes=[[0,0,400,300]])
        def accept():
            dialog=next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog)),None)
            if dialog is None:return True
            dialog.response(Gtk.ResponseType.OK);return False
        GLib.timeout_add(30,accept)
        try:result=advanced_operation_dialog(parent,'add-polygon',info,0)
        finally:parent.destroy()
        self.assertEqual(result['kind'],'add-polygon');self.assertEqual(len(result['points']),3)
