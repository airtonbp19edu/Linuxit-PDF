#!/usr/bin/env python3
"""Check directed Ghidra instruction boundaries against pinned original bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import capstone
import pefile

SOURCE = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('round', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Use a new output path to preserve evidence')
    folder = args.round.resolve()
    if not folder.is_relative_to((ROOT / 'analysis-local').resolve()):
        parser.error('Raw rounds must remain inside ignored analysis-local/')
    with args.target.open('rb') as stream:
        identity = hashlib.file_digest(stream, 'sha256').hexdigest()
    if identity != SOURCE:
        parser.error('Original differs from the pinned reference')
    metadata = json.loads((folder / 'source.json').read_text(encoding='utf-8'))
    if metadata['source_sha256'] != SOURCE:
        parser.error('Round source identity differs')
    pe = pefile.PE(str(args.target), fast_load=True)
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    entries = []
    for path in sorted((folder / 'functions').glob('0x*.json')):
        record = json.loads(path.read_text(encoding='utf-8'))
        if not record['decompile_completed'] or record.get('decompiler_message'):
            raise ValueError('Incomplete decompilation: ' + path.name)
        ranges = [(int(a, 16), int(b, 16)) for a, b in re.findall(
            r'\[([0-9a-fA-F]+), ([0-9a-fA-F]+)\]', record['body_ranges'])]
        if not ranges or any(b < a for a, b in ranges):
            raise ValueError('Invalid body ranges')
        instructions = []
        for first, last in ranges:
            raw = pe.get_data(first - pe.OPTIONAL_HEADER.ImageBase, last - first + 1)
            part = list(decoder.disasm(raw, first))
            if sum(i.size for i in part) != last - first + 1:
                raise ValueError('Undecoded bytes: ' + path.name)
            instructions.extend(part)
        ghidra = [int(line.split(':')[0], 16) for line in record['assembly']]
        if [i.address for i in instructions] != ghidra or sum(i.size for i in instructions) != record['body_bytes']:
            raise ValueError('Instruction boundaries differ: ' + path.name)
        entries.append({'entry': record['entry_va'], 'instructions': len(instructions),
                        'body_bytes': record['body_bytes'], 'all_instruction_addresses_match': True,
                        'result_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'pseudocode_sha256': hashlib.sha256(record['pseudocode'].encode()).hexdigest()})
    if not entries:
        raise ValueError('No completed entries to examine')
    report = {'schema': 'linuxit-machine-cross-check-v1', 'target_sha256': identity,
              'capstone_version': capstone.__version__, 'pefile_version': pefile.__version__,
              'round': folder.relative_to(ROOT).as_posix(), 'entries': entries,
              'original_executed': False, 'semantic_equivalence_proved': False,
              'limitations': ['Instruction boundaries do not establish complete types, semantics or function boundaries.',
                              'Body ranges may include tail-jump helpers; do not count them again as unique functions.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, indent=2);stream.write('\n')
    print(json.dumps({'entries': len(entries), 'instructions': sum(r['instructions'] for r in entries),
                      'body_bytes': sum(r['body_bytes'] for r in entries), 'passed': True}))


if __name__ == '__main__':main()
