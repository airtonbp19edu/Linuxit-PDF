#!/usr/bin/env python3
"""Explicitly fetch hash-pinned release assets before an offline/read-only audit."""
import argparse,json
from pathlib import Path
from delivery_bundle import resolve_bundle,manifest_for_file

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--all',action='store_true');args=parser.parse_args()
if args.all:
    for line in (ROOT/'releases/SHA256SUMS').read_text().splitlines():
        identity,name=line.split()
        if not (ROOT/'releases'/name).exists():
            manifest=manifest_for_file(ROOT,name)
            if manifest['artifact']['sha256']!=identity:raise ValueError('Historical checksum differs')
            resolve_bundle(ROOT,manifest,download=True)
manifest=json.loads((ROOT/'releases/manifest.json').read_text(encoding='utf-8'))
print(resolve_bundle(ROOT,manifest,download=True))
