"""Own incremental DSS and two-phase RFC 3161 document timestamps.

All material is selected locally. Exporting a query does not contact a TSA;
importing a response requires explicit trust anchors and verifies imprint/nonce.
These operations preserve revisions; they do not claim universal PAdES-LTA.
"""
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import tempfile

from pdf_changes import _require, _sha
from pdf_signing import (_signing_source, _incremental_update, append_signature_revision,
                         RESERVATION, _field_name)
from pdf_signatures import inspect_pdf_signatures, _der_payload, _dss_material
from local_files import publish_copy
from pypdf import PdfReader
from pypdf.generic import (ArrayObject, DictionaryObject, DecodedStreamObject,
                           IndirectObject, NameObject)

MAX_FILE = 64 * 1024**2
MAX_MATERIAL = 1024**2
MATERIAL_LIMITS = {'certificates': 64, 'crls': 32, 'ocsps': 32}


def _read(path, limit=MAX_MATERIAL):
    with Path(path).open('rb') as stream:
        raw = stream.read(limit + 1)
    _require(0 < len(raw) <= limit, 'Arquivo vazio ou acima do limite permitido.')
    return raw


def _files(values, limit):
    _require(isinstance(values, list) and len(values) <= limit and
             all(isinstance(p, str) and 0 < len(p) <= 4096 for p in values), 'Lista de material local inválida.')
    return [_read(p) for p in values]


def _material(request):
    from cryptography import x509
    from cryptography.x509 import ocsp
    from cryptography.hazmat.primitives import serialization
    result = {}
    for key, limit in MATERIAL_LIMITS.items():
        result[key] = []
        for raw in _files(request[key], limit):
            if key == 'certificates':
                items = x509.load_pem_x509_certificates(raw) if b'-----BEGIN' in raw else [x509.load_der_x509_certificate(raw)]
                result[key].extend(c.public_bytes(serialization.Encoding.DER) for c in items)
            elif key == 'crls':
                value = x509.load_pem_x509_crl(raw) if b'-----BEGIN' in raw else x509.load_der_x509_crl(raw)
                result[key].append(value.public_bytes(serialization.Encoding.DER))
            else:
                value = ocsp.load_der_ocsp_response(raw)
                _require(value.response_status == ocsp.OCSPResponseStatus.SUCCESSFUL, 'Resposta OCSP sem estado de sucesso.')
                _require(len(list(value.responses)) == 1, 'OCSP exige uma resposta individual por arquivo.')
                result[key].append(raw)
        result[key] = list(dict.fromkeys(result[key]))
        _require(len(result[key]) <= limit, 'Material DSS acima do limite.')
    _require(any(result.values()), 'Selecione pelo menos um certificado, CRL ou OCSP local.')
    return result


def _publish(source, target, raw, identity, validate=None):
    _require(raw.startswith(source.read_bytes()), 'A revisão incremental alterou a origem.')
    _require(len(raw) <= MAX_FILE, 'Cópia acima do limite de 64 MiB.')
    with tempfile.TemporaryDirectory(prefix='linuxit-preservation-') as directory:
        staged = Path(directory) / 'copy.pdf';staged.write_bytes(raw)
        report = inspect_pdf_signatures(staged, {})
        _require(report['signatures'] and all(s['status'] in ('verified', 'unsigned') for s in report['signatures']),
                 'Uma assinatura anterior não foi verificada; cópia recusada.')
        if validate:
            validate(report)
        publish_copy(staged, target, lambda: _require(_sha(source) == identity, 'O PDF mudou durante a operação.'))
    return report


def append_dss_copy(path, request):
    """Append validation material without rewriting any byte covered by earlier signatures.

    Existing DSS arrays and VRI keys are preserved; new data joins the global DSS.
    Optional vri_fields explicitly associates incoming material with selected
    verified signatures. It does not assert that the supplied chain is complete.
    Imported certificates are *not* trusted automatically; inspect with explicit CA.
    """
    required = {'destination', 'source_sha256', 'certificates', 'crls', 'ocsps'}
    _require(isinstance(request, dict) and required <= set(request) <= required | {'vri_fields'}, 'Pedido DSS inválido.')
    selected = request.get('vri_fields', [])
    _require(isinstance(selected,list) and len(selected)<=16 and all(isinstance(n,str) for n in selected)
             and len(set(selected))==len(selected), 'Seleção de assinaturas VRI inválida.')
    source = Path(path).resolve();target = Path(request['destination'])
    original = _read(source, MAX_FILE);incoming = _material(request)
    with _signing_source(source, request['source_sha256']) as (reader, fields, identity):
        report = inspect_pdf_signatures(source, {})
        _require(any(s['status'] == 'verified' for s in report['signatures']), 'DSS exige assinatura ou carimbo existente verificado.')
        _require(report['dss_error'] is None, 'DSS existente inválido; cópia recusada.')
        verified = {s['field']:s for s in report['signatures'] if s['status']=='verified'}
        _require(all(name in verified for name in selected), 'VRI exige selecionar assinaturas verificadas deste PDF.')
        existing = _dss_material(reader) or {'certificates': [], 'crls': [], 'ocsps': []}
        dss_ref = reader.root_object.get('/DSS')
        dss = DictionaryObject(dss_ref.get_object()) if dss_ref is not None else DictionaryObject()
        number = int(reader.trailer['/Size']);new = {}
        def stream(raw):
            nonlocal number
            value = DecodedStreamObject();value.set_data(raw);new[number] = value
            reference = IndirectObject(number, 0, reader);number += 1
            return reference
        sizes = {}
        references = {}
        for key, pdf_key in (('certificates', '/Certs'), ('crls', '/CRLs'), ('ocsps', '/OCSPs')):
            merged = list(dict.fromkeys(existing.get(key, []) + incoming[key]))
            _require(len(merged) <= MATERIAL_LIMITS[key], 'Material DSS combinado acima do limite.')
            refs = {raw:stream(raw) for raw in merged};references[key]=refs
            dss[NameObject(pdf_key)] = ArrayObject(refs.values())
            sizes[key] = len(merged)
        vri = dss.get('/VRI');vri = DictionaryObject(vri.get_object()) if vri is not None else DictionaryObject()
        for name in selected:
            digest = verified[name]['vri']['key'];pdf_key = NameObject('/'+digest)
            old = vri.get(pdf_key);entry = DictionaryObject(old.get_object()) if old is not None else DictionaryObject()
            old_material = existing.get('_vri',{}).get(digest,{})
            for key, local_key in (('certificates','/Cert'),('crls','/CRL'),('ocsps','/OCSP')):
                merged = list(dict.fromkeys(old_material.get(key,[]) + incoming[key]))
                _require(len(merged)<=MATERIAL_LIMITS[key], 'Material VRI combinado acima do limite.')
                refs = []
                for data in merged:
                    if data not in references[key]:references[key][data]=stream(data)
                    refs.append(references[key][data])
                entry[NameObject(local_key)] = ArrayObject(refs)
            vri[pdf_key] = entry
        _require(len(vri)<=256, 'Acima de 256 entradas VRI.')
        if vri:dss[NameObject('/VRI')] = vri
        new[number] = dss;updated = DictionaryObject(reader.root_object)
        updated[NameObject('/DSS')] = IndirectObject(number, 0, reader)
        reference = reader.trailer.raw_get('/Root')
        raw = original + _incremental_update(original, reader, new, {(reference.idnum, reference.generation): updated})
    def validate(final):
        by_name={item['field']:item for item in final['signatures']}
        _require(all(by_name.get(name,{}).get('vri',{}).get('matched') is True for name in selected),
                 'Associação VRI não confirmada; nenhuma cópia publicada.')
    _publish(source, target, raw, identity, validate)
    return dict(schema='linuxit-dss-copy-v1', path=str(target), source_sha256=identity,
                output_sha256=_sha(target), incremental=True, material=sizes,
                trust_assessed=False, network_used=False, pades_lta_claimed=False,
                vri_fields=selected, vri_entries=len(vri))


def prepare_document_timestamp(path, request):
    """Export a nonce-bound .tsq and the exact prepared revision into a NEW folder.

    The .pending file is an incomplete PDF revision, not a valid timestamped PDF.
    A TSA may receive timestamp.tsq by a user-chosen transport outside this tool.
    """
    _require(isinstance(request, dict) and set(request) == {'source_sha256', 'folder'}, 'Pedido de carimbo inválido.')
    from asn1crypto import tsp
    source = Path(path).resolve();original = _read(source, MAX_FILE)
    with _signing_source(source, request['source_sha256']) as (reader, fields, identity):
        name = 'LinuxitDocTimeStamp';number = 1
        while name in fields:
            number += 1;name = f'LinuxitDocTimeStamp{number}'
        stamp = DictionaryObject({NameObject('/Type'): NameObject('/DocTimeStamp'),
                                NameObject('/Filter'): NameObject('/Adobe.PPKLite'),
                                NameObject('/SubFilter'): NameObject('/ETSI.RFC3161')})
        pending, _, left, right = append_signature_revision(original, reader, name, stamp, lambda covered: b'\x30\x00')
    _require(len(pending) <= MAX_FILE, 'Revisão acima do limite de 64 MiB.')
    nonce = int.from_bytes(os.urandom(16), 'big') or 1
    query = tsp.TimeStampReq({'version': 'v1', 'message_imprint': {
        'hash_algorithm': {'algorithm': 'sha256'},
        'hashed_message': hashlib.sha256(pending[:left] + pending[right:]).digest()}, 'nonce': nonce, 'cert_req': True}).dump()
    manifest = dict(schema='linuxit-timestamp-pending-v1', source_sha256=identity, field=name,
                    pending_sha256=hashlib.sha256(pending).hexdigest(), query_sha256=hashlib.sha256(query).hexdigest(),
                    source_bytes=len(original), left=left, right=right, network_used=False)
    _require(_sha(source) == identity, 'O PDF mudou durante a preparação.')
    folder = Path(request['folder']);folder.mkdir(mode=0o700)
    # Exclusive files and a newly created directory avoid replacing another run.
    for name, data in (('document.pending', pending), ('timestamp.tsq', query),
                       ('manifest.json', (json.dumps(manifest, indent=2) + '\n').encode('utf-8'))):
        with (folder / name).open('xb') as output:
            output.write(data)
    return dict(schema='linuxit-timestamp-query-v1', folder=str(folder), source_sha256=identity,
                query=str(folder / 'timestamp.tsq'), complete=False, network_used=False)


def complete_document_timestamp(path, request):
    """Import a successful DER TimeStampResp, validate token/nonce/CA, publish a new copy."""
    _require(isinstance(request, dict) and set(request) ==
             {'source_sha256', 'folder', 'response', 'destination', 'trust_policy'}, 'Pedido de resposta TSA inválido.')
    from asn1crypto import tsp
    from signature_trust import verify_document_timestamp
    source = Path(path).resolve();original = _read(source, MAX_FILE);identity = hashlib.sha256(original).hexdigest()
    _require(identity == request['source_sha256'], 'O PDF mudou. Prepare outro pedido de carimbo.')
    folder = Path(request['folder']);manifest = json.loads(_read(folder / 'manifest.json', 16384))
    pending = _read(folder / 'document.pending', MAX_FILE);query_raw = _read(folder / 'timestamp.tsq', 16384)
    _require(manifest.get('schema') == 'linuxit-timestamp-pending-v1' and manifest.get('source_sha256') == identity and
             manifest.get('source_bytes') == len(original) and pending.startswith(original) and
             manifest.get('pending_sha256') == hashlib.sha256(pending).hexdigest() and
             manifest.get('query_sha256') == hashlib.sha256(query_raw).hexdigest(), 'Preparação alterada ou pertence a outro PDF.')
    left, right = manifest.get('left'), manifest.get('right')
    _require(type(left) is int and type(right) is int and len(original) < left < right < len(pending) and
             right - left == RESERVATION * 2 + 2, 'Reserva de carimbo inválida.')
    query = tsp.TimeStampReq.load(query_raw, strict=True)
    response = tsp.TimeStampResp.load(_read(request['response']), strict=True)
    _require(response['status']['status'].native in ('granted', 'granted_with_mods'), 'A TSA não concedeu o carimbo.')
    token = response['time_stamp_token'];encoded = token.dump()
    info = token['content']['encap_content_info']['content'].parsed
    _require(info['nonce'].native == query['nonce'].native and info['nonce'].native is not None, 'Nonce TSA divergente ou ausente.')
    _require(info['message_imprint'].dump() == query['message_imprint'].dump(), 'A resposta TSA pertence a outro pedido.')
    covered = pending[:left] + pending[right:]
    _require(query['message_imprint']['hash_algorithm']['algorithm'].native == 'sha256' and
             query['message_imprint']['hashed_message'].native == hashlib.sha256(covered).digest(), 'Resumo da preparação inválido.')
    trust = verify_document_timestamp(encoded, covered, request['trust_policy'])
    _require(trust['policy_satisfied'], 'Carimbo TSA sem confiança na política local selecionada.')
    _require(len(encoded) <= RESERVATION, 'Token TSA acima da reserva de 32 KiB.')
    raw = pending[:left] + b'<' + encoded.hex().encode('ascii').ljust(RESERVATION * 2, b'0') + b'>' + pending[right:]
    def validate(report):
        _require(any(s['field'] == manifest['field'] and s['kind'] == 'document_timestamp' and s['status'] == 'verified'
                     and s['current_file_covered'] for s in report['signatures']), 'Novo carimbo não confirmado.')
    target = Path(request['destination']);_publish(source, target, raw, identity, validate)
    return dict(schema='linuxit-timestamp-copy-v1', path=str(target), source_sha256=identity,
                output_sha256=_sha(target), incremental=True, field=manifest['field'],
                trust_assessed=True, trust=trust, network_used=False, pades_lta_claimed=False)


def invoke_preservation(command, path, request, cancel=None):
    from search_tasks import run_search_worker
    schemas = {'signature-dss': 'linuxit-dss-copy-v1', 'timestamp-prepare': 'linuxit-timestamp-query-v1',
               'timestamp-complete': 'linuxit-timestamp-copy-v1'}
    _require(command in schemas, 'Comando de preservação inválido.')
    result = run_search_worker(command, path, request, cancel, timeout=300)
    if result is None:
        return None
    _require(result.get('schema') == schemas[command] and result.get('source_sha256') == request['source_sha256'],
             'O worker não confirmou a preservação esperada.')
    return result
