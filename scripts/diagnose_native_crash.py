#!/usr/bin/env python3
"""Repeat the own test suite to catch an intermittent native crash with Python stacks.

Each repetition runs scripts/run_tests.py in a fresh process with isolated XDG
configuration, cache and temporary folders (as scripts/check_intermediate.py
does). faulthandler dumps every thread's Python stack on SIGSEGV/SIGABRT, and
also on SIGTRAP, which GLib raises for G_DEBUG=fatal-criticals: the stack then
points at the Python call that led GTK to the first critical warning, before
any later crash. This is a diagnostic aid; it never changes the tests.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = r'''
import faulthandler, runpy, signal, sys
faulthandler.enable(all_threads=True)
faulthandler.register(signal.SIGTRAP, all_threads=True, chain=True)
sys.argv = [sys.argv[1]] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name='__main__')
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--pattern', default='test*.py')
    parser.add_argument('--fatal-criticals', action='store_true', help='Stop at the first GLib/GTK critical warning')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 50:
        parser.error('--repeats must be between 1 and 50')
    args.output_dir.mkdir(parents=True, exist_ok=False)
    runs = []
    for index in range(1, args.repeats + 1):
        work = Path(tempfile.mkdtemp(prefix=f'linuxit-crash-{index}-'))
        env = dict(os.environ, PYTHONUTF8='1', XDG_CONFIG_HOME=str(work / 'config'), XDG_CACHE_HOME=str(work / 'cache'),
                   PYTHONPYCACHEPREFIX=str(work / 'pycache'))
        for name in ('TMPDIR', 'TMP', 'TEMP'):
            env[name] = str(work / 'tmp')
        (work / 'tmp').mkdir()
        if args.fatal_criticals:
            env['G_DEBUG'] = 'fatal-criticals'
        log = args.output_dir / f'run-{index}.log'
        with log.open('wb') as handle:
            proc = subprocess.run([sys.executable, '-X', 'utf8', '-c', WRAPPER, str(ROOT / 'scripts/run_tests.py'),
                                   '--pattern', args.pattern, '--temp-dir', str(work / 'tests'),
                                   '--output', str(work / 'result.json')],
                                  cwd=ROOT, env=env, stdout=handle, stderr=subprocess.STDOUT, timeout=900)
        text = log.read_text(encoding='utf-8', errors='replace')
        runs.append({'run': index, 'return_code': proc.returncode,
                     'critical': [line for line in text.splitlines() if 'CRITICAL' in line][:5],
                     'fatal_signal': 'Fatal Python error' in text or 'Current thread' in text})
        print(json.dumps(runs[-1], ensure_ascii=False), flush=True)
    summary = {'schema': 'linuxit-native-crash-diagnosis-v1', 'pattern': args.pattern, 'fatal_criticals': args.fatal_criticals,
               'repeats': args.repeats, 'failed_runs': sum(r['return_code'] != 0 for r in runs), 'runs': runs}
    (args.output_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: summary[k] for k in ('repeats', 'failed_runs')}))


if __name__ == '__main__':
    main()
