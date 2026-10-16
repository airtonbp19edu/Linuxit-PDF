#!/usr/bin/env python3
"""Publish metadata of supplementary Ghidra observations, never reconstructed code."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--evidence-root', type=Path, required=True)
parser.add_argument('--output', type=Path, help='Separate metadata file for a new analysis round')
args = parser.parse_args()
root = args.evidence_root.resolve()
repo = Path(__file__).resolve().parents[1]
destination = args.output or repo / 'docs/windows-evidence/foxit-rea/headless-cross-checks.json'
manifest = json.loads(destination.with_name('analysis-manifest.json').read_text(encoding='utf-8'))
source = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
rea_entries = {entry['entry_va'].lower() for entry in manifest['function_dossiers']
               if entry['subject_sha256'] == source}
entries = []
for path in sorted((root / 'headless').rglob('0x*.json')):
    raw = path.read_bytes()
    data = json.loads(raw)
    if not isinstance(data, dict) or 'entry_va' not in data or 'assembly' not in data:
        continue
    entries.append({
        'result': path.relative_to(root).as_posix(),
        'result_sha256': hashlib.sha256(raw).hexdigest(),
        'entry_va': data['entry_va'],
        'analyst_name': data.get('analyst_name'),
        'decompile_completed': data.get('decompile_completed', False),
        'decompiler_message': data.get('decompiler_message'),
        'body_bytes': data.get('body_bytes'),
        'body_ranges': data.get('body_ranges'),
        'pseudocode_sha256': hashlib.sha256(data.get('pseudocode', '').encode()).hexdigest(),
        'also_examined_through_mcp': data['entry_va'].lower() in rea_entries,
    })
result = {
    'source_sha256': source,
    'origin': 'Supplementary direct Ghidra headless -noanalysis, using the REA seed script. Not REA MCP Evidence.',
    'entries': entries,
    'observation_count': len(entries),
    'distinct_entries': len({entry['entry_va'].lower() for entry in entries}),
    'limitations': [
        'Successful decompilation is not proof of types, boundaries, full semantics or Linux equivalence.',
        'Repeated entries can differ by analysis profile and must not be counted as new functions.',
        'Pseudocode and assembly remain outside the repository.',
    ],
}
destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: result[key] for key in ('observation_count', 'distinct_entries')}))
