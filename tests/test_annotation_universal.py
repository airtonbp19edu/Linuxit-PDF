"""A6: one capability rule for every non-form annotation type, enforced when saving a copy."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'));sys.path.insert(0, str(APP))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject, DictionaryObject, FloatObject,
                           NameObject, NumberObject, TextStringObject)
from pdf_changes import inspect_editable_document, save_edited_copy


def numbers(*values):return ArrayObject(FloatObject(v) for v in values)


def form(writer, data, box):
    stream = DecodedStreamObject();stream.set_data(data)
    stream.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Form'),
                   NameObject('/BBox'): numbers(*box)})
    return writer._add_object(stream)


def annot(subtype, rect, **extra):
    note = DictionaryObject({NameObject('/Type'): NameObject('/Annot'), NameObject('/Subtype'): NameObject(subtype),
                             NameObject('/Rect'): numbers(*rect), NameObject('/F'): NumberObject(4)})
    for key, value in extra.items():note[NameObject('/' + key)] = value
    return note


# Index → meaning, in /Annots order on page 0.
LINK, ATTACH, STAMP, NOTE, REPLY, POPUP, SCREEN, PLAYER, UNKNOWN, WIDGET, LOCKED, ARROW, POLYGON, TAGGED, FIXED = range(15)


def build(path):
    writer = PdfWriter();page = writer.add_blank_page(300, 300)
    refs = []
    def add(note):
        ref = writer._add_object(note);refs.append(ref);return ref
    add(annot('/Link', [10, 270, 60, 290], QuadPoints=numbers(10, 290, 60, 290, 10, 270, 60, 270),
              Contents=TextStringObject('link')))
    payload = DecodedStreamObject();payload.set_data(b'attached bytes');payload[NameObject('/Type')] = NameObject('/EmbeddedFile')
    spec = DictionaryObject({NameObject('/Type'): NameObject('/Filespec'), NameObject('/F'): TextStringObject('a.txt'),
                             NameObject('/EF'): DictionaryObject({NameObject('/F'): writer._add_object(payload)})})
    add(annot('/FileAttachment', [70, 270, 90, 290], FS=spec, Contents=TextStringObject('anexo'), T=TextStringObject('A')))
    stamp_ap = form(writer, b'1 0 0 rg 0 0 40 20 re f', [0, 0, 40, 20])
    add(annot('/Stamp', [100, 250, 140, 270], AP=DictionaryObject({NameObject('/N'): stamp_ap}), Contents=TextStringObject('carimbo')))
    note = annot('/Text', [150, 250, 170, 270], Contents=TextStringObject('nota'), T=TextStringObject('Ana'))
    note_ref = add(note)
    reply = annot('/Text', [150, 250, 170, 270], Contents=TextStringObject('resposta'), IRT=note_ref, RT=NameObject('/R'))
    add(reply)
    popup = annot('/Popup', [180, 200, 280, 260], Parent=note_ref, Open=BooleanObject(False))
    note[NameObject('/Popup')] = add(popup)
    screen_ref = add(annot('/Screen', [10, 150, 110, 230], Contents=TextStringObject('tela')))
    add(annot('/Link', [120, 150, 140, 170], A=DictionaryObject({NameObject('/S'): NameObject('/Rendition'), NameObject('/AN'): screen_ref})))
    add(annot('/Foo', [150, 150, 190, 170], AP=DictionaryObject({NameObject('/N'): form(writer, b'0 0 1 rg 0 0 40 20 re f', [0, 0, 40, 20])})))
    add(annot('/Widget', [200, 150, 240, 170], FT=NameObject('/Tx'), T=TextStringObject('field')))
    add(annot('/Square', [10, 100, 60, 140], F=NumberObject(4 | 128), Contents=TextStringObject('travado')))
    add(annot('/Line', [70, 100, 170, 120], L=numbers(75, 110, 165, 110),
              LE=ArrayObject([NameObject('/None'), NameObject('/OpenArrow')]),
              AP=DictionaryObject({NameObject('/N'): form(writer, b'0 g 5 10 m 95 10 l S', [0, 0, 100, 20])})))
    add(annot('/Polygon', [180, 90, 280, 140], Vertices=numbers(185, 95, 275, 95, 230, 135), C=numbers(0, 0, 0),
              AP=DictionaryObject({NameObject('/N'): form(writer, b'0 G 5 5 m 95 5 l 50 45 l h S', [0, 0, 100, 50])})))
    add(annot('/Text', [10, 40, 30, 60], StructParent=NumberObject(0), Contents=TextStringObject('marcada')))
    add(annot('/Text', [40, 40, 60, 60], F=NumberObject(4 | 8), Contents=TextStringObject('fixa')))
    page[NameObject('/Annots')] = ArrayObject(refs)
    with open(path, 'wb') as handle:writer.write(handle)


class UniversalAnnotationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root = Path(self.temp.name)
        self.source = self.root / 'source.pdf';build(self.source);self.original = self.source.read_bytes();self.count = 0

    def save(self, *operations, source=None):
        source = source or self.source;self.count += 1;target = self.root / f'out-{self.count}.pdf'
        save_edited_copy(source, target, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), operations=list(operations))
        self.assertEqual(self.source.read_bytes(), self.original)
        return target

    def refuse(self, operation, message):
        before = sorted(p.name for p in self.root.iterdir())
        with self.assertRaisesRegex(ValueError, message):self.save(operation)
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), before)

    def annots(self, path):return [r.get_object() for r in PdfReader(path).pages[0]['/Annots']]

    def records(self, path=None):return {r['index']: r for r in inspect_editable_document(path or self.source)['annotations']}

    def test_records_list_every_non_form_type_with_capabilities_and_reasons(self):
        records = self.records()
        self.assertNotIn(WIDGET, records);self.assertNotIn(POPUP, records)
        self.assertEqual(records[UNKNOWN]['subtype'], '/Foo');self.assertEqual(records[SCREEN]['label'], 'Tela de mídia')
        expect = {  # movable, resizable, deletable, text_editable, color_editable, opacity_editable
            LINK: (1, 1, 1, 1, 0, 1), ATTACH: (1, 1, 1, 1, 1, 1), STAMP: (1, 1, 1, 1, 0, 1), NOTE: (1, 1, 0, 1, 1, 1),
            REPLY: (1, 1, 1, 1, 1, 1), SCREEN: (1, 1, 0, 1, 0, 1), UNKNOWN: (1, 1, 1, 1, 0, 1), LOCKED: (0, 0, 0, 1, 0, 0),
            ARROW: (1, 1, 1, 1, 0, 1), POLYGON: (1, 1, 1, 1, 1, 1), TAGGED: (1, 1, 0, 1, 1, 1), FIXED: (1, 0, 1, 1, 1, 1)}
        keys = ('movable', 'resizable', 'deletable', 'text_editable', 'color_editable', 'opacity_editable')
        for index, flags in expect.items():
            with self.subTest(index=index, subtype=records[index]['subtype']):
                self.assertEqual(tuple(int(records[index][k]) for k in keys), flags)
        self.assertIn('respostas', records[NOTE]['reasons']['delete'])
        self.assertIn('mídia', records[SCREEN]['reasons']['delete'])
        self.assertIn('acessibilidade', records[TAGGED]['reasons']['delete'])
        self.assertIn('NoZoom', records[FIXED]['reasons']['resize'])
        self.assertIn('travada', records[LOCKED]['reasons']['locked'])
        self.assertIn('aparência própria', records[ARROW]['reasons']['color'])
        self.assertFalse(records[LINK]['has_author']);self.assertTrue(records[ATTACH]['has_author'])

    def test_move_shifts_all_geometry_and_the_popup_but_not_replies(self):
        out = self.save({'kind': 'move-annotation', 'page': 0, 'index': LINK, 'dx': 5, 'dy': -10},
                        {'kind': 'move-annotation', 'page': 0, 'index': NOTE, 'dx': -20, 'dy': -30},
                        {'kind': 'move-annotation', 'page': 0, 'index': POLYGON, 'dx': 10, 'dy': 5})
        notes = self.annots(out)
        self.assertEqual([float(v) for v in notes[LINK]['/Rect']], [15, 260, 65, 280])
        self.assertEqual([float(v) for v in notes[LINK]['/QuadPoints']], [15, 280, 65, 280, 15, 260, 65, 260])
        self.assertEqual([float(v) for v in notes[NOTE]['/Rect']], [130, 220, 150, 240])
        self.assertEqual([float(v) for v in notes[POPUP]['/Rect']], [160, 170, 260, 230])
        self.assertEqual([float(v) for v in notes[REPLY]['/Rect']], [150, 250, 170, 270])
        self.assertIs(notes[POPUP]['/Parent'].get_object(), notes[NOTE]);self.assertIs(notes[NOTE]['/Popup'].get_object(), notes[POPUP])
        self.assertEqual([float(v) for v in notes[POLYGON]['/Vertices']], [195, 100, 285, 100, 240, 140])

    def test_delete_keeps_links_consistent_and_refuses_dangling_ones(self):
        self.refuse({'kind': 'delete-annotation', 'page': 0, 'index': NOTE}, 'respostas')
        self.refuse({'kind': 'delete-annotation', 'page': 0, 'index': SCREEN}, 'mídia')
        self.refuse({'kind': 'delete-annotation', 'page': 0, 'index': TAGGED}, 'acessibilidade')
        # Leaf reply first, then the note: its popup goes with it.
        out = self.save({'kind': 'delete-annotation', 'page': 0, 'index': REPLY},
                        {'kind': 'delete-annotation', 'page': 0, 'index': NOTE})
        subtypes = [n['/Subtype'] for n in self.annots(out)]
        self.assertNotIn('/Popup', subtypes);self.assertEqual(subtypes.count('/Text'), 2)
        out = self.save({'kind': 'delete-annotation', 'page': 0, 'index': ATTACH})
        self.assertNotIn('/FileAttachment', [n['/Subtype'] for n in self.annots(out)])
        self.assertEqual(len(self.annots(out)), 14)

    def test_resize_maps_geometry_and_keeps_foreign_appearances(self):
        before = self.annots(self.source)
        out = self.save({'kind': 'resize-annotation', 'page': 0, 'index': STAMP, 'rect': [100, 210, 180, 250]},
                        {'kind': 'resize-annotation', 'page': 0, 'index': ARROW, 'rect': [70, 100, 270, 140]},
                        {'kind': 'resize-annotation', 'page': 0, 'index': POLYGON, 'rect': [180, 40, 280, 140]})
        notes = self.annots(out)
        self.assertEqual([float(v) for v in notes[STAMP]['/Rect']], [100, 210, 180, 250])
        self.assertEqual(notes[STAMP]['/AP']['/N'].get_object().get_data(), before[STAMP]['/AP']['/N'].get_object().get_data())
        self.assertEqual([round(float(v), 3) for v in notes[ARROW]['/L']], [80, 120, 260, 120])
        self.assertEqual(notes[ARROW]['/AP']['/N'].get_object().get_data(), b'0 g 5 10 m 95 10 l S')
        self.assertEqual([round(float(v), 3) for v in notes[POLYGON]['/Vertices']], [185, 50, 275, 50, 230, 130])
        self.assertNotEqual(notes[POLYGON]['/AP']['/N'].get_object().get_data(), b'0 G 5 5 m 95 5 l 50 45 l h S')
        self.refuse({'kind': 'resize-annotation', 'page': 0, 'index': FIXED, 'rect': [40, 40, 80, 80]}, 'NoZoom')

    def test_opacity_wraps_any_appearance_once_and_colour_only_where_faithful(self):
        out = self.save({'kind': 'style-annotation', 'page': 0, 'index': STAMP, 'color': None, 'opacity': .5},
                        {'kind': 'style-annotation', 'page': 0, 'index': ATTACH, 'color': [0, 0, 1], 'opacity': 1})
        notes = self.annots(out);wrapper = notes[STAMP]['/AP']['/N'].get_object()
        self.assertIn(b'/LinuxitOriginal Do', wrapper.get_data())
        original = wrapper['/Resources']['/XObject']['/LinuxitOriginal'].get_object()
        self.assertEqual(original.get_data(), b'1 0 0 rg 0 0 40 20 re f');self.assertEqual(float(notes[STAMP]['/CA']), .5)
        self.assertEqual([float(c) for c in notes[ATTACH]['/C']], [0, 0, 1]);self.assertNotIn('/AP', notes[ATTACH])
        again = self.save({'kind': 'style-annotation', 'page': 0, 'index': STAMP, 'color': None, 'opacity': .3}, source=out)
        wrapper = self.annots(again)[STAMP]['/AP']['/N'].get_object()
        self.assertEqual(wrapper['/Resources']['/XObject']['/LinuxitOriginal'].get_object().get_data(), b'1 0 0 rg 0 0 40 20 re f')
        self.assertAlmostEqual(float(wrapper['/Resources']['/ExtGState']['/LinuxitOpacity']['/ca']), .3)
        self.refuse({'kind': 'style-annotation', 'page': 0, 'index': STAMP, 'color': [0, 0, 1], 'opacity': 1}, 'aparência própria')
        if shutil.which('pdftocairo'):
            from PIL import Image
            base = self.root / 'render'
            subprocess.run(['pdftocairo', '-png', '-r', '72', '-singlefile', str(out), str(base)], check=True, timeout=60)
            r, g, b = Image.open(str(base) + '.png').convert('RGB').getpixel((120, 300 - 260))
            self.assertGreater(r, 200);self.assertTrue(100 < g < 160 and 100 < b < 160, (r, g, b))  # red at 50%

    def test_locks_and_text_rules(self):
        for operation in ({'kind': 'move-annotation', 'page': 0, 'index': LOCKED, 'dx': 1, 'dy': 1},
                          {'kind': 'resize-annotation', 'page': 0, 'index': LOCKED, 'rect': [10, 100, 70, 150]},
                          {'kind': 'style-annotation', 'page': 0, 'index': LOCKED, 'color': None, 'opacity': .5},
                          {'kind': 'delete-annotation', 'page': 0, 'index': LOCKED}):
            with self.subTest(kind=operation['kind']):self.refuse(operation, 'travada')
        out = self.save({'kind': 'update-annotation', 'page': 0, 'index': LOCKED, 'text': 'novo', 'author': ''},
                        {'kind': 'update-annotation', 'page': 0, 'index': LINK, 'text': 'descrição do link', 'author': ''},
                        {'kind': 'update-annotation', 'page': 0, 'index': UNKNOWN, 'text': 'desconhecida', 'author': ''})
        notes = self.annots(out)
        self.assertEqual(notes[LOCKED]['/Contents'], 'novo');self.assertEqual(notes[LINK]['/Contents'], 'descrição do link')
        self.assertNotIn('/T', notes[LINK])
        self.refuse({'kind': 'update-annotation', 'page': 0, 'index': LINK, 'text': 'x', 'author': 'Ana'}, 'não tem autor')
        self.refuse({'kind': 'update-annotation', 'page': 0, 'index': WIDGET, 'text': 'x', 'author': ''}, 'formulário')
        self.refuse({'kind': 'move-annotation', 'page': 0, 'index': POPUP, 'dx': 1, 'dy': 1}, 'Popup')

    def test_unknown_and_media_types_move_resize_and_fade_without_rewriting_drawings(self):
        out = self.save({'kind': 'move-annotation', 'page': 0, 'index': UNKNOWN, 'dx': 0, 'dy': -100},
                        {'kind': 'resize-annotation', 'page': 0, 'index': SCREEN, 'rect': [10, 150, 210, 230]},
                        {'kind': 'style-annotation', 'page': 0, 'index': UNKNOWN, 'color': None, 'opacity': .4})
        notes = self.annots(out)
        self.assertEqual([float(v) for v in notes[UNKNOWN]['/Rect']], [150, 50, 190, 70])
        self.assertEqual([float(v) for v in notes[SCREEN]['/Rect']], [10, 150, 210, 230])
        self.assertIs(notes[PLAYER]['/A']['/AN'].get_object(), notes[SCREEN])
        self.assertEqual(notes[UNKNOWN]['/AP']['/N'].get_object()['/Resources']['/XObject']['/LinuxitOriginal'].get_object().get_data(),
                         b'0 0 1 rg 0 0 40 20 re f')


if __name__ == '__main__':unittest.main()
