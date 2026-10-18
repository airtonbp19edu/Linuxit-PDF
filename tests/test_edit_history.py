"""Real draft snapshots, atomic cursor changes and source identity checks."""
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from concurrent.futures import CancelledError

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'))))
from edit_history import EditSession
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader
from test_advanced_edits import make_controls


class EditHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='linuxit-history-test-');self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';make_controls(self.source);self.original=self.source.read_bytes()
        self.session=EditSession(self.source)
    def tearDown(self):self.session.close();self.temp.cleanup()
    def add(self,title):self.session.add({'kind':'add-bookmark','title':title,'page':0})
    def test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only(self):
        self.add('A');self.add('B');self.session.undo()
        self.assertEqual([n.title for n in PdfReader(self.session.preview).outline if not isinstance(n,list)],['Parent','Sibling','A'])
        out=self.root/'out.pdf';self.session.save(out);before=out.read_bytes()
        self.session.redo();self.assertEqual(self.session.cursor,2)
        self.assertEqual(out.read_bytes(),before);self.assertEqual(self.source.read_bytes(),self.original)
    def test_undo_all_restores_base_and_disables_save_until_redone(self):
        self.add('A');self.session.undo()
        self.assertIsNone(self.session.preview);self.assertFalse(self.session.can_undo);self.assertTrue(self.session.can_redo)
        with self.assertRaises(ValueError):self.session.save(self.root/'empty.pdf')
        self.session.redo();self.assertTrue(self.session.can_undo)
    def test_new_branch_discards_redo_but_invalid_branch_preserves_it(self):
        self.add('A');self.add('B');self.session.undo()
        preview=self.session.preview
        with self.assertRaises(RuntimeError):self.session.add({'kind':'move-bookmark','path':[99],'parent':[],'position':0})
        self.assertTrue(self.session.can_redo);self.assertEqual(self.session.preview,preview);self.assertTrue(preview.exists())
        self.add('C');self.assertFalse(self.session.can_redo);self.assertEqual(self.session.operations[-1]['title'],'C')
    def test_operation_values_are_defensively_copied(self):
        operation={'kind':'add-bookmark','title':'A','page':0};self.session.add(operation)
        operation['title']='external';ops=self.session.operations;ops[0]['title']='mutated'
        self.assertEqual(self.session.operations[0]['title'],'A')
    def test_changed_original_blocks_add_undo_redo_and_save(self):
        self.add('A');self.source.write_bytes(self.original+b'\n% modified\n')
        for action in (lambda:self.add('B'),self.session.undo,lambda:self.session.save(self.root/'out.pdf')):
            with self.assertRaises((RuntimeError,ValueError)):action()
        self.assertEqual(self.session.cursor,1);self.assertFalse((self.root/'out.pdf').exists())
    def test_existing_destination_is_not_overwritten_and_draft_survives(self):
        self.add('A');out=self.root/'out.pdf';out.write_bytes(b'keep')
        with self.assertRaises(RuntimeError):self.session.save(out)
        self.assertEqual(out.read_bytes(),b'keep');self.assertEqual(self.session.cursor,1)
    def test_closed_session_refuses_work_and_removes_private_previews(self):
        self.add('A');preview=self.session.preview;self.session.close()
        self.assertFalse(preview.exists())
        with self.assertRaises(CancelledError):self.add('B')
    def test_pre_cancelled_session_does_not_start_worker(self):
        cancel=threading.Event();cancel.set()
        with self.assertRaises(CancelledError):EditSession(self.source,cancel=cancel)


if __name__=='__main__':unittest.main()
