"""Real signature verification UI with a synthetic untrusted certificate."""
import os
import unittest
from test_security_accessibility_gtk import _UISetup, Gtk, wait_for, capture, PdfWriter
from test_pdf_signatures import signing_identity,signed_pdf


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')),'Requires GTK3 and X11')
class SignatureGTKTests(_UISetup,unittest.TestCase):
    def test_integrity_ui_reports_verification_without_certificate_trust(self):
        path=self.root/'signed.pdf';original=signed_pdf(path,signing_identity())
        self.parent._show_signatures();w=self.parent.signature_window;self.windows.append(w)
        w.path.set_text(str(path));w._verify();wait_for(lambda:not w.busy and w.result is not None)
        self.assertTrue(w.result['signatures'][0]['integrity_verified'])
        self.assertFalse(w.result['trust_chain_verified'])
        row=w.rows.get_row_at_index(0);self.assertIn('Integridade CMS verificada',row.get_child().get_text())
        self.assertIn('Confiança dos certificados não avaliada',w.status.get_text())
        capture(w,'signature-integrity');self.assertEqual(path.read_bytes(),original)

    def test_unsigned_and_encrypted_inputs_have_distinct_results(self):
        self.parent._show_signatures();w=self.parent.signature_window;self.windows.append(w)
        w._verify();wait_for(lambda:not w.busy and w.result is not None)
        self.assertEqual(w.result['signatures'],[])
        protected=self.root/'encrypted.pdf';writer=PdfWriter();writer.add_blank_page(100,100);writer.encrypt('synthetic');writer.write(protected)
        w.path.set_text(str(protected));self.assertIsNone(w.result);w._verify()
        wait_for(lambda:not w.busy and 'criptografados' in w.status.get_text());self.assertIsNone(w.result)
