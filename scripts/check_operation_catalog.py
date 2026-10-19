#!/usr/bin/env python3
"""Validate the provisional operation catalog; never calculate global completion."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def local_file(name):
    path = (ROOT / name).resolve()
    require(path.is_relative_to(ROOT) and path.is_file(), 'Missing/external reference: ' + name)
    return path

def read(name):
    return json.loads(local_file(name).read_text(encoding='utf-8'))

def validate(catalog):
    require(catalog['schema'] == 'linuxit-operation-catalog-v1', 'Unknown catalog')
    require(catalog['inventory_complete'] is False and catalog['implementation_completion_percent'] is None,
            'Unknown global inventory cannot have a completion percentage')
    require(not catalog['weighting_defined'] and not catalog['operation_count_is_recoding_percentage'],
            'Unweighted operation counts are not reconstruction completion')
    spec = read('docs/especificacao-funcional.json')
    project = read('progresso/projeto.json')
    require(catalog['reference_sha256'] == project['reference_sha256'], 'Reference identity drift')
    ids = [f['id'] for f in spec['families']]
    require([f['id'] for f in catalog['families']] == ids and len(ids) == 25, 'Family mapping drift')
    operations = catalog['operations']
    operation_ids = [o['id'] for o in operations]
    require(len(operation_ids) == len(set(operation_ids)), 'Duplicate operation')
    evidence = read(catalog['recorded_related_test_evidence_ref'])
    require(evidence['new_execution'] is False and evidence['recorded_ci_run_id'] == 39172130287,
            'Recorded Linux tests are not a new execution')
    passed = {c['id'] for c in evidence['cases'] if c['status'] == 'passed'}
    current_passed = set()
    if catalog.get('current_own_test_evidence_ref'):
        current = read(catalog['current_own_test_evidence_ref'])
        require(current['new_own_execution'] is True and current['foxit_executed'] is False
                and current['complete_family_acceptance'] is False, 'Own evidence is not parity')
        suite = read(current['source_report_ref'])['test_runs'][0]
        require(suite['run'] == suite['passed'] == len(suite['cases'])
                and all(suite[k] == 0 for k in ('failures', 'errors', 'skipped')),
                'Current own suite incomplete')
        current_passed = {c['id'] for c in suite['cases'] if c['status'] == 'passed'}
        for name, digest in current['test_file_hashes'].items():
            require(hashlib.sha256(local_file(name).read_bytes()).hexdigest() == digest,
                    'Current test source drift: ' + name)
        for name, digest in current['app_file_hashes'].items():
            require(hashlib.sha256(local_file(name).read_bytes()).hexdigest() == digest,
                    'Current app source drift: ' + name)
    test_cache = {}
    def check_tests(tests):
        for test in tests:
            require(test['id'] in passed and test['recorded_status'] == 'passed' and
                    test['rerun_by_catalog'] is False, 'Unproven/new test execution')
            path = local_file(test['path'])
            if path not in test_cache:
                tree = ast.parse(path.read_text(encoding='utf-8'))
                test_cache[path] = {path.stem+'.'+c.name+'.'+f.name for c in tree.body
                                    if isinstance(c, ast.ClassDef) for f in c.body
                                    if isinstance(f, ast.FunctionDef)}
            require(test['id'] in test_cache[path], 'Test symbol missing')
    symbols = set()
    for operation in operations:
        require(operation['family_id'] in ids and operation['id'].startswith(operation['family_id']+'/'),
                'Operation family mismatch')
        require(operation['input_context'] and operation['output_and_acceptance'].strip() and
                operation['failure_contract_refs'], 'Operation contract incomplete')
        require(operation['operation_acceptance_new_execution'] == 'not_run' and
                operation['comparison_state'] == 'not_verified_as_complete_operation' and
                operation['complete_operation_or_family_equivalence'] is False,
                'Related evidence cannot approve a complete operation/family')
        state = operation['implementation_state']
        require(state in {'bounded_source_present', 'pending_or_target_characterization', 'deferred_by_user'},
                'Unknown implementation state')
        require(bool(operation['source_evidence']) == (state == 'bounded_source_present'),
                'Implementation must have code; pending is not implemented')
        require((state == 'deferred_by_user') == (operation['family_id'] == 'cloud'),
                'Cloud deferral changed')
        for source in operation['source_evidence']:
            path = local_file(source['path']); raw = path.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == source['file_sha256'], 'Code snapshot changed: '+str(path))
            text = raw.decode('utf-8'); node = ast.parse(text)
            for part in source['symbol'].split('.'):
                matches = [n for n in node.body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == part]
                require(len(matches) == 1, 'Code symbol missing: '+source['symbol']); node = matches[0]
            body = '\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])
            require((node.lineno,node.end_lineno) == (source['line'],source['end_line']) and
                    hashlib.sha256(body.encode()).hexdigest() == source['excerpt_sha256'], 'Code excerpt drift')
            symbols.add((source['path'],source['symbol']))
        check_tests(operation['recorded_related_tests'])
        check_tests(operation.get('current_refusal_evidence', []))
        require(set(operation.get('validated_current_test_ids', [])) <= current_passed,
                'Current related tests lack passing own evidence')
        for name in operation['original_observation_refs']:
            local_file(name)
        for error in operation['failure_contract_refs']:
            family = next(f for f in spec['families'] if f['id'] == error['family_id'])
            require(family['id'] == operation['family_id'] and 0 <= error['error_index'] < len(family['errors']),
                    'Failure contract reference invalid')
    for family in catalog['families']:
        require(family['operation_ids'] == [o['id'] for o in operations if o['family_id'] == family['id']],
                'Family operations omitted/reordered')
        require(family['open_questions'] and family['full_family_parity'] == 'not_verified' and
                family['global_family_inventory_complete'] is False, 'Family scope remains incomplete')
    counts = dict(Counter(o['implementation_state'] for o in operations))
    require(catalog['summary']['operations'] == len(operations) and
            catalog['summary']['implementation_states'] == counts, 'Summary drift')
    return {'families':len(ids), 'operations':len(operations), 'implementation_states':counts,
            'source_symbols_checked':len(symbols), 'recorded_related_tests_checked':len(passed),
            'current_own_cases_referenced':len({test for op in operations
                for test in op.get('validated_current_test_ids', [])}),
            'new_app_test_executions':0, 'new_original_executions':0,
            'inventory_complete':False, 'implementation_completion_percent':None}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=ROOT/'progresso/inventario-operacoes-v1.json')
    args = parser.parse_args()
    print(json.dumps(validate(json.loads(args.catalog.read_text(encoding='utf-8')))))

if __name__ == '__main__':
    main()
