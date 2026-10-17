"""The Linux campaign must reuse the exact original synthetic input bytes."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from run_comparison_campaign import preserved_corpus


class PreservedCorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-preserved-')
        self.work = Path(self.temp.name)
        self.source = self.work / 'source'
        shutil.copytree(ROOT / 'testes/fixtures/campaign18', self.source)
        self.manifest = self.source / 'manifest.json'
        self.output = self.work / 'output'

    def tearDown(self):
        self.temp.cleanup()

    def test_exact_eight_inputs_reused_without_templates_or_protocol_changes(self):
        fixtures = preserved_corpus(self.manifest, self.output)
        self.assertEqual(len(fixtures), 8)
        self.assertEqual({p.name for p in self.output.iterdir()}, {r['name'] for r in fixtures})
        for row in fixtures:
            self.assertEqual((self.output / row['name']).read_bytes(), (self.source / row['name']).read_bytes())

    def test_changed_bytes_rejected_before_destination_creation(self):
        (self.source / 'controle.txt').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'Fixture changed'):
            preserved_corpus(self.manifest, self.output)
        self.assertFalse(self.output.exists())

    def test_missing_fixture_rejected(self):
        (self.source / 'vazio.pdf').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            preserved_corpus(self.manifest, self.output)
        self.assertFalse(self.output.exists())

    def test_manifest_cannot_replace_baseline_hash(self):
        data = json.loads(self.manifest.read_text(encoding='utf-8'))
        data['fixtures'][0]['sha256'] = '0' * 64
        self.manifest.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'identities'):
            preserved_corpus(self.manifest, self.output)

    def test_manifest_cannot_add_traversal_or_duplicate_entries(self):
        data = json.loads(self.manifest.read_text(encoding='utf-8'))
        data['fixtures'].append({**data['fixtures'][0], 'name': '../outside.pdf'})
        self.manifest.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'identities'):
            preserved_corpus(self.manifest, self.output)


if __name__ == '__main__':
    unittest.main()
