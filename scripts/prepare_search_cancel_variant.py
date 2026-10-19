#!/usr/bin/env python3
"""Create a bounded synthetic D12 variant; never launch or control the original."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app/vendor'))
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject


def create(output, count):
    if not 1 <= count <= 5000:
        raise ValueError('Page count must be between 1 and 5000')
    if output.exists() or output.with_suffix('.json').exists():
        raise FileExistsError('Preserve existing fixture and manifest')
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({
        NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'),
        NameObject('/BaseFont'): NameObject('/Helvetica')}))
    for number in range(count):
        page = writer.add_blank_page(595, 842)
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        lines = ['BT /F1 8 Tf 40 800 Td 11 TL', f'(PAGE {number+1:05d} sintese local) Tj']
        for row in range(60):
            lines.append(f'T* (LINHA {row:02d} documento sintetico de leitura busca controle paginas texto sem dados privados.) Tj')
        lines.extend(['T* (alvo) Tj', 'ET'])
        stream = DecodedStreamObject()
        stream.set_data(('\n'.join(lines) + '\n').encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(stream.flate_encode())
    writer.add_metadata({'/Title': f'Linuxit P03 D12 corpus bounded {count} pages',
                         '/Author': 'Linuxit synthetic fixture'})
    with output.open('xb') as destination:
        writer.write(destination)
    if output.stat().st_size >= 16 * 1024 * 1024:
        raise ValueError('Fixture exceeded byte bound; file preserved for diagnosis')
    reader = PdfReader(output)
    samples = sorted({0, (count - 1) // 2, count - 1})
    if len(reader.pages) != count or not all(reader.pages[i].extract_text().count('alvo') == 1 for i in samples):
        raise ValueError('Generated fixture validation failed; preserve for diagnosis')
    result = {'schema': 'linuxit-d12-fixture-variant-v1', 'name': output.name,
              'pages': count, 'dense_lines_per_page': 60, 'query': 'alvo',
              'occurrences_per_page': 1, 'bytes': output.stat().st_size,
              'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'limits': {'pages': 5000, 'bytes': 16 * 1024 * 1024},
              'sample_pages_extracted': [i + 1 for i in samples],
              'original_ten_inputs_changed': False, 'original_executed': False,
              'cancellation_proved': False}
    with output.with_suffix('.json').open('x', encoding='utf-8') as manifest:
        json.dump(result, manifest, indent=2)
        manifest.write('\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pages', type=int, default=5000)
    args = parser.parse_args()
    print(json.dumps(create(args.output, args.pages)))


if __name__ == '__main__':
    main()
