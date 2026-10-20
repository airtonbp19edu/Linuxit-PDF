#!/usr/bin/env python3
"""Generate the own synthetic fixtures used by the S12 acceptance cases.

Only the pinned BSD pypdf distributed with the application is used. No Foxit
file, resource or observation is involved. The committed bytes are identified
by SHA-256 in manifest.json; the acceptance runner refuses mismatched files.
Run with --check to confirm the committed manifest without writing anything.
"""
import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'app' / 'vendor'))
from pypdf import PdfWriter  # noqa: E402
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject, NameObject,  # noqa: E402
                           NumberObject, TextStringObject)

FOLDER = Path(__file__).resolve().parent / 'fixtures'


def _font(writer):
    return writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')}))


def _text_page(writer, font, text, size=(200, 200), extra=b''):
    page = writer.add_blank_page(*size)
    page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
    stream = DecodedStreamObject()
    stream.set_data(b'BT /F1 12 Tf 10 100 Td (' + text.encode('ascii') + b') Tj ET\n' + extra)
    page[NameObject('/Contents')] = writer._add_object(stream)
    return page


def _bytes(writer):
    writer._ID = None  # no random file identifier: same input, same bytes
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def eight_pages():
    writer = PdfWriter();font = _font(writer)
    for number in range(1, 9):_text_page(writer, font, f'PAGE{number}', (420, 595))
    return _bytes(writer)


def proximity():
    writer = PdfWriter();_text_page(writer, _font(writer), 'alfa um dois beta')
    return _bytes(writer)


def form():
    writer = PdfWriter();font = _font(writer)
    page = writer.add_blank_page(300, 200)
    fields = []
    for name, value, flags, max_len, y in (('nome', 'Original', 0, None, 150), ('fixo', 'Bloqueado', 1, None, 100),
                                           ('curto', 'abc', 0, 5, 50)):
        widget = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
            NameObject('/FT'): NameObject('/Tx'), NameObject('/T'): TextStringObject(name),
            NameObject('/V'): TextStringObject(value), NameObject('/Ff'): NumberObject(flags),
            NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/Rect'): ArrayObject([NumberObject(v) for v in (20, y, 280, y + 20)])})
        if max_len is not None:widget[NameObject('/MaxLen')] = NumberObject(max_len)
        reference = writer._add_object(widget);fields.append(reference)
        page.setdefault(NameObject('/Annots'), ArrayObject()).append(reference)
    writer.root_object[NameObject('/AcroForm')] = writer._add_object(DictionaryObject({
        NameObject('/Fields'): ArrayObject(fields), NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
        NameObject('/DR'): DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/Helv'): font})})}))
    return _bytes(writer)


def numeric_form():
    writer = PdfWriter();font = _font(writer)
    page = writer.add_blank_page(300, 200)
    action = lambda script: DictionaryObject({NameObject('/S'): NameObject('/JavaScript'), NameObject('/JS'): TextStringObject(script)})
    keystroke = 'AFNumber_Keystroke(2, 2, 0, 0, "", true);'
    fields = []
    for name, y, flags, events in (
            ('preco', 150, 0, {'/K': keystroke}), ('quantidade', 100, 0, {'/K': keystroke}),
            ('total', 50, 1, {'/C': 'AFSimple_Calculate("PRD", ["preco", "quantidade"]);',
                              '/F': 'AFNumber_Format(2, 2, 0, 0, "R$ ", true);'})):
        widget = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
            NameObject('/FT'): NameObject('/Tx'), NameObject('/T'): TextStringObject(name), NameObject('/V'): TextStringObject('0'),
            NameObject('/Ff'): NumberObject(flags), NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/Rect'): ArrayObject([NumberObject(v) for v in (20, y, 280, y + 20)]),
            NameObject('/AA'): DictionaryObject({NameObject(k): action(v) for k, v in events.items()})})
        reference = writer._add_object(widget);fields.append(reference)
        page.setdefault(NameObject('/Annots'), ArrayObject()).append(reference)
    writer.root_object[NameObject('/AcroForm')] = writer._add_object(DictionaryObject({
        NameObject('/Fields'): ArrayObject(fields), NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
        NameObject('/DR'): DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/Helv'): font})})}))
    return _bytes(writer)


def date_form():
    writer = PdfWriter();font = _font(writer)
    page = writer.add_blank_page(300, 120)
    action = lambda script: DictionaryObject({NameObject('/S'): NameObject('/JavaScript'), NameObject('/JS'): TextStringObject(script)})
    widget = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
        NameObject('/FT'): NameObject('/Tx'), NameObject('/T'): TextStringObject('vencimento'), NameObject('/V'): TextStringObject(''),
        NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
        NameObject('/Rect'): ArrayObject([NumberObject(v) for v in (20, 50, 280, 70)]),
        NameObject('/AA'): DictionaryObject({NameObject('/K'): action('AFDate_KeystrokeEx("dd/mm/yyyy");'),
                                             NameObject('/F'): action('AFDate_FormatEx("dd/mm/yyyy");')})})
    reference = writer._add_object(widget);page[NameObject('/Annots')] = ArrayObject([reference])
    writer.root_object[NameObject('/AcroForm')] = writer._add_object(DictionaryObject({
        NameObject('/Fields'): ArrayObject([reference]), NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
        NameObject('/DR'): DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/Helv'): font})})}))
    return _bytes(writer)


def mask_form():
    writer = PdfWriter();font = _font(writer)
    page = writer.add_blank_page(300, 150)
    action = lambda script: DictionaryObject({NameObject('/S'): NameObject('/JavaScript'), NameObject('/JS'): TextStringObject(script)})
    fields = []
    for name, y, keystroke, display in (('cep', 90, 'AFSpecial_KeystrokeEx("99999-999");', 'AFSpecial_KeystrokeEx("99999-999");'),
                                        ('telefone', 40, 'AFSpecial_Keystroke(2);', 'AFSpecial_Format(2);')):
        widget = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject('/Widget'),
            NameObject('/FT'): NameObject('/Tx'), NameObject('/T'): TextStringObject(name), NameObject('/V'): TextStringObject(''),
            NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/Rect'): ArrayObject([NumberObject(v) for v in (20, y, 280, y + 20)]),
            NameObject('/AA'): DictionaryObject({NameObject('/K'): action(keystroke), NameObject('/F'): action(display)})})
        reference = writer._add_object(widget);fields.append(reference)
        page.setdefault(NameObject('/Annots'), ArrayObject()).append(reference)
    writer.root_object[NameObject('/AcroForm')] = writer._add_object(DictionaryObject({
        NameObject('/Fields'): ArrayObject(fields), NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
        NameObject('/DR'): DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/Helv'): font})})}))
    return _bytes(writer)


def layers():
    writer = PdfWriter();font = _font(writer)
    groups = [writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/OCG'),
                                                   NameObject('/Name'): TextStringObject(name)}))
              for name in ('Base', 'Notas')]
    page = _text_page(writer, font, 'camadas', extra=b'/OC /MC0 BDC BT /F1 12 Tf 10 60 Td (notas) Tj ET EMC\n')
    page['/Resources'][NameObject('/Properties')] = DictionaryObject({NameObject('/MC0'): groups[1]})
    writer.root_object[NameObject('/OCProperties')] = DictionaryObject({
        NameObject('/OCGs'): ArrayObject(groups),
        NameObject('/D'): DictionaryObject({NameObject('/Order'): ArrayObject(groups),
                                            NameObject('/OFF'): ArrayObject([groups[1]])})})
    return _bytes(writer)


def dangerous_attachment():
    writer = PdfWriter();writer.add_blank_page(200, 200)
    writer.add_attachment('../fora.txt', b'conteudo sintetico que nao deve sair da pasta\n')
    return _bytes(writer)


FIXTURES = {
    'oito-paginas.pdf': (eight_pages, 'Oito páginas PAGE1..PAGE8 em A4 retrato para imposição.'),
    'proximidade.pdf': (proximity, 'Uma página com "alfa um dois beta": duas palavras entre alfa e beta.'),
    'formulario.pdf': (form, 'AcroForm Tx: nome editável, fixo ReadOnly e curto com MaxLen 5; sem XFA ou assinatura.'),
    'formulario-numerico.pdf': (numeric_form, 'AcroForm: preco e quantidade com AFNumber_Keystroke (vírgula decimal); total calculado com AFNumber_Format em reais.'),
    'formulario-data.pdf': (date_form, 'AcroForm: campo vencimento com AFDate_KeystrokeEx e AFDate_FormatEx("dd/mm/yyyy").'),
    'formulario-mascaras.pdf': (mask_form, 'AcroForm: cep com máscara livre 99999-999 e telefone com AFSpecial_Format(2).'),
    'camadas.pdf': (layers, 'Dois OCGs nomeados: Base visível e Notas desligada na configuração padrão.'),
    'anexo-nome-perigoso.pdf': (dangerous_attachment, 'Um anexo de catálogo chamado ../fora.txt.'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare generated bytes with the manifest only')
    args = parser.parse_args()
    manifest = {'schema': 'linuxit-acceptance-fixtures-v1',
                'provenance': 'Own synthetic PDFs generated by testes/aceitacao/gerar_fixtures.py with the pinned BSD pypdf; no Foxit material.',
                'files': []}
    for name, (build, description) in FIXTURES.items():
        data = build()
        manifest['files'].append({'file': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                                  'description': description})
        if args.check:
            stored = (FOLDER / name).read_bytes()
            if stored != data:raise SystemExit(f'{name}: committed bytes differ from the generator')
        else:
            FOLDER.mkdir(exist_ok=True)
            (FOLDER / name).write_bytes(data)
    text = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if (FOLDER / 'manifest.json').read_text(encoding='utf-8') != text:raise SystemExit('manifest.json differs')
        print('fixtures match')
    else:
        (FOLDER / 'manifest.json').write_text(text, encoding='utf-8', newline='\n')
        print(json.dumps([f['file'] for f in manifest['files']]))


if __name__ == '__main__':
    main()
