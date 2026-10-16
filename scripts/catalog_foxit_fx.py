#!/usr/bin/env python3
"""Inventory Foxit UI/translation XML from .fx files without executing Foxit.

Format recovered with REA/Ghidra from agnosticuilib.dll. This analysis helper
uses standard RC4 and verifies the format's ciphertext MD5 trailer. It writes
metadata only, never copies decrypted templates into the application runtime.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import pefile

LIBRARY_SHA256 = '90d7a3482c88ccabf5f992fc449a6fc3e341ac9405b399daea4d0179042e2658'
KEY_RVA = 0x106354  # REA data reference 0x10106354, image base 0x10000000.
KEY_BYTES = 27
MAX_FILE_BYTES = 16 * 1024 * 1024


def rc4(data, key):
    """Standard RC4 KSA/PRGA, implemented independently for format inspection."""
    state = list(range(256))
    j = 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) & 255
        state[i], state[j] = state[j], state[i]
    i = j = 0
    result = bytearray()
    for value in data:
        i = (i + 1) & 255
        j = (j + state[i]) & 255
        state[i], state[j] = state[j], state[i]
        result.append(value ^ state[(state[i] + state[j]) & 255])
    return bytes(result)


def catalog(root, output):
    library = (root / 'agnosticuilib.dll').read_bytes()
    if hashlib.sha256(library).hexdigest() != LIBRARY_SHA256:
        raise ValueError('Unsupported UI library: recover/verify its format and key location first')
    pe = pefile.PE(data=library, fast_load=True)
    key = pe.get_data(KEY_RVA, KEY_BYTES)
    pe.close()
    if len(key) != KEY_BYTES:
        raise ValueError('UI format key is not mapped in the supplied library')
    rows, errors = [], []
    for file in sorted(root.rglob('*.fx')):
        relative = str(file.relative_to(root))
        try:
            if not 16 < file.stat().st_size <= MAX_FILE_BYTES:
                raise ValueError('FX file outside the inspected size budget')
            raw = file.read_bytes()
            encrypted, checksum = raw[:-16], raw[-16:]
            if hashlib.md5(encrypted, usedforsecurity=False).digest() != checksum:
                raise ValueError('Ciphertext MD5 trailer mismatch')
            decoded = rc4(encrypted, key)
            text = decoded.decode('utf-8-sig')
            # Qt translation files declare a root name, without a DTD subset.
            # It supplies no entities and has no effect on the metadata parser.
            text = re.sub(r'<!DOCTYPE\s+TS\s*>', '', text, flags=re.IGNORECASE)
            if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
                raise ValueError('DTD/entity declarations are outside this inventory format')
            tree = ET.fromstring(text)
            row = {
                'path': relative, 'source_sha256': hashlib.sha256(raw).hexdigest(),
                'decoded_sha256': hashlib.sha256(decoded).hexdigest(),
                'ciphertext_checksum_valid': True, 'root': tree.tag,
                'root_attributes': tree.attrib, 'widgets': [], 'entries': [],
                'connections': [],
            }
            for widget in tree.iter('widget'):
                properties = {}
                for prop in widget.findall('property'):
                    properties[prop.get('name', '')] = ''.join(prop.itertext()).strip()
                row['widgets'].append({**widget.attrib, 'properties': properties})
            if tree.tag == 'TS':
                for context in tree.findall('context'):
                    for message in context.findall('message'):
                        row['entries'].append({
                            'context': context.findtext('name'),
                            'source': message.findtext('source'),
                            'translation': ''.join(message.find('translation').itertext())
                            if message.find('translation') is not None else None,
                        })
            elif tree.tag != 'ui':
                for leaf in tree.iter():
                    if len(leaf) == 0 and leaf.text and leaf.text.strip():
                        row['entries'].append({
                            'tag': leaf.tag, **leaf.attrib, 'text': leaf.text.strip(),
                        })
            for connection in tree.findall('.//connections/connection'):
                row['connections'].append({child.tag: child.text for child in connection})
            rows.append(row)
        except (OSError, ValueError, ET.ParseError) as exc:
            errors.append({'path': relative, 'error': str(exc)})
    summary = {
        'library_sha256': LIBRARY_SHA256,
        'files_discovered': len(rows) + len(errors), 'decoded_xml_files': len(rows),
        'root_types': dict(Counter(row['root'] for row in rows)),
        'widgets': sum(len(row['widgets']) for row in rows),
        'entries': sum(len(row['entries']) for row in rows),
        'connections': sum(len(row['connections']) for row in rows), 'errors': errors,
        'limitations': [
            'Format-specific RC4 decoding and MD5 integrity check, not publisher authentication.',
            'Templates/translations can include shared Editor functionality; runtime Reader availability is unproven.',
            'A declared XML connection is not proof of its native implementation or Linux equivalence.',
            'Root version attributes describe individual resources, not the current Reader executable version.',
        ],
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / 'fx-catalog.json').write_text(json.dumps({'summary': summary, 'files': rows}, ensure_ascii=False, indent=2) + '\n')
    (output / 'fx-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({**summary, 'errors': len(errors)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('foxit_directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    catalog(args.foxit_directory.resolve(), args.output.resolve())
