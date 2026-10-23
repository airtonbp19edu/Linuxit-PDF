"""Bounded, offline DSS/VRI parsing and per-Contents selection.

SHA-1 is the PDF VRI lookup identifier, not a signature/trust algorithm.
Embedded certificates are validation material and never trust anchors.
"""
import hashlib
import re

MAX_TOTAL = 16 * 1024**2
MAX_ITEM = 1024**2
KINDS = (('certificates', '/Certs', '/Cert', 64), ('crls', '/CRLs', '/CRL', 32), ('ocsps', '/OCSPs', '/OCSP', 32))


def material(reader):
    raw = reader.root_object.get('/DSS')
    if raw is None:
        return None
    root = raw.get_object()
    if not isinstance(root, dict):
        raise ValueError('DSS inválido.')
    from cryptography import x509
    from cryptography.x509 import ocsp
    validators = dict(certificates=x509.load_der_x509_certificate, crls=x509.load_der_x509_crl, ocsps=ocsp.load_der_ocsp_response)
    total, cache = 0, {}
    def read(node, per_signature=False):
        nonlocal total
        result = {}
        for label, global_key, local_key, limit in KINDS:
            refs = node.get(local_key if per_signature else global_key)
            refs = refs.get_object() if refs is not None else []
            if not isinstance(refs, list) or len(refs) > limit:
                raise ValueError('Lista DSS/VRI inválida ou acima do limite.')
            values = []
            for ref in refs:
                stream = ref.get_object()
                cache_key = (label, id(stream))
                if cache_key not in cache:
                    data = stream.get_data()
                    total += len(data)
                    if not data or len(data) > MAX_ITEM or total > MAX_TOTAL:
                        raise ValueError('Material DSS/VRI acima do limite.')
                    validators[label](data)
                    cache[cache_key] = data
                data = cache[cache_key]
                if data not in values:
                    values.append(data)
            result[label] = values
        result['ocsp_responses'] = len(result['ocsps'])
        return result
    result = read(root)
    raw_vri = root.get('/VRI')
    raw_vri = raw_vri.get_object() if raw_vri is not None else {}
    if not isinstance(raw_vri, dict) or len(raw_vri) > 256:
        raise ValueError('Índice VRI inválido ou acima de 256 assinaturas.')
    entries = {}
    for key, ref in raw_vri.items():
        if not re.fullmatch('/[0-9A-F]{40}', str(key)):
            raise ValueError('Chave VRI deve conter SHA-1 hexadecimal maiúsculo.')
        entry = ref.get_object()
        if not isinstance(entry, dict):
            raise ValueError('Entrada VRI inválida.')
        entries[str(key)[1:]] = read(entry, per_signature=True)
    result.update(vri_entries=len(entries), _vri=entries)
    return result


def for_signature(dss, contents):
    key = hashlib.sha1(contents).hexdigest().upper()
    entry = dss.get('_vri', {}).get(key) if dss else None
    # A matching VRI is authoritative for the selected signature. Do not add
    # another VRI's material or silently fill holes from a global mixed pool.
    selected = entry if entry is not None else dss
    counts = {label:len(selected.get(label, [])) if selected else 0 for label, *_ in KINDS}
    report = dict(key=key, matched=entry is not None,
                  scope='matching_vri' if entry is not None else 'global_fallback' if dss else 'absent',
                  **counts, certificates_present=counts['certificates'] > 0,
                  revocation_material_present=counts['crls'] + counts['ocsps'] > 0,
                  validation_material_complete=None)
    return selected, report
