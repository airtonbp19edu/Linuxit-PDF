#!/usr/bin/env python3
"""Build the own corpus of damaged PDFs (E17) and its manifest with expected outcomes.

Every fixture is derived deterministically from one synthetic two-page PDF written
here by hand (no third-party PDFs, no Foxit material). The expected outcome of each
fixture is the own reading contract: open, recover only with consent, or refuse
without inventing pages. `--check` regenerates in memory and compares with the files.
"""
import argparse, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'testes/fixtures/danificados'


def base_pdf():
    """Two pages, text 'alpha first page' and 'beta second page', classic xref."""
    objects = [b'<< /Producer (Linuxit corpus) >>',
               b'<< /Type /Pages /Count 2 /Kids [ 5 0 R 7 0 R ] >>',
               b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
    for number, text in ((6, b'alpha first page'), (8, b'beta second page')):
        stream = b'BT /F1 12 Tf 10 100 Td (' + text + b') Tj ET'
        objects.append(b'<< /Type /Page /Resources << /Font << /F1 4 0 R >> >> /MediaBox [ 0 0 200 200 ] /Parent 2 0 R /Contents '
                       + str(number).encode() + b' 0 R >>')
        objects.append(b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'\nendstream')
    out = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offsets = []
    for index, body in enumerate(objects, 1):
        offsets.append(len(out));out += str(index).encode() + b' 0 obj\n' + body + b'\nendobj\n'
    xref = len(out)
    out += b'xref\n0 ' + str(len(objects) + 1).encode() + b'\n0000000000 65535 f \n'
    out += b''.join(b'%010d 00000 n \n' % o for o in offsets)
    out += b'trailer\n<< /Size ' + str(len(objects) + 1).encode() + b' /Root 3 0 R >>\nstartxref\n' + str(xref).encode() + b'\n%%EOF\n'
    return bytes(out)


BOTH = ['alpha first page', 'beta second page']


def corpus():
    base = base_pdf();xref = base.index(b'xref\n')
    shifted = base[:xref] + re.sub(rb'(\d{10}) 00000 n', lambda m: b'%010d 00000 n' % (int(m.group(1)) + 7), base[xref:])
    rows = [
        ('integro.pdf', base, 'Sem dano (controle).', dict(open='ready', pages=2, text=BOTH, repairs=[])),
        ('startxref-errado.pdf', re.sub(rb'(startxref\s+)\d+', rb'\g<1>1', base), 'startxref aponta para o byte 1.',
         dict(open='recovery_required', recovered=dict(pages=2, text=BOTH, repairs=['xref']))),
        ('xref-deslocado.pdf', shifted, 'Todas as entradas da tabela xref deslocadas 7 bytes.',
         dict(open='recovery_required', recovered=dict(pages=2, text=BOTH, repairs=['xref']))),
        ('sem-xref-trailer.pdf', base[:xref], 'Arquivo cortado antes da tabela xref: sem xref, trailer e %%EOF.',
         dict(open='recovery_required', recovered=dict(pages=2, text=BOTH, repairs=['fim_do_arquivo', 'xref']))),
        ('sem-eof.pdf', base.replace(b'%%EOF', b''), 'Marcador %%EOF removido.',
         dict(open='recovery_required', recovered=dict(pages=2, text=BOTH, repairs=['fim_do_arquivo']))),
        ('length-errado.pdf', base.replace(b'/Length 47', b'/Length 30', 1), '/Length do primeiro fluxo menor que o real.',
         dict(open='recovery_required', recovered=dict(pages=2, text=BOTH, repairs=['estrutura']))),
        ('stream-truncado.pdf', base[:base.index(b'beta second') + 4], 'Arquivo cortado no meio do fluxo da página 2.',
         dict(open='recovery_required', recovered=dict(pages=2, text=['alpha first page', ''], repairs=['conteudo_ilegivel', 'fim_do_arquivo', 'xref']))),
        ('conteudo-ausente.pdf', base.replace(b'/Contents 8 0 R', b'/Contents 98 0 R'), 'Página 2 aponta para um fluxo de conteúdo inexistente.',
         dict(open='recovery_required', recovered=dict(pages=2, text=['alpha first page', ''], repairs=['conteudo_ilegivel', 'objeto_ausente']))),
        ('pagina-ausente.pdf', base.replace(b'/Kids [ 5 0 R 7 0 R ]', b'/Kids [ 5 0 R 97 0 R ]'), 'A árvore de páginas aponta para uma página inexistente.',
         dict(open='recovery_required', recovered=dict(pages=1, text=['alpha first page'], repairs=['objeto_ausente', 'pagina_ausente']))),
        ('catalogo-sem-paginas.pdf', base.replace(b'/Pages 2 0 R', b'/Pages 96 0 R'), 'O catálogo aponta para uma árvore de páginas inexistente.',
         dict(open='recovery_required', refused=True)),
        ('cabecalho-invalido.pdf', b'NOTAPDF' + base[8:], 'Cabeçalho %PDF trocado por bytes inválidos.',
         dict(open='recovery_required', recovered=dict(pages=2, text=BOTH, repairs=['cabecalho', 'xref']))),
        ('nao-pdf.pdf', bytes(range(256)) * 8, 'Bytes arbitrários com extensão .pdf.', dict(open='recovery_required', refused=True)),
    ]
    assert base.count(b'/Length 47') == 2, 'base stream length changed'
    return rows


def manifest(rows):
    return {'schema': 'linuxit-damaged-corpus-v1',
            'provenance': 'Own synthetic PDFs from scripts/gerar_corpus_danificado.py; no third-party or Foxit material.',
            'contract': 'Abrir direto só sem reparo; com dano, pedir consentimento; recuperar sem inventar páginas (conteúdo perdido fica em branco, página inexistente é omitida); recusar sem cópia de leitura quando não há páginas.',
            'files': [dict(file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), damage=damage, expected=expected)
                      for name, data, damage, expected in rows]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument('--check', action='store_true')
    args = parser.parse_args();rows = corpus();expected = manifest(rows)
    if args.check:
        current = json.loads((FOLDER / 'corpus.json').read_text(encoding='utf-8'))
        assert current == expected, 'manifest differs from generator'
        for name, data, _, _ in rows:assert (FOLDER / name).read_bytes() == data, name
        print(json.dumps({'checked': len(rows)}));return
    FOLDER.mkdir(parents=True, exist_ok=True)
    for name, data, _, _ in rows:(FOLDER / name).write_bytes(data)
    (FOLDER / 'corpus.json').write_text(json.dumps(expected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'written': len(rows)}))


if __name__ == '__main__':
    main()
