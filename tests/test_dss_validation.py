"""E10: certificates and CRLs from the document security store (DSS) are used offline, never as anchors."""
import hashlib,sys,tempfile,unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'testes'/'aceitacao'))

from test_attachment_search import text_pdf
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from pdf_signing import sign_pdf_copy
from pdf_signatures import inspect_pdf_signatures
import carimbo


def name(text):return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,text)])


class DSSValidationTests(unittest.TestCase):
    """Root CA (selected anchor) -> intermediate CA (only in the DSS) -> signer (in the CMS)."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        now=self.now=datetime.now(timezone.utc)
        def cert(subject,issuer,key,signer,serial,ca):
            builder=(x509.CertificateBuilder().subject_name(name(subject)).issuer_name(name(issuer)).public_key(key.public_key())
                     .serial_number(serial).not_valid_before(now-timedelta(days=1)).not_valid_after(now+timedelta(days=30))
                     .add_extension(x509.BasicConstraints(ca=ca,path_length=1 if ca else None),True))
            if not ca:builder=builder.add_extension(x509.KeyUsage(True,False,False,False,False,False,False,False,False),True)
            return builder.sign(signer,hashes.SHA256())
        self.root_key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        self.ca=cert('Linuxit DSS root','Linuxit DSS root',self.root_key,self.root_key,1,True)
        self.mid_key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        self.mid=(x509.CertificateBuilder().subject_name(name('Linuxit DSS intermediate')).issuer_name(name('Linuxit DSS root'))
                  .public_key(self.mid_key.public_key()).serial_number(2).not_valid_before(now-timedelta(days=1)).not_valid_after(now+timedelta(days=30))
                  .add_extension(x509.BasicConstraints(ca=True,path_length=0),True).sign(self.root_key,hashes.SHA256()))
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        self.leaf=cert('Linuxit DSS signer','Linuxit DSS intermediate',key,self.mid_key,3,False)
        (self.root/'key.pem').write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        (self.root/'cert.pem').write_bytes(self.leaf.public_bytes(serialization.Encoding.PEM))
        (self.root/'root.pem').write_bytes(self.ca.public_bytes(serialization.Encoding.PEM))
        source=self.root/'source.pdf';source.write_bytes(text_pdf(['alpha']));self.signed=self.root/'signed.pdf'
        sign_pdf_copy(source,dict(destination=str(self.signed),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                  certificate=str(self.root/'cert.pem'),private_key=str(self.root/'key.pem'),password=''))

    def crl(self,issuer,key,revoked=()):
        builder=x509.CertificateRevocationListBuilder().issuer_name(name(issuer)).last_update(self.now-timedelta(minutes=1)).next_update(self.now+timedelta(days=1))
        for serial in revoked:
            builder=builder.add_revoked_certificate(x509.RevokedCertificateBuilder().serial_number(serial).revocation_date(self.now-timedelta(seconds=30)).build())
        return builder.sign(key,hashes.SHA256()).public_bytes(serialization.Encoding.DER)

    def trust(self,path,require_revocation=False):
        policy=dict(roots=[str(self.root/'root.pem')],crls=[],require_revocation=require_revocation,at_time=None)
        report=inspect_pdf_signatures(path,{'trust_policy':policy})
        return report,report['signatures'][0]['trust']

    def with_dss(self,certs,crls,label):
        target=self.root/f'{label}.pdf';carimbo.add_dss(self.signed,target,certs,crls);return target

    def test_intermediate_and_crls_from_dss_complete_the_offline_chain(self):
        _,without=self.trust(self.signed,True)
        self.assertFalse(without['chain_verified'])  # intermediate missing: no path to the anchor
        der=lambda c:c.public_bytes(serialization.Encoding.DER)
        crls=[self.crl('Linuxit DSS intermediate',self.mid_key),self.crl('Linuxit DSS root',self.root_key)]
        path=self.with_dss([der(self.mid)],crls,'dss')
        report,trust=self.trust(path,True)
        self.assertEqual(report['dss'],{'certificates':1,'crls':2,'ocsp_responses':0,'vri_entries':0})
        self.assertTrue(trust['chain_verified']);self.assertTrue(trust['revocation_verified']);self.assertTrue(trust['policy_satisfied'])
        self.assertEqual(trust['dss_used'],{'certificates':1,'crls':2});self.assertFalse(trust['network_used'])
        self.assertEqual(report['signatures'][0]['status'],'verified')

    def test_revoked_signer_in_dss_crl_and_dss_root_is_not_an_anchor(self):
        der=lambda c:c.public_bytes(serialization.Encoding.DER)
        revoked=self.with_dss([der(self.mid)],[self.crl('Linuxit DSS intermediate',self.mid_key,[3]),self.crl('Linuxit DSS root',self.root_key)],'revoked')
        _,trust=self.trust(revoked,True)
        self.assertTrue(trust['chain_verified']);self.assertFalse(trust['revocation_verified']);self.assertFalse(trust['policy_satisfied'])
        # A self-signed root placed in the DSS must not replace the user's selected anchor.
        other_key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        other=(x509.CertificateBuilder().subject_name(name('Unrelated root')).issuer_name(name('Unrelated root')).public_key(other_key.public_key())
               .serial_number(9).not_valid_before(self.now-timedelta(days=1)).not_valid_after(self.now+timedelta(days=30))
               .add_extension(x509.BasicConstraints(ca=True,path_length=0),True).sign(other_key,hashes.SHA256()))
        (self.root/'root.pem').write_bytes(other.public_bytes(serialization.Encoding.PEM))
        path=self.with_dss([der(self.mid),der(self.ca)],[],'root-in-dss')
        self.assertFalse(self.trust(path)[1]['chain_verified'])

    def test_malformed_dss_is_reported_and_ignored(self):
        path=self.with_dss([b'not a certificate'],[],'bad')
        report=inspect_pdf_signatures(path,{})
        self.assertIsNone(report['dss']);self.assertIn('DSS',report['dss_error'])
        self.assertEqual(report['signatures'][0]['status'],'verified')


if __name__=='__main__':unittest.main()
