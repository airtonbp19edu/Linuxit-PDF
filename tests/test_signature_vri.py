"""Per-signature VRI lookup, isolation and bounded DER parsing."""
from datetime import datetime, timedelta, timezone
import hashlib
import os
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from signature_dss import material, for_signature
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, DecodedStreamObject
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID


class VRITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        key = ec.generate_private_key(ec.SECP256R1())
        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Synthetic VRI CA')])
        now = datetime.now(timezone.utc)
        cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
                .serial_number(1).not_valid_before(now-timedelta(days=1)).not_valid_after(now+timedelta(days=1))
                .sign(key, hashes.SHA256()))
        cls.cert = cert.public_bytes(serialization.Encoding.DER)
        cls.crl = (x509.CertificateRevocationListBuilder().issuer_name(name).last_update(now-timedelta(minutes=1))
                   .next_update(now+timedelta(days=1)).sign(key, hashes.SHA256()).public_bytes(serialization.Encoding.DER))

    def document(self, contents=b'cms\x00\x00'):
        writer = PdfWriter();writer.add_blank_page(100, 100)
        def stream(data):
            value = DecodedStreamObject();value.set_data(data);return writer._add_object(value)
        cert, crl = stream(self.cert), stream(self.crl)
        key = '/' + hashlib.sha1(contents).hexdigest().upper()
        entry = DictionaryObject({NameObject('/Cert'):ArrayObject([cert]),NameObject('/CRL'):ArrayObject([crl])})
        vri = DictionaryObject({NameObject(key):entry})
        dss = DictionaryObject({NameObject('/Certs'):ArrayObject([cert]),NameObject('/VRI'):vri})
        writer.root_object[NameObject('/DSS')] = dss
        return writer, dss, entry

    def test_full_contents_including_padding_selects_exact_entry(self):
        writer, _, _ = self.document()
        selected, report = for_signature(material(writer), b'cms\x00\x00')
        self.assertTrue(report['matched']);self.assertEqual(report['scope'], 'matching_vri')
        self.assertEqual(selected['certificates'], [self.cert]);self.assertEqual(selected['crls'], [self.crl])
        self.assertIsNone(report['validation_material_complete'])
        self.assertFalse(for_signature(material(writer), b'cms')[1]['matched'])

    def test_other_signature_material_is_not_merged_into_matching_vri(self):
        writer, dss, entry = self.document()
        entry.pop('/CRL')
        foreign = DictionaryObject({NameObject('/CRL'):ArrayObject([self._stream(writer,self.crl)])})
        dss['/VRI'][NameObject('/'+'A'*40)] = foreign
        selected, report = for_signature(material(writer), b'cms\x00\x00')
        self.assertEqual(selected['crls'], []);self.assertFalse(report['revocation_material_present'])

    @staticmethod
    def _stream(writer, data):
        stream = DecodedStreamObject();stream.set_data(data);return writer._add_object(stream)

    def test_unknown_signature_uses_only_global_material(self):
        writer, _, _ = self.document()
        selected, report = for_signature(material(writer), b'other')
        self.assertEqual(selected['crls'], []);self.assertFalse(report['matched'])
        self.assertEqual(report['scope'], 'global_fallback')

    def test_invalid_keys_and_non_stream_entries_are_refused(self):
        for key in ('/'+'a'*40, '/ABC', '/'+'G'*40):
            writer, dss, entry = self.document();dss[NameObject('/VRI')] = DictionaryObject({NameObject(key):entry})
            with self.subTest(key=key), self.assertRaises(ValueError):material(writer)
        writer, _, entry = self.document();entry[NameObject('/Cert')] = ArrayObject([DictionaryObject()])
        with self.assertRaises(AttributeError):material(writer)

    def test_invalid_der_oversized_lists_and_missing_dss(self):
        writer = PdfWriter();self.assertIsNone(material(writer))
        self.assertEqual(for_signature(None, b'x')[1]['scope'], 'absent')
        writer, _, entry = self.document();entry[NameObject('/Cert')] = ArrayObject([self._stream(writer,b'bad DER')])
        with self.assertRaises(ValueError):material(writer)
        writer, _, entry = self.document();entry[NameObject('/CRL')] = ArrayObject([self._stream(writer,self.crl)]*33)
        with self.assertRaises(ValueError):material(writer)
