"""Real CMS + incremental VRI + explicit offline CA/CRL validation."""
from io import BytesIO
import hashlib
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
sys.path.insert(0,str(ROOT/'testes/aceitacao'))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, IndirectObject, NameObject
from pdf_signing import sign_pdf_copy, _incremental_update
from pdf_signatures import inspect_pdf_signatures
from test_attachment_search import text_pdf
import carimbo


@unittest.skipUnless(shutil.which('openssl'), 'Real OpenSSL offline chain/revocation backend required')
class VRIChainTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.chain=carimbo.chain_identity(self.root/'keys')
        self.source=self.root/'source.pdf';self.source.write_bytes(text_pdf(['alpha']))
        self.signed=self.root/'signed.pdf'
        sign_pdf_copy(self.source,dict(destination=str(self.signed),source_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),
            certificate=str(self.chain['certificate']),private_key=str(self.chain['key']),password=''))

    def with_vri(self, *, matching_crls=True, foreign_revoked=False, global_crls=False):
        raw=self.signed.read_bytes();reader=PdfReader(BytesIO(raw),strict=True)
        number=int(reader.trailer['/Size']);objects={}
        def stream(data):
            nonlocal number
            obj=DecodedStreamObject();obj.set_data(data);objects[number]=obj
            ref=IndirectObject(number,0,reader);number+=1;return ref
        cert=stream(self.chain['intermediate'])
        crls=[stream(self.chain['crl']('mid')),stream(self.chain['crl']('root'))]
        contents=next(f for f in reader.get_fields().values() if f.get('/FT')=='/Sig')['/V']['/Contents']
        contents=bytes(contents) if isinstance(contents,bytes) else contents.original_bytes
        self.key=hashlib.sha1(contents).hexdigest().upper()
        entry=DictionaryObject({NameObject('/Cert'):ArrayObject([cert])})
        if matching_crls:entry[NameObject('/CRL')]=ArrayObject(crls)
        vri=DictionaryObject({NameObject('/'+self.key):entry})
        if foreign_revoked:
            vri[NameObject('/'+'A'*40)]=DictionaryObject({NameObject('/Cert'):ArrayObject([cert]),
                NameObject('/CRL'):ArrayObject([stream(self.chain['crl']('mid',[3]))])})
        dss=DictionaryObject({NameObject('/VRI'):vri,NameObject('/Certs'):ArrayObject([cert])})
        if global_crls:dss[NameObject('/CRLs')]=ArrayObject(crls)
        objects[number]=dss
        root=DictionaryObject(reader.root_object);root[NameObject('/DSS')]=IndirectObject(number,0,reader)
        ref=reader.trailer.raw_get('/Root');target=self.root/'with-vri.pdf'
        target.write_bytes(raw+_incremental_update(raw,reader,objects,{(ref.idnum,ref.generation):root}))
        return target

    def inspect(self, path, policy=True):
        request={'trust_policy':dict(roots=[str(self.chain['root'])],crls=[],require_revocation=True,at_time=None)} if policy else {}
        return inspect_pdf_signatures(path,request)['signatures'][0]

    def test_matching_material_validates_real_chain_and_revocation_without_network(self):
        original=self.signed.read_bytes();record=self.inspect(self.with_vri())
        self.assertEqual(record['status'],'verified');self.assertTrue(record['integrity_verified'])
        self.assertEqual(record['vri']['key'],self.key);self.assertTrue(record['vri']['matched'])
        self.assertTrue(record['vri']['validation_material_complete'])
        self.assertTrue(record['trust']['policy_satisfied']);self.assertFalse(record['trust']['network_used'])
        self.assertEqual(original,self.signed.read_bytes())

    def test_foreign_revocation_does_not_contaminate_selected_signature(self):
        record=self.inspect(self.with_vri(foreign_revoked=True))
        self.assertTrue(record['vri']['validation_material_complete']);self.assertTrue(record['trust']['policy_satisfied'])

    def test_missing_matching_crl_is_incomplete_even_with_global_crls(self):
        record=self.inspect(self.with_vri(matching_crls=False,global_crls=True))
        self.assertTrue(record['trust']['chain_verified']);self.assertFalse(record['trust']['revocation_verified'])
        self.assertFalse(record['vri']['validation_material_complete']);self.assertFalse(record['trust']['policy_satisfied'])

    def test_der_presence_without_explicit_trust_is_not_complete_validation(self):
        record=self.inspect(self.with_vri(),policy=False)
        self.assertTrue(record['vri']['matched']);self.assertIsNone(record['vri']['validation_material_complete'])
        self.assertNotIn('trust',record)
