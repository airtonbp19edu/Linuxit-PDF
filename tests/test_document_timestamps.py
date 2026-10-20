"""E09: existing RFC 3161 document timestamps (ETSI.RFC3161) are recognised and verified offline."""
import hashlib,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'testes'/'aceitacao'))

from test_attachment_search import text_pdf
from test_pdf_signatures import signing_identity
from cryptography.hazmat.primitives import serialization
from pdf_signing import sign_pdf_copy
from pdf_signatures import inspect_pdf_signatures
import carimbo


@unittest.skipUnless(shutil.which('openssl'),'OpenSSL creates and checks the synthetic tokens')
class DocumentTimestampTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(text_pdf(['alpha']))
        self.stamped=self.root/'stamped.pdf';self.ca=carimbo.add_document_timestamp(self.source,self.stamped,self.root/'tsa')

    def policy(self,ca=None,**changes):
        return dict(dict(roots=[str(ca or self.ca)],crls=[],require_revocation=False,at_time=None),**changes)

    def test_timestamp_is_recognised_verified_and_trusted_only_with_its_ca(self):
        item=inspect_pdf_signatures(self.stamped,{})['signatures'][0]
        self.assertEqual((item['kind'],item['status'],item['current_file_covered']),('document_timestamp','verified',True))
        self.assertTrue(item['timestamp_time'])
        trusted=inspect_pdf_signatures(self.stamped,{'trust_policy':self.policy()})['signatures'][0]
        self.assertTrue(trusted['trust']['chain_verified']);self.assertTrue(trusted['trust_chain_verified'])
        other=carimbo.authority(self.root/'other')
        untrusted=inspect_pdf_signatures(self.stamped,{'trust_policy':self.policy(other)})['signatures'][0]
        self.assertFalse(untrusted['trust']['chain_verified'])
        self.assertEqual(untrusted['status'],'verified')  # integrity is independent of trust

    def test_changed_covered_bytes_and_wrong_imprint_fail(self):
        raw=self.stamped.read_bytes();changed=self.root/'changed.pdf'
        changed.write_bytes(raw.replace(b'alpha',b'ALPHA',1))
        item=inspect_pdf_signatures(changed,{})['signatures'][0]
        self.assertEqual(item['status'],'not_verified');self.assertIsNone(item['timestamp_time'])
        # A valid token for other data must not verify this document.
        other=self.root/'other.pdf';other_source=self.root/'other-source.pdf';other_source.write_bytes(text_pdf(['beta']))
        carimbo.add_document_timestamp(other_source,other,self.root/'tsa-other')
        token_start=raw.index(b'/Contents <')+len(b'/Contents <')
        foreign=other.read_bytes();foreign_start=foreign.index(b'/Contents <')+len(b'/Contents <')
        swapped=self.root/'swapped.pdf'
        swapped.write_bytes(raw[:token_start]+foreign[foreign_start:foreign_start+65536]+raw[token_start+65536:])
        self.assertEqual(inspect_pdf_signatures(swapped,{})['signatures'][0]['status'],'not_verified')

    def test_signature_after_a_timestamp_keeps_both_valid(self):
        key,cert=signing_identity();key_path=self.root/'k.pem';cert_path=self.root/'c.pem'
        key_path.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        signed=self.root/'signed.pdf'
        sign_pdf_copy(self.stamped,dict(destination=str(signed),source_sha256=hashlib.sha256(self.stamped.read_bytes()).hexdigest(),
                                        certificate=str(cert_path),private_key=str(key_path),password=''))
        items=inspect_pdf_signatures(signed,{})['signatures']
        self.assertEqual([(i['kind'],i['status'],i['current_file_covered']) for i in items],
                         [('document_timestamp','verified',False),('signature','verified',True)])
        if shutil.which('pdfsig'):
            # poppler lists the timestamp field but does not verify ETSI.RFC3161; the later signature it does.
            report=subprocess.run(['pdfsig',str(signed)],capture_output=True,text=True,timeout=60).stdout
            self.assertIn('LinuxitDocTimeStamp',report);self.assertEqual(report.count('Signature is Valid.'),1)


if __name__=='__main__':unittest.main()
