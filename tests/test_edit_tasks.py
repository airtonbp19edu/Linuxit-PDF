import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
from edit_tasks import invoke_edit_worker
from pdf_changes import inspect_editable_document
from pypdf import PdfWriter, PdfReader


class EditWorkerTests(unittest.TestCase):
    def test_real_worker_roundtrip_and_existing_destination_message(self):
        with tempfile.TemporaryDirectory(prefix='linuxit-edit-worker-') as temp:
            source, target = Path(temp)/'source.pdf', Path(temp)/'copy.pdf'
            writer = PdfWriter()
            writer.add_blank_page(100, 100)
            writer.write(source)
            info = invoke_edit_worker('edit-info', source)
            request = {'source_sha256': info['source_sha256'], 'operations': [
                {'kind': 'add-bookmark', 'title': 'ação', 'page': 0}]}
            invoke_edit_worker('copy-edit', source, target, request)
            self.assertEqual(PdfReader(target).outline[0].title, 'ação')
            with self.assertRaisesRegex(RuntimeError, 'nome novo'):
                invoke_edit_worker('copy-edit', source, target, request)

    def test_wrong_protocol_is_not_success(self):
        for content in ('not JSON', '{"schema":"unrecognized"}', '{"schema":"linuxit-copy-edit-info-v1"}'):
            with patch('edit_tasks.subprocess.run', return_value=subprocess.CompletedProcess([], 0, content, '')):
                with self.assertRaisesRegex(RuntimeError, 'confirmação'):
                    invoke_edit_worker('edit-info', 'synthetic.pdf')

    def test_timeout_requires_destination_check_and_does_not_claim_success(self):
        with patch('edit_tasks.subprocess.run', side_effect=subprocess.TimeoutExpired([], 600)):
            with self.assertRaisesRegex(RuntimeError, 'Confira o destino'):
                invoke_edit_worker('edit-info', 'synthetic.pdf')

    def test_invalid_command_and_missing_destination_are_rejected_before_subprocess(self):
        with patch('edit_tasks.subprocess.run') as run:
            with self.assertRaises(ValueError):invoke_edit_worker('unexpected', 'file.pdf')
            with self.assertRaises(ValueError):invoke_edit_worker('copy-edit', 'file.pdf')
            run.assert_not_called()


if __name__ == '__main__':unittest.main()
