"""Bounded offline CMS integrity checks; certificate trust and legal validity are not assessed."""
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from pdf_changes import _inherited, _sha
from platform_runtime import subprocess_options
from search_tasks import run_search_worker

MAX_PDF = 64 * 1024**2
MAX_CMS = 2 * 1024**2
POWERSHELL_VERIFY = r"""$ErrorActionPreference='Stop'; try {
try { Add-Type -AssemblyName System.Security.Cryptography.Pkcs } catch { Add-Type -AssemblyName System.Security }
$r=[Console]::In.ReadToEnd() | ConvertFrom-Json
$data=[System.IO.File]::ReadAllBytes($r.content)
$ci=[System.Security.Cryptography.Pkcs.ContentInfo]::new($data)
$cms=[System.Security.Cryptography.Pkcs.SignedCms]::new($ci,$true)
$cms.Decode([System.IO.File]::ReadAllBytes($r.signature))
if ($cms.SignerInfos.Count -lt 1) { exit 1 }
$cms.CheckSignature($true)
[Console]::Out.Write('VERIFIED'); exit 0
} catch { exit 1 }"""


def _der_payload(value):
    if len(value) < 2 or value[0] != 0x30:raise ValueError('CMS DER inválido.')
    length = value[1];header = 2
    if length & 128:
        count = length & 127
        if not 1 <= count <= 4 or len(value) < 2+count:raise ValueError('Comprimento CMS inválido.')
        length = int.from_bytes(value[2:2+count], 'big');header += count
    end = header+length
    if length <= 0 or end > len(value) or end > MAX_CMS or any(value[end:]):raise ValueError('CMS truncado, acima do limite ou com dados adicionais.')
    return value[:end]


def _windows_powershell():
    """System Windows PowerShell first (always shipped, not PATH-dependent), then PowerShell 7.

    A minimal PATH (MSYS2 shells, some launchers) must not make CMS verification unavailable;
    Windows PowerShell 5.1 keeps SignedCms in System.Security, PowerShell 7 in its own assembly.
    """
    root = os.environ.get('SystemRoot') or os.environ.get('WINDIR') or r'C:\Windows'
    system = Path(root)/'System32'/'WindowsPowerShell'/'v1.0'/'powershell.exe'
    if system.is_file():return str(system)
    return shutil.which('pwsh') or shutil.which('powershell')


def _verify_detached(cms, content):
    if os.name == 'nt':
        executable = _windows_powershell()
        backend = 'Windows .NET SignedCms, signature only'
    else:
        executable = shutil.which('openssl');backend = 'OpenSSL CMS -noverify, signature only'
    if not executable:return None, 'unavailable'
    with tempfile.TemporaryDirectory(prefix='linuxit-cms-') as folder:
        folder = Path(folder);signature = folder/'signature.der';data = folder/'content.bin'
        signature.write_bytes(cms);data.write_bytes(content)
        if os.name != 'nt':signature.chmod(0o600);data.chmod(0o600)
        if os.name == 'nt':
            command = [executable, '-NoProfile', '-NonInteractive', '-Command', POWERSHELL_VERIFY]
            payload = json.dumps({'signature':str(signature),'content':str(data)}, ensure_ascii=True).encode('ascii')
        else:
            command = [executable, 'cms', '-verify', '-binary', '-inform', 'DER', '-noverify',
                       '-in', str(signature), '-content', str(data), '-out', os.devnull]
            payload = None
        try:
            result = subprocess.run(command, input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    timeout=30, **subprocess_options())
        except (OSError, subprocess.TimeoutExpired):return None, backend
        return result.returncode == 0, backend


TIMESTAMP_DIGESTS = {'sha256', 'sha384', 'sha512'}
MAX_DSS_CERTS = 64
MAX_DSS_CRLS = 32
MAX_DSS_OCSPS = 32
MAX_DSS_ITEM = 1024**2


def _dss_material(reader):
    """Certificates and CRLs of the document security store (/DSS), bounded (E10).

    They are validation material only: certificates never become trust anchors and
    nothing is fetched. OCSP is checked separately against an explicit local chain.
    """
    dss = reader.root_object.get('/DSS')
    if dss is None:return None
    dss = dss.get_object()
    if not hasattr(dss, 'get'):raise ValueError('DSS inválido.')
    def items(key, limit):
        values = dss.get(key)
        values = values.get_object() if values is not None else []
        if not isinstance(values, list) or len(values) > limit:raise ValueError('DSS acima do limite: ' + key)
        result = []
        for value in values:
            data = value.get_object().get_data()
            if not data or len(data) > MAX_DSS_ITEM:raise ValueError('Item do DSS vazio ou acima de 1 MiB.')
            result.append(data)
        return result
    vri = dss.get('/VRI');vri = vri.get_object() if vri is not None else {}
    from cryptography import x509
    from cryptography.x509 import ocsp
    certificates, crls = items('/Certs', MAX_DSS_CERTS), items('/CRLs', MAX_DSS_CRLS)
    ocsps = items('/OCSPs', MAX_DSS_OCSPS)
    for data in certificates:x509.load_der_x509_certificate(data)
    for data in crls:x509.load_der_x509_crl(data)
    for data in ocsps:ocsp.load_der_ocsp_response(data)
    return {'certificates': certificates, 'crls': crls, 'ocsps': ocsps,
            'ocsp_responses': len(ocsps), 'vri_entries': len(vri) if hasattr(vri, 'keys') else 0}


def _verify_document_timestamp(token, content):
    """Integrity of an RFC 3161 document timestamp: token signature and message imprint (E09).

    Returns (verified, backend, generation time). Trust in the TSA is separate.
    """
    executable = shutil.which('openssl')
    backend = 'OpenSSL CMS -noverify + TSTInfo imprint, signature only'
    if not executable:return None, 'unavailable', None
    from asn1crypto import cms as asn_cms, tsp
    structure = asn_cms.ContentInfo.load(token, strict=True)
    if structure['content_type'].native != 'signed_data' or \
            structure['content']['encap_content_info']['content_type'].native != 'tst_info':
        raise ValueError('Carimbo de documento sem TSTInfo.')
    with tempfile.TemporaryDirectory(prefix='linuxit-doc-ts-') as folder:
        folder = Path(folder);token_path = folder/'token.der';info_path = folder/'tstinfo.der'
        token_path.write_bytes(token)
        if os.name != 'nt':token_path.chmod(0o600)
        try:
            result = subprocess.run([executable, 'cms', '-verify', '-binary', '-inform', 'DER', '-noverify',
                                     '-in', str(token_path), '-out', str(info_path)],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, **subprocess_options())
        except (OSError, subprocess.TimeoutExpired):return None, backend, None
        if result.returncode != 0 or not info_path.is_file():return False, backend, None
        info = tsp.TSTInfo.load(info_path.read_bytes(), strict=True)
    algorithm = info['message_imprint']['hash_algorithm']['algorithm'].native
    if algorithm not in TIMESTAMP_DIGESTS:raise ValueError('Algoritmo do carimbo não suportado.')
    imprint = info['message_imprint']['hashed_message'].native
    if hashlib.new(algorithm, content).digest() != imprint:return False, backend, None
    return True, backend, info['gen_time'].native.isoformat()


def inspect_pdf_signatures(path, request):
    if not isinstance(request,dict) or set(request) not in (set(),{'trust_policy'}):raise ValueError('Pedido de assinaturas inválido.')
    policy=request.get('trust_policy')
    if policy is not None:
        from signature_trust import trust_policy
        trust_policy(policy)
    path = Path(path)
    if not path.is_file() or path.stat().st_size > MAX_PDF:raise ValueError('Selecione um PDF disponível de até 64 MiB.')
    with path.open('rb') as stream:raw = stream.read(MAX_PDF+1)
    if len(raw) > MAX_PDF:raise ValueError('O PDF excede o limite de 64 MiB.')
    identity = hashlib.sha256(raw).hexdigest();reader = PdfReader(BytesIO(raw), strict=True)
    if reader.is_encrypted:raise ValueError('A inspeção de assinaturas em PDFs criptografados ainda não é suportada.')
    signatures, omitted = [], 0
    dss_error = None
    try:
        dss = _dss_material(reader)
    except (ValueError, AttributeError, TypeError, KeyError):
        dss, dss_error = None, 'DSS inválido ou acima dos limites; ignorado.'
    for name, field in (reader.get_fields() or {}).items():
        if _inherited(field, '/FT') != '/Sig':continue
        if len(signatures) >= 16:omitted += 1;continue
        record = {'field':name,'kind':None,'integrity_verified':None,'trust_chain_verified':False,
                  'current_file_covered':False,'backend':None,'status':'unsigned','covered_revision_bytes':None}
        signatures.append(record)
        value = field.get('/V')
        if value is None:continue
        try:
            value = value.get_object()
            subfilter = value.get('/SubFilter')
            if subfilter not in ('/adbe.pkcs7.detached','/ETSI.CAdES.detached','/ETSI.RFC3161'):
                raise ValueError('SubFilter não suportado; somente CMS destacado ou carimbo RFC 3161.')
            record['kind'] = 'document_timestamp' if subfilter == '/ETSI.RFC3161' else 'signature'
            ranges = value.get('/ByteRange')
            if not isinstance(ranges, list) or len(ranges) != 4 or not all(type(x) is int or type(x).__name__ == 'NumberObject' for x in ranges):
                raise ValueError('ByteRange inválido; são exigidos dois intervalos.')
            first, left, right, tail = map(int, ranges)
            if first != 0 or not 0 < left < right <= len(raw) or tail <= 0 or right+tail > len(raw):
                raise ValueError('ByteRange fora dos limites da revisão.')
            gap = raw[left:right]
            if len(gap) > MAX_CMS*2+4096 or not gap.startswith(b'<') or not gap.endswith(b'>'):
                raise ValueError('O intervalo excluído deve conter somente o Contents hexadecimal.')
            content_bytes = bytes.fromhex(gap[1:-1].decode('ascii'))
            declared = value.get('/Contents')
            declared = bytes(declared) if isinstance(declared, bytes) else declared.original_bytes
            if content_bytes != declared:raise ValueError('Contents não corresponde ao intervalo excluído.')
            cms = _der_payload(content_bytes)
            covered = raw[:left]+raw[right:right+tail]
            if record['kind'] == 'document_timestamp':
                verified, backend, moment = _verify_document_timestamp(cms, covered)
                record['timestamp_time'] = moment
            else:
                verified, backend = _verify_detached(cms, covered)
            record.update(integrity_verified=verified,backend=backend,
                          status='verified' if verified else 'not_verified' if verified is False else 'unavailable',
                          current_file_covered=right+tail == len(raw),covered_revision_bytes=right+tail)
            if policy is not None:
                from signature_trust import verify_document_timestamp, verify_trust
                check = verify_document_timestamp if record['kind'] == 'document_timestamp' else verify_trust
                trust=check(cms,covered,policy,dss)
                record['trust']=trust;record['trust_chain_verified']=trust['chain_verified']
        except (ValueError, AttributeError, TypeError, KeyError, OverflowError):
            record['status'] = 'unsupported_or_malformed'
    if _sha(path) != identity:raise ValueError('O PDF mudou durante a verificação de assinaturas.')
    return {'schema':'linuxit-signature-integrity-v1','source_sha256':identity,'signatures':signatures,
            'omitted_signatures':omitted,'trust_chain_verified':False,'network_used':False,
            'dss':None if dss is None else {'certificates':len(dss['certificates']),'crls':len(dss['crls']),
                                            'ocsp_responses':dss['ocsp_responses'],'vri_entries':dss['vri_entries']},
            'dss_error':dss_error,
            'trust_assessed':policy is not None,
            'scope':'Per-signature explicit local CA/CRL/RFC3161 policy; no legal/LTV decision.' if policy is not None else 'CMS integrity only; no chain, revocation, timestamp or legal validity assessment.'}


def invoke_signature_inspection(path, cancel=None,trust_policy=None):
    result = run_search_worker('signature-info', path, {} if trust_policy is None else {'trust_policy':trust_policy}, cancel, timeout=300 if trust_policy else 120)
    if result is None:return None
    if (not isinstance(result, dict) or result.get('schema') != 'linuxit-signature-integrity-v1'
            or result.get('trust_chain_verified') is not False or not isinstance(result.get('signatures'), list)):
        raise RuntimeError('O worker não retornou uma inspeção de assinaturas válida.')
    return result
