#!/usr/bin/env python3
"""Check the existing project and exercise portable worker boundaries without GTK."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, __version__ as PDF_VERSION
from version import VERSION


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, help='New directory under ignored analysis-local/')
    parser.add_argument('--output', type=Path, help='New public result file; existing reports are preserved')
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('Use a new report path to preserve previous evidence')
    stamp = datetime.now(timezone(timedelta(hours=-3)))
    work = (args.work_dir or ROOT / 'analysis-local' / ('project-check-' + stamp.strftime('%Y%m%d-%H%M%S-%f'))).resolve()
    if not work.is_relative_to((ROOT / 'analysis-local').resolve()):
        parser.error('Worker results must stay under ignored analysis-local/')
    work.mkdir(parents=True, exist_ok=False)

    required = ['app/main.py', 'app/worker_cli.py', 'app/version.py', 'scripts/run.sh',
                'scripts/run_tests.py', 'scripts/build_flatpak.py', 'LICENSE',
                'docs/proveniencia-base.json', 'docs/pypdf-LICENSE.txt', 'docs/pypdf-artifact.json',
                'assets/linuxit-pdf.desktop', 'testes/fixtures/busca-escopos.pdf']
    assert all((ROOT / p).is_file() for p in required), 'Project file missing'
    provenance = json.loads((ROOT / 'docs/proveniencia-base.json').read_text(encoding='utf-8'))
    artifact = json.loads((ROOT / 'docs/pypdf-artifact.json').read_text(encoding='utf-8'))
    assert provenance['license'] == 'MIT' and (ROOT / 'LICENSE').read_text().startswith('MIT License')
    assert 'Redistribution and use in source and binary forms' in (ROOT / 'docs/pypdf-LICENSE.txt').read_text()
    assert PDF_VERSION == artifact['version'] == '6.20.1'
    assert '/usr/bin/python3' in (ROOT / 'scripts/run.sh').read_text()
    project = json.loads((ROOT / 'progresso/projeto.json').read_text(encoding='utf-8'))
    exclusion = next(x for x in project['scope_exclusions'] if x['id'] == 'foxit-ai')
    assert exclusion['future_reverse_engineering'] is False and exclusion['future_implementation'] is False
    assert exclusion['required_for_parity'] is False and exclusion['preserve_historical_inventory'] is True

    fixture = ROOT / 'testes/fixtures/busca-escopos.pdf'
    fixture_before = digest(fixture)
    snapshots = {name: digest(ROOT / name) for name in required}
    cases = []
    env = os.environ.copy()
    env['PYTHONUTF8'] = '1'
    def run(label, parts, stdin=None):
        proc = subprocess.run([sys.executable, str(ROOT / 'app/worker_cli.py'), *map(str, parts)],
                              input=stdin.encode('utf-8') if stdin is not None else None,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90, env=env)
        (work / (label + '.stdout')).write_bytes(proc.stdout)
        (work / (label + '.stderr')).write_bytes(proc.stderr)
        return proc
    def record(label, valid, proc):
        cases.append({'id': label, 'status': 'passed' if valid else 'failed', 'return_code': proc.returncode})

    proc = run('worker_info', ['info', fixture])
    info = json.loads(proc.stdout) if proc.returncode == 0 else {}
    record('worker_info', proc.returncode == 0 and info.get('pages') == 2 and
           all(w > 0 and h > 0 for w, h in info.get('sizes', [])), proc)
    proc = run('worker_panels', ['panels', fixture])
    panels = json.loads(proc.stdout) if proc.returncode == 0 else {}
    record('worker_panels', proc.returncode == 0 and len(panels.get('bookmarks', [])) == 2 and
           len(panels.get('comments', [])) == 1, proc)
    booklet = work / 'booklet.pdf'
    proc = run('worker_prepare_booklet', ['prepare', fixture, booklet], json.dumps({'print_mode': 'booklet'}))
    reader = PdfReader(booklet) if proc.returncode == 0 and booklet.is_file() else None
    record('worker_prepare_booklet', reader is not None and len(reader.pages) == 2 and
           'alvo' in ''.join(p.extract_text() or '' for p in reader.pages).casefold(), proc)
    proc = run('worker_missing_command', [])
    record('worker_missing_command', proc.returncode == 2, proc)
    invalid_output = work / 'invalid-job.pdf'
    proc = run('worker_malformed_job', ['prepare', fixture, invalid_output], '{')
    record('worker_malformed_job', proc.returncode != 0 and not invalid_output.exists(), proc)
    empty_pdf = work / 'empty.pdf'
    empty_pdf.write_bytes(b'')
    proc = run('worker_empty_pdf', ['info', empty_pdf])
    record('worker_empty_pdf', proc.returncode != 0 and not proc.stdout.strip(), proc)
    assert digest(fixture) == fixture_before, 'Fixture changed'
    assert snapshots == {name: digest(ROOT / name) for name in required}, 'Project source changed'

    runtime = {'python_modules': {name: importlib.util.find_spec(name) is not None
                                  for name in ('gi', 'cairo', 'PIL', 'cryptography')},
               'path_commands': {name: shutil.which(name) is not None for name in
                                 ('pdftocairo', 'pdftotext', 'pdfunite', 'lp', 'lpstat', 'flatpak')}}
    report = {'schema': 'linuxit-stage14-project-check-v1', 'verified_at_local': stamp.isoformat(timespec='seconds'),
              'timezone': 'America/Sao_Paulo', 'python': sys.version.split()[0], 'platform': sys.platform,
              'version': VERSION, 'vendored_pypdf_version': PDF_VERSION,
              'required_project_files': snapshots, 'provenance_commit': provenance['commit'],
              'structural_licenses_and_entrypoints_checked': True,
              'worker_cases': cases, 'passed': sum(c['status'] == 'passed' for c in cases),
              'failed': sum(c['status'] == 'failed' for c in cases),
              'source_and_fixture_unchanged': True, 'runtime_availability': runtime,
              'private_results': work.relative_to(ROOT).as_posix(), 'excluded_feature_ids': ['foxit-ai'],
              'full_linux_gtk_suite_rerun': False, 'gui_launched': False, 'original_executed': False,
              'foxit_differential_test': False, 'new_flatpak_built': False,
              'limitations': ['Portable worker checks do not execute the 50 full acceptance plans or prove Foxit parity.',
                              'No GTK startup, Poppler image rendering, Cairo poster marks or physical printer exercised.',
                              'License file/provenance checks do not re-audit the complete historical Flatpak payload.']}
    if args.output:
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': report['passed'], 'failed': report['failed'],
                      'version': VERSION, 'pypdf': PDF_VERSION, 'runtime': runtime}))
    raise SystemExit(0 if report['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
