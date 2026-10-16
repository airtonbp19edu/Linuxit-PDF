#!/usr/bin/env python3
"""Inventory static registration callbacks found with REA in the sampled Foxit.

This decodes instruction metadata, never invokes a callback. Registrations are
not proof of runtime loading, reachable features, recovered signatures or behavior.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

import capstone
from capstone.x86_const import X86_INS_CALL, X86_INS_PUSH, X86_INS_RET, X86_OP_IMM
import pefile

SOURCE_SHA256 = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
COUNT_VA = 0x6b71dd8
DESCRIPTORS_VA = 0x6b6fc1c


def catalog(target, output):
    raw = target.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Recover descriptor locations for this executable version first')
    pe = pefile.PE(data=raw, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    count, = struct.unpack('<I', pe.get_data(COUNT_VA - base, 4))
    if count != 717:
        raise ValueError('Descriptor count differs from the REA observation')
    descriptors = list(struct.iter_unpack('<III', pe.get_data(DESCRIPTORS_VA - base, count * 12)))
    callback_addresses = sorted({callback for _, callback, _ in descriptors})
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    decoder.detail = True
    rows = []
    for index, (capacity, callback, tag) in enumerate(descriptors):
        section = pe.get_section_by_rva(callback - base)
        if section is None or not section.Characteristics & 0x20000000:
            rows.append({'index': index, 'declared_slots': capacity, 'error': 'Callback is not in an executable section'})
            continue
        upper = next((address for address in callback_addresses if address > callback), base + section.VirtualAddress + section.Misc_VirtualSize)
        limit = min(65536, upper - callback)
        pushes, registrations = [], []
        branches = False
        terminated = False
        for instruction in decoder.disasm(pe.get_data(callback - base, limit), callback):
            if instruction.id == X86_INS_PUSH:
                operand = instruction.operands[0]
                pushes.append(operand.imm & 0xffffffff if operand.type == X86_OP_IMM else None)
            elif instruction.id == X86_INS_CALL:
                if len(pushes) >= 3 and all(value is not None for value in pushes[-3:]):
                    function, slot, table = pushes[-3:]
                    code_section = pe.get_section_by_rva(function - base)
                    mapped_code = code_section is not None and bool(code_section.Characteristics & 0x20000000)
                    if slot < capacity and (table < count or table == 0xffffffff) and (function == 0 or mapped_code):
                        registrations.append({'callsite_va': hex(instruction.address), 'table_id': table, 'slot': slot, 'function_va': hex(function), 'null_pointer': function == 0})
                pushes.clear()
            elif instruction.id == X86_INS_RET:
                terminated = True
                break
            elif instruction.group(capstone.CS_GRP_JUMP):
                branches = True
        slots = {registration['slot'] for registration in registrations}
        repeated = [slot for slot, occurrences in Counter(r['slot'] for r in registrations).items() if occurrences > 1]
        rows.append({
            'index': index, 'declared_slots': capacity, 'descriptor_tag': tag,
            'initializer_va': hex(callback), 'decoded_bytes_limit': limit,
            'return_observed': terminated, 'branches_observed': branches,
            'structural_slot_coverage_complete': terminated and slots == set(range(capacity)) and not repeated,
            'duplicate_slots': repeated, 'registrations': registrations,
        })
    summary = {
        'source_sha256': SOURCE_SHA256, 'descriptor_count': count,
        'nonempty_descriptors': sum(capacity > 0 for capacity, _, _ in descriptors),
        'declared_slots': sum(capacity for capacity, _, _ in descriptors),
        'decoded_registrations': sum(len(row.get('registrations', [])) for row in rows),
        'complete_structural_callbacks': sum(row.get('structural_slot_coverage_complete', False) for row in rows),
        'capstone_version': capstone.__version__, 'pefile_version': pefile.__version__,
        'limitations': [
            'Literal PUSH/PUSH/PUSH/CALL template recognition; a nonmatching callback remains partial.',
            'Linear decoding stops at the first RET; callbacks with branches can have conditional or unvisited paths.',
            'A complete structural slot list does not establish runtime callback invocation, availability, signatures or semantics.',
            'Slots and registrations are not counts of unique product features or fully recovered functions.',
        ],
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / 'dispatch-catalog.json').write_text(json.dumps({'summary': summary, 'tables': rows}, indent=2) + '\n')
    (output / 'dispatch-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    catalog(args.executable.resolve(), args.output.resolve())
