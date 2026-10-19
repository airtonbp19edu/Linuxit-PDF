"""Real own encrypted/corrupt PDFs, private-view lifetime and secret transport."""
from io import BytesIO
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', Path(__file__).resolve().parents[1] / 'app'))
sys.path.insert(0, str(APP))
from document_session import DocumentSession, DocumentError, prepare_document
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions as Permissions
from test_attachment_search import text_pdf
from navigation import page_index, zoom_value, page_width, rotated_size


class DocumentSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-session-tests-')
        self.root = Path(self.temp.name)
        self.source = self.root / 'plain.pdf'
        self.source.write_bytes(text_pdf(['alpha first page', 'beta second page']))
        self.sessions = []

    def tearDown(self):
        for session in self.sessions:session.close()
        self.temp.cleanup()

    def session(self, source=None):
        result = DocumentSession(source or self.source)
        self.sessions.append(result)
        return result

    def encrypted(self, password='session-secret', copying=True):
        path = self.root / 'protected.pdf'
        writer = PdfWriter(clone_from=self.source)
        flags = Permissions.from_dict({'extract':copying, 'print':False, 'extract_text_and_graphics':True})
        writer.encrypt(password, 'separate-owner-secret', algorithm='AES-256', permissions_flag=flags)
        writer.write(path)
        return path

    def damaged(self):
        path = self.root / 'damaged.pdf'
        path.write_bytes(re.sub(rb'(startxref\s+)\d+', rb'\g<1>1', self.source.read_bytes()))
        return path

    def test_plain_session_preserves_original_identity_and_no_view_copy(self):
        original = self.source.read_bytes(); session = self.session()
        info = session.prepare()
        self.assertEqual((info['status'], info['pages']), ('ready', 2))
        self.assertFalse(info['recovered']); self.assertFalse(info['encrypted'])
        self.assertEqual(session.read_path, str(self.source.resolve()))
        self.assertFalse((session.root / 'view.pdf').exists())
        self.assertEqual(original, self.source.read_bytes())

    def test_password_required_then_invalid_then_correct_in_real_worker(self):
        path = self.encrypted(); original = path.read_bytes(); session = self.session(path)
        self.assertEqual(session.prepare()['status'], 'password_required')
        self.assertEqual(session.prepare('wrong')['status'], 'password_invalid')
        info = session.prepare('session-secret')
        self.assertTrue(info['encrypted']); self.assertEqual(info['pages'], 2)
        self.assertNotEqual(session.read_path, str(path))
        view = PdfReader(session.read_path)
        self.assertFalse(view.is_encrypted); self.assertIn('beta', view.pages[1].extract_text())
        self.assertTrue(PdfReader(path).is_encrypted); self.assertEqual(original, path.read_bytes())

    def test_unicode_password_and_original_permission_policy(self):
        path = self.encrypted('senha-ação-123', copying=False)
        info = self.session(path).prepare('senha-ação-123')
        self.assertEqual(info['status'], 'ready')
        self.assertFalse(info['permissions']['copy']); self.assertFalse(info['permissions']['print'])
        self.assertTrue(info['permissions']['accessibility'])

    def test_owner_password_can_read_without_rewriting_original_permissions(self):
        path = self.encrypted(copying=False); before = path.read_bytes()
        info = self.session(path).prepare('separate-owner-secret')
        self.assertTrue(all(info['permissions'].values()))
        self.assertEqual(before, path.read_bytes())

    def test_broken_xref_requires_consent_then_recovers_content(self):
        path = self.damaged(); before = path.read_bytes(); session = self.session(path)
        self.assertEqual(session.prepare()['status'], 'recovery_required')
        info = session.prepare(recover=True)
        self.assertTrue(info['recovered']); self.assertEqual(info['pages'], 2)
        self.assertIn('alpha', PdfReader(session.read_path, strict=True).pages[0].extract_text())
        self.assertEqual(before, path.read_bytes())

    def test_irrecoverable_and_empty_sources_do_not_publish_view(self):
        for content in (b'', b'%PDF-1.7\nnot a document'):
            path = self.root / 'invalid.pdf'; path.write_bytes(content)
            session = self.session(path)
            with self.assertRaises(RuntimeError):session.prepare(recover=True)
            self.assertFalse((session.root / 'view.pdf').exists())

    def test_close_waits_for_active_reader_and_removes_private_view(self):
        session = self.session(self.encrypted()); session.prepare('session-secret')
        ready, release = threading.Event(), threading.Event()
        def read():
            with session.lease() as path:
                ready.set(); release.wait(5)
                self.assertTrue(Path(path).is_file())
        worker = threading.Thread(target=read); worker.start()
        self.assertTrue(ready.wait(5)); session.close()
        self.assertTrue(session.root.exists())
        with self.assertRaises(DocumentError):
            with session.lease():pass
        release.set(); worker.join(5)
        self.assertFalse(worker.is_alive()); self.assertFalse(session.root.exists())

    def test_cancellation_before_worker_leaves_no_reading_file(self):
        session = self.session(self.encrypted()); cancelled = threading.Event(); cancelled.set()
        self.assertIsNone(session.prepare('session-secret', cancel=cancelled))
        session.close(); self.assertFalse(session.root.exists())

    def test_password_is_absent_from_argv_and_worker_errors(self):
        session = self.session(self.encrypted())
        with patch('search_tasks.subprocess.Popen', wraps=subprocess.Popen) as process:
            self.assertEqual(session.prepare('secret-not-valid')['status'], 'password_invalid')
        argv = process.call_args.args[0]
        self.assertNotIn('secret-not-valid', json.dumps(argv))
        self.assertEqual(argv[-2], 'document-open')
        self.assertFalse((session.root / 'view.pdf').exists())

    def test_private_reading_file_is_not_world_readable(self):
        session = self.session(self.encrypted()); session.prepare('session-secret')
        if os.name != 'nt':
            self.assertEqual(session.root.stat().st_mode & 0o077, 0)
            self.assertEqual(Path(session.read_path).stat().st_mode & 0o077, 0)
        self.assertNotIn('password', session.info)

    def test_invalid_request_and_existing_view_are_refused(self):
        session = self.session()
        request = {'password':'', 'recover':False, 'view_dir':str(session.root)}
        with self.assertRaises(DocumentError):prepare_document(self.source, {**request, 'extra':True})
        target = session.root / 'view.pdf'; target.write_bytes(b'preserve')
        with self.assertRaises(DocumentError):prepare_document(self.source, request)
        self.assertEqual(target.read_bytes(), b'preserve')


class NavigationDomainTests(unittest.TestCase):
    def test_page_bounds_and_rejected_nonintegers(self):
        self.assertEqual(page_index('-500', 8, True), 0)
        self.assertEqual(page_index('9999999999', 8, True), 7)
        self.assertEqual(page_index('2', 8, True), 1)
        for value in ('nan', '2.5', '1e3', '', '9' * 100):
            with self.assertRaises(ValueError):page_index(value, 8, True)

    def test_zoom_percent_decimal_and_clamped_bounds(self):
        self.assertEqual(zoom_value('37,5%'), 37.5)
        self.assertEqual(zoom_value('-10'), 1)
        self.assertEqual(zoom_value('99999'), 6400)
        for value in ('nan', 'inf', '-inf', 'x', '', '9' * 100):
            with self.assertRaises(ValueError):zoom_value(value)

    def test_rotated_fit_page_stays_in_viewport(self):
        for rotation in (0, 90, 180, 270):
            width, height = rotated_size((200, 600), rotation)
            target = page_width((200, 600), rotation, 'fit-page', 100, (800, 500))
            self.assertLessEqual(target, 800)
            self.assertLessEqual(target * height / width, 500)
        self.assertEqual(page_width((72, 144), 0, 'percent', 6400, (800, 500)), 6144)
