#!/usr/bin/env python3
"""Directed Ghidra cross-check on Windows/Linux; raw results stay unversioned."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess


SOURCE_SHA256 = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('seeds', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--ghidra', type=Path, required=True)
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--rea-root', type=Path, required=True)
    args = parser.parse_args()
    target, seeds, output = (p.resolve() for p in (args.target, args.seeds, args.output))
    ghidra, java_home, rea = (p.resolve() for p in (args.ghidra, args.java_home, args.rea_root))
    if digest(target) != SOURCE_SHA256:
        parser.error('Target differs from the preserved Foxit reference')
    if output.exists():
        parser.error('Use a new output directory to preserve previous evidence')
    if any(part.startswith('.') for part in output.parts):
        parser.error('Ghidra project paths cannot contain dot-prefixed components')
    java = java_home / 'bin' / ('java.exe' if os.name == 'nt' else 'java')
    support = ghidra / 'support' / 'LaunchSupport.jar'
    seed_script = rea / 'bridge' / 'ghidra' / 'ReaGhidraApplySeeds.java'
    for path in (seeds, java, support, seed_script):
        if not path.is_file():
            parser.error(f'Required file missing: {path}')
    for name in ('project', 'home', 'tmp', 'config', 'cache'):
        (output / name).mkdir(parents=True, exist_ok=False)
    properties = [f'-Duser.home={output / "home"}',
                  f'-Djava.io.tmpdir={output / "tmp"}',
                  f'-Dapplication.settingsdir={output / "config"}',
                  f'-Dapplication.cachedir={output / "cache"}']
    environment = {**os.environ, 'JAVA_HOME': str(java_home)}
    support_result = subprocess.run(
        [str(java), *properties, '-cp', str(support), 'LaunchSupport', str(ghidra), '-vmargs'],
        capture_output=True, text=True, encoding='utf-8', env=environment, check=True, timeout=60)
    vmargs = support_result.stdout.splitlines()
    if any(not arg.startswith('-') or '\0' in arg for arg in vmargs):
        raise ValueError('Invalid LaunchSupport VM argument')
    scripts = Path(__file__).resolve().parent
    command = [str(java), *vmargs, '-Xmx4G', '-XX:ParallelGCThreads=2',
               '-XX:CICompilerCount=2', '-Djava.awt.headless=true', *properties,
               '-cp', str(ghidra / 'Ghidra/Framework/Utility/lib/Utility.jar'),
               'ghidra.Ghidra', 'ghidra.app.util.headless.AnalyzeHeadless',
               str(output / 'project'), 'foxit-selected', '-import', str(target), '-noanalysis',
               '-scriptPath', f'{scripts / "ghidra"};{seed_script.parent}',
               '-preScript', 'ReaGhidraApplySeeds.java', str(seeds),
               '-postScript', 'FoxitSelectedFunctions.java', str(seeds), str(output / 'functions'),
               '-log', str(output / 'ghidra.log'), '-scriptlog', str(output / 'script.log')]
    source = {'target': str(target), 'source_sha256': SOURCE_SHA256,
              'seeds_sha256': digest(seeds), 'command': command,
              'mode': 'Direct Ghidra headless -noanalysis; not REA MCP Evidence',
              'limitations': 'Types, function boundaries and behavior remain provisional; no differential equivalence.'}
    (output / 'source.json').write_text(json.dumps(source, indent=2) + '\n', encoding='utf-8')
    try:
        with (output / 'console.log').open('w', encoding='utf-8') as log:
            subprocess.run(command, env=environment, stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=900)
    finally:
        if digest(target) != SOURCE_SHA256:
            raise RuntimeError('Original target bytes changed during analysis')
    print(f'Direct Ghidra results preserved: {output}')


if __name__ == '__main__':
    main()
