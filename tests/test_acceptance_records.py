"""Acceptance execution records must be backed by a clean own-run result file."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_acceptance  # noqa: E402
import validate_functional_spec as spec_check  # noqa: E402


class AcceptanceRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / 'docs/especificacao-funcional.json').read_text(encoding='utf-8'))

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.root = Path(self.temp.name)
        self.spec_copy = copy.deepcopy(self.spec)
        self.family = next(f for f in self.spec_copy['families'] if f['contract_kind'] == 'implemented_subset')
        self.case = self.family['acceptance_cases'][0]
        for family in self.spec_copy['families']:
            for item in family['acceptance_cases']:
                item['execution_status'] = 'not_run';item.pop('execution', None)
        original = spec_check.local_file
        self.patch = patch.object(spec_check, 'local_file',
                                  side_effect=lambda name: Path(name) if name.startswith(str(self.root)) else original(name))
        self.patch.start()

    def tearDown(self):
        self.patch.stop();self.temp.cleanup()

    def result(self, status='passed', dirty=False, foxit=0, name='run.json'):
        report = {'schema': 'linuxit-acceptance-run-v1', 'revision': 'a' * 40, 'revision_dirty': dirty,
                  'foxit_observations': foxit,
                  'results': [{'id': self.case['id'], 'status': status, 'boundary': 'worker info',
                               'started_at_local': '2026-10-20T00:10:00-03:00'}]}
        path = self.root / name;path.write_text(json.dumps(report), encoding='utf-8')
        return str(path)

    def record(self, reference, status='passed', **changes):
        self.case['execution_status'] = status
        self.case['execution'] = dict({'result_ref': reference, 'revision': 'a' * 40,
                                       'executed_at_local': '2026-10-20T00:10:00-03:00', 'boundary': 'worker info'}, **changes)

    def test_matching_clean_run_is_counted(self):
        self.record(self.result())
        summary = spec_check.validate(self.spec_copy)
        self.assertEqual((summary['recorded_acceptance_executions'], summary['recorded_acceptance_passed']), (1, 1))
        self.assertEqual(summary['new_acceptance_executions'], 0)

    def test_status_without_result_or_with_contradicting_result_is_refused(self):
        self.case['execution_status'] = 'passed'
        with self.assertRaises((ValueError, KeyError)):spec_check.validate(self.spec_copy)
        self.record(self.result(status='failed'))
        with self.assertRaisesRegex(ValueError, 'differs'):spec_check.validate(self.spec_copy)
        self.record(self.result(name='other.json'), revision='b' * 40)
        with self.assertRaisesRegex(ValueError, 'differs'):spec_check.validate(self.spec_copy)

    def test_dirty_runs_foxit_data_and_proposals_cannot_back_a_status(self):
        self.record(self.result(dirty=True))
        with self.assertRaisesRegex(ValueError, 'clean revision'):spec_check.validate(self.spec_copy)
        self.record(self.result(foxit=1, name='foxit.json'))
        with self.assertRaisesRegex(ValueError, 'Foxit'):spec_check.validate(self.spec_copy)
        self.case['execution_status'] = 'not_run';self.case.pop('execution')
        # No family is a proposal any more (cloud closed in E28); make one in the copy to keep the rule tested.
        proposal = next(f for f in self.spec_copy['families'] if f['id'] == 'cloud')
        proposal['contract_kind'] = 'proposed_only';proposal['existing_test_refs'] = []
        for case in proposal['acceptance_cases']:
            case['expected_basis'] = 'proposed_independent_requirement';case['execution_status'] = 'not_run';case.pop('execution', None)
        self.case = proposal['acceptance_cases'][0];self.record(self.result(name='proposal.json'))
        with self.assertRaisesRegex(ValueError, 'proposal'):spec_check.validate(self.spec_copy)

    def test_not_run_case_cannot_keep_an_execution_record(self):
        self.record(self.result());self.case['execution_status'] = 'not_run'
        with self.assertRaisesRegex(ValueError, 'without an executed status'):spec_check.validate(self.spec_copy)

    def test_runner_refuses_fixture_bytes_that_differ_from_the_manifest(self):
        folder = self.root / 'fixtures';folder.mkdir()
        (folder / 'a.pdf').write_bytes(b'%PDF-1.4 sintetico')
        manifest = {'files': [{'file': 'a.pdf', 'bytes': 18, 'sha256': run_acceptance.sha256(folder / 'a.pdf')}]}
        (folder / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        with patch.object(run_acceptance, 'FIXTURES', folder):
            self.assertEqual(list(run_acceptance.verify_fixtures()), ['a.pdf'])
            (folder / 'a.pdf').write_bytes(b'%PDF-1.4 alterado!')
            with self.assertRaises(SystemExit):run_acceptance.verify_fixtures()

    def test_committed_acceptance_fixtures_match_their_generator(self):
        import subprocess
        result = subprocess.run([sys.executable, str(ROOT / 'testes/aceitacao/gerar_fixtures.py'), '--check'],
                                capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
