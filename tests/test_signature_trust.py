"""Synthetic CA/CRL/RFC3161 decisions with OpenSSL; no online identities."""
from datetime import datetime,timedelta,timezone
import os,sys,tempfile,unittest,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from signature_trust import trust_policy,verify_trust
from cryptography import x509
from cryptography.x509.oid import NameOID,ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7


class TrustPolicyTests(unittest.TestCase):
    def test_policy_requires_explicit_anchors_bounded_files_and_zoned_time(self):
        good=dict(roots=['root.pem'],crls=[],require_revocation=False,at_time=None)
        self.assertIsNotNone(trust_policy(good)['moment'].utcoffset())
        for changed in [dict(roots=[]),dict(roots=['x']*17),dict(require_revocation=1),dict(at_time='2026-01-01')]:
            with self.subTest(changed=changed),self.assertRaises(ValueError):trust_policy(dict(good,**changed))


@unittest.skipIf(os.name=='nt','Native OpenSSL and packaged ASN.1 integration')
class OfflineTrustTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.now=datetime.now(timezone.utc);self.ca_key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        self.ca_name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Linuxit synthetic CA')])
        self.ca=(x509.CertificateBuilder().subject_name(self.ca_name).issuer_name(self.ca_name).public_key(self.ca_key.public_key()).serial_number(1)
                 .not_valid_before(self.now-timedelta(days=1)).not_valid_after(self.now+timedelta(days=2))
                 .add_extension(x509.BasicConstraints(ca=True,path_length=0),True).sign(self.ca_key,hashes.SHA256()))
        self.key,self.leaf=self.identity('Signer',2)
        self.ca_path=self.root/'ca.pem';self.ca_path.write_bytes(self.ca.public_bytes(serialization.Encoding.PEM))
        self.policy=dict(roots=[str(self.ca_path)],crls=[],require_revocation=False,at_time=None)
        self.content=b'Synthetic signed document content'
        self.cms=(pkcs7.PKCS7SignatureBuilder().set_data(self.content).add_signer(self.leaf,self.key,hashes.SHA256()).add_certificate(self.ca)
                  .sign(serialization.Encoding.DER,[pkcs7.PKCS7Options.Binary,pkcs7.PKCS7Options.DetachedSignature]))

    def identity(self,name,serial,tsa=False):
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        builder=(x509.CertificateBuilder().subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,name)]))
                 .issuer_name(self.ca_name).public_key(key.public_key()).serial_number(serial)
                 .not_valid_before(self.now-timedelta(hours=1)).not_valid_after(self.now+timedelta(days=1))
                 .add_extension(x509.BasicConstraints(ca=False,path_length=None),True)
                 .add_extension(x509.KeyUsage(True,False,False,False,False,False,False,False,False),True))
        if tsa:builder=builder.add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.TIME_STAMPING]),True)
        return key,builder.sign(self.ca_key,hashes.SHA256())

    def crl(self,revoked=False):
        builder=x509.CertificateRevocationListBuilder().issuer_name(self.ca_name).last_update(self.now-timedelta(minutes=1)).next_update(self.now+timedelta(days=1))
        if revoked:builder=builder.add_revoked_certificate(x509.RevokedCertificateBuilder().serial_number(self.leaf.serial_number).revocation_date(self.now-timedelta(seconds=30)).build())
        target=self.root/'crl.pem';target.write_bytes(builder.sign(self.ca_key,hashes.SHA256()).public_bytes(serialization.Encoding.PEM));return str(target)

    def test_explicit_ca_trust_integrity_and_expiry_are_independent_of_revocation(self):
        result=verify_trust(self.cms,self.content,self.policy)
        self.assertTrue(result['chain_verified']);self.assertTrue(result['policy_satisfied']);self.assertFalse(result['revocation_verified']);self.assertFalse(result['network_used'])
        self.assertFalse(verify_trust(self.cms,self.content+b'changed',self.policy)['chain_verified'])
        self.assertFalse(verify_trust(self.cms,self.content,dict(self.policy,at_time=(self.now+timedelta(days=10)).isoformat()))['chain_verified'])

    def test_offline_crl_required_missing_clear_and_revoked(self):
        policy=dict(self.policy,require_revocation=True)
        self.assertFalse(verify_trust(self.cms,self.content,policy)['policy_satisfied'])
        policy['crls']=[self.crl()]
        self.assertTrue(verify_trust(self.cms,self.content,policy)['revocation_verified'])
        policy['crls']=[self.crl(True)]
        result=verify_trust(self.cms,self.content,policy)
        self.assertTrue(result['chain_verified']);self.assertFalse(result['revocation_verified']);self.assertFalse(result['policy_satisfied'])

    def test_non_ca_anchor_and_unrelated_ca_are_not_implicitly_trusted(self):
        self.ca_path.write_bytes(self.leaf.public_bytes(serialization.Encoding.PEM))
        with self.assertRaises(ValueError):verify_trust(self.cms,self.content,self.policy)

    def test_actual_rfc3161_token_is_bound_to_signer_signature_value(self):
        from asn1crypto import cms
        structure=cms.ContentInfo.load(self.cms);signer=structure['content']['signer_infos'][0]
        tsa_key,tsa=self.identity('Synthetic timestamp authority',3,True)
        cert=self.root/'tsa.pem';key=self.root/'tsa-key.pem';cert.write_bytes(tsa.public_bytes(serialization.Encoding.PEM))
        key.write_bytes(tsa_key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        serial=self.root/'serial';serial.write_text('01\n');data=self.root/'signature.bin';data.write_bytes(signer['signature'].native)
        config=self.root/'tsa.cnf';config.write_text(f'''[tsa_config1]
serial = {serial}
crypto_device = builtin
signer_cert = {cert}
signer_key = {key}
signer_digest = sha256
default_policy = 1.2.3.4.1
digests = sha256
accuracy = secs:1
ordering = yes
tsa_name = yes
ess_cert_id_chain = no
''')
        request=self.root/'request.tsq';token=self.root/'token.der'
        subprocess.run(['openssl','ts','-query','-config',str(config),'-data',str(data),'-sha256','-cert','-out',str(request)],check=True,capture_output=True)
        subprocess.run(['openssl','ts','-reply','-queryfile',str(request),'-config',str(config),'-section','tsa_config1','-token_out','-out',str(token)],check=True,capture_output=True)
        signer['unsigned_attrs']=cms.CMSAttributes([cms.CMSAttribute({'type':'signature_time_stamp_token','values':[cms.ContentInfo.load(token.read_bytes())]})])
        result=verify_trust(structure.dump(),self.content,self.policy)
        self.assertEqual(len(result['timestamps']),1);self.assertTrue(result['timestamps'][0]['verified'],result)
        signer['signature']=bytes([signer['signature'].native[0]^1])+signer['signature'].native[1:]
        result=verify_trust(structure.dump(),self.content,self.policy)
        self.assertFalse(result['timestamps'][0]['verified']);self.assertIsNone(result['timestamps'][0]['time'])
