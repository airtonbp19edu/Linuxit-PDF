#!/usr/bin/env python3
"""Audit an existing development delivery without rebuilding or closing parity gaps."""
import argparse
import ast
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def local(folder, name):
    relative = PurePosixPath(name)
    require(name and '\\' not in name and not relative.is_absolute()
            and '..' not in relative.parts and ':' not in name, 'Unsafe relative path: ' + name)
    target = (folder / name).resolve()
    require(target.is_relative_to(folder.resolve()) and target.is_file(), 'Missing/external file: ' + name)
    return target


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def tested_bytes(commit, name):
    """A file exactly as it was in the tested source commit (the checkout may be newer)."""
    require(re.fullmatch('[0-9a-f]{40}', commit), 'Invalid tested commit')
    return subprocess.check_output(['git', 'show', commit + ':' + name], cwd=ROOT)


def tested_inventory(commit, folder):
    """{relative path: SHA-256} of every file under `folder` in the tested commit."""
    listing = subprocess.check_output(['git', 'ls-tree', '-r', '-z', '--name-only', commit, '--', folder + '/'], cwd=ROOT)
    names = [n.decode('utf-8') for n in listing.split(b'\0') if n]
    return {n[len(folder) + 1:]: hashlib.sha256(tested_bytes(commit, n)).hexdigest() for n in names
            if '__pycache__' not in n.split('/') and not n.endswith(('.pyc', '.pyo'))}


def inventory(folder):
    return {p.relative_to(folder).as_posix(): sha(p) for p in folder.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.pyo')}


def indexed(rows):
    result = {}
    for row in rows:
        name = row['file']
        require(name not in result, 'Duplicate manifest file: ' + name)
        require(re.fullmatch('[0-9a-f]{64}', row['sha256']), 'Invalid SHA-256: ' + name)
        result[name] = row['sha256']
    require(result, 'Empty file inventory')
    return result


def verify_suite(suite):
    cases = suite['cases']
    ids = [c['id'] for c in cases]
    require(suite['schema'] == 'linuxit-test-run-v1' and suite['full_suite_requested'] is True
            and suite['test_pattern'] == 'test*.py', 'Not a complete test suite')
    require(type(suite['run']) is int and suite['run'] > 0
            and suite['run'] == suite['passed'] == len(cases), 'Inconsistent test counts')
    require(len(set(ids)) == len(ids) and all(c['status'] == 'passed' for c in cases)
            and all(suite[k] == 0 for k in ('failures', 'errors', 'skipped')), 'Failed/skipped/duplicate test cases')
    return sorted(ids)


def verify_runtime_files(payload, audit):
    expected = indexed(audit['files'])
    require(audit['all_files_attributed'] is True and audit['files_audited'] == len(expected), 'Runtime inventory incomplete')
    packages, expected_elf, notice_hashes = set(), set(), {}
    for row in audit['files']:
        path = local(payload, row['file'])
        require(sha(path) == row['sha256'], 'Runtime bytes differ: ' + row['file'])
        require(row['packages'] or row['overlay_notice'], 'Runtime file without provenance')
        require(row['generated_from_group'] is None or row['generated_from_group'] in audit['generated_input_groups'], 'Unknown derived data')
        with path.open('rb') as stream:
            is_elf = stream.read(4) == b'\x7fELF'
        require(is_elf == row['elf'], 'Wrong ELF classification: ' + row['file'])
        if is_elf:
            expected_elf.add(row['file'])
        packages.update(row['packages'])
        if row['overlay_notice']:
            require(row['overlay_notice'] in ('python3-gi-cairo.txt','quickjs.txt'), 'Unknown overlay notice')
            notice_hashes[row['overlay_notice']] = sha(local(payload, 'share/doc/linuxit-pdf/runtime-copyright/' + row['overlay_notice']))
    actual_elf = set()
    for path in payload.rglob('*'):
        if path.is_file():
            with path.open('rb') as stream:
                if stream.read(4) == b'\x7fELF':
                    actual_elf.add(path.relative_to(payload).as_posix())
    require(actual_elf == expected_elf, 'Uncatalogued/missing ELF payload files')
    require(len(expected_elf) == audit['elf_files_audited'] and len(packages) == audit['debian_packages'], 'Runtime audit counts disagree')
    for package in sorted(packages):
        require(re.fullmatch(r'[a-z0-9][a-z0-9+.-]*(?::[a-z0-9-]+)?', package), 'Invalid package identity')
        name = package.replace(':', '_') + '.txt'
        notice = local(payload, 'share/doc/linuxit-pdf/runtime-copyright/' + name)
        require(notice.stat().st_size > 0, 'Empty copyright notice: ' + package)
        notice_hashes[name] = sha(notice)
    return {'runtime_files_verified': len(expected), 'elf_files_verified': len(expected_elf),
            'debian_package_notices_verified': len(packages), 'notice_sha256': notice_hashes}


def audit(installed_root=None):
    from delivery_bundle import resolve_bundle,manifest_for_file
    manifest = read(ROOT / 'releases/manifest.json')
    version = manifest['version']
    require(re.fullmatch(r'\d+\.\d+\.\d+', version), 'Invalid delivery version')
    require(manifest == read(ROOT / f'releases/manifest-{version}.json'), 'Versioned/latest manifests differ')
    require(manifest['flatpak_branch'] == 'devel' and not manifest['foxit_differential_test'], 'Unexpected release/parity claim')
    reports = ROOT / 'testes/resultados' / version
    candidate = read(reports / 'candidate.json')
    require(all(manifest.get(k) == v for k, v in candidate.items()), 'Manifest differs from CI candidate')
    artifact = manifest['artifact']
    bundle = resolve_bundle(ROOT,manifest)
    require(bundle.stat().st_size == artifact['bytes'] and sha(bundle) == artifact['sha256'], 'Bundle identity mismatch')
    checksum_count = 0
    for line in (ROOT / 'releases/SHA256SUMS').read_text().splitlines():
        digest, name = line.split()
        existing=ROOT/'releases'/name
        path=local(ROOT/'releases',name) if existing.exists() else resolve_bundle(ROOT,manifest_for_file(ROOT,name))
        require(sha(path) == digest, 'Checksum mismatch: ' + name)
        checksum_count += 1
    require(artifact['sha256'] + '  ' + artifact['file'] in (ROOT / 'releases/SHA256SUMS').read_text(), 'Delivery missing from checksums')
    required_reports = {'source-payload-integrity.json', 'source-intermediate.json', 'payload-tests.json',
                        'sandbox-tests.json', 'sandbox-smoke.json', 'flatpak-normal-launch.json', 'runtime-origins.json'}
    require(required_reports <= manifest['report_hashes'].keys(), 'Required CI evidence missing')
    for name, digest in manifest['report_hashes'].items():
        require(PurePosixPath(name).name == name and sha(local(reports, name)) == digest, 'Changed CI report: ' + name)
    source = read(reports / 'source-intermediate.json')
    require(source['profile'] == 'linux' and source['platform'] == 'linux'
            and source['passed'] is True and source['linux_source_runtime_passed'] is True
            and all(c['passed'] for c in source['checks']) and not source['errors'], 'Linux source not approved')
    require(source['git_head_before_check'] == manifest['source_commit'] and len(source['test_runs']) == 1, 'Wrong tested source commit')
    suites = {'source': source['test_runs'][0], 'payload': read(reports / 'payload-tests.json'), 'sandbox': read(reports / 'sandbox-tests.json')}
    ids = [verify_suite(s) for s in suites.values()]
    require(all(value == ids[0] for value in ids), 'Different test populations')
    require(suites['sandbox']['tested_app'] == '/app/share/linuxit-pdf', 'Wrong tested sandbox application')
    for name, suite in suites.items():
        require(manifest['validation'][name] == {k: suite[k] for k in ('run', 'passed', 'failures', 'errors', 'skipped')}, 'Test summary mismatch')
    for filename, count in (('sandbox-smoke.json', 5), ('flatpak-normal-launch.json', 3)):
        result = read(reports / filename)
        require(result['passed'] is True and len(result['checks']) == count and all(result['checks'].values()), 'Smoke/launcher incomplete')
    require(read(reports / 'sandbox-smoke.json')['inside_flatpak'] is True, 'Smoke outside sandbox')
    integrity = read(reports / 'source-payload-integrity.json')
    files = indexed(integrity['files'])
    # The audit may run on a newer checkout (development continues after a candidate);
    # what must match is the tested source commit, read from Git, not the working tree.
    commit = manifest['source_commit']
    require(integrity['all_match'] is True and integrity['matched_files'] == len(files)
            and indexed(source['app_files']) == files == tested_inventory(commit, 'app'), 'Application source changed since tests')
    require(hashlib.sha256(tested_bytes(commit, 'scripts/build_flatpak.py')).hexdigest() == manifest['builder_sha256'],
            'Builder changed since delivery')
    checkout_differs = inventory(ROOT / 'app') != files
    for name, digest in files.items():
        data = subprocess.check_output(['git', 'show', manifest['source_commit'] + ':app/' + name], cwd=ROOT)
        require(hashlib.sha256(data).hexdigest() == digest, 'Tested Git source differs: ' + name)
    tree = ast.parse(tested_bytes(commit, 'app/version.py').decode('utf-8'))
    source_version = next(n.value.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'VERSION' for t in n.targets))
    require(version == source_version, 'Application/delivery version differs')
    require(b'MIT License' in tested_bytes(commit, 'LICENSE'), 'Own MIT license missing')
    require(b'Redistribution and use' in tested_bytes(commit, 'docs/pypdf-LICENSE.txt'), 'pypdf BSD notice missing')
    require(read(ROOT / 'docs/proveniencia-base.json')['license'] == 'MIT', 'Base provenance missing')
    runtime = read(reports / 'runtime-origins.json')
    indexed(runtime['files'])
    package_names = {p for row in runtime['files'] for p in row['packages']}
    with local(ROOT, manifest['runtime_packages']).open(encoding='utf-8', newline='') as stream:
        package_rows = list(csv.DictReader(stream, delimiter='\t'))
    require({p['binary_package'] for p in package_rows} == package_names
            and len(package_rows) == runtime['debian_packages'], 'Package inventory mismatch')
    require(all(p['version'] and p['source_package'] and p['source_version'] for p in package_rows), 'Package version/source missing')
    source_access_path = None
    if manifest.get('runtime_source_access'):
        access = manifest['runtime_source_access']
        source_access_path = local(ROOT, access['file'])
        require(sha(source_access_path) == access['sha256'], 'Runtime source-access manifest changed')
        expected_access = [dict(binary_package=p['binary_package'], binary_version=p['version'],
            source_package=p['source_package'], source_version=p['source_version'],
            corresponding_source_url='https://sources.debian.org/src/' + quote(p['source_package'], safe='')
            + '/' + quote(p['source_version'], safe='') + '/') for p in package_rows]
        require(read(source_access_path) == expected_access, 'Corresponding-source versions differ from packages')
    progress = read(ROOT / 'progresso/progresso.json')
    pending = read(ROOT / 'progresso/pendencias-analises.json')
    unfinished = [(s['id'], c['criterion'], c['status']) for s in progress['stages'] for c in s['checks'] if c['status'] != 'done']
    require(unfinished == [(c['stage_id'], c['criterion'], c['criterion_status']) for c in pending['unfinished_criteria']], 'Open obligations omitted')
    done = [c for s in progress['stages'] for c in s['checks'] if c['status'] == 'done']
    for check in done:
        require(check['evidence'], 'Done criterion without evidence')
        for name in check['evidence']:
            local(ROOT, name.split('#')[0])
    total = sum(s['weight_percent'] * sum(c['weight'] for c in s['checks'] if c['status'] == 'done') / sum(c['weight'] for c in s['checks']) for s in progress['stages'])
    require(sum(s['weight_percent'] for s in progress['stages']) == 100 and round(total, 2) == progress['general_progress_percent'], 'Roadmap arithmetic drift')
    with (ROOT / 'progresso/matriz-paridade.csv').open(encoding='utf-8', newline='') as stream:
        parity = list(csv.DictReader(stream))
    verified = sum(p['equivalent_to_foxit'] == 'verified' for p in parity)
    require(verified == progress['verified_functional_parity']['verified'], 'Parity summary mismatch')
    spec = read(ROOT / 'docs/especificacao-funcional.json')
    cases = [c for f in spec['families'] for c in f['acceptance_cases']]
    result = {'version': version, 'bundle_sha256': artifact['sha256'], 'tested_source_commit': manifest['source_commit'],
              'bundle_checksums_verified': checksum_count, 'sealed_ci_reports_verified': len(manifest['report_hashes']),
              'application_source_files_verified': len(files), 'historical_complete_tests_per_environment': {k: s['passed'] for k, s in suites.items()},
              'new_full_regression_suite_executed': False, 'runtime_manifest_files': runtime['files_audited'],
              'runtime_manifest_packages': len(package_names), 'done_criteria_evidence_links_checked': len(done),
              'historical_done_criteria_reexecuted': False,
              'unfinished_criteria': [{'stage': s, 'criterion': c, 'status': status} for s, c, status in unfinished],
              'general_progress_percent': round(total, 2), 'verified_parity': verified,
              'identified_families': len(parity), 'complete_acceptance_cases_not_run': sum(c['execution_status'] == 'not_run' for c in cases),
              'project_complete': False, 'original_executed': False, 'physical_printing_verified': False,
              'installed_payload_verified': False,
              'limitations': ['Checks own delivery and recorded evidence, not original Foxit behavior.',
                              'Existing done criteria get structural link checks, not a rerun of all reverse-engineering work.',
                              'GTK layout, desktop integrations, accessibility and physical printing remain open.']}
    result['checkout_app_differs_from_tested_commit'] = checkout_differs
    if source_access_path:
        result['corresponding_source_versions_verified'] = len(package_rows)
        result['source_download_availability_live_checked'] = False
    if installed_root:
        payload = installed_root.resolve()
        app_ref = manifest['application_id'] + '//' + manifest['flatpak_branch']
        def flatpak_info(option, ref):
            return subprocess.check_output(['flatpak', 'info', '--user', option, ref], text=True).strip()
        deployment = Path(flatpak_info('--show-location', app_ref)).resolve()
        require(payload == (deployment / 'files').resolve(), 'Audit root differs from installed Flatpak deployment')
        require(flatpak_info('--show-commit', app_ref) == manifest['app_ostree_commit'], 'Wrong installed OSTree commit')
        require(flatpak_info('--show-commit', manifest['runtime']) == manifest['runtime_commit_tested'], 'Runtime commit changed since original validation')
        result['installed_app_ostree_commit'] = manifest['app_ostree_commit']
        result['installed_runtime_commit'] = manifest['runtime_commit_tested']
        require(inventory(payload / 'share/linuxit-pdf') == files, 'Installed application differs from tested source')
        for name in ('runtime-origins.json', 'runtime-packages.tsv'):
            reference = reports / name if name.endswith('.json') else local(ROOT, manifest['runtime_packages'])
            require(sha(local(payload, 'share/doc/linuxit-pdf/' + name)) == sha(reference), 'Installed provenance differs: ' + name)
        def tested_sha(name):return hashlib.sha256(tested_bytes(commit, name)).hexdigest()
        require(sha(local(payload, 'share/doc/linuxit-pdf/LICENSE')) == tested_sha('LICENSE'), 'Installed MIT license differs')
        require(sha(local(payload, 'share/doc/linuxit-pdf/pypdf-LICENSE.txt')) == tested_sha('docs/pypdf-LICENSE.txt'), 'Installed BSD license differs')
        if source_access_path:
            require(sha(local(payload, 'share/doc/linuxit-pdf/runtime-source-access.json')) == sha(source_access_path), 'Installed corresponding-source manifest differs')
            require(sha(local(payload, 'share/doc/linuxit-pdf/RUNTIME-SOURCE-ACCESS.md')) == tested_sha('docs/RUNTIME-SOURCE-ACCESS.md'), 'Installed source-access instructions differ')
            require(sha(local(payload, 'share/doc/linuxit-pdf/snowballstemmer-COPYING.txt')) == tested_sha('app/vendor/snowballstemmer/COPYING'), 'Installed Snowball BSD notice differs')
        result['installed_runtime'] = verify_runtime_files(payload, runtime)
        result['installed_payload_verified'] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--installed-root', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Use a new report path to preserve previous audits')
    report = {'schema': 'linuxit-delivery-audit-v1', 'date_local': datetime.now(timezone(timedelta(hours=-3))).isoformat(),
              'timezone': 'America/Sao_Paulo', 'passed': False, 'errors': []}
    try:
        report.update(audit(args.installed_root))
        report['audit_code_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        report['passed'] = True
    except Exception as exc:
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({k: report[k] for k in ('passed', 'errors')}))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
