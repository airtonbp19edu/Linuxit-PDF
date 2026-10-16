#!/usr/bin/env python3
"""Check retained emulation archives/adapters; does not launch the original."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path('/workspace/foxit-rea-analysis'))
args = parser.parse_args()
repo = Path(__file__).resolve().parents[1]
manifest = json.loads((repo / 'docs/windows-evidence/foxit-rea/wine-emulation-toolchain.json').read_text())
checked = []
for package in manifest['packages']:
    directory = 'qemu-downloads' if package['Package'] == 'qemu-user' else 'wine32-downloads'
    path = args.root / directory / package['filename']
    if hashlib.sha256(path.read_bytes()).hexdigest() != package['sha256']:
        raise ValueError('Archive integrity mismatch: ' + str(path))
    checked.append(str(path))
for relative, metadata in manifest['runtime_binaries'].items():
    path = args.root / relative
    if hashlib.sha256(path.read_bytes()).hexdigest() != metadata['sha256']:
        raise ValueError('Runtime integrity mismatch: ' + str(path))
print(json.dumps({'verified_archives': len(checked),
                  'verified_runtime_files': len(manifest['runtime_binaries']),
                  'functional_foxit_validation': False}))
