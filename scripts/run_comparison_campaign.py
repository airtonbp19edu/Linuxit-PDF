#!/usr/bin/env python3
"""Collect own PDF observables; compare only separately supplied offline records."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False)


def hash_value(value):
    return hashlib.sha256(canonical(value).encode('ascii')).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def positive(value):
    return type(value) is int and value > 0


def validate_metrics(kind, value):
    require(isinstance(value, dict), 'Metrics must be an object')
    if kind == 'info':
        require(set(value) == {'pages'} and positive(value['pages']), 'Invalid page count')
    elif kind == 'invalid':
        require(set(value) == {'accepted'} and type(value['accepted']) is bool, 'Invalid acceptance result')
    elif kind == 'search':
        require(set(value) == {'count', 'hits'} and isinstance(value['hits'], list), 'Invalid search fields')
        require(type(value['count']) is int and value['count'] == len(value['hits']), 'Inconsistent search count')
        for hit in value['hits']:
            require(isinstance(hit, dict) and set(hit) == {'source', 'page'}, 'Invalid search hit')
            require(hit['source'] in ('page_text', 'bookmark', 'comment') and
                    (hit['page'] is None or positive(hit['page'])), 'Invalid source/page; pages are base 1 or null')
    elif kind == 'attachments':
        require(set(value) == {'entries'} and isinstance(value['entries'], list), 'Invalid attachment fields')
        for item in value['entries']:
            require(isinstance(item, dict) and set(item) == {'name', 'size', 'sha256'}, 'Invalid attachment entry')
            require(isinstance(item['name'], str) and type(item['size']) is int and item['size'] >= 0
                    and isinstance(item['sha256'], str) and re.fullmatch('[0-9a-f]{64}', item['sha256']), 'Invalid attachment values')
    elif kind == 'prepare':
        require(set(value) == {'pages', 'content_labels'} and positive(value['pages'])
                and isinstance(value['content_labels'], list) and value['pages'] == len(value['content_labels']), 'Invalid output pages')
        require(all(isinstance(labels, list) and all(positive(n) for n in labels)
                    for labels in value['content_labels']), 'Invalid output content labels')
    else:
        raise ValueError('Unknown observable kind')


def load_plan():
    plan = read(ROOT / 'testes/plano-comparativo.json')
    dynamic = {case['id']: case for case in read(ROOT / plan['dynamic_plan_ref'])['cases']}
    families = {item['id'] for item in read(ROOT / plan['functional_spec_ref'])['families']}
    require(plan['schema'] == 'linuxit-comparison-plan-v1' and plan['automatic_parity_update'] is False, 'Unknown plan')
    require(plan['excluded_feature_ids'] == ['foxit-ai'], 'Scope exclusion drift')
    require(read(ROOT / plan['dynamic_plan_ref'])['target_sha256'] == TARGET
            and read(ROOT / 'progresso/projeto.json')['reference_sha256'] == TARGET, 'Target identity drift')
    ids = set()
    for case in plan['cases']:
        require(re.fullmatch(r'C18-D\d{2}-[a-z-]+', case['id']) and case['id'] not in ids, 'Duplicate/invalid case ID')
        ids.add(case['id'])
        require(case['dynamic_case_ref'] in dynamic and
                case['fixture'] == dynamic[case['dynamic_case_ref']]['fixture'], 'Fixture/dynamic case mismatch')
        require(case['family_ids'] and set(case['family_ids']) <= families, 'Unknown family')
        require(case['expected_basis'] == 'own_contract_only' and case['observable_version'] == 1, 'Unknown metric contract')
        validate_metrics(case['kind'], case['expected_linuxit'])
    return plan


def protocol(case):
    return {key: case[key] for key in ('id', 'fixture', 'kind', 'parameters', 'observable_version', 'measurement')}


def probe(case, source, output):
    """Observe the implementation, without reading expected_linuxit."""
    app = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app')).resolve()
    sys.path.insert(0, str(app))
    from pdf_dependency import configure_pdf_library
    configure_pdf_library()
    from rendering import document_info
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
    kind = case['kind']
    if kind == 'info':
        return {'pages': document_info(str(source))['pages']}
    if kind == 'invalid':
        try:
            document_info(str(source))
        except PdfReadError:
            return {'accepted': False}
        return {'accepted': True}
    if kind == 'search':
        from search_engine import TextSearchIndex
        hits = TextSearchIndex(source).search(case['parameters']['query'], **case['parameters']['options'])
        return {'count': len(hits), 'hits': [{'source': hit['source'],
                'page': hit['page'] + 1 if hit['page'] is not None else None} for hit in hits]}
    if kind == 'attachments':
        from pdf_attachments import list_attachments, extract_attachment
        listing = list_attachments(source)
        entries = []
        for item in listing['attachments']:
            saved = extract_attachment(source, item['index'], output, source_sha256=listing['source_sha256'])
            target = Path(saved['path'])
            entries.append({'name': item['name'], 'size': target.stat().st_size, 'sha256': sha(target)})
        return {'entries': entries}
    if kind == 'prepare':
        from imposition import prepare_output
        target = output / 'prepared.pdf'
        require(not target.exists(), 'Preserve previous PDF output')
        prepare_output(str(source), str(target), case['parameters'])
        pdf = PdfReader(target)
        return {'pages': len(pdf.pages), 'content_labels': [
            [int(n) for n in re.findall(r'PAGE\s+(\d{3})', page.extract_text() or '')] for page in pdf.pages]}
    raise ValueError('Unsupported probe kind')


def observation_template(campaign):
    return {'schema': 'linuxit-offline-observations-v1', 'target_sha256': TARGET,
            'session': {'target_sha256_before': None, 'target_sha256_after': None,
                        'offline': None, 'synthetic_profile': None, 'runtime_control_verified': None,
                        'observed_at': None, 'environment': None},
            'cases': [{'id': case['id'], 'fixture_sha256': case['fixture_sha256'],
                       'protocol_sha256': case['protocol_sha256'], 'status': 'not_run',
                       'metrics': None, 'evidence': []} for case in campaign['cases']]}


def differences(left, right, path='$'):
    if type(left) is not type(right):
        return [{'path': path, 'linuxit': left, 'recorded_original': right}]
    if isinstance(left, dict):
        result = []
        for key in sorted(left.keys() | right.keys()):
            if key not in left or key not in right:
                result.append({'path': path + '.' + key, 'linuxit': left.get(key), 'recorded_original': right.get(key)})
            else:
                result.extend(differences(left[key], right[key], path + '.' + key))
        return result
    if isinstance(left, list):
        if len(left) != len(right):
            return [{'path': path, 'linuxit': left, 'recorded_original': right}]
        return [diff for index, (a, b) in enumerate(zip(left, right)) for diff in differences(a, b, f'{path}[{index}]')]
    return [] if left == right else [{'path': path, 'linuxit': left, 'recorded_original': right}]


def verify_evidence(items, root):
    require(isinstance(items, list) and items, 'Observed metrics require evidence')
    for item in items:
        require(isinstance(item, dict) and set(item) == {'file', 'sha256'}, 'Invalid evidence record')
        relative = Path(item['file'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'Evidence path must stay inside evidence root')
        target = (root / relative).resolve()
        require(target.is_relative_to(root.resolve()) and target.is_file() and target.stat().st_size > 0, 'Missing/external/empty evidence')
        require(sha(target) == item['sha256'], 'Evidence SHA-256 mismatch')


def compare_records(campaign, observations, evidence_root):
    require(campaign['schema'] == 'linuxit-comparison-campaign-v1'
            and campaign['source_unchanged'] is True and campaign['fixtures_unchanged'] is True,
            'Invalid or changed-source/fixture campaign')
    require(observations['schema'] == 'linuxit-offline-observations-v1'
            and observations['target_sha256'] == TARGET, 'Original identity mismatch')
    known = {case['id']: case for case in campaign['cases']}
    require(len(known) == len(campaign['cases']), 'Duplicate campaign case')
    fixtures = {item['name']: item['sha256'] for item in campaign['fixtures']}
    for case in campaign['cases']:
        require(case['protocol_sha256'] == hash_value(protocol(case)), 'Campaign protocol/options changed')
        require(case['fixture_sha256'] == fixtures.get(case['fixture']), 'Campaign fixture binding changed')
        require(case['linuxit']['status'] in ('observed', 'blocked_runtime', 'error', 'not_run'), 'Unknown Linuxit status')
        if case['linuxit']['status'] == 'observed':
            validate_metrics(case['kind'], case['linuxit']['metrics'])
        else:
            require(case['linuxit']['metrics'] is None, 'Unobserved Linuxit metrics must remain null')
    supplied = {}
    states = ('not_run', 'observed', 'error', 'unavailable_in_context', 'inconclusive')
    for item in observations['cases']:
        require(item['id'] in known and item['id'] not in supplied, 'Unknown/duplicate observation case')
        case = known[item['id']]
        require(item['fixture_sha256'] == case['fixture_sha256'], 'Fixture SHA-256 mismatch')
        require(item['protocol_sha256'] == case['protocol_sha256'], 'Protocol/options mismatch')
        require(item['status'] in states, 'Unknown observation status')
        if item['status'] != 'not_run':
            session = observations['session']
            require(session['target_sha256_before'] == session['target_sha256_after'] == TARGET, 'Original before/after identity mismatch')
            require(all(session.get(key) is True for key in ('offline', 'synthetic_profile', 'runtime_control_verified')), 'Offline containment/control not recorded')
            require(isinstance(session.get('environment'), str) and session['environment'].strip(), 'Missing environment')
            require(datetime.fromisoformat(session['observed_at']).utcoffset() is not None, 'Missing observation timestamp offset')
        if item['status'] == 'observed':
            validate_metrics(case['kind'], item['metrics'])
            verify_evidence(item['evidence'], evidence_root)
        else:
            require(item['metrics'] is None, 'Unobserved metrics must remain null')
            if item['status'] == 'not_run':
                require(item['evidence'] == [], 'not_run cannot contain observation evidence')
            elif item['evidence']:
                verify_evidence(item['evidence'], evidence_root)
        supplied[item['id']] = item
    results = []
    for case in campaign['cases']:
        item = supplied.get(case['id'])
        diff = []
        if item is None or item['status'] == 'not_run':
            state = 'awaiting_original'
        elif item['status'] != 'observed':
            state = 'inconclusive_original'
        elif case['linuxit']['status'] != 'observed':
            state = 'linuxit_not_run'
        else:
            validate_metrics(case['kind'], case['linuxit']['metrics'])
            diff = differences(case['linuxit']['metrics'], item['metrics'])
            state = 'different_recorded_metrics' if diff else 'match_recorded_metrics'
        results.append({'id': case['id'], 'family_ids': case['family_ids'], 'status': state, 'differences': diff})
    return {'schema': 'linuxit-recorded-comparison-v1', 'cases': results,
            'recorded_metric_cases': sum(item['status'] == 'observed' for item in supplied.values()),
            'matches': sum(item['status'] == 'match_recorded_metrics' for item in results),
            'differences': sum(item['status'] == 'different_recorded_metrics' for item in results),
            'manual_evidence_requires_review': True, 'foxit_executed_by_this_tool': False,
            'automatic_parity_update': False, 'whole_family_equivalence_verified': False}


def collect(work):
    from check_intermediate import app_snapshot
    from prepare_foxit_dynamic import build_corpus
    plan = load_plan()
    before = app_snapshot(ROOT / 'app')
    work = work.resolve()
    local = (ROOT / 'analysis-local').resolve()
    require(work != local and work.is_relative_to(local) and not work.exists(), 'Use a new child directory under analysis-local/')
    work.mkdir(parents=True)
    fixtures = build_corpus(work / 'input')
    fixture_hashes = {item['name']: item['sha256'] for item in fixtures}
    campaign = {'schema': 'linuxit-comparison-campaign-v1',
                'date_local': datetime.now(timezone(timedelta(hours=-3))).isoformat(timespec='seconds'),
                'platform': sys.platform, 'python': sys.version.split()[0],
                'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'plan_sha256': sha(ROOT / 'testes/plano-comparativo.json'),
                'source_files': before, 'fixtures': fixtures, 'cases': [], 'source_unchanged': False,
                'whole_dynamic_cases_completed': 0, 'foxit_executed': False, 'foxit_observations': 0,
                'full_gtk_suite_executed': False, 'flatpak_built': False,
                'limitations': ['Own backend subsets, not complete D cases or S12 acceptance cases.',
                                'No original execution. Own expectations never populate original observations.',
                                'Output label order is PDF content-stream order, not visual placement/geometry.']}
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PRINT_VIEW_TEST_APP'] = str(ROOT / 'app')
    for case in plan['cases']:
        folder = work / 'probes' / case['id']
        folder.mkdir(parents=True)
        write_new(folder / 'request.json', protocol(case))
        row = {**case, 'fixture_sha256': fixture_hashes[case['fixture']],
               'protocol_sha256': hash_value(protocol(case)),
               'linuxit': {'status': 'not_run', 'metrics': None, 'own_contract_passed': None},
               'foxit': {'status': 'not_run', 'metrics': None, 'evidence': []}}
        needs_poppler = case['kind'] == 'search' and case['parameters']['options']['include_page_text']
        if needs_poppler and not shutil.which('pdftotext'):
            row['linuxit'].update(status='blocked_runtime', reason='pdftotext unavailable; no synthetic replacement for page-text extraction')
        else:
            try:
                proc = subprocess.run([sys.executable, '-X', 'utf8', str(Path(__file__).resolve()),
                    'probe', '--request', str(folder / 'request.json'), '--input', str(work / 'input' / case['fixture']),
                    '--output-dir', str(folder)], cwd=ROOT, env=env, capture_output=True, timeout=90)
                (folder / 'stdout').write_bytes(proc.stdout)
                (folder / 'stderr').write_bytes(proc.stderr)
                require(proc.returncode == 0, 'Probe failed; inspect private stderr')
                metrics = json.loads(proc.stdout)
                validate_metrics(case['kind'], metrics)
                row['linuxit'].update(status='observed', metrics=metrics,
                                      own_contract_passed=not differences(case['expected_linuxit'], metrics))
            except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
                row['linuxit'].update(status='error', reason=type(exc).__name__ + ': ' + str(exc))
        campaign['cases'].append(row)
    campaign['source_unchanged'] = before == app_snapshot(ROOT / 'app')
    campaign['fixtures_unchanged'] = all(sha(work / 'input' / item['name']) == item['sha256'] for item in fixtures)
    campaign['own_observed_subchecks'] = sum(case['linuxit']['status'] == 'observed' for case in campaign['cases'])
    campaign['own_contract_passed'] = sum(case['linuxit']['own_contract_passed'] is True for case in campaign['cases'])
    campaign['blocked_runtime'] = sum(case['linuxit']['status'] == 'blocked_runtime' for case in campaign['cases'])
    campaign['errors'] = sum(case['linuxit']['status'] == 'error' for case in campaign['cases'])
    template = observation_template(campaign)
    write_new(work / 'foxit-observations-template.json', template)
    campaign['comparison'] = compare_records(campaign, template, work)
    campaign['families'] = [{'id': family['id'], 'planned_subchecks': sum(family['id'] in case['family_ids'] for case in campaign['cases']),
                            'foxit_observations': 0, 'equivalence': 'not_verified'}
                           for family in read(ROOT / 'docs/especificacao-funcional.json')['families']]
    campaign['full_dynamic_cases'] = [{'id': case['id'], 'linuxit_full_case_status': 'not_run', 'foxit_status': 'not_run',
        'backend_subcheck_refs': [row['id'] for row in campaign['cases'] if row['dynamic_case_ref'] == case['id']]}
        for case in read(ROOT / 'testes/cenarios-dinamicos.json')['cases']]
    return campaign


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    run = commands.add_parser('run')
    run.add_argument('--work-dir', type=Path, required=True)
    run.add_argument('--output', type=Path, required=True)
    internal = commands.add_parser('probe')
    internal.add_argument('--request', type=Path, required=True)
    internal.add_argument('--input', type=Path, required=True)
    internal.add_argument('--output-dir', type=Path, required=True)
    compare = commands.add_parser('compare')
    compare.add_argument('--campaign', type=Path, required=True)
    compare.add_argument('--observations', type=Path, required=True)
    compare.add_argument('--evidence-root', type=Path, required=True)
    compare.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'probe':
        print(json.dumps(probe(read(args.request), args.input, args.output_dir), ensure_ascii=True))
        return 0
    if args.output.exists():
        parser.error('Use a new report path; previous evidence is preserved')
    try:
        if args.command == 'run':
            result = collect(args.work_dir)
            success = result['source_unchanged'] and result['fixtures_unchanged'] and result['errors'] == 0 and result['own_observed_subchecks'] == result['own_contract_passed']
            summary = {key: result[key] for key in ('own_observed_subchecks', 'own_contract_passed', 'blocked_runtime', 'errors', 'foxit_observations')}
        else:
            result = compare_records(read(args.campaign), read(args.observations), args.evidence_root.resolve())
            result['campaign_sha256'] = sha(args.campaign)
            result['observations_sha256'] = sha(args.observations)
            success = True  # A measured difference is a result, not importer failure.
            summary = {key: result[key] for key in ('recorded_metric_cases', 'matches', 'differences')}
        write_new(args.output, result)
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(1, type(exc).__name__ + ': ' + str(exc) + '\n')
    print(json.dumps(summary))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
