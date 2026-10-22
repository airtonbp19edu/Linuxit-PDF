"""The A4 register must stay complete without fabricating runtime acceptance."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('operation_contract_validator', ROOT / 'scripts/validate_functional_spec.py')
validator = importlib.util.module_from_spec(loader)
loader.loader.exec_module(validator)


class OperationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads((ROOT / 'docs/especificacao-funcional.json').read_text(encoding='utf-8'))
        cls.register = json.loads((ROOT / cls.spec['operation_contracts_ref']).read_text(encoding='utf-8'))
        cls.case_ids = {case['id'] for family in cls.spec['families'] for case in family['acceptance_cases']}

    def validate_register(self, register):
        class RegisterInput:
            def read_text(self, encoding):
                return json.dumps(register)
        original = validator.local_file
        def resolve(name):
            return RegisterInput() if name == self.spec['operation_contracts_ref'] else original(name)
        with patch.object(validator, 'local_file', side_effect=resolve):
            return validator.validate_operation_contracts(self.spec, self.case_ids)

    def test_all_known_ids_have_individual_contracts_and_original_is_unknown(self):
        result = self.validate_register(self.register)
        inventory = json.loads((ROOT / 'progresso/inventario-operacoes-v1.json').read_text(encoding='utf-8'))
        self.assertEqual(result['operation_contracts_checked'], len(inventory['operations']))
        self.assertEqual(result['operation_contract_families'], 25)
        self.assertFalse(result['complete_bounded_register_is_reference_completion'])

    def test_missing_or_duplicated_operation_is_rejected(self):
        data = copy.deepcopy(self.register)
        data['operations'][-1] = data['operations'][0]
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            self.validate_register(data)

    def test_blank_cancellation_is_rejected(self):
        data = copy.deepcopy(self.register)
        data['operations'][0]['cancellation'] = ' '
        with self.assertRaisesRegex(ValueError, 'cancellation'):
            self.validate_register(data)

    def test_missing_specific_error_is_rejected(self):
        data = copy.deepcopy(self.register)
        data['operations'][0]['errors'] = []
        with self.assertRaisesRegex(ValueError, 'error contract'):
            self.validate_register(data)

    def test_unknown_source_symbol_is_rejected(self):
        data = copy.deepcopy(self.register)
        data['operations'][0]['source_anchors'][0]['symbol'] = 'NoSuchContractSymbol'
        with self.assertRaisesRegex(ValueError, 'Missing source symbol'):
            self.validate_register(data)

    def test_contract_review_cannot_become_original_runtime_observation(self):
        data = copy.deepcopy(self.register)
        data['operations'][0]['foxit_observed'] = {'passed': True}
        with self.assertRaisesRegex(ValueError, 'not a runtime execution'):
            self.validate_register(data)

    def test_pending_requirement_cannot_be_labeled_as_current_source(self):
        data = copy.deepcopy(self.register)
        pending = next(item for item in data['operations'] if item['contract_state'] != 'current_bounded_source')
        pending['basis'] = 'current_linuxit_source'
        with self.assertRaisesRegex(ValueError, 'conflation'):
            self.validate_register(data)

    def test_unknown_acceptance_plan_is_rejected(self):
        data = copy.deepcopy(self.register)
        data['operations'][0]['acceptance_plan_refs'].append('S12-unknown')
        with self.assertRaisesRegex(ValueError, 'Unknown family acceptance'):
            self.validate_register(data)


if __name__ == '__main__':
    unittest.main()
