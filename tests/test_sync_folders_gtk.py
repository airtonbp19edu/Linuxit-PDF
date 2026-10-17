"""Own GTK folder/copy workflows; native portal responses are tested at the UI seam."""
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch,Mock

from test_security_accessibility_gtk import _UISetup,Gtk,GLib,wait_for,capture
import local_files as local
if Gtk is not None:import folder_dialogs as folders
else:folders=None


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class SyncFolderGTKTests(_UISetup,unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.config=patch.dict(os.environ,{'XDG_CONFIG_HOME':str(self.root/'config')});self.config.start()
        self.sync=self.root/'Pasta sincronizada ç';self.sync.mkdir()
        local.remember_folder('sync_folder',str(self.sync))
        self.messages=[];self.parent._error=self.messages.append

    def tearDown(self):
        try:super().tearDown()
        finally:self.config.stop()

    def run_chooser(self,title,target,action):
        def respond():
            dialog=next((w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.FileChooserDialog) and w.get_title()==title),None)
            if dialog is None:return True
            if dialog.get_current_folder()!=str(target.parent):dialog.set_current_folder(str(target.parent));return True
            if dialog.get_action()==Gtk.FileChooserAction.SAVE:
                dialog.set_current_name(target.name)
            elif dialog.get_filename()!=str(target):
                dialog.select_filename(str(target));return True
            dialog.response(Gtk.ResponseType.OK);return False
        timer=GLib.timeout_add(40,respond)
        try:action()
        finally:
            if GLib.MainContext.default().find_source_by_id(timer):GLib.source_remove(timer)

    def test_real_file_chooser_uses_preferred_folder_and_shortcut(self):
        chooser=Gtk.FileChooserDialog(title='Folder fixture',transient_for=self.parent,action=Gtk.FileChooserAction.OPEN)
        try:
            folders.prepare_chooser(chooser)
            wait_for(lambda:chooser.get_current_folder()==str(self.sync))
            self.assertIn(str(self.sync),chooser.list_shortcut_folders())
        finally:chooser.destroy()

    def test_native_folder_response_and_cancel_preserve_explicit_choice(self):
        # This simulates the desktop reply; it is not proof of an actual portal backend.
        other=self.root/'another';other.mkdir()
        chooser=Mock();chooser.run.return_value=Gtk.ResponseType.ACCEPT;chooser.get_filename.return_value=str(other)
        with patch.object(folders.Gtk.FileChooserNative,'new',return_value=chooser):self.parent._choose_sync_folder()
        self.assertEqual(local.read_folders()['sync_folder'],str(other));chooser.destroy.assert_called_once()
        chooser=Mock();chooser.run.return_value=Gtk.ResponseType.CANCEL
        with patch.object(folders.Gtk.FileChooserNative,'new',return_value=chooser):self.parent._choose_sync_folder()
        self.assertEqual(local.read_folders()['sync_folder'],str(other))

    def test_open_pdf_from_preferred_folder_really_renders(self):
        source=self.sync/'document.pdf';source.write_bytes(self.original)
        self.run_chooser('Abrir PDF',source,self.parent._open_sync_folder)
        wait_for(lambda:self.parent.filepath==str(source) and self.parent.current_pixbuf is not None)
        self.assertEqual(self.parent.page_count,2);self.assertEqual(local.read_folders()['last_open'],str(self.sync))
        self.assertEqual(source.read_bytes(),self.original)

    def test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save(self):
        target=self.sync/'document-copia.pdf'
        self.run_chooser('Salvar cópia',target,self.parent._save_copy)
        wait_for(lambda:target.exists() and 'salva localmente' in self.parent.status_file.get_text())
        self.assertEqual(target.read_bytes(),self.original);self.assertEqual(self.source.read_bytes(),self.original)
        self.assertIn('sincronizador',self.parent.status_file.get_text())
        self.assertEqual(local.read_folders()['last_save'],str(self.sync));capture(self.parent,'synced-local-folder')

    def test_external_replacement_blocks_save_and_edit_until_reopen(self):
        self.source.write_bytes(self.original+b'\n% external replacement')
        with patch('main.Gtk.FileChooserDialog') as chooser:
            self.parent._save_copy();self.parent._begin_copy_edit('add-bookmark');chooser.assert_not_called()
        self.assertEqual(len(self.messages),2);self.assertTrue(all('externamente' in m for m in self.messages))
        self.parent.open_document(str(self.source));wait_for(lambda:self.parent.current_pixbuf is not None)
        self.assertTrue(self.parent._source_unchanged())

    def test_document_change_during_destination_choice_does_not_start_stale_copy(self):
        target=self.sync/'obsolete.pdf';chooser=Mock()
        def reopened():self.parent.open_document(str(self.source));return Gtk.ResponseType.OK
        chooser.run.side_effect=reopened;chooser.get_filename.return_value=str(target)
        with patch('main.Gtk.FileChooserDialog',return_value=chooser),patch('main.run_search_worker') as worker:
            self.parent._save_copy();worker.assert_not_called()
        self.assertFalse(target.exists())

    def test_forget_removes_preference_without_changing_files_or_other_preferences(self):
        target=self.sync/'keep.pdf';target.write_bytes(self.original)
        local.remember_folder('last_save',str(self.sync));self.parent._forget_sync_folder()
        self.assertNotIn('sync_folder',local.read_folders());self.assertEqual(local.read_folders()['last_save'],str(self.sync))
        self.assertEqual(target.read_bytes(),self.original)
        self.sync.rename(self.root/'moved')
        self.assertIsNone(local.preferred_folder())

    def test_existing_destination_is_preserved_and_failure_is_shown(self):
        target=self.sync/'exists.pdf';target.write_bytes(b'keep')
        # Avoid the desktop's optional overwrite prompt: the backend must refuse independently.
        chooser=Mock();chooser.run.return_value=Gtk.ResponseType.OK;chooser.get_filename.return_value=str(target)
        with patch('main.Gtk.FileChooserDialog',return_value=chooser):self.parent._save_copy()
        wait_for(lambda:bool(self.messages));self.assertEqual(target.read_bytes(),b'keep')
        self.assertIn('nome novo',self.messages[-1]);self.assertEqual(self.source.read_bytes(),self.original)
