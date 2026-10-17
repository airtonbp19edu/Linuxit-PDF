#!/usr/bin/env python3
"""Check documented source boundaries and the complete unfinished-criteria register."""
import argparse
import ast
from datetime import datetime, timedelta, timezone
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


def read_json(name):
    return json.loads(local_file(name).read_text(encoding='utf-8'))


def imported_roots(tree):
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split('.')[0])
    return roots


def has_symbol(tree, symbol):
    node = tree
    for part in symbol.split('.'):
        node = next((child for child in node.body
                     if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                     and child.name == part), None)
        if node is None:
            return False
    return True


def check():
    architecture = read_json('docs/arquitetura-componentes.json')
    pending = read_json('progresso/pendencias-analises.json')
    progress = read_json('progresso/progresso.json')
    spec = read_json('docs/especificacao-funcional.json')
    project = read_json('progresso/projeto.json')
    excluded = [item['id'] for item in project['scope_exclusions']]
    for data in (architecture, pending):
        require(data['scope_exclusions_ref'] == 'progresso/projeto.json' and
                data['excluded_feature_ids'] == excluded, 'Scope exclusion drift')
    require(architecture['schema'] == 'linuxit-architecture-v1', 'Unknown architecture schema')
    require(pending['schema'] == 'linuxit-analysis-pendencies-v1', 'Unknown pendencies schema')
    for data in (architecture, pending):
        require(data['timezone'] == 'America/Sao_Paulo', 'Timezone missing')
        require(datetime.fromisoformat(data['reviewed_at_local']).utcoffset() is not None,
                'Timestamp must include offset')

    paths = [m['path'] for m in architecture['modules']]
    require(len(paths) == len(set(paths)), 'Duplicate module')
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'app').glob('*.py')}
    require(set(paths) == actual, 'Module inventory drift; vendor files are not application modules')
    trees, imports, snapshots = {}, {}, []
    for module in architecture['modules']:
        path = local_file(module['path'])
        require(module['id'] == path.stem and module['boundary'] and module['responsibility'],
                'Module identity/responsibility missing')
        source = path.read_bytes()
        tree = ast.parse(source.decode('utf-8-sig'))
        trees[module['id']] = tree
        imports[module['id']] = imported_roots(tree)
        snapshots.append({'path': module['path'], 'sha256': hashlib.sha256(source).hexdigest(),
                          'boundary': module['boundary']})
    for ref in architecture['interface_refs']:
        require(has_symbol(trees[local_file(ref['path']).stem], ref['symbol']),
                'Unknown interface: ' + ref['symbol'])
    gui_roots = {'gi', 'cairo'}
    closures = {}
    for start in architecture['no_gtk_or_cairo_import_closure']:
        require(start in trees, 'Unknown portable module: ' + start)
        visited, queue = set(), [start]
        while queue:
            name = queue.pop()
            if name in visited:
                continue
            visited.add(name)
            require(not imports[name] & gui_roots, start + ' reaches GUI imports through ' + name)
            queue.extend(imports[name] & trees.keys())
        closures[start] = sorted(visited)
    require(has_symbol(trees['rendering'], 'search_text') and
            'search_engine' in imports['rendering'] and 'rendering' in imports['search_engine'],
            'Reassess documented rendering/search compatibility cycle')
    require('cairo' in imports['imposition'] and has_symbol(trees['imposition'], '_merge_poster_marks'),
            'Reassess documented conditional Cairo dependency')
    version = next(n.value.value for n in trees['version'].body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'VERSION' for t in n.targets))
    require(version == architecture['application_version'], 'Architecture version drift')
    assignments = architecture['family_assignments']
    require([f['id'] for f in assignments] == [f['id'] for f in spec['families']], 'Family mapping drift')
    for assignment, family in zip(assignments, spec['families']):
        require(assignment['contract_kind'] == family['contract_kind'], 'Contract kind drift')
        require(assignment['current_source_refs'] == [p for p in family['source_refs'] if p.startswith('app/')],
                'Source mapping drift: ' + family['id'])
        for name in assignment['current_source_refs']:
            local_file(name)
        require(assignment['future_boundary_implemented'] in (None, False), 'Future boundary not implemented')
    require(not architecture['full_application_implemented'] and not architecture['foxit_parity_verified'],
            'Architecture design is not full implementation/parity')

    expected = [(s['id'], s['title'], c['criterion'], c['status']) for s in progress['stages']
                for c in s['checks'] if c['status'] != 'done']
    actual_pending = [(c['stage_id'], c['stage_title'], c['criterion'], c['criterion_status'])
                      for c in pending['unfinished_criteria']]
    require(actual_pending == expected, 'Unfinished criteria omitted, duplicated or stale')
    references = set()
    for item in pending['unfinished_criteria']:
        require(item['blocker_categories'] and item['next_action'].strip(), 'Missing blocker/action')
        require(item['token_exhaustion_confirmed'] is None, 'Unconfirmed token cause must remain null')
        require(item['evidence_refs'], 'Blocker needs evidence')
        for name in item['evidence_refs']:
            local_file(name); references.add(name)
    require(pending['confirmed_token_exhaustion_events'] == [], 'Reassess confirmed interruption evidence')
    for limit in pending['execution_limits']:
        require(limit['is_token_exhaustion'] is False, 'Execution timeout conflated with tokens')
        local_file(limit['evidence_ref']); references.add(limit['evidence_ref'])
    require(pending['general_progress_percent'] == progress['general_progress_percent'] and
            pending['criteria_revision'] == progress['criteria_revision'], 'Progress snapshot drift')
    stage13 = next(s for s in progress['stages'] if s['id'] == 13)
    require(stage13['verified_fraction'] == 1 and all(c['status'] == 'done' for c in stage13['checks']),
            'Reassess current design criteria')
    require(not pending['stage_13_is_partial_due_to_vm'], 'Stage 13 design does not require the VM')
    return {'schema': 'linuxit-stage13-architecture-validation-v1',
            'verified_at_local': datetime.now(timezone(timedelta(hours=-3))).isoformat(timespec='seconds'),
            'timezone': 'America/Sao_Paulo', 'application_version': version,
            'application_modules': len(trees), 'module_snapshots': snapshots,
            'excluded_feature_ids': excluded,
            'documented_interfaces': len(architecture['interface_refs']),
            'family_assignments': len(assignments), 'no_gtk_or_cairo_import_closures': closures,
            'internal_import_edges': {k: sorted(v & trees.keys()) for k, v in imports.items()},
            'import_check_scope': 'AST includes conditional/deferred imports; no dynamic import or runtime proof.',
            'unfinished_criteria_registered': len(expected),
            'unfinished_stages_registered': len({x[0] for x in expected}),
            'blocker_evidence_files_checked': len(references),
            'confirmed_token_exhaustion_events': 0, 'recorded_execution_timeouts': 2,
            'stage_13_design_verified_fraction': stage13['verified_fraction'],
            'general_progress_percent': progress['general_progress_percent'],
            'full_application_implemented': False, 'application_behavior_changed': False,
            'original_executed': False, 'new_rea_ghidra_observations': 0,
            'gtk_suite_rerun': False, 'new_flatpak_built': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Save the examined structural report')
    args = parser.parse_args()
    report = check()
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({key: report[key] for key in
                     ('application_modules', 'documented_interfaces', 'family_assignments',
                      'unfinished_criteria_registered', 'unfinished_stages_registered',
                      'confirmed_token_exhaustion_events', 'recorded_execution_timeouts')}))


if __name__ == '__main__':
    main()
