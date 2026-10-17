#!/usr/bin/env python3
"""Compile an isolated source candidate and validate portable or Linux behavior."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PORTABLE_PATTERNS = ('test_pdf_attachments.py', 'test_attachment_tasks.py',
                     'test_intermediate_check.py')
NOTICES = ('LICENSE', 'docs/pypdf-LICENSE.txt', 'docs/pypdf-artifact.json',
           'docs/proveniencia-base.json')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def app_snapshot(folder):
    """Only source files; reject links rather than following an external target."""
    files = {}
    for path in sorted(folder.rglob('*')):
        if '__pycache__' in path.relative_to(folder).parts or path.suffix in ('.pyc', '.pyo'):
            continue
        if path.is_symlink():
            raise ValueError('Source candidate must not contain links: ' + str(path))
        if path.is_file():
            files[path.relative_to(folder).as_posix()] = digest(path)
    if not files:
        raise ValueError('Empty source candidate')
    return files


def test_report_passed(report, app, *, full_suite=False):
    """A skipped, empty, mismatched or inconsistent run cannot approve a candidate."""
    cases = report.get('cases', [])
    count = report.get('run', 0)
    return (report.get('schema') == 'linuxit-test-run-v1'
            and Path(report.get('tested_app', '')).resolve() == app.resolve()
            and isinstance(count, int) and count > 0
            and report.get('passed') == count == len(cases)
            and all(case.get('status') == 'passed' for case in cases)
            and all(report.get(name) == 0 for name in ('failures', 'errors', 'skipped'))
            and (not full_suite or (report.get('full_suite_requested') is True
                                   and report.get('test_pattern') == 'test*.py')))


def published_delta(current):
    reference = ROOT / 'testes/resultados/0.1.1/payload-source-integrity.json'
    old = {item['file']: item['sha256'] for item in json.loads(reference.read_text())['files']}
    return {'reference': reference.relative_to(ROOT).as_posix(),
            'added': sorted(current.keys() - old.keys()),
            'removed': sorted(old.keys() - current.keys()),
            'changed': sorted(name for name in current.keys() & old.keys() if current[name] != old[name]),
            'unchanged': sum(current[name] == old[name] for name in current.keys() & old.keys()),
            'method': 'Compare current source hashes with preserved 0.1.1 payload source hashes; not a new bundle extraction.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=('portable', 'linux'), required=True)
    parser.add_argument('--work-dir', type=Path, required=True, help='New directory under analysis-local/')
    parser.add_argument('--output', type=Path, required=True, help='New result path; never overwritten')
    args = parser.parse_args(argv)
    output = args.output.resolve()
    work = args.work_dir.resolve()
    if output.exists():
        parser.error('Use a new report path to preserve previous evidence')
    local = (ROOT / 'analysis-local').resolve()
    if not work.is_relative_to(local) or work == local or work.exists():
        parser.error('Use a new child directory under analysis-local/')
    work.mkdir(parents=True, exist_ok=False)
    candidate = work / 'candidate'
    candidate.mkdir()
    report = {'schema': 'linuxit-intermediate-check-v1', 'profile': args.profile,
              'date': datetime.now(timezone(timedelta(hours=-3))).isoformat(),
              'platform': sys.platform, 'python': sys.version.split()[0],
              'git_head_before_check': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'candidate_directory': str(candidate), 'checks': [], 'test_runs': [], 'errors': [],
              'passed': False, 'linux_source_runtime_passed': False,
              'flatpak_built': False, 'foxit_executed': False, 'foxit_differential_test': False,
              'limitations': ['Portable bytecode and worker tests do not validate GTK or the Linux runtime.',
                              'This check never builds or installs a Flatpak and never launches the original.',
                              'Stage-17 historical evidence for 0.1.1 is separate from this current-source candidate.']}

    def check(name, passed, **details):
        report['checks'].append({'id': name, 'passed': bool(passed), **details})

    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    env['PRINT_VIEW_TEST_APP'] = str(candidate / 'app')
    # Keep child-process caches and smoke temporary files in the ignored workspace.
    temp = work / 'temp'
    temp.mkdir()
    for name in ('TMPDIR', 'TMP', 'TEMP'):
        env[name] = str(temp)
    env['PYTHONPYCACHEPREFIX'] = str(work / 'import-cache')
    env['XDG_CONFIG_HOME'] = str(work / 'config')
    env['XDG_CACHE_HOME'] = str(work / 'cache')

    def run(label, command, timeout):
        proc = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=timeout)
        (work / (label + '.stdout')).write_bytes(proc.stdout)
        (work / (label + '.stderr')).write_bytes(proc.stderr)
        return proc

    try:
        before = app_snapshot(ROOT / 'app')
        for name in before:
            target = candidate / 'app' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / 'app' / name, target)
        for name in NOTICES:
            target = candidate / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        check('candidate_matches_source', app_snapshot(candidate / 'app') == before)
        report['app_files'] = [{'file': name, 'sha256': sha} for name, sha in before.items()]
        report['notices'] = {name: digest(candidate / name) for name in NOTICES}
        report['published_0_1_1_delta'] = published_delta(before)
        compiled = 0
        for source in sorted((candidate / 'app').rglob('*.py')):
            relative = source.relative_to(candidate)
            bytecode = work / 'bytecode' / relative.with_suffix('.pyc')
            bytecode.parent.mkdir(parents=True, exist_ok=True)
            py_compile.compile(str(source), cfile=str(bytecode), dfile=relative.as_posix(),
                               doraise=True, invalidation_mode=py_compile.PycInvalidationMode.CHECKED_HASH)
            compiled += 1
        check('candidate_python_compiles', compiled > 0, files=compiled,
              scope='CPython syntax/bytecode only; no native or GTK execution')

        linux_ready = False
        if args.profile == 'linux':
            commands = {name: shutil.which(name) for name in
                        ('pdftocairo', 'pdftotext', 'pdfinfo', 'pdfunite', 'lp', 'lpstat', 'lpoptions')}
            report['linux_prerequisites'] = {'linux_host': sys.platform == 'linux',
                                             'x11_display': bool(env.get('DISPLAY')), 'commands': commands}
            # Some existing GUI cases require DISPLAY explicitly. A Wayland-only session
            # cannot silently turn those cases into approval; use Xwayland or xvfb-run.
            if sys.platform == 'linux' and env.get('DISPLAY') and all(commands.values()):
                probe = run('linux-probe', [sys.executable, '-X', 'utf8', '-c',
                    "import gi,cairo,PIL,cryptography; gi.require_version('Gtk','3.0'); "
                    "gi.require_foreign('cairo'); from gi.repository import Gtk; "
                    "assert Gtk.init_check()[0], 'GTK could not connect to the display'"], 30)
                linux_ready = probe.returncode == 0
            check('linux_prerequisites', linux_ready, **report['linux_prerequisites'])

        patterns = PORTABLE_PATTERNS if args.profile == 'portable' else ('test*.py',) if linux_ready else ()
        for index, pattern in enumerate(patterns):
            result_file = work / ('tests-' + str(index) + '.json')
            proc = run('tests-' + str(index), [sys.executable, '-X', 'utf8', str(ROOT / 'scripts/run_tests.py'),
                       '--app', str(candidate / 'app'), '--pattern', pattern,
                       '--temp-dir', str(temp), '--output', str(result_file)], 600)
            result = json.loads(result_file.read_text()) if result_file.exists() else {}
            report['test_runs'].append(result)
            check('tests_' + pattern, proc.returncode == 0 and test_report_passed(
                result, candidate / 'app', full_suite=args.profile == 'linux'), return_code=proc.returncode)
        if args.profile == 'linux' and linux_ready:
            proc = run('gtk-smoke', [sys.executable, '-X', 'utf8', str(ROOT / 'scripts/smoke_linuxit.py')], 90)
            smoke = json.loads(proc.stdout) if proc.returncode == 0 else {}
            report['gtk_smoke'] = smoke
            check('gtk_smoke', proc.returncode == 0 and smoke.get('passed') is True
                  and len(smoke.get('checks', {})) == 5 and all(smoke['checks'].values())
                  and smoke.get('errors') == [], return_code=proc.returncode)
        check('candidate_unchanged_after_tests', app_snapshot(candidate / 'app') == before)
        check('source_unchanged_after_tests', app_snapshot(ROOT / 'app') == before)
        report['passed'] = bool(patterns) and all(item['passed'] for item in report['checks'])
        report['linux_source_runtime_passed'] = args.profile == 'linux' and report['passed']
    except Exception as error:
        report['errors'].append(type(error).__name__ + ': ' + str(error))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as target:
        json.dump(report, target, ensure_ascii=False, indent=2)
        target.write('\n')
    print(json.dumps({'profile': args.profile, 'passed': report['passed'],
                      'linux_source_runtime_passed': report['linux_source_runtime_passed'],
                      'test_cases_passed': sum(item.get('passed', 0) for item in report['test_runs']),
                      'errors': report['errors'], 'output': str(output)}, ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
