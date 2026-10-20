#!/usr/bin/env python3
"""Require examined source, payload and installed-sandbox checks before candidate metadata."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess

from check_intermediate import ROOT, app_snapshot, test_report_passed


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2)
        stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='mode', required=True)
    integrity = commands.add_parser('integrity')
    integrity.add_argument('--payload', required=True, type=Path)
    integrity.add_argument('--output', required=True, type=Path)
    finalize = commands.add_parser('finalize')
    for name in ('reports', 'stage', 'artifact', 'output'):
        finalize.add_argument('--' + name, required=True, type=Path)
    args = parser.parse_args()
    if args.mode == 'integrity':
        source, payload = app_snapshot(ROOT / 'app'), app_snapshot(args.payload)
        require(source == payload, 'Source/payload mismatch')
        result = {'schema': 'linuxit-source-payload-v1', 'all_match': True,
                  'matched_files': len(source), 'files': [{'file': name, 'sha256': value} for name, value in source.items()]}
    else:
        reports = args.reports
        source = read(reports / 'source-intermediate.json')
        require(source['profile'] == 'linux' and source['passed'] is True
                and source['linux_source_runtime_passed'] is True, 'Source Linux checks incomplete')
        require(len(source['test_runs']) == 1, 'Expected one full source suite')
        suites = {'source': source['test_runs'][0], 'payload': read(reports / 'payload-tests.json'),
                  'sandbox': read(reports / 'sandbox-tests.json')}
        app_paths = {'source': Path(source['candidate_directory']) / 'app',
                     'payload': args.stage / 'files/share/linuxit-pdf', 'sandbox': Path('/app/share/linuxit-pdf')}
        for name, suite in suites.items():
            require(test_report_passed(suite, app_paths[name], full_suite=True), name + ' full suite failed or skipped')
        smoke = read(reports / 'sandbox-smoke.json')
        require(smoke['passed'] is True and len(smoke['checks']) == 5 and all(smoke['checks'].values())
                and smoke['inside_flatpak'] is True and not smoke['errors'], 'Installed sandbox smoke incomplete')
        launcher = read(reports / 'flatpak-normal-launch.json')
        require(launcher['passed'] is True and len(launcher['checks']) == 3 and all(launcher['checks'].values()), 'Normal launcher incomplete')
        integrity_report = read(reports / 'source-payload-integrity.json')
        require(integrity_report['all_match'] is True, 'Integrity check incomplete')
        require(app_snapshot(ROOT / 'app') == app_snapshot(args.stage / 'files/share/linuxit-pdf'), 'Source/payload changed after checks')
        version = runpy.run_path(str(ROOT / 'app/version.py'))['VERSION']
        require(args.artifact.name == f'LinuxitPDF-{version}-x86_64.flatpak' and args.artifact.stat().st_size > 0, 'Wrong/missing candidate bundle')
        packages = args.stage / 'files/share/doc/linuxit-pdf/runtime-packages.tsv'
        require(not (reports / 'runtime-packages.tsv').exists(), 'Preserve previous package manifest')
        shutil.copy2(packages, reports / 'runtime-packages.tsv')
        origins_path = args.stage / 'files/share/doc/linuxit-pdf/runtime-origins.json'
        origins = read(origins_path)
        require(origins['all_files_attributed'] is True
                and origins['files_audited'] == len(origins['files']) > 0
                and all(row['packages'] or row['overlay_notice'] for row in origins['files']),
                'Bundled runtime provenance incomplete')
        require(not (reports / 'runtime-origins.json').exists(), 'Preserve previous runtime audit')
        shutil.copy2(origins_path, reports / 'runtime-origins.json')
        access_path = args.stage / 'files/share/doc/linuxit-pdf/runtime-source-access.json'
        if access_path.exists():
            # The corresponding-source manifest travels with the reports for the release record.
            require(not (reports / 'runtime-source-access.json').exists(), 'Preserve previous source-access manifest')
            shutil.copy2(access_path, reports / 'runtime-source-access.json')
        def output(*command):
            return subprocess.check_output(command, cwd=ROOT, text=True).strip()
        result = {'schema': 'linuxit-linux-candidate-v1', 'date_utc': datetime.now(timezone.utc).isoformat(),
            'version': version, 'status': 'development; full reconstruction incomplete',
            'application_id': 'io.github.airtonbp19edu.LinuxitPDF', 'flatpak_branch': 'devel', 'architecture': 'x86_64',
            'runtime': 'org.freedesktop.Platform/x86_64/25.08',
            'runtime_commit_tested': output('flatpak', 'info', '--user', '--show-commit', 'org.freedesktop.Platform//25.08'),
            'app_ostree_commit': output('flatpak', 'info', '--user', '--show-commit', 'io.github.airtonbp19edu.LinuxitPDF//devel'),
            'source_commit': source['git_head_before_check'], 'validation_commit':output('git','rev-parse','HEAD'), 'builder_sha256': sha(ROOT / 'scripts/build_flatpak.py'),
            'artifact': {'file': args.artifact.name, 'bytes': args.artifact.stat().st_size,
                         'sha256': sha(args.artifact), 'digitally_signed': False},
            'validation': {name: {key: suite[key] for key in ('run', 'passed', 'failures', 'errors', 'skipped')}
                           for name, suite in suites.items()},
            'source_payload_matched_files': integrity_report['matched_files'],
            'bundled_runtime_files_audited': origins['files_audited'],
            'bundled_elf_files_audited': origins['elf_files_audited'],
            'bundled_debian_packages': origins['debian_packages'],
            'sandbox_smoke_checks_passed': 5, 'normal_launcher_checks_passed': 3,
            'report_hashes': {path.name: sha(path) for path in reports.glob('*.json')},
            'foxit_differential_test': False, 'physical_printing_verified': False,
            'restrictions': ['Development build, not complete Foxit reconstruction.',
                             'Only own application and licensed dependencies; no proprietary originals or reverse-engineering payloads.']}
    write_new(args.output, result)
    print(json.dumps({'mode': args.mode, 'output': str(args.output), 'passed': True}))


if __name__ == '__main__':
    main()
