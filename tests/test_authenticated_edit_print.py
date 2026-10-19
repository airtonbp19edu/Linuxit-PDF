import hashlib,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader,PdfWriter
from pypdf.constants import UserAccessPermissions as Permissions
from pdf_changes import save_edited_copy,inspect_editable_document
from edit_history import EditSession
from edit_tasks import invoke_edit_worker
from document_session import DocumentSession
import cups_backend as cups


def encrypted(path,algorithm='AES-256',**allowed):
    writer=PdfWriter();writer.add_blank_page(200,200)
    flags=Permissions.from_dict(dict(print=True,print_to_representation=True,extract=True,modify=True,
        add_or_modify=True,fill_form_fields=True,assemble_doc=True,extract_text_and_graphics=True,**{}))
    values=flags.to_dict();values.update(allowed);flags=Permissions.from_dict(values)
    writer.encrypt('synthetic-user','synthetic-owner',permissions_flag=flags,algorithm=algorithm);writer.write(path)
    return dict(password='synthetic-user',recover=False)


class AuthenticatedEditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf'

    def test_four_encryption_algorithms_keep_user_owner_and_permissions_after_edit(self):
        for index,algorithm in enumerate(('RC4-128','AES-128','AES-256-R5','AES-256')):
            auth=encrypted(self.source,algorithm);original=self.source.read_bytes();output=self.root/f'copy-{index}.pdf'
            info=inspect_editable_document(self.source,auth=auth)
            save_edited_copy(self.source,output,source_sha256=info['source_sha256'],auth=auth,operations=[dict(kind='add-note',page=0,text='authorized',rect=[10,10,30,30])])
            reader=PdfReader(output);self.assertTrue(reader.is_encrypted);self.assertEqual(reader.decrypt('synthetic-user'),1)
            self.assertEqual(reader.pages[0]['/Annots'][0]['/Contents'],'authorized')
            original_reader=PdfReader(self.source);original_reader.decrypt('synthetic-user')
            self.assertEqual(reader.trailer['/Encrypt']['/P'],original_reader.trailer['/Encrypt']['/P'])
            self.assertEqual(reader.decrypt('synthetic-owner'),2);self.assertEqual(self.source.read_bytes(),original)

    def test_user_annotation_denial_cannot_be_bypassed_by_reading_representation(self):
        auth=encrypted(self.source,add_or_modify=False,fill_form_fields=False,modify=False,assemble_doc=False)
        with self.assertRaisesRegex(ValueError,'permissão'):
            save_edited_copy(self.source,self.root/'denied.pdf',source_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),auth=auth,operations=[dict(kind='add-note',page=0,text='denied',rect=[10,10,30,30])])
        self.assertFalse((self.root/'denied.pdf').exists())

    def test_owner_authorized_edit_keeps_original_user_restrictions_in_output(self):
        auth=encrypted(self.source,add_or_modify=False,modify=False);auth['password']='synthetic-owner'
        output=self.root/'owner.pdf';save_edited_copy(self.source,output,source_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),auth=auth,operations=[dict(kind='add-bookmark',title='Owner allowed',page=0)])
        reader=PdfReader(output);self.assertEqual(reader.decrypt('synthetic-user'),1)
        self.assertFalse(Permissions(int(reader.trailer['/Encrypt']['/P'])).to_dict()['modify'])

    def test_authenticated_draft_undo_redo_and_saved_copy_stay_encrypted(self):
        auth=encrypted(self.source);session=EditSession(self.source,auth=auth)
        try:
            session.add(dict(kind='add-bookmark',title='A',page=0));self.assertTrue(PdfReader(session.preview).is_encrypted)
            session.undo();session.redo();output=self.root/'history.pdf';session.save(output)
            reader=PdfReader(output);reader.decrypt('synthetic-user');self.assertEqual(reader.outline[0].title,'A')
        finally:session.close()

    def test_wrong_credentials_and_plain_auth_shape_never_publish_or_leak(self):
        encrypted(self.source);output=self.root/'wrong.pdf'
        for auth in ({'password':'bad-secret','recover':False},{'password':'x','recover':'yes'},{'password':'x','recover':False,'extra':True}):
            with self.assertRaises(ValueError) as error:inspect_editable_document(self.source,auth=auth)
            self.assertNotIn('bad-secret',str(error.exception));self.assertFalse(output.exists())

    def test_worker_secret_is_stdin_only_and_not_in_reply(self):
        auth=encrypted(self.source);seen=[];run=subprocess.run
        def record(argv,**kwargs):seen.extend(argv);return run(argv,**kwargs)
        with patch('edit_tasks.subprocess.run',side_effect=record):info=invoke_edit_worker('edit-info',self.source,request={'auth':auth})
        self.assertNotIn('synthetic-user',' '.join(seen));self.assertNotIn('synthetic-user',repr(info))
        self.assertTrue(info['edit_permissions']['annotate'])

    def test_session_retains_only_private_authorization_and_fixed_path_lease(self):
        encrypted(self.source);session=DocumentSession(self.source)
        try:
            info=session.prepare('synthetic-user');self.assertNotIn('synthetic-user',repr(info))
            self.assertEqual(session.edit_authorization()['password'],'synthetic-user')
            path=session.read_path
            with session.lease(path):
                session.close();self.assertTrue(Path(path).exists())
            self.assertFalse(Path(path).exists())
            with self.assertRaises(ValueError):session.edit_authorization()
        finally:session.close()

    def test_source_mutation_is_detected_before_printing_private_view(self):
        encrypted(self.source);session=DocumentSession(self.source)
        try:
            session.prepare('synthetic-user');self.source.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'mudou'):session.assert_source_unchanged()
        finally:session.close()


class CUPSJobControlTests(unittest.TestCase):
    def test_receipt_binding_and_cancel_never_use_shell_or_unknown_options(self):
        self.assertEqual(cups.submitted_job_id('request id is Lab-42 (1 file(s))','Lab'),'Lab-42')
        self.assertIsNone(cups.submitted_job_id('request id is Other-42 (1 file(s))','Lab'))
        result=subprocess.CompletedProcess([],0,'','')
        with patch('cups_backend.shutil.which',return_value='/usr/bin/cancel'),patch('cups_backend._run',return_value=result) as command:
            self.assertIn('aceito',cups.cancel_job('Lab-42'));self.assertEqual(command.call_args.args[0],['cancel','Lab-42'])
        for identifier in ('-a','Lab-0','Lab-42\n-a','../42','Lab 42',''):
            with self.assertRaises(ValueError):cups.cancel_job(identifier)

    def test_queue_listing_and_backend_refusal_are_explicit(self):
        with patch('cups_backend._run',return_value=subprocess.CompletedProcess([],0,'Lab-7 user 120 bytes\nOther-2 user 60 bytes','')):
            self.assertEqual(cups.pending_jobs(),{'Lab-7','Other-2'})
        with patch('cups_backend.shutil.which',return_value='cancel'),patch('cups_backend._run',return_value=subprocess.CompletedProcess([],1,'','not allowed')):
            with self.assertRaisesRegex(RuntimeError,'not allowed'):cups.cancel_job('Lab-7')


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK/Poppler')
class AuthenticatedPrintGUITests(unittest.TestCase):
    def test_encrypted_reader_prints_private_view_and_enforces_low_resolution(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            source=Path(directory)/'encrypted.pdf';encrypted(source,print_to_representation=False)
            window=PDFWindow()
            try:
                with patch.object(window,'_ask_document_password',return_value='synthetic-user'):window.open_document(str(source));wait_for(lambda:window.filepath==str(source.resolve()) and window.displayed_page==0)
                seen=[]
                def prepare(path,out,job,cancel):
                    seen.append((path,job));writer=PdfWriter();writer.add_blank_page(100,100);writer.write(out);return out
                with patch('main.prepare_print',side_effect=prepare),patch('main.cups.print_file',return_value='request id is Lab-42 (1 file(s))') as printer:
                    window._submit_print_job(dict(destination='printer',printer='Lab',image_dpi=600))
                    wait_for(lambda:printer.called and getattr(window,'print_jobs',None))
                self.assertNotEqual(seen[0][0],str(source));self.assertTrue(seen[0][1]['print_as_image']);self.assertEqual(seen[0][1]['image_dpi'],150)
                self.assertEqual(window.print_jobs[0]['id'],'Lab-42')
            finally:window.destroy()

    def test_copy_denial_refuses_pdf_output_before_preparation(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            source=Path(directory)/'encrypted.pdf';encrypted(source,extract=False);window=PDFWindow();errors=[];window._error=errors.append
            try:
                with patch.object(window,'_ask_document_password',return_value='synthetic-user'):window.open_document(str(source));wait_for(lambda:window.filepath==str(source.resolve()) and window.displayed_page==0)
                with patch('main.prepare_print') as prepare:window._submit_print_job(dict(destination='save-pdf',save_path=str(Path(directory)/'out.pdf')));prepare.assert_not_called()
                self.assertTrue(errors);self.assertIn('permissão',errors[-1])
            finally:window.destroy()
