"""Own bounded first-signature PDF copies with a user-selected PEM identity.

CMS/SHA256 uses cryptography; no trust, revocation, TSA, token or service calls.
The original is never rewritten and existing signature fields are refused.
"""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import os
import tempfile

from pdf_changes import _editable, _sha, _require
from local_files import publish_copy
from search_tasks import run_search_worker
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, ByteStringObject, DictionaryObject,
                           NameObject, NumberObject, TextStringObject)

RESERVATION = 32768


def _bounded_read(path, maximum):
    with Path(path).open('rb') as stream:data=stream.read(maximum+1)
    _require(len(data)<=maximum,'Arquivo de identidade acima do limite.')
    return data


def sign_pdf_copy(path, request):
    keys={'destination','source_sha256','certificate','private_key','password'}
    _require(isinstance(request,dict) and set(request)==keys,'Pedido de assinatura inválido.')
    _require(isinstance(request['password'],str) and len(request['password'].encode('utf-8'))<=4096,'Senha da chave acima do limite.')
    path=Path(path).resolve();destination=Path(request['destination'])
    _require(path.stat().st_size<=64*1024**2,'Assinatura limitada a PDFs de até64MiB.')
    _require(not destination.exists() and not destination.is_symlink(),'Escolha um arquivo novo para a cópia assinada.')
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes,serialization
    from cryptography.hazmat.primitives.asymmetric import rsa,ec
    from cryptography.hazmat.primitives.serialization import pkcs7
    try:
        cert=x509.load_pem_x509_certificate(_bounded_read(request['certificate'],1024**2))
        key=serialization.load_pem_private_key(_bounded_read(request['private_key'],1024**2),
            password=request['password'].encode('utf-8') if request['password'] else None)
    except (ValueError,TypeError):raise ValueError('Certificado, chave PEM ou senha inválidos.') from None
    _require(isinstance(key,(rsa.RSAPrivateKey,ec.EllipticCurvePrivateKey)) and
             key.key_size>=(2048 if isinstance(key,rsa.RSAPrivateKey) else 256),'Use chave RSA de2048bits ou EC de256bits, no mínimo.')
    public=lambda k:k.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
    _require(public(key.public_key())==public(cert.public_key()),'Certificado não corresponde à chave privada.')
    with _editable(path,request['source_sha256']) as (reader,fields,identity):
        _require(len(reader.pages)>0,'PDF sem páginas.')
        _require('LinuxitSignature' not in fields,'Nome reservado de campo já existe neste PDF.')
        writer=PdfWriter(clone_from=reader)
        placeholder=os.urandom(RESERVATION)
        signature=writer._add_object(DictionaryObject({
            NameObject('/Type'):NameObject('/Sig'),NameObject('/Filter'):NameObject('/Adobe.PPKLite'),
            NameObject('/SubFilter'):NameObject('/adbe.pkcs7.detached'),
            NameObject('/ByteRange'):ArrayObject(NumberObject(v) for v in (0,1111111111,2222222222,3333333333)),
            NameObject('/Contents'):ByteStringObject(placeholder),
            NameObject('/M'):TextStringObject(datetime.now(timezone.utc).strftime("D:%Y%m%d%H%M%S+00'00'")),
        }))
        field=writer._add_object(DictionaryObject({NameObject('/FT'):NameObject('/Sig'),
            NameObject('/T'):TextStringObject('LinuxitSignature'),NameObject('/V'):signature,
            NameObject('/Ff'):NumberObject(1)}))
        form=writer.root_object.get('/AcroForm')
        if form is None:
            form=DictionaryObject({NameObject('/Fields'):ArrayObject()})
            writer.root_object[NameObject('/AcroForm')]=writer._add_object(form)
        else:form=form.get_object()
        _require(isinstance(form,DictionaryObject),'AcroForm inválido.')
        existing=form.get('/Fields',ArrayObject());existing=existing.get_object()
        _require(isinstance(existing,ArrayObject),'Lista de campos inválida.')
        existing.append(field);form[NameObject('/Fields')]=existing
        form[NameObject('/SigFlags')]=NumberObject(3)
        output=BytesIO();writer.write(output);raw=output.getvalue()
    marker=b'[ 0 1111111111 2222222222 3333333333 ]'
    contents=b'<'+placeholder.hex().encode('ascii')+b'>'
    _require(raw.count(marker)==raw.count(contents)==1,'Reserva de assinatura ambígua; cópia recusada.')
    left=raw.index(contents);right=left+len(contents)
    replacement=f'[ 0 {left:010d} {right:010d} {len(raw)-right:010d} ]'.encode('ascii')
    _require(len(replacement)==len(marker),'PDF acima do limite de offsets.')
    raw=raw.replace(marker,replacement)
    cms=(pkcs7.PKCS7SignatureBuilder().set_data(raw[:left]+raw[right:])
         .add_signer(cert,key,hashes.SHA256()).sign(serialization.Encoding.DER,
              [pkcs7.PKCS7Options.DetachedSignature,pkcs7.PKCS7Options.Binary]))
    _require(len(cms)<=RESERVATION,'CMS acima da reserva de32KiB.')
    raw=raw[:left]+b'<'+cms.hex().encode('ascii').ljust(RESERVATION*2,b'0')+b'>'+raw[right:]
    _require(len(raw)<=64*1024**2,'Cópia assinada acima de64MiB.')
    check=PdfReader(BytesIO(raw),strict=True)
    _require('LinuxitSignature' in (check.get_fields() or {}),'Campo assinado não confirmado.')
    from pdf_signatures import _verify_detached
    verified, backend=_verify_detached(cms,raw[:left]+raw[right:])
    _require(verified is True,'Verificação CMS independente indisponível ou falhou; cópia não publicada.')
    def unchanged():_require(_sha(path)==identity,'O PDF mudou durante a assinatura.')
    with tempfile.TemporaryDirectory(prefix='linuxit-signing-') as folder:
        staged=Path(folder)/'signed.pdf';staged.write_bytes(raw)
        publish_copy(staged,destination,unchanged)
    return dict(schema='linuxit-signed-copy-v1',path=str(destination),source_sha256=identity,
                output_sha256=_sha(destination),signature_format='adbe.pkcs7.detached',
                trust_assessed=False,timestamp_added=False)


def invoke_sign_copy(path,request,cancel=None):
    result=run_search_worker('sign-copy',path,request,cancel)
    if result is None:return None
    if (result.get('schema')!='linuxit-signed-copy-v1' or result.get('trust_assessed') is not False
            or Path(result.get('path','')).resolve()!=Path(request['destination']).resolve()
            or result.get('source_sha256')!=request['source_sha256']):
        raise RuntimeError('Assinatura não confirmou a cópia esperada.')
    return result
