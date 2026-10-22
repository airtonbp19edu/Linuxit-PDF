"""Offline CMS chain/CRL/OCSP and RFC3161 checks against explicitly selected anchors.

This is a technical policy (purpose=any plus digitalSignature key usage), not
PAdES-LTV, an identity registry, or a legal validity decision. No URLs fetched.
"""
from datetime import datetime,timezone
import hashlib,os,shutil,subprocess,tempfile
from pathlib import Path
from platform_runtime import subprocess_options


def trust_policy(request):
    required={'roots','crls','require_revocation','at_time'}
    if not isinstance(request,dict) or set(request) not in (required,required|{'ocsps'}):
        raise ValueError('Política de confiança inválida.')
    if type(request['require_revocation']) is not bool:raise ValueError('Opção de revogação inválida.')
    for key in ('roots','crls'):
        values=request[key]
        if not isinstance(values,list) or not (1 if key=='roots' else 0)<=len(values)<=16 or not all(isinstance(v,str) and len(v)<=4096 for v in values):
            raise ValueError('Escolha1–16 arquivos de raízes e até16 arquivos CRL locais.')
    if 'ocsps' in request:
        values=request['ocsps']
        if not isinstance(values,list) or len(values)>32 or not all(isinstance(v,str) and 0<len(v)<=4096 for v in values):
            raise ValueError('Escolha até32 respostas OCSP locais.')
    moment=datetime.now(timezone.utc) if request['at_time'] is None else datetime.fromisoformat(request['at_time'])
    if moment.utcoffset() is None:raise ValueError('A data de validação deve incluir fuso horário.')
    return dict(request,moment=moment)


def _ocsp_assessment(signers,certs,policy,dss):
    """Assess local OCSP on actual signer chains, without promoting DSS roots."""
    from cryptography import x509
    from signature_ocsp import verify_ocsp_chain
    anchors=[]
    for name in policy['roots']:anchors.extend(x509.load_pem_x509_certificates(_read(name)))
    helpers=[x509.load_der_x509_certificate(c.dump()) for c in certs]
    helpers.extend(x509.load_der_x509_certificate(raw) for raw in (dss or {}).get('certificates',[]))
    selected=[]
    for signer in signers:
        sid=signer['sid'];matching=[]
        for cert in certs:
            if sid.name=='issuer_and_serial_number':
                value=sid.chosen
                same=cert.serial_number==value['serial_number'].native and cert.issuer.dump()==value['issuer'].dump()
            else:same=cert.key_identifier==sid.native
            if same:matching.append(cert)
        if len(matching)==1:selected.append(x509.load_der_x509_certificate(matching[0].dump()))
    responses=[_read(name) for name in policy.get('ocsps',[])]+(dss or {}).get('ocsps',[])
    if len(responses)>64:raise ValueError('OCSP combinado acima de64 respostas.')
    return verify_ocsp_chain(selected,helpers,anchors,responses,policy['moment'])


def _read(path):
    with Path(path).open('rb') as stream:raw=stream.read(1024**2+1)
    if not raw or len(raw)>1024**2:raise ValueError('Certificado/CRL vazio ou acima de1MiB.')
    return raw


def _run(command):
    result=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                          timeout=30,**subprocess_options())
    return result.returncode==0


def _anchors(policy):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    bundle=[];identities=[]
    for name in policy['roots']:
        raw=_read(name)
        certificates=x509.load_pem_x509_certificates(raw)
        if not certificates or len(certificates)>32:raise ValueError('Arquivo de raízes sem certificados PEM ou acima de32 certificados.')
        for cert in certificates:
            try:ca=cert.extensions.get_extension_for_class(x509.BasicConstraints).value.ca
            except x509.ExtensionNotFound:ca=False
            if not ca:raise ValueError('Uma âncora selecionada não declara certificado de CA.')
            bundle.append(cert.public_bytes(serialization.Encoding.PEM))
        identities.append(hashlib.sha256(raw).hexdigest())
    for name in policy['crls']:
        raw=_read(name)
        crl=x509.load_pem_x509_crl(raw) if b'-----BEGIN' in raw else x509.load_der_x509_crl(raw)
        bundle.append(crl.public_bytes(serialization.Encoding.PEM));identities.append(hashlib.sha256(raw).hexdigest())
    return bundle,identities


def _dss_files(folder,dss):
    """Write DSS material (E10): certificates only as untrusted helpers, CRLs as revocation data."""
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    dss=dss or {'certificates':[],'crls':[]}
    certs=[x509.load_der_x509_certificate(raw).public_bytes(serialization.Encoding.PEM) for raw in dss['certificates']]
    crls=[x509.load_der_x509_crl(raw).public_bytes(serialization.Encoding.PEM) for raw in dss['crls']]
    path=Path(folder)/'dss-untrusted.pem';path.write_bytes(b''.join(certs))
    return (path if certs else None),crls,dict(certificates=len(certs),crls=len(crls))


def verify_trust(cms,content,policy,dss=None):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    from asn1crypto import cms as asn_cms,tsp
    executable=shutil.which('openssl')
    if not executable:raise RuntimeError('OpenSSL indisponível para política offline.')
    policy=trust_policy(policy)
    bundle,identities=_anchors(policy)
    structure=asn_cms.ContentInfo.load(cms,strict=True)
    signed=structure['content'];signers=signed['signer_infos']
    if not 1<=len(signers)<=8:raise ValueError('CMS limitado a1–8 signatários.')
    certs=[]
    for entry in signed['certificates']:
        if entry.name=='certificate':certs.append(entry.chosen)
    if len(certs)>64:raise ValueError('CMS acima de64 certificados.')
    # CMS verifies cryptography and its matching signer certificate independently.
    # Enforce the signing key usage on the actual SID, not every included cert.
    usage_ok=True
    for signer in signers:
        sid=signer['sid'];matching=[]
        for certificate in certs:
            if sid.name=='issuer_and_serial_number':
                item=sid.chosen
                same=certificate.serial_number==item['serial_number'].native and certificate.issuer.dump()==item['issuer'].dump()
            else:same=certificate.key_identifier==sid.native
            if same:matching.append(certificate)
        if len(matching)!=1:usage_ok=False;continue
        cert=x509.load_der_x509_certificate(matching[0].dump())
        try:usage=cert.extensions.get_extension_for_class(x509.KeyUsage).value;usage_ok=usage_ok and (usage.digital_signature or usage.content_commitment)
        except x509.ExtensionNotFound:pass
    result=dict(chain_verified=False,revocation_verified=False,revocation_required=policy['require_revocation'],
                validation_time=policy['moment'].isoformat(),selected_material_sha256=identities,timestamps=[],network_used=False,
                policy='OpenSSL explicit CA, purpose any, signing key usage; no legal/LTV decision')
    with tempfile.TemporaryDirectory(prefix='linuxit-trust-') as directory:
        folder=Path(directory)
        dss_certs,dss_crls,result['dss_used']=_dss_files(folder,dss)
        ca=folder/'ca.pem';ca.write_bytes(b'\n'.join(bundle+dss_crls))
        # `openssl cms -verify` builds the chain only from the SignedData certificates and the
        # store, so DSS certificates join the (unsigned) certificate set of a verification copy:
        # they help to build a path but never become anchors.
        verified_cms=cms
        if dss and dss['certificates']:
            from asn1crypto import x509 as asn_x509
            augmented=asn_cms.ContentInfo.load(cms,strict=True)
            present={c.dump() for c in certs}
            extra=[asn_cms.CertificateChoices({'certificate':asn_x509.Certificate.load(raw)}) for raw in dss['certificates'] if raw not in present]
            augmented['content']['certificates']=asn_cms.CertificateSet(list(augmented['content']['certificates'])+extra)
            verified_cms=augmented.dump()
        signature=folder/'cms.der';signature.write_bytes(verified_cms);data=folder/'data.bin';data.write_bytes(content)
        chain=folder/'included.pem';chain.write_bytes(b''.join(x509.load_der_x509_certificate(c.dump()).public_bytes(serialization.Encoding.PEM) for c in certs)
                                                       +(dss_certs.read_bytes() if dss_certs else b''))
        empty_store=folder/'empty-ca-store';empty_store.mkdir()
        # The ts command always loads a config, including for verification.
        # Use an own empty policy file rather than assuming /etc/ssl is mounted.
        configuration=folder/'openssl.cnf';configuration.write_text('[default]\n')
        options=['-CAfile',str(ca),'-no-CApath','-no-CAstore','-attime',str(int(policy['moment'].timestamp()))]
        base=[executable,'cms','-verify','-binary','-inform','DER','-in',str(signature),'-content',str(data),'-purpose','any',*options,'-out',os.devnull]
        result['chain_verified']=usage_ok and _run(base)
        if result['chain_verified'] and (policy['crls'] or dss_crls):result['revocation_verified']=_run([*base,'-crl_check_all'])
        result['ocsp']=_ocsp_assessment(signers,certs,policy,dss)
        if result['chain_verified'] and result['ocsp']['verified']:result['revocation_verified']=True
        if result['ocsp']['revoked']:result['revocation_verified']=False
        for signer in signers:
            signature_value=signer['signature'].native
            for attribute in signer['unsigned_attrs']:
                if attribute['type'].native!='signature_time_stamp_token':continue
                for token in attribute['values']:
                    if len(result['timestamps'])>=8:raise ValueError('CMS acima de8 carimbos de tempo.')
                    encoded=token.dump();token_path=folder/'timestamp.der';token_path.write_bytes(encoded)
                    value_path=folder/'signature-value.bin';value_path.write_bytes(signature_value)
                    # ts lacks cms' -no-CApath/-no-CAstore switches. An explicit
                    # empty CApath and a CAstore naming the caller's own anchors
                    # suppress platform anchors. OpenSSL 3.0 refuses an empty
                    # directory as a store URI, so the store is the anchor file.
                    ts_options=['-CAfile',str(ca),'-CApath',str(empty_store),'-CAstore',str(ca),'-attime',str(int(policy['moment'].timestamp()))]
                    args=[executable,'ts','-config',str(configuration),'-verify','-token_in','-in',str(token_path),'-data',str(value_path),*ts_options]
                    if certs or dss_certs:args+=['-untrusted',str(chain)]
                    if policy['require_revocation']:args+=['-crl_check_all']
                    verified=_run(args)
                    timestamp=token['content']['encap_content_info']['content'].parsed['gen_time'].native
                    result['timestamps'].append(dict(verified=verified,time=timestamp.isoformat() if verified else None))
        result['policy_satisfied']=result['chain_verified'] and not result['ocsp']['revoked'] and (result['revocation_verified'] or not policy['require_revocation'])
    return result


def verify_document_timestamp(token,content,policy,dss=None):
    """RFC 3161 document timestamp (ETSI.RFC3161) against the caller's anchors only (E09)."""
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    from asn1crypto import cms as asn_cms
    executable=shutil.which('openssl')
    if not executable:raise RuntimeError('OpenSSL indisponível para política offline.')
    policy=trust_policy(policy)
    bundle,identities=_anchors(policy)
    structure=asn_cms.ContentInfo.load(token,strict=True)
    certs=[entry.chosen for entry in structure['content']['certificates'] if entry.name=='certificate']
    if len(certs)>64:raise ValueError('Carimbo acima de64 certificados.')
    result=dict(chain_verified=False,revocation_verified=False,revocation_required=policy['require_revocation'],
                validation_time=policy['moment'].isoformat(),selected_material_sha256=identities,timestamps=[],network_used=False,
                policy='OpenSSL ts -verify with explicit CA only; document timestamp, no legal/LTV decision')
    with tempfile.TemporaryDirectory(prefix='linuxit-doc-ts-') as directory:
        folder=Path(directory)
        dss_certs,dss_crls,result['dss_used']=_dss_files(folder,dss)
        ca=folder/'ca.pem';ca.write_bytes(b'\n'.join(bundle+dss_crls))
        empty_store=folder/'empty-ca-store';empty_store.mkdir()
        configuration=folder/'openssl.cnf';configuration.write_text('[default]\n')
        token_path=folder/'token.der';token_path.write_bytes(token);data=folder/'data.bin';data.write_bytes(content)
        chain=folder/'included.pem'
        chain.write_bytes(b''.join(x509.load_der_x509_certificate(c.dump()).public_bytes(serialization.Encoding.PEM) for c in certs)
                          +(dss_certs.read_bytes() if dss_certs else b''))
        args=[executable,'ts','-config',str(configuration),'-verify','-token_in','-in',str(token_path),'-data',str(data),
              '-CAfile',str(ca),'-CApath',str(empty_store),'-CAstore',str(ca),'-attime',str(int(policy['moment'].timestamp()))]
        if certs or dss_certs:args+=['-untrusted',str(chain)]
        result['chain_verified']=_run(args)
        if result['chain_verified'] and (policy['crls'] or dss_crls):result['revocation_verified']=_run([*args,'-crl_check_all'])
        result['ocsp']=_ocsp_assessment(structure['content']['signer_infos'],certs,policy,dss)
        if result['chain_verified'] and result['ocsp']['verified']:result['revocation_verified']=True
        if result['ocsp']['revoked']:result['revocation_verified']=False
        result['policy_satisfied']=result['chain_verified'] and not result['ocsp']['revoked'] and (result['revocation_verified'] or not policy['require_revocation'])
    return result
