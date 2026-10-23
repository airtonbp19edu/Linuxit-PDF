#!/usr/bin/env python3
"""Run the executable S12 acceptance cases and record results per code revision.

`run` executes cases against app/ (or --app) and writes a new results file.
`apply` copies the outcome of a clean-revision run into the functional spec,
where scripts/validate_functional_spec.py cross-checks it. Results are own
contract executions only; Foxit expectations/observations stay null.
"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / 'testes' / 'aceitacao'
FIXTURES = CASES_DIR / 'fixtures'
SPEC = ROOT / 'docs' / 'especificacao-funcional.json'
STATUSES = ('passed', 'failed', 'error', 'not_run')


def local_now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo('America/Sao_Paulo'))
    except Exception:  # noqa: BLE001 - systems without tzdata keep the documented fixed offset
        return datetime.now(timezone(timedelta(hours=-3)))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    try:
        return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, text=True, timeout=60).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ''


def verify_fixtures():
    manifest = json.loads((FIXTURES / 'manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        path = FIXTURES / item['file']
        if not path.is_file() or path.stat().st_size != item['bytes'] or sha256(path) != item['sha256']:
            raise SystemExit(f'Fixture de aceitação divergente do manifesto: {item["file"]}')
    return {item['file']: item['sha256'] for item in manifest['files']}


def tool_version(command):
    try:
        out = subprocess.run(command, capture_output=True, text=True, timeout=30)
        return (out.stdout or out.stderr).strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def load_cases(app):
    sys.path.insert(0, str(app))
    import rendering  # noqa: F401 - activates the vendored pypdf exactly as the application does
    sys.path.insert(0, str(CASES_DIR))
    import casos
    cases = dict(casos.CASES)
    display = bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))
    if display:
        import casos_gtk
        import casos_portal  # registers its cases only when the portal desktop tools exist
        cases.update(casos_gtk.CASES)
        cases.update(casos_portal.CASES)
    return casos, cases, display


def run(args):
    app = Path(args.app).resolve()
    output = Path(args.output)
    if output.exists():
        raise SystemExit('Escolha um arquivo de resultados novo; nenhum resultado anterior é substituído.')
    fixtures = verify_fixtures()
    casos, cases, display = load_cases(app)
    spec = json.loads(SPEC.read_text(encoding='utf-8'))
    planned = {c['id']: (f['id'], f['contract_kind'], c['kind']) for f in spec['families'] for c in f['acceptance_cases']}
    unknown = sorted(set(cases) - set(planned))
    if unknown:
        raise SystemExit('Casos sem plano na especificação: ' + ', '.join(unknown))
    selected = sorted(cases) if not args.cases else [c.strip() for c in args.cases.split(',') if c.strip()]
    revision = git('rev-parse', 'HEAD')
    dirty = bool(git('status', '--porcelain', '--', 'app', 'testes/aceitacao', 'scripts/run_acceptance.py'))
    started = local_now()
    results = []
    for case_id in selected:
        if case_id not in cases:
            raise SystemExit('Caso desconhecido ou indisponível neste ambiente: ' + case_id)
        entry = cases[case_id]
        family, _, kind = planned[case_id]
        with tempfile.TemporaryDirectory(prefix='linuxit-aceitacao-') as work:
            context = casos.Context(ROOT, app, work)
            began = time.monotonic()
            if args.progress_output:print(f'{case_id}: started', flush=True)
            record = dict(id=case_id, family=family, kind=kind, boundary=entry['boundary'],
                          started_at_local=local_now().isoformat(timespec='seconds'))
            try:
                record['evidence'] = entry['function'](context)
                changed = [name for name, same in context.unchanged().items() if not same]
                if changed:
                    raise casos.Failed('Fixture alterada pelo caso: ' + ', '.join(changed))
                record['status'] = 'passed'
            except AssertionError as exc:
                record['status'], record['message'] = 'failed', str(exc)[:2000]
            except Exception as exc:  # noqa: BLE001 - recorded as an execution error, never as a pass
                record['status'] = 'error'
                record['message'] = f'{type(exc).__name__}: {exc}'[:2000]
                record['traceback_tail'] = traceback.format_exc()[-1500:]
            record['elapsed_sec'] = round(time.monotonic() - began, 3)
            record['fixtures_sha256'] = dict(context.fixtures)
        results.append(record)
        print(f"{case_id}: {record['status']}" + (f" — {record.get('message', '')}" if record['status'] != 'passed' else ''), flush=True)
        if args.progress_output:
            # Partial checkpoint so a later hang keeps the finished cases; never an approval record.
            progress = Path(args.progress_output);progress.parent.mkdir(parents=True, exist_ok=True)
            pending = progress.with_name(progress.name + '.pending')
            pending.write_text(json.dumps({'schema': 'linuxit-acceptance-progress-v1', 'complete': False,
                                           'approval_report': False, 'selected': selected, 'results': results},
                                          ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            os.replace(pending, progress)
    deferred = sorted(cid for cid, (_, contract, _) in planned.items() if contract == 'proposed_only')
    report = {
        'schema': 'linuxit-acceptance-run-v1',
        'scope': 'Own Linuxit contract executions of S12 cases; not Foxit observations, parity or whole-family acceptance.',
        'started_at_local': started.isoformat(timespec='seconds'),
        'finished_at_local': local_now().isoformat(timespec='seconds'),
        'revision': revision, 'revision_dirty': dirty, 'tested_app': str(app),
        'environment': {'python': platform.python_version(), 'platform': platform.platform(),
                        'display_present': display, 'poppler': tool_version(['pdftotext', '-v']),
                        'openssl': tool_version(['openssl', 'version'])},
        'acceptance_fixtures_sha256': fixtures,
        'counts': {status: sum(r['status'] == status for r in results) for status in STATUSES},
        'not_executed_proposed_only': deferred,
        'not_executed_needing_display': [] if display else sorted(cid for cid in planned if cid not in cases and cid not in deferred),
        'foxit_observations': 0,
        'results': results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['counts']))
    return 0 if report['counts']['failed'] == report['counts']['error'] == 0 else 1


def apply(args):
    path = Path(args.results).resolve()
    reference = path.relative_to(ROOT).as_posix()
    report = json.loads(path.read_text(encoding='utf-8'))
    if report.get('schema') != 'linuxit-acceptance-run-v1':
        raise SystemExit('Resultado de aceitação desconhecido.')
    if report['revision_dirty'] or not report['revision']:
        raise SystemExit('Somente execuções de uma revisão limpa podem ser registradas na especificação.')
    spec = json.loads(SPEC.read_text(encoding='utf-8'))
    by_id = {c['id']: c for f in spec['families'] for c in f['acceptance_cases']}
    applied = 0
    for result in report['results']:
        if result['status'] not in ('passed', 'failed'):
            continue
        case = by_id[result['id']]
        case['execution_status'] = result['status']
        case['execution'] = {'result_ref': reference, 'revision': report['revision'],
                             'executed_at_local': result['started_at_local'], 'boundary': result['boundary']}
        applied += 1
    spec['updated_at_local'] = local_now().isoformat(timespec='seconds')
    SPEC.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'applied': applied, 'result_ref': reference}))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    runner = sub.add_parser('run');runner.add_argument('--output', required=True)
    runner.add_argument('--app', default=str(ROOT / 'app'));runner.add_argument('--cases')
    runner.add_argument('--progress-output', help='Optional partial checkpoint written after each case')
    recorder = sub.add_parser('apply');recorder.add_argument('--results', required=True)
    args = parser.parse_args()
    return run(args) if args.command == 'run' else apply(args)


if __name__ == '__main__':
    sys.exit(main())
