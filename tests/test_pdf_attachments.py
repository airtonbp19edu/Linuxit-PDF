"""Portable tests of the independent attachment contract, with real synthetic PDFs."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, PropertyMock

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))
sys.path.insert(0, str(APP))
import pdf_attachments as attachments
from pypdf import PdfWriter
from pypdf.errors import PdfReadError
from pypdf.generic import ArrayObject, DictionaryObject, EmbeddedFile, NameObject, NumberObject


class AttachmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-attachments-')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.pdf = self.root / 'source.pdf'
        self.output = self.root / 'output'
        self.output.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def make_pdf(self, items=(), *, encrypted=False, portfolio=False, kids=False, declared=None):
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        for name, content in items:
            embedded = writer.add_attachment(name, content)
            if declared is not None:
                embedded.size = NumberObject(declared)
        if encrypted:
            writer.encrypt('synthetic-password')
        if portfolio:
            writer.root_object[NameObject('/Collection')] = DictionaryObject()
        if kids:
            tree = writer.root_object['/Names']['/EmbeddedFiles']
            tree[NameObject('/Kids')] = ArrayObject()
        writer.write(self.pdf)

    def extract(self, index=0):
        listing = attachments.list_attachments(self.pdf)
        return attachments.extract_attachment(self.pdf, index, self.output,
                                              source_sha256=listing['source_sha256'])

    def test_listing_keeps_duplicate_entries_and_does_not_decode_payloads(self):
        self.make_pdf([('same.txt', b'first'), ('same.txt', b'second')])
        with patch.object(EmbeddedFile, 'content', new_callable=PropertyMock,
                          side_effect=AssertionError('Listing decoded a payload')):
            listing = attachments.list_attachments(self.pdf)
        self.assertEqual([(e['index'], e['name']) for e in listing['attachments']],
                         [(0, 'same.txt'), (1, 'same.txt')])
        self.assertTrue(all(e['declared_size_bytes'] is None for e in listing['attachments']))
        self.assertEqual(list(self.output.iterdir()), [])

    def test_empty_catalog_returns_an_empty_list(self):
        self.make_pdf()
        self.assertEqual(attachments.list_attachments(self.pdf)['attachments'], [])

    def test_extract_preserves_binary_content_hash_and_original(self):
        payload = b'\x00\xff\x80attachment\r\n'
        self.make_pdf([('ação.bin', payload)], declared=len(payload))
        original = self.pdf.read_bytes()
        result = self.extract()
        self.assertEqual((self.output / 'ação.bin').read_bytes(), payload)
        self.assertEqual(result['size_bytes'], len(payload))
        self.assertEqual(result['sha256'], hashlib.sha256(payload).hexdigest())
        self.assertEqual(self.pdf.read_bytes(), original)

    def test_duplicate_names_are_selected_by_index_and_never_overwrite(self):
        self.make_pdf([('same.txt', b'first'), ('same.txt', b'second')])
        self.extract(1)
        self.assertEqual((self.output / 'same.txt').read_bytes(), b'second')
        with self.assertRaises(FileExistsError):
            self.extract(0)
        self.assertEqual((self.output / 'same.txt').read_bytes(), b'second')

    def test_unsafe_pdf_names_are_reported_and_refused_without_writes(self):
        names = ['../outside.txt', r'..\outside.txt', '/tmp/out.txt', r'C:\out.txt',
                 'stream:ads', 'name.', 'name ', ' CON', 'CON.txt', 'LPT1',
                 'CONOUT$', 'a\x00b', 'a\u202eb', 'é' * 121, '..', '']
        for name in names:
            with self.subTest(name=repr(name)):
                self.make_pdf([(name, b'payload')])
                listing = attachments.list_attachments(self.pdf)
                self.assertFalse(listing['attachments'][0]['filename_allowed'])
                with self.assertRaises(ValueError):
                    attachments.extract_attachment(self.pdf, 0, self.output,
                                                    source_sha256=listing['source_sha256'])
                self.assertEqual(list(self.output.iterdir()), [])
                self.assertFalse((self.root / 'outside.txt').exists())

    def test_existing_destination_is_not_replaced(self):
        self.make_pdf([('existing.txt', b'new')])
        target = self.output / 'existing.txt'
        target.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):
            self.extract()
        self.assertEqual(target.read_bytes(), b'keep')

    def test_source_changed_during_decode_leaves_no_output(self):
        self.make_pdf([('note.txt', b'content')])
        identity = attachments.list_attachments(self.pdf)['source_sha256']
        original_content = EmbeddedFile.content.fget
        def changed(entry):
            value = original_content(entry)
            with self.pdf.open('ab') as stream:
                stream.write(b'\n%changed-during-decode\n')
            return value
        with patch.object(EmbeddedFile, 'content', property(changed)):
            with self.assertRaisesRegex(ValueError, 'alterado'):
                attachments.extract_attachment(self.pdf, 0, self.output, source_sha256=identity)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_invalid_pdf_is_not_reported_as_an_empty_inventory(self):
        self.pdf.write_bytes(b'not a PDF')
        with self.assertRaises(PdfReadError):
            attachments.list_attachments(self.pdf)

    def test_source_hash_prevents_extracting_from_a_changed_pdf(self):
        self.make_pdf([('note.txt', b'old')])
        previous = attachments.list_attachments(self.pdf)['source_sha256']
        self.make_pdf([('note.txt', b'new')])
        with self.assertRaisesRegex(ValueError, 'mudou'):
            attachments.extract_attachment(self.pdf, 0, self.output, source_sha256=previous)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_invalid_index_hash_and_destination_are_refused(self):
        self.make_pdf([('note.txt', b'data')])
        identity = attachments.list_attachments(self.pdf)['source_sha256']
        for index in (-1, True, 1.0, '0', attachments.MAX_ATTACHMENTS, 8):
            with self.subTest(index=index), self.assertRaises(ValueError):
                attachments.extract_attachment(self.pdf, index, self.output, source_sha256=identity)
        for identity in (None, '', 'xyz', '0' * 63):
            with self.subTest(hash=identity), self.assertRaises(ValueError):
                attachments.extract_attachment(self.pdf, 0, self.output, source_sha256=identity)
        with self.assertRaises(FileNotFoundError):
            attachments.extract_attachment(self.pdf, 0, self.root / 'absent',
                                            source_sha256=attachments.list_attachments(self.pdf)['source_sha256'])

    def test_declared_and_actual_size_limits_are_checked(self):
        self.make_pdf([('note.txt', b'short')], declared=attachments.MAX_ATTACHMENT_BYTES + 1)
        with patch.object(EmbeddedFile, 'content', new_callable=PropertyMock,
                          side_effect=AssertionError('Oversized declared payload decoded')):
            with self.assertRaisesRegex(ValueError, 'declarado'):
                self.extract()
        self.make_pdf([('note.txt', b'123456')], declared=1)
        with patch.object(attachments, 'MAX_ATTACHMENT_BYTES', 5):
            with self.assertRaisesRegex(ValueError, 'conteúdo'):
                self.extract()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_attachment_count_limit_is_not_silent_truncation(self):
        self.make_pdf([('a.txt', b'a'), ('b.txt', b'b')])
        with patch.object(attachments, 'MAX_ATTACHMENTS', 1):
            with self.assertRaisesRegex(ValueError, 'limite'):
                attachments.list_attachments(self.pdf)

    def test_password_and_portfolio_are_explicitly_unsupported(self):
        self.make_pdf([('note.txt', b'data')], encrypted=True)
        with self.assertRaisesRegex(ValueError, 'senha'):
            attachments.list_attachments(self.pdf)
        for option in ('portfolio',):
            with self.subTest(option=option):
                self.make_pdf([('note.txt', b'data')], **{option: True})
                # Historical ID retained: valid collections now expose embedded files.
                listing=attachments.list_attachments(self.pdf)
                self.assertTrue(listing['portfolio']);self.assertEqual(len(listing['attachments']),1)

    def test_worker_protocol_lists_extracts_and_reports_conflict(self):
        self.make_pdf([('note.txt', b'worker bytes')])
        command = [sys.executable, str(APP / 'worker_cli.py')]
        proc = subprocess.run([*command, 'attachments', str(self.pdf)], capture_output=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        listing = json.loads(proc.stdout)
        request = json.dumps({'index': 0, 'source_sha256': listing['source_sha256']}).encode()
        proc = subprocess.run([*command, 'extract-attachment', str(self.pdf), str(self.output)],
                              input=request, capture_output=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['sha256'], hashlib.sha256(b'worker bytes').hexdigest())
        self.assertEqual((self.output / 'note.txt').read_bytes(), b'worker bytes')
        conflict = subprocess.run([*command, 'extract-attachment', str(self.pdf), str(self.output)],
                                  input=request, capture_output=True, timeout=60)
        self.assertNotEqual(conflict.returncode, 0)
        self.assertEqual((self.output / 'note.txt').read_bytes(), b'worker bytes')


if __name__ == '__main__':
    unittest.main()
