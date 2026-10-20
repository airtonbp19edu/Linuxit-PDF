"""Own synthetic RFC 3161 document timestamps for tests and acceptance cases (E09).

A throw-away CA and timestamp authority are generated per call and the token is
produced by the local `openssl ts` tools; nothing is fetched from a network TSA.
The revision is appended with pdf_signing.append_signature_revision, the same
incremental writer the application uses for signatures.
"""
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
import subprocess

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def _certificate(name, issuer, key, signer, serial, now, ca=False, tsa=False):
    builder = (x509.CertificateBuilder().subject_name(name).issuer_name(issuer).public_key(key.public_key())
               .serial_number(serial).not_valid_before(now - timedelta(days=1)).not_valid_after(now + timedelta(days=30))
               .add_extension(x509.BasicConstraints(ca=ca, path_length=0 if ca else None), True))
    if tsa:
        builder = builder.add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.TIME_STAMPING]), True)
    return builder.sign(signer, hashes.SHA256())


def authority(folder):
    """Create a synthetic CA (returned as PEM path) and a TSA configuration in `folder`."""
    folder = Path(folder);folder.mkdir(parents=True, exist_ok=True);now = datetime.now(timezone.utc)
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Linuxit synthetic timestamp CA')])
    ca = _certificate(ca_name, ca_name, ca_key, ca_key, 1, now, ca=True)
    tsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    tsa = _certificate(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Linuxit synthetic TSA')]), ca_name, tsa_key, ca_key, 2, now, tsa=True)
    (folder / 'ca.pem').write_bytes(ca.public_bytes(serialization.Encoding.PEM))
    (folder / 'tsa.pem').write_bytes(tsa.public_bytes(serialization.Encoding.PEM))
    (folder / 'tsa-key.pem').write_bytes(tsa_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                               serialization.NoEncryption()))
    (folder / 'serial').write_text('01\n')
    (folder / 'tsa.cnf').write_text(f'''[tsa_config1]
serial = {folder / 'serial'}
crypto_device = builtin
signer_cert = {folder / 'tsa.pem'}
signer_key = {folder / 'tsa-key.pem'}
signer_digest = sha256
default_policy = 1.2.3.4.1
digests = sha256
accuracy = secs:1
ordering = yes
tsa_name = yes
ess_cert_id_chain = no
''')
    return folder / 'ca.pem'


def token(folder, data):
    folder = Path(folder);(folder / 'data.bin').write_bytes(data)
    for name in ('request.tsq', 'token.der'):(folder / name).unlink(missing_ok=True)
    subprocess.run(['openssl', 'ts', '-query', '-config', str(folder / 'tsa.cnf'), '-data', str(folder / 'data.bin'),
                    '-sha256', '-cert', '-out', str(folder / 'request.tsq')], check=True, capture_output=True, timeout=60)
    subprocess.run(['openssl', 'ts', '-reply', '-queryfile', str(folder / 'request.tsq'), '-config', str(folder / 'tsa.cnf'),
                    '-section', 'tsa_config1', '-token_out', '-out', str(folder / 'token.der')], check=True, capture_output=True, timeout=60)
    return (folder / 'token.der').read_bytes()


def add_document_timestamp(source, target, folder):
    """Write `target` = `source` + a DocTimeStamp revision; return the CA PEM path that trusts it."""
    from pypdf import PdfReader
    from pypdf.generic import DictionaryObject, NameObject
    from pdf_signing import _field_name, append_signature_revision
    ca = authority(folder);original = Path(source).read_bytes()
    reader = PdfReader(BytesIO(original), strict=True)
    stamp = DictionaryObject({NameObject('/Type'): NameObject('/DocTimeStamp'), NameObject('/Filter'): NameObject('/Adobe.PPKLite'),
                              NameObject('/SubFilter'): NameObject('/ETSI.RFC3161')})
    name = _field_name(reader.get_fields() or {}).replace('LinuxitSignature', 'LinuxitDocTimeStamp')
    raw, _, _, _ = append_signature_revision(original, reader, name, stamp, lambda covered: token(folder, covered))
    Path(target).write_bytes(raw)
    return ca
