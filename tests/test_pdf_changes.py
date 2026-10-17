"""Copy-only edits roundtrip through real synthetic PDFs and the worker."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))
sys.path.insert(0, str(APP))
import pdf_changes as changes
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject


class PDFChangeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-copy-edits-')
        self.root = Path(self.temp.name)
        self.source, self.output = self.root / 'source.pdf', self.root / 'result.pdf'
        self.make_pdf()
        self.original = self.source.read_bytes()
        self.identity = hashlib.sha256(self.original).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def make_pdf(self, unsupported=None, readonly=False):
        writer = PdfWriter()
        for _ in range(2):writer.add_blank_page(100, 100)
        writer.add_metadata({'/Title': 'Synthetic copy edits'})
        writer.add_outline_item('Existing', 1)
        writer.add_annotation(0, Text(rect=(10, 10, 20, 20), text='Existing note'))
        writer.add_attachment('keep.txt', b'attachment retained')
        font = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
            NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')}))
        widget = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Annot'),
            NameObject('/Subtype'): NameObject('/Widget'), NameObject('/FT'): NameObject('/Tx'),
            NameObject('/T'): TextStringObject('name'), NameObject('/V'): TextStringObject('Original'),
            NameObject('/Ff'): NumberObject(int(readonly)), NameObject('/MaxLen'): NumberObject(20),
            NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/Rect'): ArrayObject([NumberObject(v) for v in (10, 30, 90, 50)])}))
        writer.pages[0]['/Annots'].append(widget)
        form = DictionaryObject({NameObject('/Fields'): ArrayObject([widget]),
            NameObject('/DA'): TextStringObject('/Helv 10 Tf 0 g'),
            NameObject('/DR'): DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/Helv'): font})})})
        writer.root_object[NameObject('/AcroForm')] = writer._add_object(form)
        if unsupported == 'xfa':form[NameObject('/XFA')] = TextStringObject('synthetic unsupported XFA')
        if unsupported == 'signature':widget.get_object()[NameObject('/FT')] = NameObject('/Sig')
        if unsupported == 'permissions':writer.root_object[NameObject('/Perms')] = DictionaryObject()
        if unsupported == 'portfolio':writer.root_object[NameObject('/Collection')] = DictionaryObject()
        if unsupported == 'encrypted':writer.encrypt('synthetic-password', algorithm='RC4-128')
        writer.write(self.source)

    def save(self, operations):
        return changes.save_edited_copy(self.source, self.output, source_sha256=self.identity, operations=operations)

    def bookmark(self):return {'kind': 'add-bookmark', 'title': 'Novo marcador', 'page': 0}
    def note(self):return {'kind': 'add-note', 'text': 'Nota nova', 'author': 'Teste', 'page': 1, 'rect': [10, 10, 30, 30]}

    def assert_no_output(self):
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.linuxit-copy-*')), [])

    def test_info_reports_identity_pages_and_text_fields_without_writes(self):
        info = changes.inspect_editable_document(self.source)
        self.assertEqual((info['source_sha256'], info['pages']), (self.identity, 2))
        self.assertEqual(info['text_fields'], [{'name': 'name', 'value': 'Original', 'read_only': False}])
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assert_no_output()

    def test_combined_copy_preserves_source_metadata_attachment_and_previous_objects(self):
        result = self.save([self.bookmark(), self.note(), {'kind': 'fill-text-fields', 'values': {'name': 'ação'}}])
        reader = PdfReader(self.output)
        self.assertEqual(len(reader.pages), 2)
        self.assertEqual(reader.metadata.title, 'Synthetic copy edits')
        self.assertEqual([x.title for x in reader.outline], ['Existing', 'Novo marcador'])
        self.assertEqual([reader.get_destination_page_number(x) for x in reader.outline], [1, 0])
        self.assertEqual(next(reader.attachment_list).content, b'attachment retained')
        self.assertEqual(reader.pages[0]['/Annots'][0].get_object()['/Contents'], 'Existing note')
        self.assertEqual(reader.get_fields()['name']['/V'], 'ação')
        self.assertNotIn('/NeedAppearances', reader.root_object['/AcroForm'])
        note = reader.pages[1]['/Annots'][0].get_object()
        self.assertEqual((note['/Contents'], note['/T'], note['/F']), ('Nota nova', 'Teste', 4))
        self.assertNotIn('/Flags', note)
        self.assertEqual(result['operations_applied'], 3)
        self.assertEqual(result['output_sha256'], hashlib.sha256(self.output.read_bytes()).hexdigest())
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_existing_destination_and_original_are_never_overwritten(self):
        self.output.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):self.save([self.bookmark()])
        self.assertEqual(self.output.read_bytes(), b'keep')
        with self.assertRaises(FileExistsError):
            changes.save_edited_copy(self.source, self.source, source_sha256=self.identity, operations=[self.bookmark()])
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_wrong_identity_refuses_before_creating_output(self):
        with self.assertRaisesRegex(ValueError, 'mudou'):
            changes.save_edited_copy(self.source, self.output, source_sha256='0'*64, operations=[self.bookmark()])
        self.assert_no_output()

    def test_invalid_second_operation_discards_entire_batch(self):
        with self.assertRaises(ValueError):self.save([self.bookmark(), {'kind': 'unsupported'}])
        self.assert_no_output()
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_invalid_page_title_and_operation_shapes_are_refused(self):
        for operation in ({**self.bookmark(), 'page': True}, {**self.bookmark(), 'page': 2},
                          {**self.bookmark(), 'title': ''}, {**self.bookmark(), 'unexpected': True}):
            with self.subTest(operation=operation):
                with self.assertRaises(ValueError):self.save([operation])
                self.assert_no_output()

    def test_note_coordinates_are_finite_ordered_and_inside_cropbox(self):
        for rect in ([20, 20, 10, 30], [0, 0, float('nan'), 20], [True, 0, 20, 20], [0, 0, 101, 20]):
            with self.subTest(rect=rect):
                with self.assertRaises(ValueError):self.save([{**self.note(), 'rect': rect}])
                self.assert_no_output()

    def test_read_only_form_field_and_unknown_field_are_refused(self):
        with self.assertRaisesRegex(ValueError, 'não encontrado'):
            self.save([{'kind': 'fill-text-fields', 'values': {'missing': 'x'}}])
        self.make_pdf(readonly=True);self.identity = changes.inspect_editable_document(self.source)['source_sha256']
        with self.assertRaisesRegex(ValueError, 'somente leitura'):
            self.save([{'kind': 'fill-text-fields', 'values': {'name': 'x'}}])
        self.assert_no_output()

    def test_form_max_length_and_value_types_are_enforced(self):
        for value in ('x'*21, 42, None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):self.save([{'kind': 'fill-text-fields', 'values': {'name': value}}])
                self.assert_no_output()

    def test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported(self):
        for kind in ('encrypted', 'signature', 'permissions', 'xfa', 'portfolio'):
            with self.subTest(kind=kind):
                self.make_pdf(unsupported=kind)
                with self.assertRaises(NotImplementedError):changes.inspect_editable_document(self.source)
                identity = hashlib.sha256(self.source.read_bytes()).hexdigest()
                with self.assertRaises(NotImplementedError):
                    changes.save_edited_copy(self.source, self.output, source_sha256=identity, operations=[self.bookmark()])
                self.assert_no_output()

    def test_writer_failure_removes_private_temporary_and_creates_no_destination(self):
        with patch.object(PdfWriter, 'write', side_effect=OSError('synthetic disk failure')):
            with self.assertRaises(OSError):self.save([self.bookmark()])
        self.assert_no_output()

    def test_changed_source_during_serialization_is_refused(self):
        original_write = PdfWriter.write
        def changed(writer, stream):
            result = original_write(writer, stream)
            with self.source.open('ab') as source:source.write(b'\n% changed during edit\n')
            return result
        with patch.object(PdfWriter, 'write', changed):
            with self.assertRaisesRegex(ValueError, 'alterado'):self.save([self.bookmark()])
        self.assert_no_output()

    def test_empty_and_oversized_batches_are_rejected(self):
        for operations in ([], 'not a list', [self.bookmark()]*(changes.MAX_OPERATIONS+1)):
            with self.assertRaises(ValueError):self.save(operations)
            self.assert_no_output()

    def test_worker_inspects_and_saves_a_copy_from_json_without_modifying_source(self):
        cmd = [sys.executable, '-X', 'utf8', str(APP/'worker_cli.py')]
        proc = subprocess.run([*cmd, 'edit-info', str(self.source)], capture_output=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode('utf-8'))
        info = json.loads(proc.stdout)
        request = json.dumps({'source_sha256': info['source_sha256'], 'operations': [self.bookmark()]})
        proc = subprocess.run([*cmd, 'copy-edit', str(self.source), str(self.output)], input=request.encode(), capture_output=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode('utf-8'))
        self.assertEqual(json.loads(proc.stdout)['operations_applied'], 1)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_default_note_rectangle_stays_inside_offset_rotated_cropbox(self):
        writer = PdfWriter(clone_from=PdfReader(self.source))
        page = writer.pages[1]
        page.cropbox.lower_left = (-20, -10)
        page.cropbox.upper_right = (80, 90)
        page.rotate(90)
        writer.write(self.source)
        self.identity = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.save([{**self.note(), 'rect': None}])
        reader = PdfReader(self.output)
        note = reader.pages[1]['/Annots'][0].get_object()
        self.assertEqual(list(note['/Rect']), [-10, 60, 10, 80])
        self.assertEqual(reader.pages[1].rotation, 90)

    def test_nested_field_inherits_read_only_and_max_length(self):
        writer = PdfWriter(clone_from=PdfReader(self.source))
        form = writer.root_object['/AcroForm']
        child_ref = form['/Fields'][0]
        child = child_ref.get_object()
        for key in ('/FT', '/Ff', '/MaxLen'):child.pop(key, None)
        parent = DictionaryObject({NameObject('/T'): TextStringObject('group'), NameObject('/FT'): NameObject('/Tx'),
            NameObject('/Ff'): NumberObject(1), NameObject('/MaxLen'): NumberObject(3),
            NameObject('/Kids'): writer._add_object(ArrayObject([child_ref]))})
        parent_ref = writer._add_object(parent)
        child[NameObject('/Parent')] = parent_ref
        form[NameObject('/Fields')] = ArrayObject([parent_ref])
        writer.write(self.source)
        info = changes.inspect_editable_document(self.source)
        self.assertEqual([f['name'] for f in info['text_fields']], ['group.name'])
        self.assertTrue(info['text_fields'][0]['read_only'])
        self.identity = info['source_sha256']
        with self.assertRaisesRegex(ValueError, 'somente leitura'):
            self.save([{'kind': 'fill-text-fields', 'values': {'group.name': 'ab'}}])
        parent[NameObject('/Ff')] = NumberObject(0)
        writer.write(self.source)
        self.identity = changes.inspect_editable_document(self.source)['source_sha256']
        with self.assertRaisesRegex(ValueError, 'limite de caracteres'):
            self.save([{'kind': 'fill-text-fields', 'values': {'group.name': 'abcd'}}])
        self.assert_no_output()
        self.save([{'kind': 'fill-text-fields', 'values': {'group.name': 'abc'}}])
        self.assertEqual(PdfReader(self.output).get_fields()['group.name']['/V'], 'abc')


if __name__ == '__main__':unittest.main()
