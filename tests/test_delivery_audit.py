"""Synthetic refusal controls for delivery evidence; no original Foxit is used."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_delivery import indexed, local, verify_runtime_files, verify_suite


class DeliveryAuditControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-delivery-control-')
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name).resolve()
        self.file = self.folder / 'runtime-lib/example.so'
        self.file.parent.mkdir()
        self.file.write_bytes(b'\x7fELFSynthetic control; not a usable binary')
        digest = hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.notice = self.folder / 'share/doc/linuxit-pdf/runtime-copyright/libexample_amd64.txt'
        self.notice.parent.mkdir(parents=True)
        self.notice.write_text('Synthetic copyright notice control.')
        self.audit = {'all_files_attributed': True, 'files_audited': 1,
                      'elf_files_audited': 1, 'debian_packages': 1, 'generated_input_groups': {},
                      'files': [{'file': 'runtime-lib/example.so', 'sha256': digest,
                                 'packages': ['libexample:amd64'], 'overlay_notice': None,
                                 'generated_from_group': None, 'elf': True}]}

    def test_complete_synthetic_payload_includes_hashed_notice(self):
        result = verify_runtime_files(self.folder, self.audit)
        self.assertEqual(result['elf_files_verified'], 1)
        self.assertEqual(result['debian_package_notices_verified'], 1)
        self.assertEqual(result['notice_sha256']['libexample_amd64.txt'], hashlib.sha256(self.notice.read_bytes()).hexdigest())

    def test_changed_runtime_bytes_are_rejected(self):
        self.file.write_bytes(b'\x7fELFchanged synthetic bytes')
        with self.assertRaisesRegex(ValueError, 'Runtime bytes differ'):
            verify_runtime_files(self.folder, self.audit)

    def test_missing_notice_is_rejected(self):
        self.notice.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing/external file'):
            verify_runtime_files(self.folder, self.audit)

    def test_uncatalogued_native_file_is_rejected(self):
        (self.file.parent / 'unknown.so').write_bytes(b'\x7fELFunknown synthetic native file')
        with self.assertRaisesRegex(ValueError, 'Uncatalogued/missing ELF'):
            verify_runtime_files(self.folder, self.audit)

    def test_unattributed_file_and_unknown_derivation_are_rejected(self):
        for field, value, error in [('packages', [], 'without provenance'),
                                    ('generated_from_group', 'unknown', 'Unknown derived data')]:
            audit = copy.deepcopy(self.audit)
            audit['files'][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, error):
                verify_runtime_files(self.folder, audit)

    def test_duplicate_inventory_and_escaping_paths_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            indexed(self.audit['files'] * 2)
        for name in ('../outside', '/absolute', 'C:/external', 'folder\\outside'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Unsafe'):
                local(self.folder, name)

    def test_skips_and_duplicate_test_ids_cannot_approve_evidence(self):
        report = json.loads((ROOT / 'testes/resultados/0.1.2/sandbox-tests.json').read_text())
        self.assertEqual(len(verify_suite(report)), 104)
        for change in ('skip', 'duplicate'):
            invalid = copy.deepcopy(report)
            if change == 'skip':
                invalid['skipped'] = 1
            else:
                invalid['cases'][1]['id'] = invalid['cases'][0]['id']
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'Failed/skipped/duplicate'):
                verify_suite(invalid)


if __name__ == '__main__':
    unittest.main()
