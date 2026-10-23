"""GTK annotation dialogs and independent Poppler pixel checks of saved PDFs."""
from gtk_cleanup import cleanup_temp
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from test_advanced_edits import make_controls
from test_copy_edit_gtk import Gtk, GLib, wait_for, descendants
from test_search_extensions_gtk import capture
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, RectangleObject


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class AnnotationExtensionGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow,load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-annotations-gtk-');self.root = Path(self.temp.name)
        self.source = self.root/'source.pdf';make_controls(self.source);self.original = self.source.read_bytes()
        self.callback_errors = [];self.hook = patch.object(sys,'excepthook',lambda *e:self.callback_errors.append(e));self.hook.start()
        self.quit = patch.object(Gtk,'main_quit');self.quit.start();load_css()
        self.parent = PDFWindow();self.parent.open_document(str(self.source))
        wait_for(lambda:self.parent.page_count==2 and self.parent.current_pixbuf is not None)
        self.parent._show_edit_draft();self.window = self.parent.edit_window
        wait_for(lambda:self.window.session is not None and not self.window.busy)
        self.window.page.set_value(2)
    def tearDown(self):
        if not self.window.closed:self.window.destroy()
        self.parent.destroy();self.quit.stop();self.hook.stop();cleanup_temp(self.temp)
        self.assertEqual(self.callback_errors,[])
    def respond(self,title,edit):
        def callback():
            dialog = next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog) and w.get_title()==title),None)
            if dialog is None:return True
            try:edit(dialog)
            except Exception as exc:
                self.dialog_error = exc;dialog.response(Gtk.ResponseType.CANCEL);return False
            dialog.response(Gtk.ResponseType.OK);return False
        return GLib.timeout_add(20,callback)
    def real_add(self,kind,title,edit):
        self.dialog_error = None
        self.window.kind.set_active_id(kind);count = self.window.session.cursor;idle = self.respond(title,edit)
        try:
            self.window.add_button.clicked()
            if self.dialog_error is not None:raise self.dialog_error
            wait_for(lambda:not self.window.busy and self.window.session.cursor==count+1)
        finally:
            if GLib.MainContext.default().find_source_by_id(idle):GLib.source_remove(idle)
    def geometry(self,dialog,values):
        for widget in descendants(dialog):
            if isinstance(widget,Gtk.SpinButton):widget.set_value(values[widget.get_accessible().get_name()])
            elif isinstance(widget,Gtk.Entry):widget.set_text('Marca de revisão')
    def add(self,operation):
        count = self.window.session.cursor
        with patch.object(self.parent,'_copy_edit_operation_dialog',return_value=operation):self.window.add_button.clicked()
        wait_for(lambda:not self.window.busy and self.window.session.cursor==count+1)
    def save(self,name='saved.pdf'):
        target = self.root/name
        with patch.object(self.window,'_choose_destination',return_value=str(target)):self.window.save_button.clicked()
        wait_for(lambda:not self.window.busy and target.exists());return target
    def red_near(self,pix,x,y,radius=3):
        data,stride,channels = pix.get_pixels(),pix.get_rowstride(),pix.get_n_channels()
        for py in range(max(0,round(y)-radius),min(pix.get_height(),round(y)+radius+1)):
            for px in range(max(0,round(x)-radius),min(pix.get_width(),round(x)+radius+1)):
                r,g,b = data[py*stride+px*channels:py*stride+px*channels+3]
                if r>180 and g<100 and b<100:return True
        return False

    def test_real_dialogs_create_all_five_types_and_history_recreates_deleted_shape(self):
        cases = [('add-underline','Sublinhar área','/Underline'),('add-strikeout','Tachar área','/StrikeOut'),
                 ('add-squiggly','Sublinhar área com ondulado','/Squiggly'),('add-ellipse','Adicionar elipse','/Circle')]
        for kind,title,subtype in cases:
            self.real_add(kind,title,lambda d:self.geometry(d,{'Esquerda':20,'Inferior':30,'Direita':120,'Superior':60}))
            self.assertEqual(self.window.session.info['annotations'][-1]['subtype'],subtype)
        self.real_add('add-line','Adicionar linha',lambda d:self.geometry(d,{'X inicial':150,'Y inicial':100,'X final':30,'Y final':100}))
        target = self.save();self.assertEqual(len(PdfReader(target).pages[1]['/Annots']),5)
        capture(self.window,'annotation-extensions')
        self.real_add('delete-annotation','Excluir anotação',lambda d:next(w for w in descendants(d) if isinstance(w,Gtk.ComboBoxText)).set_active(3))
        self.assertEqual(len(self.window.session.info['annotations']),5)
        self.window.undo_button.clicked();wait_for(lambda:not self.window.busy and self.window.session.cursor==5)
        self.assertEqual(len(self.window.session.info['annotations']),6)
        self.assertEqual(self.source.read_bytes(),self.original)

    def test_comment_dialog_prefills_selected_annotation_accepts_multiline_and_can_clear(self):
        for kind in ('add-ellipse','add-underline'):
            self.add({'kind':kind,'page':1,'rect':[20,30,120,60],'text':kind})
        def edit(dialog):
            widgets = list(descendants(dialog));combo = next(w for w in widgets if isinstance(w,Gtk.ComboBoxText))
            combo.set_active(1)
            comment = next(w for w in widgets if isinstance(w,Gtk.TextView));buffer = comment.get_buffer()
            self.assertEqual(buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True),'add-underline')
            buffer.set_text('Primeira linha\nSegunda çã')
            next(w for w in widgets if isinstance(w,Gtk.Entry)).set_text('Pessoa ç')
            capture(dialog,'annotation-comment')
        self.real_add('update-annotation','Editar comentário da anotação',edit)
        record = self.window.session.info['annotations'][-1]
        self.assertEqual((record['text'],record['author']),('Primeira linha\nSegunda çã','Pessoa ç'))
        def clear(dialog):
            widgets = list(descendants(dialog));next(w for w in widgets if isinstance(w,Gtk.ComboBoxText)).set_active(1)
            next(w for w in widgets if isinstance(w,Gtk.TextView)).get_buffer().set_text('')
            next(w for w in widgets if isinstance(w,Gtk.Entry)).set_text('')
        self.real_add('update-annotation','Editar comentário da anotação',clear)
        self.assertEqual(self.window.session.info['annotations'][-1]['text'],'')
        self.assertEqual(self.window.session.info['annotations'][-1]['author'],'')

    def test_invalid_line_is_explained_in_dialog_and_cancel_does_not_change_draft(self):
        self.window.kind.set_active_id('add-line');seen = []
        def attempt():
            dialog = next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog) and w.get_title()=='Adicionar linha'),None)
            if dialog is None:return True
            if not seen:
                self.geometry(dialog,{'X inicial':20,'Y inicial':20,'X final':20,'Y final':20})
                seen.append('submitted');dialog.response(Gtk.ResponseType.OK);return True
            labels = [w.get_text() for w in descendants(dialog) if isinstance(w,Gtk.Label)]
            seen.append('explained' if any('0,25 ponto' in label for label in labels) else 'missing explanation')
            dialog.response(Gtk.ResponseType.CANCEL);return False
        idle = GLib.timeout_add(20,attempt)
        try:self.window.add_button.clicked()
        finally:
            if GLib.MainContext.default().find_source_by_id(idle):GLib.source_remove(idle)
        self.assertEqual(seen,['submitted','explained']);self.assertEqual(self.window.session.cursor,0)
        self.assertFalse(self.window.busy);self.assertEqual(sorted(p.name for p in self.root.iterdir()),['source.pdf'])

    def test_saved_five_appearances_have_expected_poppler_pixels_and_unfilled_interiors(self):
        from rendering import render_page_to_png
        from gi.repository import GdkPixbuf
        for kind,key,geometry in [('add-underline','rect',[20,240,180,260]),('add-strikeout','rect',[20,190,180,210]),
                                  ('add-squiggly','rect',[20,140,180,160]),('add-ellipse','rect',[40,70,160,120]),
                                  ('add-line','points',[180,20,20,50])]:
            self.add({'kind':kind,'page':1,key:geometry,'text':''})
        target = self.save();png = Path(render_page_to_png(target,1,self.root/'render.png',dpi=144))
        pix = GdkPixbuf.Pixbuf.new_from_file(str(png));self.assertEqual((pix.get_width(),pix.get_height()),(400,600))
        for x,y in ((80,240.625),(80,200),(100,142),(100,119.375),(40.625,95),(100,35)):
            self.assertTrue(self.red_near(pix,x*2,(300-y)*2),f'missing mark at {x},{y}')
        for x,y in ((80,250),(80,205),(100,155),(100,95),(30,100)):
            self.assertFalse(self.red_near(pix,x*2,(300-y)*2,1),f'unexpected fill at {x},{y}')
        folder = os.environ.get('LINUXIT_SEARCH_CAPTURE_DIR')
        if folder:
            directory = Path(folder);directory.mkdir(parents=True,exist_ok=True);dest = directory/'annotation-render.png';shutil.copyfile(png,dest)
            (directory/'annotation-render.json').write_text(json.dumps({'scope':'Own saved PDF rendered with Poppler; no Foxit observation',
                'width':pix.get_width(),'height':pix.get_height(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')

    def test_offset_cropbox_and_rotation_render_line_at_transformed_location(self):
        from pdf_changes import save_edited_copy
        from rendering import render_page
        from gi.repository import GdkPixbuf
        source,target = self.root/'offset.pdf',self.root/'offset-copy.pdf'
        writer = PdfWriter();page = writer.add_blank_page(200,300)
        page.mediabox = RectangleObject([10,-30,210,270]);page.cropbox = RectangleObject([20,-20,200,250])
        page[NameObject('/Rotate')] = NumberObject(90);writer.write(source)
        original = source.read_bytes()
        save_edited_copy(source,target,source_sha256=hashlib.sha256(original).hexdigest(),
                         operations=[{'kind':'add-strikeout','page':0,'rect':[40,50,160,70],'text':'offset'}])
        png = render_page(str(target),0,540,self.root/'cache')
        pix = GdkPixbuf.Pixbuf.new_from_file(png);self.assertEqual((pix.get_width(),pix.get_height()),(540,360))
        self.assertTrue(self.red_near(pix,160,120));self.assertFalse(self.red_near(pix,120,160,1))
        self.assertEqual(source.read_bytes(),original)

    def test_edited_nontext_annotation_comment_is_searchable_after_reopening_saved_copy(self):
        self.add({'kind':'add-squiggly','page':1,'rect':[20,30,120,60],'text':'before'})
        self.add({'kind':'update-annotation','page':1,'index':0,'text':'revisaoUnica','author':'Pessoa'})
        target = self.save();self.parent.open_document(str(target))
        wait_for(lambda:self.window.closed and self.parent.current_pixbuf is not None)
        w = self.parent;w._show_find();w.find_results_toggle.set_active(True)
        w.find_options['include_page_text'].set_active(False);w.find_options['include_comments'].set_active(True)
        w.find_entry.set_text('revisaoUnica');wait_for(lambda:len(w.search_hits)==1 and not w.search_running)
        self.assertEqual(w.search_hits[0]['page'],1)
        self.assertEqual(self.source.read_bytes(),self.original)


if __name__=='__main__':unittest.main()
