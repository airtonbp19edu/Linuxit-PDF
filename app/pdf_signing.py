"""Own bounded signed PDF copies with a user-selected PEM identity.

CMS/SHA256 uses cryptography; no trust, revocation, TSA, token or service calls.
The original is never rewritten. Every signature is an incremental update
appended to the exact source bytes, so earlier signatures keep covering their
own revisions (E08); the first signature of an unsigned PDF works the same way.
Certification with DocMDP P=1 and usage-rights (UR3) documents are refused.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from io import BytesIO
from pathlib import Path
import os
import tempfile

from pdf_changes import _inherited, _sha, _require
from local_files import publish_copy
from search_tasks import run_search_worker
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, ByteStringObject, DictionaryObject, IndirectObject,
                           NameObject, NumberObject, TextStringObject)

RESERVATION = 32768
MAX_SIGNATURES = 15


class SigningRefused(ValueError):
    """A document-policy refusal whose message is safe to show (no key or password data)."""


def _policy(condition, message):
    if not condition:
        raise SigningRefused(message)


@contextmanager
def _signing_source(path, expected):
    """Checks before appending a signature revision; earlier signatures may exist."""
    raw = Path(path).read_bytes()
    identity = hashlib.sha256(raw).hexdigest()
    _policy(identity == expected, 'O PDF mudou. Leia o documento novamente.')
    reader = PdfReader(BytesIO(raw), strict=True)
    if reader.is_encrypted:
        raise SigningRefused('Assinar PDFs criptografados ainda não é suportado.')
    root = reader.root_object
    form = root.get('/AcroForm');form = form.get_object() if form is not None else None
    if form is not None and '/XFA' in form:
        raise SigningRefused('Assinar formulários XFA ainda não é suportado.')
    if '/Collection' in root:
        raise SigningRefused('Assinar portfólios ainda não é suportado.')
    perms = root.get('/Perms');perms = perms.get_object() if perms is not None else {}
    _policy(set(perms) <= {'/DocMDP'}, 'Direitos de uso (UR3) impedem uma nova assinatura nesta cópia.')
    if '/DocMDP' in perms:
        level = 2
        for reference in perms['/DocMDP'].get_object().get('/Reference', []):
            params = reference.get_object().get('/TransformParams')
            if params is not None and '/P' in params.get_object():
                level = int(params.get_object()['/P'])
        _policy(level in (2, 3), 'A assinatura de certificação deste PDF não permite novas alterações (DocMDP P=1).')
    fields = reader.get_fields() or {}
    count = sum(_inherited(f, '/FT') == '/Sig' for f in fields.values())
    _policy(count < MAX_SIGNATURES, f'Limite de {MAX_SIGNATURES} assinaturas por PDF.')
    if count:
        from pdf_signatures import inspect_pdf_signatures
        report = inspect_pdf_signatures(path, {})
        _policy(report['source_sha256'] == identity, 'O PDF mudou durante a leitura das assinaturas.')
        bad = [r['field'] for r in report['signatures'] if r['status'] not in ('verified', 'unsigned')]
        _policy(not bad, 'Assinatura existente não verificada (' + ', '.join(bad[:3]) + '); nova assinatura recusada.')
    yield reader, fields, identity


def _serialize(obj):
    stream = BytesIO();obj.write_to_stream(stream);return stream.getvalue()


def _incremental_update(original, reader, new_objects, replaced):
    """Bytes appended after `original`: objects, then a cross-reference section of the same kind.

    new_objects: {number: object}; replaced: {(number, generation): object}. The previous
    revision is never touched; /Prev points at its last cross-reference section.
    pypdf's own incremental writer was not used: across successive updates it reused
    object numbers of the previous revision (seen when adding a third signature).
    """
    tail = original[-1024:]
    _require(b'startxref' in tail, 'PDF sem startxref final; nova assinatura recusada.')
    previous = int(tail[tail.rindex(b'startxref') + 9:].split()[0])
    _require(0 < previous < len(original), 'startxref inválido; nova assinatura recusada.')
    is_stream = not original[previous:previous + 4] == b'xref'
    size = int(reader.trailer['/Size'])
    body = BytesIO();body.write(b'\n')
    offsets = {}
    entries = {(n, 0): o for n, o in new_objects.items()};entries.update(replaced)
    for (number, generation), obj in sorted(entries.items()):
        offsets[number] = (len(original) + body.tell(), generation)
        body.write(f'{number} {generation} obj\n'.encode('ascii') + _serialize(obj) + b'\nendobj\n')
    size = max([size] + [n + 1 for n in offsets])
    trailer = DictionaryObject({NameObject('/Size'): NumberObject(size), NameObject('/Prev'): NumberObject(previous)})
    for key in ('/Root', '/Info', '/ID'):
        if key in reader.trailer:trailer[NameObject(key)] = reader.trailer.raw_get(key)
    numbers = sorted(offsets)
    if is_stream:
        number = size;size += 1;trailer[NameObject('/Size')] = NumberObject(size)
        start = len(original) + body.tell();offsets[number] = (start, 0);numbers.append(number)
        data = b''.join(b'\x01' + offsets[n][0].to_bytes(4, 'big') + offsets[n][1].to_bytes(2, 'big') for n in numbers)
        trailer.update({NameObject('/Type'): NameObject('/XRef'),
                        NameObject('/W'): ArrayObject(NumberObject(v) for v in (1, 4, 2)),
                        NameObject('/Index'): ArrayObject(v for n in numbers for v in (NumberObject(n), NumberObject(1))),
                        NameObject('/Length'): NumberObject(len(data))})
        body.write(f'{number} 0 obj\n'.encode('ascii') + _serialize(trailer) + b'\nstream\n' + data + b'\nendstream\nendobj\n')
        xref = start
    else:
        xref = len(original) + body.tell()
        body.write(b'xref\n0 1\n0000000000 65535 f\r\n')
        for n in numbers:
            body.write(f'{n} 1\n{offsets[n][0]:010d} {offsets[n][1]:05d} n\r\n'.encode('ascii'))
        body.write(b'trailer\n' + _serialize(trailer) + b'\n')
    body.write(f'startxref\n{xref}\n%%EOF\n'.encode('ascii'))
    return body.getvalue()


def _field_name(fields):
    name, number = 'LinuxitSignature', 1
    while name in fields:
        number += 1;name = f'LinuxitSignature{number}'
    return name


def _bounded_read(path, maximum):
    with Path(path).open('rb') as stream:data=stream.read(maximum+1)
    _require(len(data)<=maximum,'Arquivo de identidade acima do limite.')
    return data


def _incremental_signature(original, reader, name, signature_dict):
    """Later signature: append the field, its value and the updated AcroForm to the exact bytes."""
    size=int(reader.trailer['/Size'])
    signature_ref=IndirectObject(size,0,reader);field_ref=IndirectObject(size+1,0,reader)
    field=DictionaryObject({NameObject('/FT'):NameObject('/Sig'),NameObject('/T'):TextStringObject(name),
                            NameObject('/V'):signature_ref,NameObject('/Ff'):NumberObject(1)})
    root=reader.root_object;form_ref=root.raw_get('/AcroForm') if '/AcroForm' in root else None
    form=DictionaryObject(form_ref.get_object()) if form_ref is not None else DictionaryObject()
    _require(isinstance(form,DictionaryObject),'AcroForm inválido.')
    existing=form.get('/Fields',ArrayObject());existing=existing.get_object()
    _require(isinstance(existing,ArrayObject),'Lista de campos inválida.')
    form[NameObject('/Fields')]=ArrayObject(list(existing)+[field_ref])
    form[NameObject('/SigFlags')]=NumberObject(3)
    replaced={};new={size:signature_dict,size+1:field}
    if isinstance(form_ref,IndirectObject):
        replaced[(form_ref.idnum,form_ref.generation)]=form
    else:
        # A direct or missing AcroForm becomes a new object referenced by an updated catalog.
        new[size+2]=form
        updated=DictionaryObject(root);updated[NameObject('/AcroForm')]=IndirectObject(size+2,0,reader)
        reference=reader.trailer.raw_get('/Root');replaced[(reference.idnum,reference.generation)]=updated
    return original+_incremental_update(original,reader,new,replaced)


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
    with _signing_source(path,request['source_sha256']) as (reader,fields,identity):
        _require(len(reader.pages)>0,'PDF sem páginas.')
        name=_field_name(fields)
        previous=[n for n,f in fields.items() if _inherited(f,'/FT')=='/Sig' and f.get('/V') is not None]
        placeholder=os.urandom(RESERVATION)
        signature_dict=DictionaryObject({
            NameObject('/Type'):NameObject('/Sig'),NameObject('/Filter'):NameObject('/Adobe.PPKLite'),
            NameObject('/SubFilter'):NameObject('/adbe.pkcs7.detached'),
            NameObject('/ByteRange'):ArrayObject(NumberObject(v) for v in (0,1111111111,2222222222,3333333333)),
            NameObject('/Contents'):ByteStringObject(placeholder),
            NameObject('/M'):TextStringObject(datetime.now(timezone.utc).strftime("D:%Y%m%d%H%M%S+00'00'")),
        })
        original=path.read_bytes()
        _require(hashlib.sha256(original).hexdigest()==identity,'O PDF mudou durante a assinatura.')
        raw=_incremental_signature(original,reader,name,signature_dict)
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
    _require(raw.startswith(original),'A atualização incremental alterou bytes da revisão assinada.')
    check=PdfReader(BytesIO(raw),strict=True)
    _require(name in (check.get_fields() or {}),'Campo assinado não confirmado.')
    from pdf_signatures import _verify_detached
    verified, backend=_verify_detached(cms,raw[:left]+raw[right:])
    _require(verified is True,'Verificação CMS independente indisponível ou falhou; cópia não publicada.')
    def unchanged():_require(_sha(path)==identity,'O PDF mudou durante a assinatura.')
    with tempfile.TemporaryDirectory(prefix='linuxit-signing-') as folder:
        staged=Path(folder)/'signed.pdf';staged.write_bytes(raw)
        # Every earlier signature must still verify for its own revision.
        from pdf_signatures import inspect_pdf_signatures
        report={r['field']:r for r in inspect_pdf_signatures(staged,{})['signatures']}
        _policy(all(report.get(n,{}).get('status')=='verified' and not report[n]['current_file_covered'] for n in previous),
                 'Uma assinatura anterior deixaria de ser válida; cópia não publicada.')
        _policy(report.get(name,{}).get('status')=='verified' and report[name]['current_file_covered'],
                 'A nova assinatura não cobre o arquivo inteiro; cópia não publicada.')
        publish_copy(staged,destination,unchanged)
    return dict(schema='linuxit-signed-copy-v1',path=str(destination),source_sha256=identity,
                output_sha256=_sha(destination),signature_format='adbe.pkcs7.detached',
                trust_assessed=False,timestamp_added=False,field=name,incremental=True,
                previous_signatures=previous)


def invoke_sign_copy(path,request,cancel=None):
    result=run_search_worker('sign-copy',path,request,cancel)
    if result is None:return None
    if (result.get('schema')!='linuxit-signed-copy-v1' or result.get('trust_assessed') is not False
            or Path(result.get('path','')).resolve()!=Path(request['destination']).resolve()
            or result.get('source_sha256')!=request['source_sha256']):
        raise RuntimeError('Assinatura não confirmou a cópia esperada.')
    return result
