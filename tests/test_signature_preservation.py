"""A6: actual local OCSP, incremental DSS and nonce-bound RFC3161 requests/responses."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from test_attachment_search import text_pdf
from test_pdf_signatures import signed_pdf
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.x509 import ocsp
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from pdf_preservation import append_dss_copy, prepare_document_timestamp, complete_document_timestamp
from pdf_signatures import inspect_pdf_signatures
from signature_ocsp import verify_ocsp_chain


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name);self.now = datetime.now(timezone.utc)
        self.ca_key, self.ca = self.identity('Synthetic preservation CA', 1, ca=True)
        self.key, self.leaf = self.identity('Synthetic signer', 2, issuer=self.ca, signer=self.ca_key)
        self.ca_path = self.root / 'ca.pem';self.ca_path.write_bytes(self.ca.public_bytes(serialization.Encoding.PEM))
        self.source = self.root / 'source.pdf';self.source.write_bytes(text_pdf(['alpha']))

    def identity(self, name, serial, issuer=None, signer=None, ca=False, eku=None):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, name)])
        builder = (x509.CertificateBuilder().subject_name(subject).issuer_name(issuer.subject if issuer else subject)
                   .public_key(key.public_key()).serial_number(serial).not_valid_before(self.now-timedelta(days=1))
                   .not_valid_after(self.now+timedelta(days=2))
                   .add_extension(x509.BasicConstraints(ca=ca, path_length=1 if ca else None), True)
                   .add_extension(x509.KeyUsage(True, False, False, False, False, ca, ca, False, False), True))
        if eku:
            builder = builder.add_extension(x509.ExtendedKeyUsage([eku]), True)
            if eku == ExtendedKeyUsageOID.OCSP_SIGNING:
                builder = builder.add_extension(x509.OCSPNoCheck(), False)
        return key, builder.sign(signer or key, hashes.SHA256())

    def response(self, status=ocsp.OCSPCertStatus.GOOD, stale=False, cert=None, key=None, include=(), **kwargs):
        builder = ocsp.OCSPResponseBuilder().add_response(
            self.leaf, self.ca, hashes.SHA256(), status, self.now-timedelta(minutes=2),
            self.now-timedelta(minutes=1) if stale else self.now+timedelta(hours=1),
            self.now-timedelta(hours=1) if status == ocsp.OCSPCertStatus.REVOKED else None, None)
        builder = builder.responder_id(ocsp.OCSPResponderEncoding.HASH, cert or self.ca)
        if include:
            builder = builder.certificates(list(include))
        return builder.sign(key or self.ca_key, hashes.SHA256()).public_bytes(serialization.Encoding.DER)

    def assess(self, responses, **changes):
        values = dict(signers=[self.leaf], helpers=[self.ca], anchors=[self.ca], responses=responses, moment=self.now)
        values.update(changes)
        return verify_ocsp_chain(**values)

    def test_ocsp_good_revoked_unknown_and_stale_are_distinct(self):
        good = self.assess([self.response()])
        self.assertTrue(good['verified']);self.assertFalse(good['revoked']);self.assertFalse(good['network_used'])
        revoked = self.assess([self.response(), self.response(ocsp.OCSPCertStatus.REVOKED)])
        self.assertFalse(revoked['verified']);self.assertTrue(revoked['revoked'])
        for raw in (self.response(stale=True), self.response(ocsp.OCSPCertStatus.UNKNOWN), b'invalid'):
            self.assertFalse(self.assess([raw])['verified'])

    def test_ocsp_requires_matching_certid_signature_and_explicit_anchor(self):
        other_key, other = self.identity('Other root', 9, ca=True)
        self.assertFalse(self.assess([self.response()], anchors=[other])['verified'])
        wrong = self.response(cert=other, key=other_key, include=[other])
        self.assertFalse(self.assess([wrong])['verified'])
        _, foreign = self.identity('Other signer', 10, issuer=self.ca, signer=self.ca_key)
        self.assertFalse(self.assess([self.response()], signers=[foreign])['verified'])
        broken = bytearray(self.response());broken[-1] ^= 1
        self.assertFalse(self.assess([bytes(broken)])['verified'])

    def test_ocsp_delegation_requires_eku_and_actual_issuer(self):
        key, delegate = self.identity('OCSP responder', 3, issuer=self.ca, signer=self.ca_key, eku=ExtendedKeyUsageOID.OCSP_SIGNING)
        response = self.response(cert=delegate, key=key, include=[delegate])
        self.assertTrue(self.assess([response])['verified'])
        key, ordinary = self.identity('Ordinary signer', 4, issuer=self.ca, signer=self.ca_key)
        self.assertFalse(self.assess([self.response(cert=ordinary, key=key, include=[ordinary])])['verified'])

    def signed(self):
        source = self.root / 'signed.pdf';signed_pdf(source, (self.key, self.leaf));return source

    def test_dss_appends_certificates_and_ocsp_and_preserves_earlier_bytes(self):
        source = self.signed();before = source.read_bytes();target = self.root / 'dss.pdf'
        response = self.root / 'ocsp.der';response.write_bytes(self.response())
        result = append_dss_copy(source, dict(destination=str(target), source_sha256=hashlib.sha256(before).hexdigest(),
                                             certificates=[str(self.ca_path)], crls=[], ocsps=[str(response)]))
        self.assertTrue(target.read_bytes().startswith(before));self.assertEqual(source.read_bytes(), before)
        self.assertEqual(result['material'], dict(certificates=1, crls=0, ocsps=1))
        self.assertFalse(result['trust_assessed']);self.assertFalse(result['pades_lta_claimed'])
        report = inspect_pdf_signatures(target, {})
        self.assertEqual(report['dss']['ocsp_responses'], 1)
        self.assertEqual(report['signatures'][0]['status'], 'verified')
        self.assertFalse(report['signatures'][0]['current_file_covered'])
        # A second revision merges material without multiplying identical streams.
        another = self.root / 'dss2.pdf'
        again = append_dss_copy(target, dict(destination=str(another), source_sha256=result['output_sha256'],
                                            certificates=[str(self.ca_path)], crls=[], ocsps=[str(response)]))
        self.assertEqual(again['material'], result['material']);self.assertTrue(another.read_bytes().startswith(target.read_bytes()))
        with self.assertRaises(FileExistsError):
            append_dss_copy(source, dict(destination=str(target), source_sha256=hashlib.sha256(before).hexdigest(),
                                        certificates=[str(self.ca_path)], crls=[], ocsps=[]))

    def test_dss_rejects_unsigned_changed_and_malformed_input_without_output(self):
        target = self.root / 'never.pdf';request = dict(destination=str(target), source_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),
                                                      certificates=[str(self.ca_path)], crls=[], ocsps=[])
        with self.assertRaisesRegex(ValueError, 'existente'):
            append_dss_copy(self.source, request)
        signed = self.signed()
        with self.assertRaisesRegex(ValueError, 'mudou'):
            append_dss_copy(signed, request)
        bad = self.root / 'bad.der';bad.write_bytes(b'invalid')
        with self.assertRaises(ValueError):
            append_dss_copy(signed, dict(request, source_sha256=hashlib.sha256(signed.read_bytes()).hexdigest(), ocsps=[str(bad)]))
        self.assertFalse(target.exists())

    def prepare(self, source=None, name='pending'):
        source = source or self.source;folder = self.root / name
        result = prepare_document_timestamp(source, dict(folder=str(folder), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
        return source, folder, result

    def test_timestamp_query_is_nonce_bound_to_exact_prepared_revision_and_export_is_exclusive(self):
        from asn1crypto import tsp
        source, folder, result = self.prepare()
        raw = (folder / 'document.pending').read_bytes();manifest = json.loads((folder / 'manifest.json').read_bytes())
        query = tsp.TimeStampReq.load((folder / 'timestamp.tsq').read_bytes())
        self.assertGreater(query['nonce'].native, 0);self.assertTrue(query['cert_req'].native)
        covered = raw[:manifest['left']] + raw[manifest['right']:]
        self.assertEqual(query['message_imprint']['hashed_message'].native, hashlib.sha256(covered).digest())
        self.assertTrue(raw.startswith(source.read_bytes()));self.assertFalse(result['complete']);self.assertFalse(result['network_used'])
        with self.assertRaises(FileExistsError):self.prepare()

    def tsa_response(self, folder, nonce_delta=0):
        from asn1crypto import tsp, cms, x509 as asn_x509
        query = tsp.TimeStampReq.load((folder / 'timestamp.tsq').read_bytes())
        tsa_key, tsa = self.identity('Synthetic local TSA', 20, issuer=self.ca, signer=self.ca_key, eku=ExtendedKeyUsageOID.TIME_STAMPING)
        info = tsp.TSTInfo({'version': 'v1', 'policy': '1.2.3.4.1', 'message_imprint': query['message_imprint'],
                            'serial_number': 1, 'gen_time': datetime.now(timezone.utc), 'nonce': query['nonce'].native + nonce_delta})
        certificate = asn_x509.Certificate.load(tsa.public_bytes(serialization.Encoding.DER))
        attrs = cms.CMSAttributes([
            cms.CMSAttribute({'type': 'content_type', 'values': ['tst_info']}),
            cms.CMSAttribute({'type': 'message_digest', 'values': [hashlib.sha256(info.dump()).digest()]}),
            cms.CMSAttribute({'type': 'signing_certificate_v2', 'values': [tsp.SigningCertificateV2({'certs': [
                tsp.ESSCertIDv2({'cert_hash': hashlib.sha256(certificate.dump()).digest()})]})]})])
        signer = cms.SignerInfo({'version': 'v1', 'sid': {'issuer_and_serial_number': {'issuer': certificate.issuer, 'serial_number': 20}},
                                 'digest_algorithm': {'algorithm': 'sha256'}, 'signed_attrs': attrs,
                                 'signature_algorithm': {'algorithm': 'sha256_rsa'},
                                 'signature': tsa_key.sign(attrs.dump(), padding.PKCS1v15(), hashes.SHA256())})
        token = cms.ContentInfo({'content_type': 'signed_data', 'content': {'version': 'v3', 'digest_algorithms': [{'algorithm': 'sha256'}],
            'encap_content_info': {'content_type': 'tst_info', 'content': info}, 'certificates': [certificate], 'signer_infos': [signer]}})
        response = self.root / f'response-{nonce_delta}.tsr'
        response.write_bytes(tsp.TimeStampResp({'status': {'status': 'granted'}, 'time_stamp_token': token}).dump())
        return response

    def complete(self, source, folder, response, target='stamped.pdf', **policy):
        return complete_document_timestamp(source, dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            folder=str(folder), response=str(response), destination=str(self.root / target),
            trust_policy=dict(dict(roots=[str(self.ca_path)], crls=[], require_revocation=False, at_time=None), **policy)))

    def test_nonce_mismatch_and_changed_preparation_are_refused_before_publish(self):
        source, folder, _ = self.prepare()
        with self.assertRaisesRegex(ValueError, 'Nonce'):
            self.complete(source, folder, self.tsa_response(folder, 1))
        valid = self.tsa_response(folder)
        pending = folder / 'document.pending';pending.write_bytes(pending.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'Preparação'):
            self.complete(source, folder, valid)
        self.assertFalse((self.root / 'stamped.pdf').exists())

    @unittest.skipUnless(shutil.which('openssl'), 'OpenSSL verifies the actual synthetic RFC3161 token independently')
    def test_timestamp_response_import_trust_and_prior_signature_preserved(self):
        source = self.signed();before = source.read_bytes()
        _, folder, _ = self.prepare(source)
        response = self.tsa_response(folder)
        result = self.complete(source, folder, response)
        self.assertTrue(result['trust']['chain_verified']);self.assertFalse(result['pades_lta_claimed'])
        target = Path(result['path']);self.assertTrue(target.read_bytes().startswith(before))
        rows = inspect_pdf_signatures(target, {})['signatures']
        self.assertEqual([(r['kind'], r['status'], r['current_file_covered']) for r in rows],
                         [('signature', 'verified', False), ('document_timestamp', 'verified', True)])
        _, wrong = self.identity('Wrong root', 99, ca=True)
        path = self.root / 'wrong.pem';path.write_bytes(wrong.public_bytes(serialization.Encoding.PEM))
        with self.assertRaisesRegex(ValueError, 'confiança'):
            self.complete(source, folder, response, target='wrong.pdf', roots=[str(path)])
        self.assertFalse((self.root / 'wrong.pdf').exists())

    @unittest.skipUnless(shutil.which('openssl'), 'OpenSSL builds and verifies the explicit CMS chain')
    def test_dss_ocsp_satisfies_required_revocation_and_revoked_overrides_clear_crl(self):
        source = self.signed();response = self.root / 'good.der';response.write_bytes(self.response())
        target = self.root / 'dss.pdf'
        append_dss_copy(source, dict(destination=str(target), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                     certificates=[str(self.ca_path)], crls=[], ocsps=[str(response)]))
        policy = dict(roots=[str(self.ca_path)], crls=[], require_revocation=True, at_time=None)
        trust = inspect_pdf_signatures(target, {'trust_policy': policy})['signatures'][0]['trust']
        self.assertTrue(trust['chain_verified']);self.assertTrue(trust['revocation_verified']);self.assertTrue(trust['policy_satisfied'])
        response.write_bytes(self.response(ocsp.OCSPCertStatus.REVOKED));bad = self.root / 'revoked.pdf'
        append_dss_copy(source, dict(destination=str(bad), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                     certificates=[], crls=[], ocsps=[str(response)]))
        trust = inspect_pdf_signatures(bad, {'trust_policy': policy})['signatures'][0]['trust']
        self.assertTrue(trust['chain_verified']);self.assertFalse(trust['policy_satisfied']);self.assertTrue(trust['ocsp']['revoked'])


if __name__ == '__main__':unittest.main()
