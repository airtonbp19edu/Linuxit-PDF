"""Synthetic keys only; CMS checked independently by .NET/OpenSSL."""
import hashlib
from pathlib import Path
import tempfile
import unittest

from test_attachment_search import text_pdf,request
from test_pdf_signatures import signing_identity
from pypdf import PdfReader,PdfWriter
from pypdf.constants import UserAccessPermissions as Permissions
from pypdf.generic import DictionaryObject,NameObject
from cryptography.hazmat.primitives import serialization
from pdf_signing import sign_pdf_copy,invoke_sign_copy
from pdf_signatures import inspect_pdf_signatures
from pdf_attachments import list_attachments,extract_attachment
from attachment_search import search_attachment_text
from document_session import DocumentSession
import imposition


class SigningAttachmentsPermissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.identity=signing_identity()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(text_pdf(['alpha']))
        self.out=self.root/'signed.pdf';self.key=self.root/'key.pem';self.cert=self.root/'cert.pem'
        key,cert=self.identity
        self.key.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,
                                               serialization.BestAvailableEncryption(b'synthetic-secret')))
        self.cert.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    def tearDown(self):self.temp.cleanup()

    def request(self,**kwargs):
        result=dict(destination=str(self.out),source_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),
                    certificate=str(self.cert),private_key=str(self.key),password='synthetic-secret')
        result.update(kwargs);return result

    def test_signed_copy_verifies_covers_file_and_does_not_change_original_or_identity(self):
        before=[p.read_bytes() for p in (self.source,self.key,self.cert)]
        result=sign_pdf_copy(self.source,self.request())
        self.assertFalse(result['trust_assessed']);self.assertFalse(result['timestamp_added'])
        inspection=inspect_pdf_signatures(self.out,{})['signatures'][0]
        self.assertTrue(inspection['integrity_verified']);self.assertTrue(inspection['current_file_covered'])
        self.assertEqual([p.read_bytes() for p in (self.source,self.key,self.cert)],before)

    def test_worker_uses_selected_identity_and_tampered_signed_bytes_fail(self):
        result=invoke_sign_copy(self.source,self.request())
        self.assertEqual(result['schema'],'linuxit-signed-copy-v1')
        raw=self.out.read_bytes();self.assertIn(b'alpha',raw)
        self.out.write_bytes(raw.replace(b'alpha',b'ALPHA',1))
        self.assertFalse(inspect_pdf_signatures(self.out,{})['signatures'][0]['integrity_verified'])

    def test_wrong_key_password_and_existing_destination_never_publish_or_expose_secret(self):
        for secret in ('wrong-secret',''):
            with self.subTest(secret_empty=not secret),self.assertRaises(ValueError) as caught:
                sign_pdf_copy(self.source,self.request(password=secret))
            self.assertNotIn('wrong-secret',str(caught.exception));self.assertFalse(self.out.exists())
        self.out.write_bytes(b'preserve')
        with self.assertRaises(ValueError):sign_pdf_copy(self.source,self.request())
        self.assertEqual(self.out.read_bytes(),b'preserve')

    def test_changed_source_is_refused_and_a_second_signature_is_incremental(self):
        with self.assertRaises(ValueError):sign_pdf_copy(self.source,self.request(source_sha256='0'*64))
        sign_pdf_copy(self.source,self.request())
        second=self.root/'second.pdf'
        # Since E08 a signed PDF receives an incremental revision instead of being refused.
        result=sign_pdf_copy(self.out,self.request(destination=str(second),source_sha256=hashlib.sha256(self.out.read_bytes()).hexdigest()))
        self.assertEqual((result['field'],result['previous_signatures']),('LinuxitSignature2',['LinuxitSignature']))
        self.assertTrue(second.read_bytes().startswith(self.out.read_bytes()))

    def portfolio(self,password=None,copying=True,printing=True):
        writer=PdfWriter();writer.add_blank_page(200,300);writer.add_attachment('member.txt',b'alpha attachment')
        writer.root_object[NameObject('/Collection')]=DictionaryObject()
        if password is not None:
            flags=Permissions.from_dict({'extract':copying,'print':printing,'print_to_representation':printing})
            writer.encrypt(password,'owner-secret',permissions_flag=flags,algorithm='AES-256')
        writer.write(self.source)

    def test_portfolio_members_are_listed_and_extracted_without_running_layout(self):
        self.portfolio();before=self.source.read_bytes();listing=list_attachments(self.source)
        self.assertTrue(listing['portfolio']);self.assertEqual(len(listing['attachments']),1)
        folder=self.root/'export';folder.mkdir()
        result=extract_attachment(self.source,0,folder,source_sha256=listing['source_sha256'])
        self.assertEqual(Path(result['path']).read_bytes(),b'alpha attachment')
        self.assertEqual(self.source.read_bytes(),before)

    def test_password_session_can_read_portfolio_members_and_retains_permission_policy(self):
        self.portfolio('user-secret',copying=False)
        session=DocumentSession(self.source)
        try:
            self.assertEqual(session.prepare('user-secret')['status'],'ready')
            self.assertFalse(session.info['permissions']['copy'])
            listing=session.call(list_attachments)
            self.assertTrue(listing['portfolio'])
            self.assertEqual(listing['attachments'][0]['name'],'member.txt')
        finally:session.close()

    def test_direct_encrypted_extract_search_and_print_refuse_permission_denial(self):
        self.portfolio('',copying=False,printing=False)
        listing=list_attachments(self.source);folder=self.root/'export';folder.mkdir()
        with self.assertRaises(PermissionError):extract_attachment(self.source,0,folder,source_sha256=listing['source_sha256'])
        with self.assertRaises(PermissionError):search_attachment_text(self.source,request('alpha'))
        with self.assertRaises(PermissionError):imposition.prepare_output(self.source,self.root/'print.pdf',{})
        self.assertFalse(list(folder.iterdir()));self.assertFalse((self.root/'print.pdf').exists())
