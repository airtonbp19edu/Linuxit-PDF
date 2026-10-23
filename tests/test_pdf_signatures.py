"""Own synthetic CMS signatures checked with .NET on Windows and OpenSSL on Linux."""
from datetime import datetime,timedelta,timezone
from io import BytesIO
import hashlib
import os
from pathlib import Path
import re
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
import pdf_signatures as signatures
from pypdf import PdfReader,PdfWriter
from pypdf.generic import DictionaryObject,NameObject,NumberObject,TextStringObject,ByteStringObject,ArrayObject
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7


def signing_identity():
    key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Linuxit synthetic untrusted test')])
    now=datetime.now(timezone.utc)
    cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number())
          .not_valid_before(now-timedelta(days=1)).not_valid_after(now+timedelta(days=1)).sign(key,hashes.SHA256()))
    return key,cert


def signed_pdf(path,identity):
    key,cert=identity;writer=PdfWriter();writer.add_blank_page(200,200)
    value=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Sig'),NameObject('/Filter'):NameObject('/Adobe.PPKLite'),
        NameObject('/SubFilter'):NameObject('/adbe.pkcs7.detached'),NameObject('/Reason'):TextStringObject('fixtureAAAA'),
        NameObject('/ByteRange'):ArrayObject([NumberObject(v) for v in (0,1111111111,1111111111,1111111111)]),
        NameObject('/Contents'):ByteStringObject(b'\0'*8192)}))
    field=writer._add_object(DictionaryObject({NameObject('/FT'):NameObject('/Sig'),NameObject('/T'):TextStringObject('Synthetic signature'),NameObject('/V'):value}))
    writer.root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject([field])})
    output=BytesIO();writer.write(output);raw=output.getvalue()
    match=re.search(rb'/Contents\s*(<[0-9a-fA-F]+>)',raw);assert match
    left,right=match.span(1)
    marker=b'[ 0 1111111111 1111111111 1111111111 ]'
    replacement=f'[ 0 {left:010d} {right:010d} {len(raw)-right:010d} ]'.encode('ascii');assert len(marker)==len(replacement)
    assert raw.count(marker)==1;raw=raw.replace(marker,replacement)
    content=raw[:left]+raw[right:]
    cms=(pkcs7.PKCS7SignatureBuilder().set_data(content).add_signer(cert,key,hashes.SHA256())
         .sign(serialization.Encoding.DER,[pkcs7.PKCS7Options.DetachedSignature,pkcs7.PKCS7Options.Binary]))
    assert len(cms)<=8192
    raw=raw[:left]+b'<'+cms.hex().encode('ascii').ljust((right-left-2),b'0')+b'>'+raw[right:]
    path.write_bytes(raw);return raw


class PDFSignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.identity=signing_identity()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-signatures-');self.root=Path(self.temp.name);self.source=self.root/'signed.pdf'
        self.original=signed_pdf(self.source,self.identity)
    def tearDown(self):self.temp.cleanup()
    def inspect(self):return signatures.inspect_pdf_signatures(self.source,{})

    def test_real_detached_cms_integrity_is_separate_from_certificate_trust(self):
        result=self.inspect();self.assertEqual(len(result['signatures']),1);item=result['signatures'][0]
        self.assertTrue(item['integrity_verified'],item);self.assertTrue(item['current_file_covered'])
        self.assertFalse(result['trust_chain_verified']);self.assertFalse(item['trust_chain_verified'])
        self.assertFalse(result['network_used']);self.assertEqual(self.source.read_bytes(),self.original)

    def test_modified_signed_bytes_fail_cryptographic_verification(self):
        changed=self.original.replace(b'fixtureAAAA',b'fixtureBBBB');self.assertNotEqual(changed,self.original)
        self.source.write_bytes(changed)
        item=self.inspect()['signatures'][0]
        self.assertFalse(item['integrity_verified']);self.assertEqual(item['status'],'not_verified')

    def test_appended_bytes_report_only_signed_revision_coverage(self):
        self.source.write_bytes(self.original+b'\n% trailing unsigned data\n')
        item=self.inspect()['signatures'][0];self.assertTrue(item['integrity_verified'])
        self.assertFalse(item['current_file_covered']);self.assertEqual(item['covered_revision_bytes'],len(self.original))

    def test_unsupported_filter_or_invalid_byte_range_never_report_verified(self):
        for raw in [self.original.replace(b'/adbe.pkcs7.detached',b'/adbe.pkcs7.unknownx'),
                    self.original.replace(b'/ByteRange [ 0 ',b'/ByteRange [ 1 ')]:
            self.source.write_bytes(raw);item=self.inspect()['signatures'][0]
            self.assertIsNone(item['integrity_verified']);self.assertEqual(item['status'],'unsupported_or_malformed')

    def test_der_bounds_and_padding_are_checked(self):
        for value in (b'',b'wrong',b'\x30\x80',b'\x30\x82\xff\xff',b'\x30\x01aEXTRA'):
            with self.assertRaises(ValueError):signatures._der_payload(value)
        self.assertEqual(signatures._der_payload(b'\x30\x01a\0\0'),b'\x30\x01a')

    def test_unsigned_fields_and_count_limit_are_explicit(self):
        writer=PdfWriter();writer.add_blank_page(100,100);fields=[]
        for i in range(17):fields.append(writer._add_object(DictionaryObject({NameObject('/FT'):NameObject('/Sig'),NameObject('/T'):TextStringObject(str(i))})))
        writer.root_object[NameObject('/AcroForm')]=DictionaryObject({NameObject('/Fields'):ArrayObject(fields)});writer.write(self.source)
        result=self.inspect();self.assertEqual(len(result['signatures']),16);self.assertEqual(result['omitted_signatures'],1)
        self.assertTrue(all(s['status']=='unsigned' for s in result['signatures']))

    def test_encrypted_pdf_input_size_and_invalid_request_are_refused(self):
        with patch.object(signatures,'MAX_PDF',1),self.assertRaises(ValueError):self.inspect()
        with self.assertRaises(ValueError):signatures.inspect_pdf_signatures(self.source,{'extra':True})
        writer=PdfWriter();writer.add_blank_page(100,100);writer.encrypt('synthetic');writer.write(self.source)
        with self.assertRaisesRegex(ValueError,'criptografados'):self.inspect()

    def test_missing_verifier_and_source_changes_do_not_approve_integrity(self):
        with patch.object(signatures.shutil,'which',return_value=None),patch.object(signatures,'_windows_powershell',return_value=None):
            item=self.inspect()['signatures'][0];self.assertIsNone(item['integrity_verified']);self.assertEqual(item['status'],'unavailable')
        with patch.object(signatures,'_sha',return_value='0'*64),self.assertRaisesRegex(ValueError,'mudou'):self.inspect()

    def test_real_worker_roundtrip_and_cancelled_request(self):
        result=signatures.invoke_signature_inspection(self.source);self.assertTrue(result['signatures'][0]['integrity_verified'])
        event=threading.Event();event.set();self.assertIsNone(signatures.invoke_signature_inspection(self.source,event))

    def test_invalid_worker_confirmation_is_rejected(self):
        with patch.object(signatures,'run_search_worker',return_value={}):
            with self.assertRaises(RuntimeError):signatures.invoke_signature_inspection(self.source)
