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
Add-Type -AssemblyName System.Security.Cryptography.Pkcs
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


def _verify_detached(cms, content):
    if os.name == 'nt':
        executable = shutil.which('pwsh') or shutil.which('powershell')
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
    for name, field in (reader.get_fields() or {}).items():
        if _inherited(field, '/FT') != '/Sig':continue
        if len(signatures) >= 16:omitted += 1;continue
        record = {'field':name,'integrity_verified':None,'trust_chain_verified':False,
                  'current_file_covered':False,'backend':None,'status':'unsigned','covered_revision_bytes':None}
        signatures.append(record)
        value = field.get('/V')
        if value is None:continue
        try:
            value = value.get_object()
            if value.get('/SubFilter') not in ('/adbe.pkcs7.detached','/ETSI.CAdES.detached'):
                raise ValueError('SubFilter não suportado; somente CMS destacado.')
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
            verified, backend = _verify_detached(cms, raw[:left]+raw[right:right+tail])
            record.update(integrity_verified=verified,backend=backend,
                          status='verified' if verified else 'not_verified' if verified is False else 'unavailable',
                          current_file_covered=right+tail == len(raw),covered_revision_bytes=right+tail)
            if policy is not None:
                from signature_trust import verify_trust
                trust=verify_trust(cms,raw[:left]+raw[right:right+tail],policy)
                record['trust']=trust;record['trust_chain_verified']=trust['chain_verified']
        except (ValueError, AttributeError, TypeError, KeyError, OverflowError):
            record['status'] = 'unsupported_or_malformed'
    if _sha(path) != identity:raise ValueError('O PDF mudou durante a verificação de assinaturas.')
    return {'schema':'linuxit-signature-integrity-v1','source_sha256':identity,'signatures':signatures,
            'omitted_signatures':omitted,'trust_chain_verified':False,'network_used':False,
            'trust_assessed':policy is not None,
            'scope':'Per-signature explicit local CA/CRL/RFC3161 policy; no legal/LTV decision.' if policy is not None else 'CMS integrity only; no chain, revocation, timestamp or legal validity assessment.'}


def invoke_signature_inspection(path, cancel=None,trust_policy=None):
    result = run_search_worker('signature-info', path, {} if trust_policy is None else {'trust_policy':trust_policy}, cancel, timeout=300 if trust_policy else 120)
    if result is None:return None
    if (not isinstance(result, dict) or result.get('schema') != 'linuxit-signature-integrity-v1'
            or result.get('trust_chain_verified') is not False or not isinstance(result.get('signatures'), list)):
        raise RuntimeError('O worker não retornou uma inspeção de assinaturas válida.')
    return result
