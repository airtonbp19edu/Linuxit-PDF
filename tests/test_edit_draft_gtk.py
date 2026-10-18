"""GTK draft actions, real dialogs/workers and serialized rendering results."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from test_advanced_edits import make_controls
from pypdf import PdfReader
from test_copy_edit_gtk import Gtk, GLib, wait_for, descendants


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class EditDraftGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow,load_css
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-draft-gtk-');self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';make_controls(self.source);self.original=self.source.read_bytes()
        self.callback_errors=[];self.hook=patch.object(sys,'excepthook',lambda *e:self.callback_errors.append(e));self.hook.start()
        self.quit=patch.object(Gtk,'main_quit');self.quit.start();load_css()
        self.parent=PDFWindow();self.parent.open_document(str(self.source))
        wait_for(lambda:self.parent.page_count==2 and self.parent.current_pixbuf is not None)
        self.parent._show_edit_draft();self.window=self.parent.edit_window
        wait_for(lambda:self.window.session is not None and not self.window.busy)
    def tearDown(self):
        if not self.window.closed:self.window.destroy()
        self.parent.destroy();self.quit.stop();self.hook.stop();self.temp.cleanup()
        self.assertEqual(self.callback_errors,[])
    def add(self,operation):
        count=self.window.session.cursor
        with patch.object(self.parent,'_copy_edit_operation_dialog',return_value=operation):self.window.add_button.clicked()
        wait_for(lambda:not self.window.busy and self.window.session.cursor==count+1)
    def respond(self,title,edit):
        def callback():
            dialog=next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog) and w.get_title()==title),None)
            if dialog is None:return True
            edit(dialog);dialog.response(Gtk.ResponseType.OK);return False
        return GLib.timeout_add(20,callback)
    def real_add(self,kind,title,edit):
        self.window.kind.set_active_id(kind);count=self.window.session.cursor
        idle=self.respond(title,edit)
        try:
            self.window.add_button.clicked();wait_for(lambda:not self.window.busy and self.window.session.cursor==count+1)
        finally:
            if GLib.MainContext.default().find_source_by_id(idle):GLib.source_remove(idle)

    def test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy(self):
        self.assertFalse(self.window.undo_button.get_sensitive());self.assertFalse(self.window.save_button.get_sensitive())
        self.add({'kind':'add-bookmark','title':'A','page':0});self.add({'kind':'add-bookmark','title':'B','page':0})
        self.window.undo_button.clicked();wait_for(lambda:not self.window.busy and self.window.session.cursor==1)
        target=self.root/'saved.pdf'
        with patch.object(self.window,'_choose_destination',return_value=str(target)):self.window.save_button.clicked()
        wait_for(lambda:not self.window.busy and target.exists());saved=target.read_bytes()
        self.window.redo_button.clicked();wait_for(lambda:not self.window.busy and self.window.session.cursor==2)
        self.assertEqual(target.read_bytes(),saved);self.assertEqual(self.source.read_bytes(),self.original)
        self.assertEqual(self.parent.filepath,str(self.source))
        self.assertEqual([n.title for n in PdfReader(target).outline if not isinstance(n,list)],['Parent','Sibling','A'])
        directory=os.environ.get('LINUXIT_SEARCH_CAPTURE_DIR')
        if directory:
            from gi.repository import Gdk
            path=Path(directory);path.mkdir(parents=True,exist_ok=True)
            pix=Gdk.pixbuf_get_from_window(self.window.get_window(),0,0,self.window.get_allocated_width(),self.window.get_allocated_height())
            self.assertIsNotNone(pix);pix.savev(str(path/'edit-draft.png'),'png',[],[])

    def test_real_form_dialog_checkbox_radio_list_and_multiselect(self):
        cases=[(0,True),(1,'/Right'),(2,['B']),(4,['A','C'])]
        for field_index,expected in cases:
            def edit(dialog,index=field_index):
                first=next(w for w in descendants(dialog) if isinstance(w,Gtk.ComboBoxText));first.set_active(index)
                if index==0:
                    next(w for w in descendants(dialog) if isinstance(w,Gtk.CheckButton)).set_active(True)
                elif index==4:
                    for w in descendants(dialog):
                        if isinstance(w,Gtk.CheckButton):w.set_active(w.get_label() in ('Alpha','Gamma'))
                else:
                    combos=[w for w in descendants(dialog) if isinstance(w,Gtk.ComboBoxText)]
                    combos[1].set_active(2)
            self.real_add('fill-form-controls','Preencher caixas e listas',edit)
            records={r['name']:r for r in self.window.session.info['form_controls']}
            name=('check','radio','choice','combo','multi')[field_index]
            self.assertEqual(records[name]['value'],expected)

    def test_real_move_and_delete_bookmark_dialogs_use_updated_paths(self):
        def move(dialog):
            combos=[w for w in descendants(dialog) if isinstance(w,Gtk.ComboBoxText)]
            combos[0].set_active(0);combos[1].set_active(1)
        self.real_add('move-bookmark','Mover marcador',move)
        self.assertEqual(self.window.session.info['bookmarks'][1]['path'],[0,0])
        def delete(dialog):next(w for w in descendants(dialog) if isinstance(w,Gtk.ComboBoxText)).set_active(1)
        self.real_add('delete-bookmark','Excluir marcador e descendentes',delete)
        self.assertEqual([r['title'] for r in self.window.session.info['bookmarks']],['Sibling'])

    def test_real_area_annotation_dialog_and_delete_keep_other_annotations(self):
        def highlight(dialog):
            values={'Esquerda':20,'Inferior':30,'Direita':120,'Superior':50}
            for w in descendants(dialog):
                if isinstance(w,Gtk.SpinButton):w.set_value(values[w.get_accessible().get_name()])
                elif isinstance(w,Gtk.Entry):w.set_text('New highlight')
        self.real_add('add-highlight','Destacar área',highlight)
        self.assertEqual(self.window.session.info['annotations'][-1]['subtype'],'/Highlight')
        self.real_add('delete-annotation','Excluir anotação',lambda d:next(w for w in descendants(d) if isinstance(w,Gtk.ComboBoxText)).set_active(1))
        self.assertEqual([r['text'] for r in self.window.session.info['annotations']],['Original note'])

    def test_failed_operation_and_existing_destination_keep_history_usable(self):
        self.add({'kind':'add-bookmark','title':'A','page':0})
        with patch.object(self.parent,'_copy_edit_operation_dialog',return_value={'kind':'delete-bookmark','path':[999]}):self.window.add_button.clicked()
        wait_for(lambda:not self.window.busy);self.assertEqual(self.window.session.cursor,1)
        target=self.root/'keep.pdf';target.write_bytes(b'keep')
        with patch.object(self.window,'_choose_destination',return_value=str(target)):self.window.save_button.clicked()
        wait_for(lambda:not self.window.busy);self.assertEqual(target.read_bytes(),b'keep')
        self.assertTrue(self.window.undo_button.get_sensitive());self.assertEqual(self.source.read_bytes(),self.original)

    def test_cancel_dialog_and_reopen_parent_close_draft_without_publishing(self):
        with patch.object(self.parent,'_copy_edit_operation_dialog',return_value=None):self.window.add_button.clicked()
        self.assertEqual(self.window.session.cursor,0)
        self.add({'kind':'add-bookmark','title':'A','page':0});preview=self.window.session.preview
        self.parent.open_document(str(self.source));wait_for(lambda:self.window.closed)
        self.assertFalse(preview.exists());self.assertEqual(sorted(p.name for p in self.root.iterdir()),['source.pdf'])

    def test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes(self):
        self.add({'kind':'add-bookmark','title':'A','page':0})
        with patch.object(self.window,'_choose_destination',return_value=None):self.window.save_button.clicked()
        self.assertFalse(self.window.busy);self.assertEqual(sorted(p.name for p in self.root.iterdir()),['source.pdf'])
        target=self.root/'once.pdf'
        with patch.object(self.window,'_choose_destination',return_value=str(target)) as choose:
            self.window.save_button.clicked();self.window.save_button.clicked()
            wait_for(lambda:not self.window.busy and target.exists());self.assertEqual(choose.call_count,1)

    def test_saved_form_and_highlight_render_with_poppler(self):
        from rendering import render_page_to_png
        from gi.repository import GdkPixbuf
        self.add({'kind':'fill-form-controls','values':{'check':True,'choice':['B'],'multi':['A','C']}})
        self.add({'kind':'add-highlight','page':0,'rect':[20,200,150,230],'text':'Area'})
        target=self.root/'render.pdf'
        with patch.object(self.window,'_choose_destination',return_value=str(target)):self.window.save_button.clicked()
        wait_for(lambda:not self.window.busy and target.exists())
        png=render_page_to_png(target,0,self.root/'render.png',dpi=96)
        pix=GdkPixbuf.Pixbuf.new_from_file(str(png));self.assertEqual(pix.get_width(),267)
        self.assertTrue(any(v!=255 for v in pix.get_pixels()))
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(),self.window.session.identity)


if __name__=='__main__':unittest.main()
