#!/usr/bin/env python3
"""Validate stage-12 traceability and render the independent contract register."""
import argparse
import ast
import csv
from datetime import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(name):
    path = (ROOT / name).resolve()
    require(path.is_relative_to(ROOT) and path.is_file(), 'Missing or external reference: ' + name)
    return path


EXECUTED = ('passed', 'failed')


def execution_report(reference, cache):
    """Load an acceptance run once; only clean-revision own runs can back a status."""
    if reference not in cache:
        report = json.loads(local_file(reference).read_text(encoding='utf-8'))
        require(report.get('schema') == 'linuxit-acceptance-run-v1', 'Unknown acceptance result: ' + reference)
        require(report['revision_dirty'] is False and report['revision'], 'Acceptance result is not from a clean revision')
        require(report['foxit_observations'] == 0, 'Own acceptance runs cannot carry Foxit observations')
        cache[reference] = {item['id']: item for item in report['results']}, report['revision']
    return cache[reference]


def validate(spec):
    require(spec.get('schema') == 'linuxit-functional-spec-v1', 'Unsupported schema')
    require(datetime.fromisoformat(spec['authored_at_local']).utcoffset() is not None, 'Timestamp must include timezone')
    require(spec['timezone'] == 'America/Sao_Paulo', 'Wrong continuity timezone')
    require(spec['status'] == 'draft_with_explicit_gaps', 'Draft status must remain explicit')
    require(spec['global_rules']['inventory_complete'] is False, 'Global inventory is still open')
    project = json.loads(local_file(spec['scope_exclusions_ref']).read_text(encoding='utf-8'))
    excluded = project['scope_exclusions']
    require(spec['global_rules']['excluded_feature_ids'] == [item['id'] for item in excluded],
            'Scope exclusions differ from the user decision')
    require(any(item['id'] == 'foxit-ai' and item['future_reverse_engineering'] is False
                and item['future_implementation'] is False and item['required_for_parity'] is False
                for item in excluded), 'Foxit AI is excluded by the user')
    for rule in ('existing_test_reference_is_new_execution', 'proposed_requirement_is_implemented',
                 'static_evidence_is_runtime_availability', 'own_contract_is_foxit_parity'):
        require(spec['global_rules'][rule] is False, 'Invalid evidence rule: ' + rule)
    rows = list(csv.DictReader((ROOT / 'progresso/matriz-paridade.csv').open(encoding='utf-8')))
    require(len(spec['families']) == len(rows) == 25, 'Expected 25 identified families')
    require([f['id'] for f in spec['families']] == [r['id'] for r in rows], 'Family IDs/order differ from parity matrix')
    scenario_ids = set()
    for name in ('testes/cenarios-dinamicos.json', 'testes/cenarios-interface.json'):
        scenario_ids.update(c['id'] for c in json.loads(local_file(name).read_text(encoding='utf-8'))['cases'])
    case_ids, tests, references = set(), set(), set()
    proposed, recorded_runtime_families = 0, 0
    reports, executed, executed_passed = {}, 0, 0
    for family, row in zip(spec['families'], rows):
        prefix = family['id'] + ': '
        require(family['name'] == row['functionality'], prefix + 'Name differs from matrix')
        require(family['matrix_implementation'] == row['implementation'], prefix + 'Implementation drift from matrix')
        require(family['contract_kind'] in {'implemented_subset', 'proposed_only'}, prefix + 'Invalid contract kind')
        require(family['parity'] == 'not_verified', prefix + 'Whole-family parity is not verified')
        observed = family['foxit']['runtime_observed']
        require(type(observed) is bool, prefix + 'Runtime state must be a boolean')
        runtime_refs = family['foxit'].get('runtime_observation_refs', [])
        require(isinstance(runtime_refs, list), prefix + 'Runtime evidence must be a list')
        require(family['foxit'].get('full_family_runtime_verified', False) is False,
                prefix + 'Whole-family runtime is not verified')
        if observed:
            require(family['foxit'].get('evidence_state') == 'runtime_observed_subset' and
                    family['foxit'].get('full_family_runtime_verified') is False,
                    prefix + 'Partial observations cannot approve a whole family')
            require(runtime_refs and family['foxit'].get('recorded_runtime_scope', '').strip(),
                    prefix + 'Observed runtime needs evidence and bounded scope')
            recorded_runtime_families += 1
        else:
            require(not runtime_refs, prefix + 'Runtime references contradict unobserved state')
        for name in runtime_refs:
            require(isinstance(name, str) and name.strip(), prefix + 'Invalid runtime evidence path')
            local_file(name); references.add(name)
        require(bool(family['scope'].strip()) and bool(family['foxit']['unresolved']), prefix + 'Scope/gaps required')
        for field in ('inputs', 'outputs', 'state_and_side_effects'):
            require(bool(family[field]) and all(isinstance(x, str) and x.strip() for x in family[field]), prefix + 'Empty ' + field)
        require(bool(family['errors']), prefix + 'At least one failure contract required')
        for error in family['errors']:
            require(error['trigger'].strip() and error['response'].strip(), prefix + 'Failure needs trigger and response')
            require(error['basis'] in {'current_linuxit_source', 'proposed_independent_requirement'}, prefix + 'Unknown error basis')
        for source in family['source_refs'] + family['foxit']['source_refs']:
            local_file(source); references.add(source)
        require(bool(family['foxit']['source_refs']), prefix + 'Original evidence source required')
        for fixture in family['fixture_refs']:
            require(fixture['status'] == 'existing', prefix + 'Fixture state must be explicit')
            local_file(fixture['path'])
        for test in family['existing_test_refs']:
            path = local_file(test['path'])
            names = {n.name for n in ast.walk(ast.parse(path.read_text(encoding='utf-8')))
                     if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')}
            require(test['test'] in names, prefix + 'Unknown test reference: ' + test['test'])
            tests.add((test['path'], test['test']))
        require(set(family['dynamic_case_refs']) <= scenario_ids, prefix + 'Unknown dynamic/UI scenario')
        require(len(family['acceptance_cases']) >= 2, prefix + 'Need nominal and exception cases')
        require({c['kind'] for c in family['acceptance_cases']} >= {'nominal', 'exception'}, prefix + 'Missing failure/nominal case')
        for case in family['acceptance_cases']:
            require(case['id'] not in case_ids, prefix + 'Duplicate acceptance ID')
            case_ids.add(case['id'])
            require(all(case[k].strip() for k in ('given', 'when', 'expected_linuxit')), prefix + 'Incomplete acceptance case')
            status = case['execution_status']
            require(status in ('not_run',) + EXECUTED, prefix + 'Unknown acceptance execution status')
            if status == 'not_run':
                require('execution' not in case, prefix + 'Execution record without an executed status')
            else:
                # A referenced unit test never counts; only a recorded run of this case does.
                require(family['contract_kind'] == 'implemented_subset', prefix + 'A proposal cannot be executed as accepted')
                record = case['execution']
                require(set(record) == {'result_ref', 'revision', 'executed_at_local', 'boundary'}, prefix + 'Incomplete execution record')
                require(datetime.fromisoformat(record['executed_at_local']).utcoffset() is not None, prefix + 'Execution time needs a zone')
                results, revision = execution_report(record['result_ref'], reports)
                item = results.get(case['id'])
                require(item is not None and item['status'] == status and revision == record['revision']
                        and item['started_at_local'] == record['executed_at_local'] and item['boundary'] == record['boundary'],
                        prefix + 'Execution record differs from its result file')
                executed += 1;executed_passed += status == 'passed'
            require(case['foxit_expected'] is None and case['foxit_observed'] is None, prefix + 'Original unknowns must remain null')
            expected_basis = ('proposed_independent_requirement' if family['contract_kind'] == 'proposed_only'
                              else 'current_linuxit_source')
            require(case['expected_basis'] == expected_basis, prefix + 'Proposed/current contract conflation')
        if family['contract_kind'] == 'proposed_only':
            proposed += 1
            require(not family['existing_test_refs'], prefix + 'Proposal cannot inherit a full implementation test')
    require(spec['stage12_assessment']['detailed_contract_check'] == 'partial', 'Reference specification is incomplete')
    require(spec['stage12_assessment']['phase_a_consolidated'] is False, 'Phase A cannot be closed here')
    return {'families': len(rows), 'acceptance_cases': len(case_ids),
            'implemented_subsets': len(rows) - proposed, 'proposed_only': proposed,
            'unique_test_references_checked': len(tests), 'unique_source_references_checked': len(references),
            'new_acceptance_executions': 0, 'recorded_acceptance_executions': executed,
            'recorded_acceptance_passed': executed_passed, 'foxit_observations': 0,
            'foxit_observations_scope': 'New observations by this validator only; preserved subsets are separate.',
            'families_with_recorded_original_subsets': recorded_runtime_families,
            'reference_specification_complete': False}


def render(spec, summary):
    lines = ['# Registro de contratos funcionais — etapa 12', '',
             'Gerado de `especificacao-funcional.json` por `scripts/validate_functional_spec.py`.', '',
             f"Escopo: **{summary['families']} famílias identificadas**, **{summary['acceptance_cases']} cenários planejados**; "
             f"{summary['implemented_subsets']} subconjuntos implementados e {summary['proposed_only']} propostas futuras. O inventário global permanece aberto.", '',
             'O campo esperado é do contrato próprio atual ou de uma proposta explicitamente identificada. '
             f"Execuções próprias registradas: **{summary['recorded_acceptance_executions']}**, "
             f"das quais {summary['recorded_acceptance_passed']} aprovadas; cada uma aponta o arquivo de resultado e a revisão do código. "
             'Expectativas/observações Foxit dos cenários completos S12 permanecem `null`. '
             'Observações parciais preservadas por família são registradas separadamente. Referenciar um teste existente não o executa novamente '
             'nem comprova paridade. As duas situações de cada família são um início de cobertura, não uma lista exaustiva.', '',
             'Os campos `fixture_refs` apontam materiais já disponíveis; cenários que pedem outros documentos '
             'continuam dependendo da criação/especialização do corpus descrito em sua condição inicial.', '',
             'Índices internos de página usam base zero; páginas em relatórios de observação usam base um.', '',
             'O assistente de IA do Foxit e recursos generativos estão fora do escopo por decisão do usuário '
             'em 17/10/2026; ver [escopo do projeto](ESCOPO.md). As 25 famílias atuais e os registros históricos são preservados.', '',
             '| Família | Estado do contrato |', '|---|---|']
    for family in spec['families']:
        label = 'Subconjunto atual; lacunas abertas' if family['contract_kind'] == 'implemented_subset' else 'Proposta; não implementado'
        lines.append(f"| [{family['name']}](#{family['id']}) | {label} |")
    for family in spec['families']:
        lines += ['', f'<a id="{family["id"]}"></a>', '', f'## {family["name"]}', '', family['scope'], '',
                  '**Entradas**', '', *['- ' + x for x in family['inputs']], '', '**Saídas**', '',
                  *['- ' + x for x in family['outputs']], '', '**Erros e casos excepcionais**', '']
        for error in family['errors']:
            lines.append(f"- {error['trigger']}: {error['response']}")
        lines += ['', '**Estado e efeitos**', '', *['- ' + x for x in family['state_and_side_effects']], '', '**Critérios planejados**', '']
        for case in family['acceptance_cases']:
            basis = 'proposta futura' if case['expected_basis'] == 'proposed_independent_requirement' else 'contrato próprio atual'
            line = (f"- **{case['id']}** ({case['kind']}, {basis}, `{case['execution_status']}`): dado {case['given']} "
                    f"Ação: {case['when']} Esperado: {case['expected_linuxit']}")
            if case['execution_status'] != 'not_run':
                record = case['execution']
                line += (f" Execução própria em {record['executed_at_local']}, revisão `{record['revision'][:12]}`, "
                         f"fronteira {record['boundary']}: [resultado](../{record['result_ref']}).")
            lines.append(line)
        lines += ['', '**Lacunas da referência Foxit**', '', *['- ' + x for x in family['foxit']['unresolved']], '']
        runtime_refs = family['foxit'].get('runtime_observation_refs', [])
        if family['foxit']['runtime_observed']:
            lines += ['**Observação parcial preservada do original:** ' + family['foxit']['recorded_runtime_scope'], '',
                      'Evidências: ' + ', '.join(f'[{name}](../{name})' for name in runtime_refs) + '.', '']
        refs = family['source_refs'] + family['foxit']['source_refs']
        lines.append('Fontes: ' + ', '.join(f'[{name}](../{name})' for name in dict.fromkeys(refs)) + '.')
        if family['existing_test_refs']:
            lines += ['', 'Testes próprios existentes, sem nova execução nesta tabela: ' +
                      '; '.join(f'[{t["test"]}](../{t["path"]})' for t in family['existing_test_refs']) + '.']
        if family['dynamic_case_refs']:
            lines += ['', 'Relacionados aos planos dinâmicos/UI: ' + ', '.join(family['dynamic_case_refs']) + '.']
    lines += ['', 'A especificação de referência e a consolidação da fase A continuam parciais. '
              'Não promover propostas, presença de recursos ou testes próprios a funcionalidade Foxit recuperada.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, default=ROOT / 'docs/especificacao-funcional.json')
    parser.add_argument('--render', type=Path, help='Write the human-readable register after validation')
    parser.add_argument('--check-render', type=Path, help='Verify an existing register matches the JSON')
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding='utf-8'))
    result = validate(spec)
    document = render(spec, result)
    if args.check_render:
        require(args.check_render.read_text(encoding='utf-8') == document, 'Rendered register is stale')
    if args.render:
        args.render.write_text(document, encoding='utf-8', newline='\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
