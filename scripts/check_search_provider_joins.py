#!/usr/bin/env python3
"""Re-check, from the pinned original bytes, the structural joins of the search
index provider lifecycle (load, create, release, unload).

Only facts readable from the PE files are checked: instruction sequences,
import names, string literals, exports and RTTI names. Nothing is executed and
no original code is copied into the repository; the output records addresses,
mnemonics and hashes only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import capstone
import pefile

EXE_SHA = '90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6'
DLL_SHA = '20908415a56a8bf63ad4500a2696e6da38a10191402a36b4d84fc577b61c82e1'
MODULE_GLOBAL = 0x6d1ec34
FIELD = 0x1e48


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


class Image:
    def __init__(self, path):
        self.pe = pefile.PE(str(path), fast_load=False)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        self.imports = {}
        for entry in getattr(self.pe, 'DIRECTORY_ENTRY_IMPORT', []):
            for item in entry.imports:
                name = item.name.decode() if item.name else f'#{item.ordinal}'
                self.imports[item.address] = (entry.dll.decode(), name)

    def data(self, va, size):
        return self.pe.get_data(va - self.base, size)

    def ascii(self, va):
        return self.data(va, 128).split(b'\0')[0].decode('ascii')

    def wide(self, va):
        raw = self.data(va, 256)
        end = next(i for i in range(0, len(raw), 2) if raw[i:i + 2] == b'\0\0')
        return raw[:end].decode('utf-16le')

    def code(self, va, count):
        rows = []
        for address, _size, mnemonic, operands in self.md.disasm_lite(self.data(va, count * 15), va, count):
            rows.append((address, mnemonic, operands))
        return rows

    def rtti(self, vtable):
        locator = struct.unpack('<I', self.data(vtable - 4, 4))[0]
        descriptor = struct.unpack('<I', self.data(locator + 12, 4))[0]
        return self.data(descriptor + 8, 96).split(b'\0')[0].decode('ascii')


def find(rows, mnemonic, needle):
    return next((hex(a) for a, m, o in rows if m == mnemonic and needle in o), None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exe', type=Path)
    parser.add_argument('dll', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Use a new output path to preserve evidence')
    if digest(args.exe) != EXE_SHA or digest(args.dll) != DLL_SHA:
        parser.error('Inputs differ from the pinned Foxit reference files')
    exe, dll = Image(args.exe), Image(args.dll)
    checks = {}

    loader = exe.code(0x172a2e0, 42)
    load_call = next(o for a, m, o in loader if m == 'call' and o.startswith('dword ptr [0x'))
    checks['loader_0x172a2e0'] = {
        'appends_string': exe.wide(0x53df6d0),
        'string_pushed_at': find(loader, 'push', hex(0x53df6d0)),
        'guard_on_cached_module': find(loader, 'cmp', hex(MODULE_GLOBAL)),
        'import_called': exe.imports[int(load_call.split('[')[1].rstrip(']'), 16)][1],
        'stores_module_at': find(loader, 'mov', f'[{hex(MODULE_GLOBAL)}], eax'),
    }
    create = exe.code(0x1728ab0, 15)
    checks['create_wrapper_0x1728ab0'] = {
        'export_name': exe.ascii(0x53df6f4),
        'import_called': exe.imports[0x531c930][1],
        'null_proc_guard': find(create, 'je', '0x1728acf'),
        'tail_jump': find(create, 'jmp', 'eax'),
    }
    release = exe.code(0x1728850, 16)
    checks['release_wrapper_0x1728850'] = {
        'export_name': exe.ascii(0x53df704),
        'null_argument_guard': find(release, 'je', '0x1728875'),
        'null_proc_guard': None,
        'tail_jump': find(release, 'jmp', 'eax'),
        'note': 'GetProcAddress result is not tested before the tail jump; only module and argument are.',
    }
    dialog = exe.code(0x1770e90, 52)
    checks['dialog_create_0x1770e90'] = {
        'stores_owner_at_0x1d7c': find(dialog, 'mov', '+ 0x1d7c], edi'),
        'loads_library_via': find(dialog, 'call', '0x172a2e0'),
        'tests_field_zero': find(dialog, 'cmp', f'+ {hex(FIELD)}], 0'),
        'creates_via': find(dialog, 'call', '0x1728ab0'),
        'stores_field': find(dialog, 'mov', f'+ {hex(FIELD)}], eax'),
        'dialog_template_id': int(next(o for a, m, o in dialog if m == 'push' and o == '0x18d7'), 16),
        'context_string': exe.ascii(0x53df29c),
    }
    destructor = exe.code(0x175eb50, 120)
    checks['dialog_destructor_0x175eb50'] = {
        'class': exe.rtti(0x53e0ae4),
        'secondary_vtable_class': exe.rtti(0x53e0c74),
        'waits_worker_thread': [exe.imports[0x531c8f4][1], exe.imports[0x531c8f8][1]],
        'closes_handle_field_0x1e40': exe.imports[0x531caa4][1],
        'releases_field_via': find(destructor, 'call', '0x1728850'),
        'clears_field': find(destructor, 'mov', f'+ {hex(FIELD)}], 0'),
    }
    owner = exe.code(0x1726b90, 230)
    checks['module_owner_destructor_0x1726b90'] = {
        'class': exe.rtti(0x53df274),
        'free_import': exe.imports[0x531cac4][1],
        'free_call': find(owner, 'call', hex(0x531cac4)),
        'clears_module': find(owner, 'mov', f'[{hex(MODULE_GLOBAL)}], 0'),
    }
    exports = {e.name.decode(): hex(dll.base + e.address) for e in dll.pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name}
    new_rows = dll.code(int(exports['NewIndexHandle'], 16), 12)
    delete_rows = dll.code(int(exports['DeleteIndexHandle'], 16), 10)
    checks['dll_exports'] = {
        'NewIndexHandle': exports['NewIndexHandle'],
        'allocation_size': int(next(o for a, m, o in new_rows if m == 'push' and o.startswith('0x')), 16),
        'constructor_jump': find(new_rows, 'jmp', '0x10037e40'),
        'DeleteIndexHandle': exports['DeleteIndexHandle'],
        'deleting_destructor_call': find(delete_rows, 'call', 'dword ptr [eax]'),
    }
    expected = [
        checks['loader_0x172a2e0']['appends_string'] == '\\fxLuceneLib.dll',
        checks['loader_0x172a2e0']['import_called'] == 'LoadLibraryW',
        checks['create_wrapper_0x1728ab0']['export_name'] == 'NewIndexHandle',
        checks['release_wrapper_0x1728850']['export_name'] == 'DeleteIndexHandle',
        all(checks['dialog_create_0x1770e90'][k] for k in ('tests_field_zero', 'creates_via', 'stores_field')),
        checks['dialog_create_0x1770e90']['dialog_template_id'] == 6359,
        checks['dialog_destructor_0x175eb50']['class'] == '.?AVCFindToolDlgAdv@@',
        checks['dialog_destructor_0x175eb50']['releases_field_via'] is not None,
        checks['module_owner_destructor_0x1726b90']['class'] == '.?AVCFindToolModule@@',
        checks['module_owner_destructor_0x1726b90']['free_import'] == 'FreeLibrary',
        checks['dll_exports']['allocation_size'] == 0x20,
        checks['dll_exports']['constructor_jump'] is not None,
    ]
    report = {
        'schema': 'linuxit-structural-joins-v1',
        'subjects': {'FoxitPDFReader.exe': EXE_SHA, 'fxLuceneLib.dll': DLL_SHA},
        'tools': {'capstone': capstone.__version__, 'pefile': pefile.__version__},
        'checks': checks,
        'all_expected_facts_present': all(expected),
        'original_executed': False,
        'semantic_equivalence_proved': False,
        'limitations': [
            'Static byte/instruction joins only; runtime order, threads and failure paths were not observed.',
            'Virtual-call targets through the owner object (+0x1d7c) remain unresolved.',
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'all_expected_facts_present': report['all_expected_facts_present']}))
    if not report['all_expected_facts_present']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
