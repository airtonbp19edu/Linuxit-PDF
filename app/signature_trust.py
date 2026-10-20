"""Offline CMS chain/CRL and RFC3161 checks against explicitly selected anchors.

This is a technical policy (purpose=any plus digitalSignature key usage), not
PAdES-LTV, an identity registry, or a legal validity decision. No URLs fetched.
"""
from datetime import datetime,timezone
import hashlib,os,shutil,subprocess,tempfile
from pathlib import Path
from platform_runtime import subprocess_options


def trust_policy(request):
    if not isinstance(request,dict) or set(request)!={'roots','crls','require_revocation','at_time'}:
        raise ValueError('Política de confiança inválida.')
    if type(request['require_revocation']) is not bool:raise ValueError('Opção de revogação inválida.')
    for key in ('roots','crls'):
        values=request[key]
        if not isinstance(values,list) or not (1 if key=='roots' else 0)<=len(values)<=16 or not all(isinstance(v,str) and len(v)<=4096 for v in values):
            raise ValueError('Escolha1–16 arquivos de raízes e até16 arquivos CRL locais.')
    moment=datetime.now(timezone.utc) if request['at_time'] is None else datetime.fromisoformat(request['at_time'])
    if moment.utcoffset() is None:raise ValueError('A data de validação deve incluir fuso horário.')
    return dict(request,moment=moment)


def _read(path):
    with Path(path).open('rb') as stream:raw=stream.read(1024**2+1)
    if not raw or len(raw)>1024**2:raise ValueError('Certificado/CRL vazio ou acima de1MiB.')
    return raw


def _run(command):
    result=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                          timeout=30,**subprocess_options())
    return result.returncode==0


def verify_trust(cms,content,policy):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization
    from asn1crypto import cms as asn_cms,tsp
    executable=shutil.which('openssl')
    if not executable:raise RuntimeError('OpenSSL indisponível para política offline.')
    policy=trust_policy(policy)
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
        folder=Path(directory);ca=folder/'ca.pem';ca.write_bytes(b'\n'.join(bundle))
        signature=folder/'cms.der';signature.write_bytes(cms);data=folder/'data.bin';data.write_bytes(content)
        chain=folder/'included.pem';chain.write_bytes(b''.join(x509.load_der_x509_certificate(c.dump()).public_bytes(serialization.Encoding.PEM) for c in certs))
        empty_store=folder/'empty-ca-store';empty_store.mkdir()
        # The ts command always loads a config, including for verification.
        # Use an own empty policy file rather than assuming /etc/ssl is mounted.
        configuration=folder/'openssl.cnf';configuration.write_text('[default]\n')
        options=['-CAfile',str(ca),'-no-CApath','-no-CAstore','-attime',str(int(policy['moment'].timestamp()))]
        base=[executable,'cms','-verify','-binary','-inform','DER','-in',str(signature),'-content',str(data),'-purpose','any',*options,'-out',os.devnull]
        result['chain_verified']=usage_ok and _run(base)
        if result['chain_verified'] and policy['crls']:result['revocation_verified']=_run([*base,'-crl_check_all'])
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
                    if certs:args+=['-untrusted',str(chain)]
                    if policy['require_revocation']:args+=['-crl_check_all']
                    verified=_run(args)
                    timestamp=token['content']['encap_content_info']['content'].parsed['gen_time'].native
                    result['timestamps'].append(dict(verified=verified,time=timestamp.isoformat() if verified else None))
        result['policy_satisfied']=result['chain_verified'] and (result['revocation_verified'] or not policy['require_revocation'])
    return result
