"""Folder persistence and atomic local copies; no real cloud service is contacted."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
import local_files as local
from search_tasks import run_search_worker


class FolderPreferencesTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-folders-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.folder=self.root/'Pasta sincronizada ç';self.folder.mkdir()
        self.env=patch.dict(os.environ,{'XDG_CONFIG_HOME':str(self.root/'config')});self.env.start();self.addCleanup(self.env.stop)

    def test_sync_folder_roundtrip_is_separate_from_theme_and_contains_no_account(self):
        theme=local.folders_path().parent/'preferences.json';theme.parent.mkdir(parents=True)
        theme.write_text('{"appearance":"dark"}',encoding='utf-8')
        local.remember_folder('sync_folder',str(self.folder))
        self.assertEqual(local.read_folders(),{'sync_folder':str(self.folder)})
        self.assertEqual(json.loads(theme.read_text())['appearance'],'dark')
        self.assertEqual(local.preferred_folder(),str(self.folder))
        if os.name!='nt':self.assertEqual(local.folders_path().stat().st_mode&0o777,0o600)

    def test_last_open_save_and_source_are_fallbacks_for_unavailable_preference(self):
        other=self.root/'other';other.mkdir()
        local.remember_folder('sync_folder',str(self.folder));local.remember_folder('last_open',str(other))
        local.remember_folder('last_save',str(other));self.folder.rmdir()
        self.assertEqual(local.preferred_folder('open'),str(other));self.assertEqual(local.preferred_folder('save'),str(other))
        other.rmdir();self.assertEqual(local.preferred_folder('save',self.root/'source.pdf'),str(self.root))

    def test_forget_preserves_files_and_other_folder_preferences(self):
        file=self.folder/'preserve.pdf';file.write_bytes(b'keep')
        local.remember_folder('sync_folder',str(self.folder));local.remember_folder('last_open',str(self.root))
        local.remember_folder('sync_folder',None)
        self.assertEqual(local.read_folders(),{'last_open':str(self.root)});self.assertEqual(file.read_bytes(),b'keep')

    def test_invalid_relative_missing_and_unknown_settings_are_refused(self):
        for key,path in [('unknown',str(self.folder)),('sync_folder','relative'),('sync_folder',str(self.root/'missing'))]:
            with self.assertRaises(ValueError):local.remember_folder(key,path)
        self.assertFalse(local.folders_path().exists())

    def test_corrupt_oversized_and_malicious_settings_fall_back_without_network(self):
        path=local.folders_path();path.parent.mkdir(parents=True)
        for raw in ['[1]', 'invalid', 'x'*17000, '{"sync_folder":"https://example.test/cloud","last_open":true}']:
            path.write_text(raw);self.assertEqual(local.read_folders(),{})

    def test_failed_preference_replacement_preserves_previous_bytes(self):
        local.remember_folder('sync_folder',str(self.folder));before=local.folders_path().read_bytes()
        with patch.object(local.os,'replace',side_effect=OSError('synthetic')),self.assertRaises(OSError):
            local.remember_folder('sync_folder',None)
        self.assertEqual(local.folders_path().read_bytes(),before)
        self.assertEqual(list(local.folders_path().parent.glob('.folders-*')),[])


class AtomicLocalCopyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-atomic-');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.source=self.root/'source.pdf';self.source.write_bytes(b'%PDF synthetic fixture\n'+b'a'*1024**2)
        self.output=self.root/'copy.pdf';self.original=self.source.read_bytes()
        self.request={'destination':str(self.output),'source_stamp':local.file_stamp(self.source)}

    def test_worker_roundtrip_preserves_source_and_never_claims_remote_sync(self):
        result=run_search_worker('copy-file',self.source,self.request)
        self.assertTrue(result['saved_locally']);self.assertFalse(result['remote_sync_confirmed'])
        self.assertEqual(result['output_sha256'],hashlib.sha256(self.original).hexdigest())
        self.assertEqual(self.output.read_bytes(),self.original);self.assertEqual(self.source.read_bytes(),self.original)
        if os.name!='nt':self.assertEqual(self.output.stat().st_mode&0o777,0o600)

    def test_final_name_is_absent_while_real_copy_is_in_progress(self):
        entered=threading.Event();release=threading.Event();errors=[];original=local.shutil.copyfileobj
        def slow(input_,output,*args):
            output.write(input_.read(32));output.flush();entered.set();release.wait(10)
            original(input_,output,*args)
        def task():
            try:local.copy_local_document(self.source,self.request)
            except BaseException as exc:errors.append(exc)
        with patch.object(local.shutil,'copyfileobj',side_effect=slow):
            thread=threading.Thread(target=task);thread.start()
            try:
                self.assertTrue(entered.wait(10));self.assertFalse(self.output.exists())
                self.assertEqual(self.source.read_bytes(),self.original)
            finally:release.set();thread.join(15)
        self.assertFalse(thread.is_alive());self.assertEqual(errors,[]);self.assertEqual(self.output.read_bytes(),self.original)

    def test_existing_file_and_destination_race_are_never_overwritten(self):
        self.output.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):local.copy_local_document(self.source,self.request)
        self.assertEqual(self.output.read_bytes(),b'keep');self.output.unlink()
        def race():self.output.write_bytes(b'concurrent')
        with self.assertRaises(FileExistsError):local.publish_copy(self.source,self.output,race)
        self.assertEqual(self.output.read_bytes(),b'concurrent');self.assertEqual(list(self.root.glob('.linuxit-publish-*')),[])

    def test_write_flush_and_publication_failures_leave_no_final_or_staging_file(self):
        def fail(input_,output,*args):output.write(b'partial');raise OSError('synthetic')
        for target,error in [('copyfileobj',fail),('fsync',OSError('synthetic')),('_rename_new',OSError('synthetic'))]:
            obj=local.shutil if target=='copyfileobj' else local.os if target=='fsync' else local
            with patch.object(obj,target,side_effect=error),self.assertRaises(OSError):local.copy_local_document(self.source,self.request)
            self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-publish-*')),[])

    def test_source_changed_before_or_during_copy_refuses_publication(self):
        self.source.write_bytes(b'externally changed')
        with self.assertRaisesRegex(ValueError,'externamente'):local.copy_local_document(self.source,self.request)
        self.request['source_stamp']=local.file_stamp(self.source)
        original=local.shutil.copyfileobj
        def changed(input_,output,*args):original(input_,output,*args);self.source.write_bytes(b'another version')
        with patch.object(local.shutil,'copyfileobj',side_effect=changed),self.assertRaisesRegex(ValueError,'externamente'):
            local.copy_local_document(self.source,self.request)
        self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-publish-*')),[])

    def test_invalid_requests_remote_paths_and_same_source_destination_are_refused(self):
        for request in [{},{**self.request,'source_stamp':[True]*5},{**self.request,'destination':'https://example.test/out.pdf'},
                        {**self.request,'destination':str(self.source)}]:
            with self.assertRaises((ValueError,OSError)):local.copy_local_document(self.source,request)
        self.assertEqual(self.source.read_bytes(),self.original);self.assertFalse(self.output.exists())

    def test_hard_link_fallback_is_exclusive_and_publishes_complete_inode(self):
        staging=self.root/'staging';staging.write_bytes(self.original)
        with patch.object(local.sys,'platform','other-posix'):
            if os.name=='nt':local._rename_new(staging,self.output)
            else:local._rename_new(staging,self.output)
        self.assertEqual(self.output.read_bytes(),self.original);self.assertFalse(staging.exists())

    def test_unsupported_atomic_filesystem_is_refused_without_unsafe_fallback(self):
        staging=self.root/'staging';staging.write_bytes(self.original)
        if os.name=='nt':
            with patch.object(local.os,'rename',side_effect=OSError('unsupported')),self.assertRaises(OSError):local._rename_new(staging,self.output)
        else:
            with patch.object(local.sys,'platform','other-posix'),patch.object(local.os,'link',side_effect=OSError('unsupported')),self.assertRaisesRegex(OSError,'segura'):
                local._rename_new(staging,self.output)
        self.assertFalse(self.output.exists());self.assertEqual(staging.read_bytes(),self.original)

    def test_cancelled_worker_does_not_begin_copy(self):
        cancel=threading.Event();cancel.set()
        self.assertIsNone(run_search_worker('copy-file',self.source,self.request,cancel));self.assertFalse(self.output.exists())
