"""Real AES-R6 synthetic copies, permissions, authentication and secret transport."""
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT/'app'));sys.path.insert(0, str(APP))
import pdf_security as security
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, ArrayObject
from test_attachment_search import text_pdf


class PDFSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-security-');self.root = Path(self.temp.name)
        self.source = self.root/'source.pdf';self.output = self.root/'protected.pdf'
        writer = PdfWriter(clone_from=BytesIO(text_pdf(['synthetic content', 'second page'])))
        writer.add_metadata({'/Title':'Synthetic secret metadata'});writer.add_outline_item('Preserved bookmark', 1)
        writer.add_attachment('keep.txt', b'synthetic embedded payload');writer.write(self.source)
        self.original = self.source.read_bytes();self.identity = hashlib.sha256(self.original).hexdigest()
        self.request = {'destination':str(self.output),'source_sha256':self.identity,
                        'user_password':'synthetic-user-password','owner_password':'synthetic-owner-password',
                        'permissions':{key:False for key in security.PERMISSION_FLAGS}}

    def tearDown(self):self.temp.cleanup()
    def protect(self):return security.protect_pdf_copy(self.source, self.request)
    def absent(self):
        self.assertFalse(self.output.exists());self.assertEqual(list(self.root.glob('.linuxit-protect-*')), [])

    def test_unencrypted_inspection_identity_pages_and_permissions(self):
        info = security.inspect_pdf_security(self.source, {'password':''})
        self.assertEqual((info['pages'],info['role'],info['source_sha256']), (2,'unprotected',self.identity))
        self.assertFalse(info['encrypted']);self.assertTrue(all(info['permissions'].values()))
        self.assertEqual(self.source.read_bytes(),self.original);self.absent()

    def test_aes256_roundtrip_roles_permissions_metadata_and_attachments(self):
        result = self.protect();self.assertEqual(result['algorithm'],'AES-256')
        raw = self.output.read_bytes();self.assertNotIn(b'Synthetic secret metadata',raw)
        self.assertNotIn(b'synthetic embedded payload',raw)
        reader = PdfReader(self.output,strict=True)
        self.assertFalse(reader.decrypt(''));self.assertFalse(reader.decrypt('incorrect-synthetic-password'))
        self.assertEqual(int(reader.decrypt(self.request['user_password'])),1)
        self.assertEqual(reader.pages[0].extract_text(),'synthetic content')
        self.assertEqual(int(reader.decrypt(self.request['owner_password'])),2)
        self.assertEqual(reader.metadata.title,'Synthetic secret metadata')
        self.assertEqual(reader.outline[0].title,'Preserved bookmark')
        self.assertEqual(next(reader.attachment_list).content,b'synthetic embedded payload')
        self.assertEqual(self.source.read_bytes(),self.original)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),result['output_sha256'])
        if os.name != 'nt':self.assertEqual(self.output.stat().st_mode & 0o777,0o600)
        for secret in (self.request['user_password'],self.request['owner_password']):self.assertNotIn(secret,json.dumps(result))

    def test_each_permission_flag_and_accessibility_bit_are_preserved(self):
        for key in security.PERMISSION_FLAGS:
            with self.subTest(key=key):
                self.request['permissions']={name:name==key for name in security.PERMISSION_FLAGS}
                self.protect();info=security.inspect_pdf_security(self.output,{'password':self.request['user_password']})
                self.assertEqual(info['permissions'],self.request['permissions'])
                reader=PdfReader(self.output);self.assertTrue(int(reader.trailer['/Encrypt']['/P']) & 512)
                self.output.unlink()

    def test_encrypted_inspection_correct_wrong_and_missing_credentials(self):
        self.protect()
        for password,role in [('',None),('wrong-synthetic',None),(self.request['user_password'],'user'),(self.request['owner_password'],'owner')]:
            info=security.inspect_pdf_security(self.output,{'password':password})
            self.assertEqual(info['role'],role);self.assertEqual(info['authenticated'],role is not None)
            self.assertEqual(info['pages'],2 if role else None);self.assertEqual((info['bits'],info['revision']),(256,6))
            self.assertNotIn('password',info)

    def test_new_password_limits_and_distinct_roles(self):
        for password in ('','short','x'*65,'nonascii-á-pass','contains\nnewline',' '*10):
            with self.subTest(length=len(password)):
                request={**self.request,'user_password':password}
                with self.assertRaises(security.SecurityError):security.protect_pdf_copy(self.source,request)
                self.absent()
        with self.assertRaises(security.SecurityError):security.protect_pdf_copy(self.source,{**self.request,'owner_password':self.request['user_password']})
        self.absent()

    def test_invalid_protocol_and_permission_types_rejected(self):
        for request in ({},{**self.request,'extra':True},{**self.request,'permissions':{}},
                        {**self.request,'permissions':{key:1 for key in security.PERMISSION_FLAGS}},
                        {**self.request,'source_sha256':'invalid'}):
            with self.assertRaises(security.SecurityError):security.protect_pdf_copy(self.source,request)
            self.absent()
        for request in ({},{'password':1},{'password':'x'*128}):
            with self.assertRaises(security.SecurityError):security.inspect_pdf_security(self.source,request)

    def test_encrypted_source_not_unprotected_or_rewritten(self):
        self.protect();encrypted=self.output.read_bytes()
        with self.assertRaises(security.SecurityError):security.protect_pdf_copy(self.output,{**self.request,'destination':str(self.root/'not-created.pdf')})
        self.assertEqual(self.output.read_bytes(),encrypted);self.assertFalse((self.root/'not-created.pdf').exists())

    def test_signed_xfa_portfolio_and_permissions_sources_refused(self):
        for kind in ('/Perms','/Collection','/XFA'):
            writer=PdfWriter();writer.add_blank_page(100,100)
            if kind=='/XFA':writer.root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject(),NameObject('/XFA'):ArrayObject()})
            else:writer.root_object[NameObject(kind)]=DictionaryObject()
            writer.write(self.source);self.request['source_sha256']=hashlib.sha256(self.source.read_bytes()).hexdigest()
            with self.subTest(kind=kind),self.assertRaises(security.SecurityError):self.protect()
            self.absent()

    def test_stale_source_and_source_size_page_output_limits(self):
        with self.assertRaises(security.SecurityError):security.protect_pdf_copy(self.source,{**self.request,'source_sha256':'0'*64})
        for name,value in [('MAX_SOURCE_BYTES',1),('MAX_PAGES',1),('MAX_OUTPUT_BYTES',1)]:
            with self.subTest(name=name),patch.object(security,name,value),self.assertRaises(security.SecurityError):self.protect()
            self.absent()

    def test_existing_destination_and_source_never_overwritten(self):
        self.output.write_bytes(b'previous destination')
        with self.assertRaises(security.SecurityError):self.protect()
        self.assertEqual(self.output.read_bytes(),b'previous destination')
        with self.assertRaises(security.SecurityError):security.protect_pdf_copy(self.source,{**self.request,'destination':str(self.source)})
        self.assertEqual(self.source.read_bytes(),self.original)

    def test_handled_partial_write_removed_and_error_sanitized(self):
        def failure(source,output,*args):output.write(b'partial');raise OSError(self.request['user_password'])
        with patch.object(security.shutil,'copyfileobj',side_effect=failure),self.assertRaises(security.SecurityError) as error:self.protect()
        self.assertNotIn(self.request['user_password'],str(error.exception));self.absent()
        with patch.object(security.PdfWriter,'encrypt',side_effect=RuntimeError(self.request['owner_password'])),self.assertRaises(security.SecurityError) as error:self.protect()
        self.assertNotIn(self.request['owner_password'],str(error.exception));self.absent()

    def test_concurrent_destination_preserved(self):
        original=security._sha
        def changed(path):self.output.write_bytes(b'concurrent');return original(path)
        with patch.object(security,'_sha',side_effect=changed),self.assertRaises(security.SecurityError):self.protect()
        self.assertEqual(self.output.read_bytes(),b'concurrent');self.assertEqual(list(self.root.glob('.linuxit-protect-*')),[])

    def test_real_worker_secret_transport_and_error_channel(self):
        import search_tasks
        original=subprocess.Popen;arguments=[]
        def record(argv,**kwargs):arguments.append(argv);return original(argv,**kwargs)
        with patch.object(search_tasks.subprocess,'Popen',side_effect=record):
            result=security.invoke_security('protect-copy',self.source,self.request)
        self.assertEqual(result['pages'],2)
        for secret in (self.request['user_password'],self.request['owner_password']):self.assertNotIn(secret,repr(arguments))
        info=security.invoke_security('security-info',self.output,{'password':self.request['owner_password']})
        self.assertEqual(info['role'],'owner')
        proc=subprocess.run([sys.executable,'-X','utf8',str(APP/'worker_cli.py'),'protect-copy',str(self.source)],
            input=json.dumps({**self.request,'user_password':self.request['owner_password']}),text=True,capture_output=True,encoding='utf-8')
        self.assertNotEqual(proc.returncode,0);self.assertNotIn('Traceback',proc.stderr)
        for secret in (self.request['user_password'],self.request['owner_password']):self.assertNotIn(secret,proc.stdout+proc.stderr)

    def test_cancellation_and_invalid_confirmation_never_report_success(self):
        event=threading.Event();event.set()
        self.assertIsNone(security.invoke_security('protect-copy',self.source,self.request,event))
        with patch.object(security,'run_search_worker',return_value={}):
            with self.assertRaises(security.SecurityError):security.invoke_security('protect-copy',self.source,self.request)
        self.absent()

    def test_accessible_text_validation_limit_and_source_change(self):
        import rendering
        with patch.object(rendering,'extract_page_text',return_value='alpha\x00\nβ'):
            result=security.extract_accessible_text(self.source,{'page':0});self.assertEqual(result['text'],'alpha\nβ')
        for request in ({'page':True},{'page':-1},{'page':2},{}):
            with self.assertRaises(security.SecurityError):security.extract_accessible_text(self.source,request)
        with patch.object(rendering,'extract_page_text',return_value='x'*(1024**2+1)),self.assertRaisesRegex(security.SecurityError,'1 MiB'):
            security.extract_accessible_text(self.source,{'page':0})

    def test_accessible_text_refuses_encrypted_pdf_even_with_empty_password(self):
        writer=PdfWriter();writer.add_blank_page(100,100);writer.encrypt('',owner_password='synthetic-owner-pass',algorithm='RC4-128');writer.write(self.output)
        with self.assertRaisesRegex(security.SecurityError,'criptografados'):security.extract_accessible_text(self.output,{'page':0})

    def test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel(self):
        with patch.object(security,'run_search_worker',return_value={}):
            with self.assertRaises(security.SecurityError):security.invoke_accessible_text(self.source,0)
        event=threading.Event();event.set();self.assertIsNone(security.invoke_accessible_text(self.source,0,event))

    def test_only_owner_authentication_can_create_unprotected_copy(self):
        self.protect();protected=self.output.read_bytes();plain=self.root/'owner-copy.pdf'
        request={'destination':str(plain),'source_sha256':security._sha(self.output),'owner_password':self.request['user_password']}
        for password in ('wrong-synthetic',self.request['user_password']):
            with self.assertRaisesRegex(security.SecurityError,'proprietário'):
                security.unprotect_owner_copy(self.output,{**request,'owner_password':password})
            self.assertFalse(plain.exists())
        request['owner_password']=self.request['owner_password']
        result=security.invoke_security('owner-copy',self.output,request)
        self.assertEqual(result['algorithm'],'none');reader=PdfReader(plain)
        self.assertFalse(reader.is_encrypted);self.assertEqual(reader.pages[0].extract_text(),'synthetic content')
        self.assertEqual(next(reader.attachment_list).content,b'synthetic embedded payload')
        self.assertEqual(self.output.read_bytes(),protected)
        if os.name != 'nt':self.assertEqual(plain.stat().st_mode & 0o777,0o600)

    def test_owner_copy_stale_destination_and_partial_failure_are_safe(self):
        self.protect();plain=self.root/'plain.pdf'
        request={'destination':str(plain),'source_sha256':security._sha(self.output),'owner_password':self.request['owner_password']}
        with self.assertRaises(security.SecurityError):security.unprotect_owner_copy(self.output,{**request,'source_sha256':'0'*64})
        plain.write_bytes(b'preserve')
        with self.assertRaises(security.SecurityError):security.unprotect_owner_copy(self.output,request)
        self.assertEqual(plain.read_bytes(),b'preserve');plain.unlink()
        def fail(source,destination,*args):destination.write(b'partial');raise OSError('synthetic')
        with patch.object(security.shutil,'copyfileobj',side_effect=fail),self.assertRaises(security.SecurityError):security.unprotect_owner_copy(self.output,request)
        self.assertFalse(plain.exists());self.assertEqual(list(self.root.glob('.linuxit-protect-*')),[])

    def test_owner_copy_refuses_special_restrictions_and_signature_fields(self):
        for kind in ('/Perms','/Collection','/XFA','/Sig'):
            writer=PdfWriter();writer.add_blank_page(100,100)
            if kind in ('/Perms','/Collection'):writer.root_object[NameObject(kind)]=DictionaryObject()
            elif kind=='/XFA':writer.root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject(),NameObject('/XFA'):ArrayObject()})
            else:
                from pypdf.generic import TextStringObject
                field=writer._add_object(DictionaryObject({NameObject('/FT'):NameObject('/Sig'),NameObject('/T'):TextStringObject('Synthetic signature field')}))
                writer.root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject([field])})
            writer.encrypt(self.request['user_password'],self.request['owner_password'],algorithm='AES-256');writer.write(self.output)
            request={'destination':str(self.root/'never.pdf'),'source_sha256':security._sha(self.output),'owner_password':self.request['owner_password']}
            with self.subTest(kind=kind),self.assertRaises(security.SecurityError):security.unprotect_owner_copy(self.output,request)
            self.assertFalse((self.root/'never.pdf').exists())
