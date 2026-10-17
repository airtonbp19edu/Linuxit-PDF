"""Synthetic importer controls; these tests never execute or observe Foxit."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import run_comparison_campaign as comparison


class ComparisonControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-comparison-control-')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.plan = comparison.load_plan()
        self.case = copy.deepcopy(next(c for c in self.plan['cases'] if c['kind'] == 'search' and c['dynamic_case_ref'] == 'D07'))
        self.case.update(fixture_sha256='a' * 64,
                         protocol_sha256=comparison.hash_value(comparison.protocol(self.case)),
                         linuxit={'status': 'observed', 'metrics': copy.deepcopy(self.case['expected_linuxit'])})
        self.campaign = {'schema': 'linuxit-comparison-campaign-v1', 'source_unchanged': True,
                         'fixtures_unchanged': True, 'cases': [self.case],
                         'fixtures': [{'name': self.case['fixture'], 'sha256': 'a' * 64}]}
        self.document = comparison.observation_template(self.campaign)
        self.entry = self.document['cases'][0]

    def tearDown(self):
        self.temp.cleanup()

    def observed(self, metrics=None):
        # This session and file are invented test controls, not original evidence.
        self.document['session'] = {'target_sha256_before': comparison.TARGET,
            'target_sha256_after': comparison.TARGET, 'offline': True, 'synthetic_profile': True,
            'runtime_control_verified': True, 'observed_at': '2026-10-17T01:00:00-03:00',
            'environment': 'SYNTHETIC IMPORTER CONTROL; no Foxit process'}
        evidence = self.root / 'synthetic-control.txt'
        evidence.write_bytes(b'Synthetic validation data, not a Foxit observation.\n')
        self.entry.update(status='observed', metrics=copy.deepcopy(metrics if metrics is not None else self.case['linuxit']['metrics']),
                          evidence=[{'file': evidence.name, 'sha256': comparison.sha(evidence)}])

    def compare(self):
        return comparison.compare_records(self.campaign, self.document, self.root)

    def test_plan_reuses_known_cases_fixtures_and_families_without_ai(self):
        self.assertEqual(len(self.plan['cases']), 17)
        self.assertEqual(len({case['id'] for case in self.plan['cases']}), 17)
        self.assertEqual(self.plan['excluded_feature_ids'], ['foxit-ai'])
        self.assertFalse(self.plan['automatic_parity_update'])

    def test_template_keeps_original_unknown_instead_of_copying_own_expectations(self):
        self.assertIsNone(self.entry['metrics'])
        self.assertEqual(self.entry['evidence'], [])
        result = self.compare()
        self.assertEqual((result['recorded_metric_cases'], result['matches'], result['differences']), (0, 0, 0))
        self.assertEqual(result['cases'][0]['status'], 'awaiting_original')

    def test_matching_synthetic_records_require_review_and_never_approve_family(self):
        self.observed()
        result = self.compare()
        self.assertEqual(result['matches'], 1)
        self.assertTrue(result['manual_evidence_requires_review'])
        self.assertFalse(result['foxit_executed_by_this_tool'])
        self.assertFalse(result['automatic_parity_update'])
        self.assertFalse(result['whole_family_equivalence_verified'])

    def test_comparison_uses_measured_metrics_not_the_own_expected_contract(self):
        self.observed()
        self.case['expected_linuxit'] = {'count': 999, 'hits': []}
        self.assertEqual(self.compare()['matches'], 1)

    def test_different_destination_and_hit_order_are_reported(self):
        self.observed({'count': 2, 'hits': list(reversed(self.case['linuxit']['metrics']['hits']))})
        result = self.compare()
        self.assertEqual(result['differences'], 1)
        self.assertIn('$.hits[0].page', [item['path'] for item in result['cases'][0]['differences']])
        self.assertEqual(result['cases'][0]['differences'][0]['recorded_original'], None)

    def test_wrong_fixture_or_protocol_is_rejected(self):
        for key in ('fixture_sha256', 'protocol_sha256'):
            before = self.entry[key]
            self.entry[key] = 'b' * 64
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.compare()
            self.entry[key] = before

    def test_missing_or_changed_evidence_is_rejected(self):
        self.observed()
        record = self.entry['evidence'][0]
        (self.root / record['file']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            self.compare()
        self.entry['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'require evidence'):
            self.compare()

    def test_changed_campaign_options_fixture_or_integrity_flags_are_rejected(self):
        self.case['parameters']['query'] = 'changed query'
        with self.assertRaisesRegex(ValueError, 'protocol/options changed'):
            self.compare()
        self.case['protocol_sha256'] = comparison.hash_value(comparison.protocol(self.case))
        self.entry['protocol_sha256'] = self.case['protocol_sha256']
        self.case['fixture_sha256'] = 'b' * 64
        self.entry['fixture_sha256'] = 'b' * 64
        with self.assertRaisesRegex(ValueError, 'fixture binding changed'):
            self.compare()
        self.campaign['source_unchanged'] = False
        with self.assertRaisesRegex(ValueError, 'changed-source/fixture'):
            self.compare()

    def test_typed_unknown_is_distinct_from_zero_and_order_is_preserved(self):
        self.assertTrue(comparison.differences(None, 0))
        self.assertTrue(comparison.differences(False, 0))
        self.assertTrue(comparison.differences([1, 2], [2, 1]))
        self.assertEqual(comparison.differences(None, None), [])

    def test_evidence_cannot_escape_the_supplied_directory(self):
        self.observed()
        for name in ('../escape.txt', str(self.root / 'synthetic-control.txt')):
            self.entry['evidence'][0]['file'] = name
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'inside evidence root'):
                self.compare()

    def test_original_identity_offline_control_and_timestamp_are_required(self):
        self.observed()
        for key, value in [('target_sha256_after', '0' * 64), ('offline', False),
                           ('synthetic_profile', False), ('runtime_control_verified', False),
                           ('observed_at', '2026-10-17T01:00:00'), ('environment', '')]:
            before = self.document['session'][key]
            self.document['session'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.compare()
            self.document['session'][key] = before

    def test_runtime_errors_and_unavailable_are_inconclusive_not_feature_failures(self):
        self.observed()
        for status in ('error', 'unavailable_in_context', 'inconclusive'):
            self.entry.update(status=status, metrics=None)
            result = self.compare()
            self.assertEqual(result['cases'][0]['status'], 'inconclusive_original')
            self.assertEqual((result['matches'], result['differences']), (0, 0))

    def test_unknown_metrics_zero_based_pages_and_inconsistent_counts_are_rejected(self):
        self.observed()
        for metrics in (None, {'count': None, 'hits': []}, {'count': True, 'hits': []},
                        {'count': 9, 'hits': []}, {'count': 1, 'hits': [{'source': 'bookmark', 'page': 0}]}):
            self.entry['metrics'] = metrics
            with self.subTest(metrics=metrics), self.assertRaises(ValueError):
                self.compare()

    def test_blocked_linuxit_cannot_match_even_with_an_original_record(self):
        self.observed()
        self.case['linuxit'].update(status='blocked_runtime', metrics=None)
        self.assertEqual(self.compare()['cases'][0]['status'], 'linuxit_not_run')
        self.assertEqual(self.compare()['matches'], 0)

    def test_duplicate_unknown_or_falsely_populated_not_run_records_are_rejected(self):
        self.document['cases'].append(copy.deepcopy(self.entry))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.compare()
        self.document['cases'].pop()
        self.entry['id'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            self.compare()
        self.entry['id'] = self.case['id']
        self.entry['metrics'] = self.case['linuxit']['metrics']
        with self.assertRaisesRegex(ValueError, 'remain null'):
            self.compare()

    def test_existing_result_is_preserved_and_real_probe_reads_pdf_bytes(self):
        from prepare_foxit_dynamic import numbered_pdf
        source = self.root / 'real.pdf'
        numbered_pdf(source, 3)
        observed = comparison.probe({'kind': 'info'}, source, self.root)
        self.assertEqual(observed, {'pages': 3})
        target = self.root / 'result.json'
        comparison.write_new(target, observed)
        before = target.read_bytes()
        with self.assertRaises(FileExistsError):
            comparison.write_new(target, {'pages': 999})
        self.assertEqual(target.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
