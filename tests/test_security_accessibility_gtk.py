"""Actual GTK/ATK, secret clearing, workers, keyboard regions and copy edit dialogs."""
from gtk_cleanup import cleanup_temp
from io import BytesIO
import os
from pathlib import Path
from types import SimpleNamespace
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from test_pdf_security import security, PdfWriter, PdfReader, text_pdf
from pypdf.annotations import Text
from test_search_extensions_gtk import Gtk, wait_for, capture
from test_copy_edit_gtk import descendants, GLib


class _UISetup:
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-security-ui-');self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.output=self.root/'protected.pdf';self.children=[];self.errors=[]
        writer=PdfWriter(clone_from=BytesIO(text_pdf(['alpha first page','beta second page'])))
        writer.add_outline_item('Existing',0);writer.add_annotation(0,Text(rect=(10,10,30,30),text='Existing note'))
        writer.write(self.source);self.original=self.source.read_bytes()
        self.hook=patch.object(sys,'excepthook',lambda *args:self.errors.append(args));self.hook.start()
        self.quit=patch.object(Gtk,'main_quit');self.quit.start()
        load_css();self.parent=PDFWindow(str(self.source))
        wait_for(lambda:self.parent.current_pixbuf is not None and self.parent.displayed_page==0)
        self.windows=[]

    def tearDown(self):
        for window in self.windows:
            if not window.closed:window.destroy()
        self.parent.destroy()
        for child in self.children:
            if child.poll() is None:child.kill();child.wait()
        self.quit.stop();self.hook.stop();cleanup_temp(self.temp);self.assertEqual(self.errors,[])

    def security_window(self):
        self.parent._show_security();window=self.parent.security_window;self.windows.append(window);return window

    def inspect(self,w):
        w._inspect();wait_for(lambda:not w.busy and w.info is not None)

    def passwords(self,w):
        for key,value in [('user','synthetic-user-pass'),('user_confirm','synthetic-user-pass'),
                          ('owner','synthetic-owner-pass'),('owner_confirm','synthetic-owner-pass')]:w.secrets[key].set_text(value)

    def text_window(self):
        self.parent._show_accessible_text();w=self.parent.accessible_text_window;self.windows.append(w);return w


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class SecurityGTKTests(_UISetup,unittest.TestCase):
    def test_inspect_protect_and_secrets_cleared_without_source_change(self):
        w=self.security_window();self.inspect(w);self.passwords(w);w.permissions['copy'].set_active(False)
        with patch.object(w,'_choose',return_value=str(self.output)):w._protect()
        self.assertTrue(all(not field.get_text() and not field.get_visibility() for field in w.secrets.values()))
        wait_for(lambda:not w.busy and self.output.exists())
        self.assertIn('AES-256 criada',w.status.get_text());capture(w,'pdf-security')
        info=security.inspect_pdf_security(self.output,{'password':'synthetic-user-pass'})
        self.assertEqual(info['role'],'user');self.assertFalse(info['permissions']['copy'])
        self.assertEqual(self.source.read_bytes(),self.original)
        self.assertNotIn('synthetic-user-pass',w.status.get_text())

    def test_encrypted_inspection_wrong_and_owner_credentials(self):
        security.protect_pdf_copy(self.source,{'destination':str(self.output),'source_sha256':security._sha(self.source),
            'user_password':'synthetic-user-pass','owner_password':'synthetic-owner-pass','permissions':{k:True for k in security.PERMISSION_FLAGS}})
        w=self.security_window();w.path.set_text(str(self.output));self.inspect(w)
        self.assertFalse(w.info['authenticated']);self.assertIn('não autenticou',w.status.get_text())
        w.secrets['inspect'].set_text('synthetic-owner-pass');self.inspect(w)
        self.assertEqual(w.info['role'],'owner');self.assertIn('proprietário autenticada',w.status.get_text())
        self.assertFalse(w.secrets['inspect'].get_text());w._protect()
        self.assertIn('sem criptografia',w.status.get_text())

    def test_password_mismatch_and_cancelled_destination_create_nothing(self):
        w=self.security_window();self.inspect(w);self.passwords(w);w.secrets['user_confirm'].set_text('different-pass')
        with patch.object(w,'_choose') as chooser:w._protect();chooser.assert_not_called()
        self.assertIn('não coincidem',w.status.get_text());self.assertFalse(self.output.exists())
        self.passwords(w)
        with patch.object(w,'_choose',return_value=None):w._protect()
        self.assertFalse(w.busy);self.assertTrue(all(not f.get_text() for f in w.secrets.values()))

    def test_document_change_during_destination_dialog_discards_request(self):
        w=self.security_window();self.inspect(w);self.passwords(w)
        def changed(*args,**kwargs):w.path.set_text(str(self.root/'other.pdf'));return str(self.output)
        with patch.object(w,'_choose',side_effect=changed):w._protect()
        self.assertFalse(w.busy);self.assertIsNone(w.info);self.assertFalse(self.output.exists())

    def test_cancel_and_destroy_stop_actual_security_process(self):
        import search_tasks
        original=subprocess.Popen
        def delayed(argv,**kwargs):
            if 'security-info' not in argv:return original(argv,**kwargs)
            child=original([sys.executable,'-c','import time;time.sleep(30)'],**kwargs);self.children.append(child);return child
        w=self.security_window()
        with patch.object(search_tasks.subprocess,'Popen',side_effect=delayed):
            w._inspect();wait_for(lambda:len(self.children)==1);w._cancel()
            wait_for(lambda:self.children[0].poll() is not None);self.assertFalse(w.busy)
            w._inspect();wait_for(lambda:len(self.children)==2);w.destroy()
            wait_for(lambda:self.children[1].poll() is not None)
        self.assertTrue(w.closed);self.assertFalse(self.output.exists())

    def test_owner_copy_is_readable_by_main_reader_and_original_is_preserved(self):
        security.protect_pdf_copy(self.source,{'destination':str(self.output),'source_sha256':security._sha(self.source),
            'user_password':'synthetic-user-pass','owner_password':'synthetic-owner-pass','permissions':{k:False for k in security.PERMISSION_FLAGS}})
        original=self.output.read_bytes();plain=self.root/'plain.pdf';w=self.security_window()
        w.path.set_text(str(self.output));self.inspect(w);w.secrets['inspect'].set_text('synthetic-owner-pass')
        with patch.object(w,'_choose',return_value=str(plain)):w._unprotect()
        wait_for(lambda:not w.busy and plain.exists());self.assertIn('pelo proprietário',w.status.get_text())
        self.parent.open_document(str(plain));wait_for(lambda:self.parent.filepath==str(plain) and self.parent.displayed_page==0 and self.parent.current_pixbuf is not None)
        self.assertEqual(self.parent.page_count,2);self.assertEqual(self.output.read_bytes(),original)

    def test_owner_copy_rejects_opening_password_and_clears_it(self):
        security.protect_pdf_copy(self.source,{'destination':str(self.output),'source_sha256':security._sha(self.source),
            'user_password':'synthetic-user-pass','owner_password':'synthetic-owner-pass','permissions':{k:True for k in security.PERMISSION_FLAGS}})
        w=self.security_window();w.path.set_text(str(self.output));self.inspect(w)
        w.secrets['inspect'].set_text('synthetic-user-pass');plain=self.root/'not-created.pdf'
        with patch.object(w,'_choose',return_value=str(plain)):w._unprotect()
        wait_for(lambda:not w.busy and 'exige autenticação' in w.status.get_text())
        self.assertFalse(plain.exists());self.assertFalse(w.secrets['inspect'].get_text())


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class AccessibleGTKTests(_UISetup,unittest.TestCase):
    def test_real_poppler_text_is_exposed_through_atk_text_interface(self):
        from gi.repository import Atk
        w=self.text_window();wait_for(lambda:'disponível' in w.status.get_text())
        accessible=w.text.get_accessible()
        self.assertEqual(accessible.get_name(),'Texto extraído da página PDF')
        self.assertIn('alpha first page',Atk.Text.get_text(accessible,0,-1))
        self.assertFalse(w.text.get_editable());self.assertEqual(w.status.get_accessible().get_role(),Atk.Role.STATUSBAR)
        capture(w,'accessible-page-text');self.assertEqual(self.source.read_bytes(),self.original)

    def test_no_text_and_encrypted_pages_have_explicit_limits(self):
        blank=self.root/'blank.pdf';writer=PdfWriter();writer.add_blank_page(100,100);writer.write(blank)
        w=self.text_window();w.load(str(blank),0,1);wait_for(lambda:'não forneceu texto' in w.status.get_text())
        writer.encrypt('',owner_password='synthetic-owner-pass',algorithm='RC4-128');locked=self.root/'locked.pdf';writer.write(locked)
        w.load(str(locked),0,1);wait_for(lambda:'criptografados' in w.status.get_text())
        self.assertEqual(w.text.get_buffer().get_char_count(),0)

    def test_obsolete_page_text_does_not_replace_newer_page(self):
        import accessible_reader
        from accessible_reader import AccessibleTextWindow
        entered=threading.Event();release=threading.Event()
        def text(path,page,cancel=None):
            if page==0:entered.set();release.wait(10);return 'obsolete text'
            return 'current page text'
        w=AccessibleTextWindow(self.parent);self.windows.append(w);w.show_all()
        with patch.object(accessible_reader,'invoke_accessible_text',side_effect=text):
            w.load(str(self.source),0,2);wait_for(entered.is_set)
            w.load(str(self.source),1,2);release.set()
            wait_for(lambda:'disponível' in w.status.get_text())
            b=w.text.get_buffer();self.assertEqual(b.get_text(b.get_start_iter(),b.get_end_iter(),True),'current page text')
            self.assertEqual(w.heading.get_text(),'Página 2 de 2')

    def test_f6_focus_regions_names_and_list_arrow_delegation(self):
        from gi.repository import Gdk
        p=self.parent;p.interaction_layer.grab_focus();wait_for(lambda:p.get_focus() is p.interaction_layer)
        self.assertTrue(p._on_key(p,SimpleNamespace(keyval=Gdk.KEY_F6,state=0)))
        self.assertIsNot(p.get_focus(),p.interaction_layer)
        self.assertEqual(p.status_page_entry.get_accessible().get_name(),'Página atual')
        self.assertEqual(p.find_entry.get_accessible().get_name(),'Texto para localizar no PDF')
        p._show_side_panel(1);wait_for(lambda:len(p.bookmark_list.get_children())>0)
        row=p.bookmark_list.get_row_at_index(0);row.grab_focus()
        with patch.object(p,'goto_page') as navigate:
            self.assertFalse(p._on_key(p,SimpleNamespace(keyval=Gdk.KEY_Down,state=0)));navigate.assert_not_called()
        self.assertTrue(p._on_key(p,SimpleNamespace(keyval=Gdk.KEY_t,state=Gdk.ModifierType.CONTROL_MASK|Gdk.ModifierType.SHIFT_MASK)))
        self.windows.append(p.accessible_text_window)

    def test_text_limit_and_document_close_clear_the_accessible_window(self):
        import accessible_reader
        from accessible_reader import AccessibleTextWindow
        w=AccessibleTextWindow(self.parent);self.windows.append(w);self.parent.accessible_text_window=w;w.show_all()
        with patch.object(accessible_reader,'invoke_accessible_text',side_effect=ValueError('O texto desta página excede o limite de 1 MiB.')):
            w.load(str(self.source),0,2);wait_for(lambda:'1 MiB' in w.status.get_text())
        self.assertEqual(w.text.get_buffer().get_char_count(),0)
        self.parent.open_document(str(self.source));wait_for(lambda:w.closed)

    @unittest.skipUnless(sys.platform == 'linux','Linux process group verification')
    def test_closing_text_worker_terminates_its_real_descendant_on_linux(self):
        import search_tasks
        from accessible_reader import AccessibleTextWindow
        pidfile=self.root/'descendant.pid';original=subprocess.Popen;workdirs=[]
        def delayed(argv,**kwargs):
            if 'accessible-text' not in argv:return original(argv,**kwargs)
            workdirs.append(Path(kwargs['env']['TMPDIR']))
            code="import subprocess,sys,time,pathlib; c=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']); pathlib.Path(sys.argv[1]).write_text(str(c.pid)); time.sleep(30)"
            proc=original([sys.executable,'-c',code,str(pidfile)],**kwargs);self.children.append(proc);return proc
        w=AccessibleTextWindow(self.parent);self.windows.append(w);w.show_all()
        with patch.object(search_tasks.subprocess,'Popen',side_effect=delayed):
            w.load(str(self.source),0,2);wait_for(pidfile.exists);pid=int(pidfile.read_text())
            w.destroy();wait_for(lambda:self.children[0].poll() is not None)
            def dead():
                try:return Path(f'/proc/{pid}/stat').read_text().split()[2]=='Z'
                except FileNotFoundError:return True
            wait_for(dead)
            wait_for(lambda:all(not path.exists() for path in workdirs))


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class ExtendedEditGTKTests(_UISetup,unittest.TestCase):
    def test_real_dialogs_rename_note_and_rotation_save_new_copies(self):
        for kind,title in [('rename-bookmark','Renomear marcador'),('update-note','Editar nota'),('rotate-page','Girar página em cópia')]:
            target=self.root/(kind+'.pdf')
            def respond():
                dialog=next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.Dialog) and w.get_title()==title),None)
                if dialog is None:return True
                for widget in descendants(dialog):
                    if isinstance(widget,Gtk.Entry):widget.set_text('Renamed')
                    if isinstance(widget,Gtk.TextView):widget.get_buffer().set_text('Revised GTK note')
                dialog.response(Gtk.ResponseType.OK);return False
            timer=GLib.timeout_add(20,respond)
            try:
                with patch.object(self.parent,'_copy_edit_destination_dialog',return_value=str(target)):
                    self.parent._begin_copy_edit(kind);wait_for(lambda:not self.parent._copy_edit_busy and target.exists())
            finally:
                if GLib.MainContext.default().find_source_by_id(timer):GLib.source_remove(timer)
            reader=PdfReader(target)
            if kind=='rename-bookmark':self.assertEqual(reader.outline[0].title,'Renamed')
            elif kind=='update-note':self.assertEqual(reader.pages[0]['/Annots'][0].get_object()['/Contents'],'Revised GTK note')
            else:self.assertEqual(reader.pages[0].rotation,90)
            self.assertEqual(self.source.read_bytes(),self.original)
