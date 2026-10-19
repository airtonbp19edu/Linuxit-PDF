"""Portable attachment-panel workflow tests with real workers and deferred callbacks."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))
sys.path.insert(0, str(APP))
from attachment_tasks import AttachmentPanelController, display_attachment_name, invoke_attachment_worker
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject


class DeferredRunner:
    """Deliberately deliver invalidated callbacks to test the controller's own guards."""
    def __init__(self):
        self.jobs = []
        self.invalidations = []

    def invalidate(self, channel):
        self.invalidations.append(channel)

    def submit(self, channel, task, success, error):
        self.jobs.append((channel, task, success, error))
        return object()

    def run(self, number=-1):
        _, task, success, error = self.jobs[number]
        try:
            result = task()
        except Exception as exc:
            error(exc)
        else:
            success(result)


class AttachmentWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-attachment-ui-')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.pdf = self.root / 'one.pdf'
        self.make_pdf(self.pdf)
        self.output = self.root / 'output'
        self.output.mkdir()
        self.runner = DeferredRunner()
        self.states = []
        self.model = AttachmentPanelController(self.runner, self.states.append)

    def tearDown(self):
        self.model.close()
        self.temp.cleanup()

    def make_pdf(self, path, name='note.txt', content=b'attachment bytes', portfolio=False):
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.add_attachment(name, content)
        if portfolio:
            writer.root_object[NameObject('/Collection')] = DictionaryObject()
        writer.write(path)

    def load(self):
        self.model.set_document(self.pdf)
        self.model.ensure_loaded()
        self.runner.run()

    def test_no_document_and_lazy_loading_do_not_start_workers(self):
        self.model.set_document(None)
        self.model.ensure_loaded()
        self.assertEqual(self.runner.jobs, [])
        self.assertFalse(self.states[-1]['can_extract'])
        self.model.set_document(self.pdf)
        self.assertEqual(self.runner.jobs, [])
        self.assertTrue(self.states[-1]['can_refresh'])

    def test_real_listing_populates_selection_and_repeated_show_is_cached(self):
        self.load()
        self.assertEqual(self.states[-1]['items'][0]['name'], 'note.txt')
        self.assertTrue(self.states[-1]['can_extract'])
        self.assertFalse(self.states[-1]['loading'])
        self.model.ensure_loaded()
        self.assertEqual(len(self.runner.jobs), 1)

    def test_stale_listing_callback_cannot_replace_a_new_document(self):
        self.model.set_document(self.pdf)
        self.model.ensure_loaded()
        old_data = invoke_attachment_worker('attachments', self.pdf)
        second = self.root / 'two.pdf'
        self.make_pdf(second, name='second.txt')
        self.model.set_document(second)
        self.model.ensure_loaded()
        self.runner.run(1)
        self.runner.jobs[0][2](old_data)
        self.runner.jobs[0][3](RuntimeError('old failure'))
        self.assertEqual(self.states[-1]['items'][0]['name'], 'second.txt')
        self.assertFalse(self.states[-1]['error'])

    def test_unsafe_name_cannot_be_extracted_even_if_selected(self):
        self.make_pdf(self.pdf, name='../outside.txt')
        self.load()
        self.model.select(0)
        self.assertIsNone(self.model.selection_token())
        self.assertFalse(self.states[-1]['can_extract'])
        self.assertFalse(self.model.extract(self.output, None))
        self.assertEqual(len(self.runner.jobs), 1)

    def test_refresh_invalidates_the_selection_captured_before_a_dialog(self):
        self.load()
        selection = self.model.selection_token()
        self.model.refresh()
        self.runner.run()
        self.assertFalse(self.model.extract(self.output, selection))
        self.assertEqual(list(self.output.iterdir()), [])

    def test_cancelled_selection_starts_no_extraction(self):
        self.load()
        self.assertFalse(self.model.extract(self.output, None))
        self.assertFalse(self.model.extracting)
        self.assertEqual(len(self.runner.jobs), 1)

    def test_real_worker_extracts_selected_attachment_and_restores_buttons(self):
        original = self.pdf.read_bytes()
        self.load()
        self.assertTrue(self.model.extract(self.output, self.model.selection_token()))
        self.assertTrue(self.states[-1]['extracting'])
        self.assertFalse(self.states[-1]['can_extract'])
        self.assertFalse(self.model.extract(self.output, self.model.selection_token()))
        self.runner.run()
        self.assertEqual((self.output / 'note.txt').read_bytes(), b'attachment bytes')
        self.assertEqual(self.pdf.read_bytes(), original)
        self.assertTrue(self.states[-1]['can_extract'])
        self.assertIn('Anexo salvo', self.states[-1]['message'])

    def test_conflict_is_readable_and_does_not_replace_existing_content(self):
        (self.output / 'note.txt').write_bytes(b'keep')
        self.load()
        self.model.extract(self.output, self.model.selection_token())
        self.runner.run()
        self.assertTrue(self.states[-1]['error'])
        self.assertIn('Escolha outra pasta', self.states[-1]['message'])
        self.assertNotIn('Traceback', self.states[-1]['message'])
        self.assertEqual((self.output / 'note.txt').read_bytes(), b'keep')

    def test_switching_document_keeps_authorized_job_but_not_its_old_status(self):
        self.load()
        self.model.extract(self.output, self.model.selection_token())
        second = self.root / 'two.pdf'
        self.make_pdf(second, name='second.txt')
        self.model.set_document(second)
        self.model.ensure_loaded()
        self.runner.run(2)
        message = self.states[-1]['message']
        self.assertTrue(self.states[-1]['extracting'])
        self.runner.run(1)
        self.assertEqual((self.output / 'note.txt').read_bytes(), b'attachment bytes')
        self.assertEqual(self.states[-1]['message'], message)
        self.assertEqual(self.states[-1]['items'][0]['name'], 'second.txt')
        self.assertFalse(self.states[-1]['extracting'])

    def test_close_prevents_queued_extraction_and_late_widget_notifications(self):
        self.load()
        self.model.extract(self.output, self.model.selection_token())
        count = len(self.states)
        self.model.close()
        self.runner.run()
        self.runner.jobs[0][3](RuntimeError('late failure'))
        self.assertEqual(len(self.states), count)
        self.assertEqual(list(self.output.iterdir()), [])

    def test_unsupported_pdf_is_an_error_not_an_empty_success(self):
        self.make_pdf(self.pdf, portfolio=True)
        # Malformed Collection remains an error; valid portfolios are supported.
        reader=PdfReader(self.pdf);writer=PdfWriter(clone_from=reader)
        writer.root_object[NameObject('/Collection')]=NameObject('/Invalid');writer.write(self.pdf)
        self.load()
        self.assertTrue(self.states[-1]['error'])
        self.assertIn('portfólio', self.states[-1]['message'])
        self.assertFalse(self.states[-1]['can_extract'])

    def test_worker_timeout_and_invalid_protocol_are_reported_without_tracebacks(self):
        with patch('attachment_tasks.subprocess.run', side_effect=subprocess.TimeoutExpired('worker', 600)):
            with self.assertRaisesRegex(RuntimeError, 'tempo disponível'):
                invoke_attachment_worker('attachments', self.pdf)
        with patch('attachment_tasks.subprocess.run', return_value=subprocess.CompletedProcess([], 0, 'bad json', '')):
            with self.assertRaisesRegex(RuntimeError, 'ler o resultado'):
                invoke_attachment_worker('attachments', self.pdf)
        with self.assertRaises(ValueError):
            invoke_attachment_worker('unknown', self.pdf)

    def test_invalid_extraction_confirmation_does_not_claim_success(self):
        self.load()
        self.model.extract(self.output, self.model.selection_token())
        self.runner.jobs[-1][2]({'path': 'invented'})
        self.assertTrue(self.states[-1]['error'])
        self.assertIn('confirmar', self.states[-1]['message'])
        self.assertFalse(self.states[-1]['extracting'])

    def test_display_names_remove_controls_without_interpreting_markup(self):
        self.assertEqual(display_attachment_name('a\u202eb\n.txt'), 'a\ufffdb\ufffd.txt')
        self.assertEqual(display_attachment_name('<b>literal</b>'), '<b>literal</b>')


if __name__ == '__main__':
    unittest.main()
