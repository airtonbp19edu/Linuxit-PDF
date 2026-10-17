"""Real PDF name trees and annotation-only attachments, with malformed inputs."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, PropertyMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
import pdf_attachments as attachments
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, EmbeddedFile, NameObject, NumberObject


class AttachmentTreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-trees-')
        self.root = Path(self.temp.name)
        self.pdf = self.root / 'tree.pdf'
        self.output = self.root / 'output'
        self.output.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def writer(self):
        writer = PdfWriter()
        writer.add_blank_page(100, 100)
        writer.add_attachment('same.txt', b'first')
        writer.add_attachment('same.txt', b'second')
        tree = writer.root_object['/Names']['/EmbeddedFiles']
        pairs = tree.pop('/Names')
        return writer, tree, pairs

    def save_and_extract(self, writer, expected):
        writer.write(self.pdf)
        original = self.pdf.read_bytes()
        listing = attachments.list_attachments(self.pdf)
        self.assertEqual(len(listing['attachments']), len(expected))
        for index, payload in enumerate(expected):
            folder = self.output / str(index)
            folder.mkdir()
            result = attachments.extract_attachment(self.pdf, index, folder, source_sha256=listing['source_sha256'])
            self.assertEqual(Path(result['path']).read_bytes(), payload)
        self.assertEqual(original, self.pdf.read_bytes())
        return listing

    def test_nested_tree_preserves_duplicate_name_indices_and_bytes(self):
        writer, tree, pairs = self.writer()
        leaves = [writer._add_object(DictionaryObject({NameObject('/Names'): ArrayObject(pairs[i:i+2])})) for i in (0, 2)]
        branch = writer._add_object(DictionaryObject({NameObject('/Kids'): ArrayObject(leaves)}))
        tree[NameObject('/Kids')] = ArrayObject([branch])
        listing = self.save_and_extract(writer, [b'first', b'second'])
        self.assertEqual([x['name'] for x in listing['attachments']], ['same.txt', 'same.txt'])
        self.assertEqual([x['origin'] for x in listing['attachments']], ['catalog', 'catalog'])

    def test_annotation_only_files_are_listed_and_extracted_in_page_order(self):
        writer, tree, pairs = self.writer()
        del writer.root_object['/Names']
        writer.pages[0][NameObject('/Annots')] = ArrayObject([
            writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Annot'),
                NameObject('/Subtype'): NameObject('/FileAttachment'), NameObject('/FS'): pairs[i]})) for i in (1, 3)])
        listing = self.save_and_extract(writer, [b'first', b'second'])
        self.assertEqual([(x['origin'], x['page']) for x in listing['attachments']], [('annotation', 0), ('annotation', 0)])

    def test_listing_nested_tree_never_decodes_payload(self):
        writer, tree, pairs = self.writer()
        tree[NameObject('/Kids')] = ArrayObject([DictionaryObject({NameObject('/Names'): pairs})])
        writer.write(self.pdf)
        with patch.object(EmbeddedFile, 'content', new_callable=PropertyMock, side_effect=AssertionError('decoded')):
            self.assertEqual(len(attachments.list_attachments(self.pdf)['attachments']), 2)

    def test_cycles_and_repeated_nodes_are_rejected(self):
        for cycle in (True, False):
            with self.subTest(cycle=cycle):
                writer, tree, pairs = self.writer()
                node = writer._add_object(tree if cycle else DictionaryObject({NameObject('/Names'): pairs}))
                tree[NameObject('/Kids')] = ArrayObject([node] if cycle else [node, node])
                writer.write(self.pdf)
                with self.assertRaisesRegex(ValueError, 'ciclo|repetida'):
                    attachments.list_attachments(self.pdf)

    def test_malformed_tree_nodes_fail_instead_of_silent_truncation(self):
        for malformed in ('both', 'odd', 'invalid_kid', 'invalid_names'):
            with self.subTest(malformed=malformed):
                writer, tree, pairs = self.writer()
                if malformed == 'both':
                    tree[NameObject('/Kids')] = ArrayObject()
                    tree[NameObject('/Names')] = pairs
                elif malformed == 'odd':tree[NameObject('/Names')] = ArrayObject(pairs[:1])
                elif malformed == 'invalid_kid':tree[NameObject('/Kids')] = ArrayObject([NumberObject(7)])
                else:tree[NameObject('/Names')] = NumberObject(7)
                writer.write(self.pdf)
                with self.assertRaises(ValueError):attachments.list_attachments(self.pdf)

    def test_tree_depth_and_node_limits_fail_explicitly(self):
        writer, tree, pairs = self.writer()
        node = DictionaryObject({NameObject('/Names'): pairs})
        for _ in range(4):node = DictionaryObject({NameObject('/Kids'): ArrayObject([writer._add_object(node)])})
        tree[NameObject('/Kids')] = ArrayObject([writer._add_object(node)])
        writer.write(self.pdf)
        for setting in ('MAX_TREE_DEPTH', 'MAX_TREE_NODES'):
            with patch.object(attachments, setting, 2):
                with self.assertRaisesRegex(ValueError, 'limite'):attachments.list_attachments(self.pdf)

    def test_annotation_without_file_spec_is_an_error(self):
        writer = PdfWriter()
        page = writer.add_blank_page(100, 100)
        page[NameObject('/Annots')] = ArrayObject([DictionaryObject({NameObject('/Subtype'): NameObject('/FileAttachment')})])
        writer.write(self.pdf)
        with self.assertRaisesRegex(ValueError, 'especificação'):attachments.list_attachments(self.pdf)


if __name__ == '__main__':unittest.main()
