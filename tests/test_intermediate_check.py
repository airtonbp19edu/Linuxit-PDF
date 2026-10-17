"""Reject false approvals and source substitutions in the intermediate check."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('intermediate_check', ROOT / 'scripts/check_intermediate.py')
intermediate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intermediate)


class IntermediateApprovalTests(unittest.TestCase):
    def setUp(self):
        self.app = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app')).resolve()
        self.result = {'schema': 'linuxit-test-run-v1', 'tested_app': str(self.app),
                       'run': 1, 'passed': 1, 'failures': 0, 'errors': 0, 'skipped': 0,
                       'full_suite_requested': True, 'test_pattern': 'test*.py',
                       'cases': [{'id': 'synthetic.control', 'status': 'passed'}]}

    def test_complete_matching_run_is_accepted_but_wrong_app_is_rejected(self):
        self.assertTrue(intermediate.test_report_passed(self.result, self.app, full_suite=True))
        self.result['tested_app'] = str(self.app / 'other')
        self.assertFalse(intermediate.test_report_passed(self.result, self.app, full_suite=True))

    def test_skipped_failed_empty_and_inconsistent_results_cannot_approve(self):
        for name, value in [('skipped', 1), ('failures', 1), ('errors', 1),
                            ('run', 0), ('passed', 0), ('cases', []),
                            ('cases', [{'status': 'skipped'}])]:
            with self.subTest(name=name, value=value):
                result = {**self.result, name: value}
                self.assertFalse(intermediate.test_report_passed(result, self.app, full_suite=True))

    def test_subset_cannot_claim_full_linux_suite(self):
        for change in ({'full_suite_requested': False}, {'test_pattern': 'test_attachment_tasks.py'}):
            self.assertFalse(intermediate.test_report_passed({**self.result, **change}, self.app, full_suite=True))

    def test_snapshot_detects_changed_added_and_removed_source_but_ignores_bytecode(self):
        with tempfile.TemporaryDirectory(prefix='linuxit-candidate-control-') as folder:
            root = Path(folder).resolve()
            self.assertTrue(root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            source = root / 'main.py'
            source.write_text('value = 1\n')
            before = intermediate.app_snapshot(root)
            cache = root / '__pycache__'
            cache.mkdir()
            (cache / 'main.pyc').write_bytes(b'cache')
            self.assertEqual(intermediate.app_snapshot(root), before)
            source.write_text('value = 2\n')
            self.assertNotEqual(intermediate.app_snapshot(root), before)
            source.unlink()
            with self.assertRaisesRegex(ValueError, 'Empty'):
                intermediate.app_snapshot(root)
            (root / 'replacement.py').write_text('value = 1\n')
            self.assertNotEqual(intermediate.app_snapshot(root), before)


if __name__ == '__main__':
    unittest.main()
