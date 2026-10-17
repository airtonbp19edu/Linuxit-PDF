"""Portable checks for synthetic inputs and the stage-10 containment contract."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import prepare_foxit_dynamic as campaign
from pypdf import PdfReader
from pypdf.errors import PdfReadError


class DynamicCampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        # Exercise containment against a synthetic checkout even when the test
        # runner deliberately places TEMP inside the real checkout.
        checkout = self.root / 'synthetic-checkout'
        for name in ('testes/fixtures/busca-escopos.pdf', 'testes/cenarios-dinamicos.json',
                     'testes/cenarios-interface.json', 'docs/ETAPA-10.md', 'docs/ETAPA-11.md'):
            target = checkout / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.root_patch = patch.object(campaign, 'ROOT', checkout.resolve())
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def tearDown(self):
        self.temp.cleanup()

    def test_corpus_has_real_geometry_password_attachment_and_negative_inputs(self):
        folder = self.root / 'input'
        manifest = campaign.build_corpus(folder)
        self.assertEqual(len(manifest), 8)
        for entry in manifest:
            self.assertEqual(entry['sha256'], campaign.sha256(folder / entry['name']))
        geometry = PdfReader(folder / 'geometria.pdf')
        self.assertEqual(len(geometry.pages), 8)
        self.assertEqual([p.extract_text().strip() for p in geometry.pages],
                         [f'PAGE {i:03d} alvo' for i in range(1, 9)])
        self.assertEqual([p.rotation for p in geometry.pages], [0, 0, 90, 0, 0, 90, 0, 0])
        self.assertEqual([int(p.mediabox.width) for p in geometry.pages],
                         [595, 420, 595, 420, 595, 420, 595, 420])
        long_doc = PdfReader(folder / 'busca-longa.pdf')
        self.assertEqual(len(long_doc.pages), 250)
        self.assertIn('PAGE 250 alvo', long_doc.pages[-1].extract_text())
        encrypted = PdfReader(folder / 'com-senha.pdf')
        self.assertTrue(encrypted.is_encrypted)
        self.assertEqual(encrypted.decrypt('wrong-synthetic-password'), 0)
        self.assertNotEqual(encrypted.decrypt(campaign.PASSWORD), 0)
        self.assertEqual(len(encrypted.pages), 8)
        attached = PdfReader(folder / 'com-anexo.pdf')
        self.assertEqual(attached.attachments['nota-sintetica.txt'],
                         [b'Anexo sintetico: alvo\n'])
        with self.assertRaises(PdfReadError):
            PdfReader(folder / 'invalido.pdf')
        with self.assertRaises(PdfReadError):
            PdfReader(folder / 'vazio.pdf')

    def test_existing_search_fixture_and_own_metadata_contract_are_preserved(self):
        folder = self.root / 'input'
        campaign.build_corpus(folder)
        self.assertEqual(campaign.sha256(folder / 'busca-escopos.pdf'),
                         campaign.sha256(ROOT / 'testes/fixtures/busca-escopos.pdf'))
        reader = PdfReader(folder / 'busca-escopos.pdf')
        self.assertEqual(len(reader.pages), 2)
        self.assertEqual([str(item['/Title']) for item in reader.outline],
                         ['ALVO marcador', 'alvo externo'])
        note = reader.pages[0]['/Annots'][0].get_object()
        self.assertEqual(str(note['/Subj']), 'Assunto separado')
        self.assertIn('alvo', str(note['/Contents']))

    def test_sandbox_disables_sharing_and_maps_only_three_dedicated_folders(self):
        reference = self.root / 'reference & synthetic'
        inputs, results = self.root / 'input', self.root / 'results'
        config = ET.fromstring(campaign.sandbox_config(reference, inputs, results))
        for key in ('vGPU', 'Networking', 'AudioInput', 'VideoInput',
                    'PrinterRedirection', 'ClipboardRedirection'):
            self.assertEqual(config.findtext(key), 'Disable')
        self.assertEqual(config.findtext('ProtectedClient'), 'Enable')
        maps = config.findall('MappedFolders/MappedFolder')
        self.assertEqual([m.findtext('HostFolder') for m in maps],
                         [str(reference), str(inputs), str(results)])
        self.assertEqual([m.findtext('ReadOnly') for m in maps], ['true', 'true', 'false'])
        self.assertEqual(config.findtext('LogonCommand/Command'),
                         r'notepad.exe C:\Linuxit\Input\controle.txt')
        self.assertNotIn('FoxitPDFReader.exe', config.findtext('LogonCommand/Command'))

    def test_preparation_never_turns_expected_counts_into_observations_or_overwrites(self):
        reference = self.root / 'reference'
        reference.mkdir()
        target = reference / 'FoxitPDFReader.exe'
        target.write_bytes(b'synthetic identity control, not an executable')
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        output = self.root / 'campaign'
        with patch.object(campaign, 'TARGET_SHA256', digest):
            result = campaign.prepare(reference, output)
            before = (output / 'campaign.json').read_bytes()
            with self.assertRaises(FileExistsError):
                campaign.prepare(reference, output)
            self.assertEqual((output / 'campaign.json').read_bytes(), before)
        self.assertFalse(result['original_launched'])
        self.assertFalse(result['readiness']['runtime_verified'])
        self.assertFalse(result['functional_equivalence_verified'])
        self.assertEqual(len(result['observations']), 20)
        self.assertTrue(all(item['status'] == 'not_run' and item['observed'] is None
                            and item['evidence'] == [] for item in result['observations']))
        specs = json.loads((ROOT / 'testes/cenarios-dinamicos.json').read_text(encoding='utf-8'))
        self.assertEqual(len({case['id'] for case in specs['cases']}), 20)
        self.assertTrue(all(case['fixture'] is None or (output / 'input' / case['fixture']).is_file()
                            for case in specs['cases']))
        self.assertEqual(sha256_bytes(target.read_bytes()), digest)

    def test_wrong_identity_and_overlapping_paths_fail_before_creating_output(self):
        reference = self.root / 'reference'
        reference.mkdir()
        (reference / 'FoxitPDFReader.exe').write_bytes(b'wrong binary')
        output = self.root / 'campaign'
        with self.assertRaisesRegex(ValueError, 'Unrecognized'):
            campaign.prepare(reference, output)
        self.assertFalse(output.exists())
        with self.assertRaisesRegex(ValueError, 'overlap'):
            campaign.prepare(reference, reference / 'campaign')
        with self.assertRaisesRegex(ValueError, 'outside the checkout'):
            campaign.prepare(campaign.ROOT, output)


def sha256_bytes(content):
    return hashlib.sha256(content).hexdigest()


if __name__ == '__main__':
    unittest.main()
