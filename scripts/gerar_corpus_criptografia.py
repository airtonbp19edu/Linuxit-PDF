#!/usr/bin/env python3
"""Build the own encryption corpus (E18): one synthetic document in each Standard-handler profile.

Profiles: RC4 40-bit (R2), RC4 128-bit (R3), AES-128 (R4), AES-256 (R6) and AES-128 with
/EncryptMetadata false (XMP stream left in clear). Same two pages, Info title and XMP in
every file; synthetic passwords only. Permissions: printing allowed (low quality only),
copying and modifying denied, annotations and form filling allowed. `--check`
regenerates and compares (pypdf output is deterministic for fixed /ID and keys? no: AES
uses random IVs), so the check compares decrypted content and the encryption dictionary.
"""
import argparse, hashlib, json, sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from pdf_dependency import configure_pdf_library  # noqa: E402
configure_pdf_library()
from pypdf import PdfReader, PdfWriter  # noqa: E402
from pypdf.constants import UserAccessPermissions as P  # noqa: E402
from pypdf.generic import (ByteStringObject, BooleanObject, DecodedStreamObject, DictionaryObject,  # noqa: E402
                           NameObject, TextStringObject)

FOLDER = ROOT / 'testes/fixtures/criptografia'
USER, OWNER = 'usuario-teste', 'dono-teste'
XMP = ('<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/">'
       '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description xmlns:dc="http://purl.org/dc/elements/1.1/">'
       '<dc:title><rdf:Alt><rdf:li xml:lang="x-default">Titulo XMP Linuxit</rdf:li></rdf:Alt></dc:title>'
       '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="r"?>').encode()
FLAGS = P.from_dict({'print': True, 'print_to_representation': False, 'extract': False, 'modify': False,
                     'add_or_modify': True, 'fill_form_fields': True, 'extract_text_and_graphics': True, 'assemble_doc': False})
PROFILES = [('rc4-40.pdf', 'RC4-40', True, 1, 2, 40), ('rc4-128.pdf', 'RC4-128', True, 2, 3, 128),
            ('aes-128.pdf', 'AES-128', True, 4, 4, 128), ('aes-256.pdf', 'AES-256', True, 5, 6, 256),
            ('aes-128-metadados-claros.pdf', 'AES-128', False, 4, 4, 128)]


def plain_writer():
    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')}))
    for text in (b'alpha first page', b'beta second page'):
        page = writer.add_blank_page(200, 200)
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject();stream.set_data(b'BT /F1 12 Tf 10 100 Td (' + text + b') Tj ET')
        page[NameObject('/Contents')] = writer._add_object(stream)
    writer.add_metadata({'/Title': 'Titulo Info Linuxit'})
    xmp = DecodedStreamObject();xmp.set_data(XMP)
    xmp.update({NameObject('/Type'): NameObject('/Metadata'), NameObject('/Subtype'): NameObject('/XML')})
    writer._root_object[NameObject('/Metadata')] = writer._add_object(xmp)
    return writer, xmp


def build(algorithm, encrypt_metadata):
    writer, xmp = plain_writer()
    writer._ID = [ByteStringObject(b'LinuxitCorpusE18'), ByteStringObject(b'LinuxitCorpusE18')]
    writer.encrypt(USER, OWNER, permissions_flag=FLAGS, algorithm=algorithm)
    if not encrypt_metadata:
        encryption = writer._encryption
        encryption.EncryptMetadata = False
        entry = encryption.write_entry(USER, OWNER)
        entry[NameObject('/EncryptMetadata')] = BooleanObject(False)
        entry.indirect_reference = writer._encrypt_entry.indirect_reference
        writer._objects[entry.indirect_reference.idnum - 1] = entry;writer._encrypt_entry = entry
        # Spec 7.6.5/7.6.6: a metadata stream left in clear names the Identity crypt filter.
        xmp[NameObject('/Filter')] = NameObject('/Crypt')
        xmp[NameObject('/DecodeParms')] = DictionaryObject({NameObject('/Name'): NameObject('/Identity')})
        original = encryption.encrypt_object
        target = xmp.indirect_reference.idnum if xmp.indirect_reference else None
        def encrypt_object(obj, idnum, generation):
            return obj if idnum == target else original(obj, idnum, generation)
        encryption.encrypt_object = encrypt_object
    output = BytesIO();writer.write(output)
    return output.getvalue()


def describe(data):
    reader = PdfReader(BytesIO(data));entry = reader.trailer['/Encrypt'].get_object()
    return dict(V=int(entry['/V']), R=int(entry['/R']), Length=int(entry.get('/Length', 40)), P=int(entry['/P']),
                EncryptMetadata=getattr(entry.get('/EncryptMetadata', True), 'value', entry.get('/EncryptMetadata', True)) is not False)


def manifest(rows):
    return {'schema': 'linuxit-encryption-corpus-v1',
            'provenance': 'Own synthetic PDFs from scripts/gerar_corpus_criptografia.py with the pinned BSD pypdf; synthetic passwords only.',
            'user_password': USER, 'owner_password': OWNER,
            'content': {'pages': 2, 'text': ['alpha first page', 'beta second page'], 'info_title': 'Titulo Info Linuxit', 'xmp_title': 'Titulo XMP Linuxit'},
            'permissions_for_user': {'copy': False, 'print': True, 'accessibility': True, 'print_high_quality': False,
                                     'modify': False, 'annotate': True, 'fill_forms': True, 'assemble': False},
            'files': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument('--check', action='store_true')
    args = parser.parse_args();rows = []
    for name, algorithm, encrypt_metadata, v, r, bits in PROFILES:
        data = (FOLDER / name).read_bytes() if args.check else build(algorithm, encrypt_metadata)
        info = describe(data)
        assert (info['V'], info['R'], info['Length'], info['EncryptMetadata']) == (v, r, bits, encrypt_metadata), (name, info)
        if not encrypt_metadata:assert XMP in data, 'XMP must stay in clear'
        else:assert XMP not in data, 'XMP must be encrypted'
        rows.append(dict(file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), algorithm=algorithm, **info))
        if not args.check:FOLDER.mkdir(parents=True, exist_ok=True);(FOLDER / name).write_bytes(data)
    expected = manifest(rows)
    if args.check:
        assert json.loads((FOLDER / 'corpus.json').read_text(encoding='utf-8')) == expected, 'manifest differs'
        print(json.dumps({'checked': len(rows)}));return
    (FOLDER / 'corpus.json').write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'written': len(rows)}))


if __name__ == '__main__':
    main()
