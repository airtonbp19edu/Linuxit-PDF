"""E08: later signatures are incremental revisions; earlier ones keep covering their own bytes."""
import hashlib,shutil,subprocess,tempfile,unittest
from pathlib import Path

from test_attachment_search import text_pdf
from test_pdf_signatures import signing_identity
from pypdf import PdfReader,PdfWriter
from pypdf.generic import ArrayObject,DictionaryObject,NameObject,NumberObject
from cryptography.hazmat.primitives import serialization
from pdf_signing import sign_pdf_copy
from pdf_signatures import inspect_pdf_signatures


class IncrementalSignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.identity=signing_identity()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        key,cert=self.identity
        self.key=self.root/'key.pem';self.cert=self.root/'cert.pem'
        self.key.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
        self.cert.write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    def sign(self,source,name):
        target=self.root/name
        return target,sign_pdf_copy(source,dict(destination=str(target),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                                certificate=str(self.cert),private_key=str(self.key),password=''))

    def statuses(self,path):
        return [(r['field'],r['status'],r['current_file_covered']) for r in inspect_pdf_signatures(path,{})['signatures']]

    def test_three_signatures_each_cover_their_revision(self):
        source=self.root/'source.pdf';source.write_bytes(text_pdf(['alpha']))
        first,_=self.sign(source,'1.pdf');second,_=self.sign(first,'2.pdf');third,result=self.sign(second,'3.pdf')
        self.assertTrue(first.read_bytes().startswith(source.read_bytes()))
        self.assertTrue(third.read_bytes().startswith(second.read_bytes()))
        self.assertEqual(result['previous_signatures'],['LinuxitSignature','LinuxitSignature2'])
        self.assertEqual(self.statuses(third),[('LinuxitSignature','verified',False),('LinuxitSignature2','verified',False),
                                               ('LinuxitSignature3','verified',True)])
        PdfReader(third,strict=True)
        if shutil.which('pdfsig'):
            report=subprocess.run(['pdfsig',str(third)],capture_output=True,text=True,timeout=60).stdout
            self.assertEqual(report.count('Signature Validation: Signature is Valid.'),3)
            self.assertEqual(report.count('Total document signed'),1)

    def test_cross_reference_stream_source_gets_a_stream_update(self):
        plain=self.root/'plain.pdf';plain.write_bytes(text_pdf(['beta']))
        # pypdf's incremental writer ends the file with a cross-reference stream: a portable fixture.
        writer=PdfWriter(PdfReader(plain),incremental=True);writer.add_metadata({'/Title':'xref stream'})
        source=self.root/'xrefstream.pdf'
        with open(source,'wb') as handle:writer.write(handle)
        self.assertIn(b'/Type /XRef',source.read_bytes()[len(plain.read_bytes()):])
        first,_=self.sign(source,'1.pdf');second,_=self.sign(first,'2.pdf')
        tail=second.read_bytes()[len(first.read_bytes()):]
        self.assertIn(b'/Type /XRef',tail);self.assertNotIn(b'\nxref\n',tail)
        self.assertEqual([s for _,s,_ in self.statuses(second)],['verified','verified'])
        PdfReader(second,strict=True)
        # Independent parsers: Poppler (present wherever the suite runs with poppler-utils) and qpdf (CI installs it).
        if shutil.which('pdfsig'):
            report=subprocess.run(['pdfsig',str(second)],capture_output=True,text=True,timeout=60).stdout
            self.assertEqual(report.count('Signature Validation: Signature is Valid.'),2,report)
            self.assertEqual(report.count('Total document signed'),1,report)
        if shutil.which('qpdf'):
            result=subprocess.run(['qpdf','--check',str(second)],capture_output=True,text=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def with_perms(self,level=None,usage_rights=False):
        writer=PdfWriter();writer.add_blank_page(200,200)
        perms=DictionaryObject()
        if level is not None:
            reference=DictionaryObject({NameObject('/TransformMethod'):NameObject('/DocMDP'),
                NameObject('/TransformParams'):DictionaryObject({NameObject('/P'):NumberObject(level)})})
            perms[NameObject('/DocMDP')]=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Sig'),NameObject('/Reference'):ArrayObject([reference])}))
        if usage_rights:perms[NameObject('/UR3')]=writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Sig')}))
        writer.root_object[NameObject('/Perms')]=perms
        path=self.root/f'perms-{level}-{usage_rights}.pdf'
        with open(path,'wb') as handle:writer.write(handle)
        return path

    def test_certification_without_changes_usage_rights_and_broken_previous_signature_are_refused(self):
        for source,message in ((self.with_perms(1),'DocMDP P=1'),(self.with_perms(usage_rights=True),'UR3')):
            with self.subTest(message=message),self.assertRaisesRegex(ValueError,message):self.sign(source,'out.pdf')
        self.sign(self.with_perms(2),'p2.pdf')  # DocMDP P=2 allows signing
        source=self.root/'source.pdf';source.write_bytes(text_pdf(['gamma']))
        first,_=self.sign(source,'first.pdf')
        broken=self.root/'broken.pdf';broken.write_bytes(first.read_bytes().replace(b'gamma',b'GAMMA',1))
        with self.assertRaisesRegex(ValueError,'não verificada'):self.sign(broken,'second.pdf')
        self.assertFalse((self.root/'second.pdf').exists());self.assertFalse((self.root/'out.pdf').exists())


if __name__=='__main__':unittest.main()
