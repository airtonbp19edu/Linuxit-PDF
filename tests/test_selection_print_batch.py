"""Independent word order, cancellation of actual children and output preservation."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from test_attachment_search import text_pdf
from pypdf import PdfReader
import imposition
import print_tasks
from text_selection import select_words, selection_text


def words():
    return [dict(text=text,block=block,line=line,x0=x,y0=y,x1=x+30,y1=y+10)
            for text,block,line,x,y in [('שלום',0,0,10,10),('עולם',0,0,45,10),
                                       ('संगीत',0,1,10,30),('coluna',1,0,110,10)]]


class SelectionPrintBatchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.source=self.root/'source.pdf';self.source.write_bytes(text_pdf(['alpha']))

    def tearDown(self):self.temp.cleanup()

    def test_selection_retains_unicode_order_and_separates_columns(self):
        selected=select_words({'words':words()},(0,0,200,100))
        self.assertEqual(selection_text(selected),'שלום עולם\nसंगीत\n\ncoluna')
        left=select_words({'words':words()},(0,0,80,100))
        self.assertEqual(selection_text(left),'שלום עולם\nसंगीत')

    def test_touching_edge_is_not_a_selection_and_reversed_drag_is_equivalent(self):
        data={'words':words()}
        self.assertEqual(select_words(data,(40,10,45,20)),[])
        self.assertEqual(select_words(data,(0,0,80,100)),select_words(data,(80,100,0,0)))
        self.assertEqual(select_words(data,(0,0,0,100)),[])
        with self.assertRaises(ValueError):select_words(data,(0,0,float('nan'),100))

    def test_new_json_print_worker_produces_valid_output_without_changing_source(self):
        before=self.source.read_bytes();out=self.root/'prepared.pdf'
        result=print_tasks.prepare_print(self.source,out,{'scale_mode':'fit'})
        self.assertEqual(Path(result),out);self.assertEqual(len(PdfReader(out).pages),1)
        self.assertEqual(self.source.read_bytes(),before)

    def test_cancel_terminates_real_preparation_child_and_removes_partial_output(self):
        out=self.root/'prepared.pdf';event=threading.Event();children=[]
        original=subprocess.Popen
        def child(argv,**kwargs):
            out.write_bytes(b'partial')
            process=original([sys.executable,'-c','import time;time.sleep(30)'],**kwargs)
            children.append(process);return process
        timer=threading.Timer(.25,event.set);timer.start()
        try:
            with patch.object(subprocess,'Popen',side_effect=child):
                self.assertIsNone(print_tasks.prepare_print(self.source,out,{},event))
        finally:timer.join()
        self.assertIsNotNone(children[0].poll());self.assertFalse(out.exists())

    def test_print_output_cannot_overwrite_original_and_nonfinite_parameters_fail_early(self):
        before=self.source.read_bytes()
        with self.assertRaisesRegex(ValueError,'original'):
            imposition.prepare_output(self.source,self.source,{})
        for value in (float('nan'),float('inf'),-1):
            with self.assertRaises(ValueError):
                imposition.prepare_output(self.source,self.root/'out.pdf',{'poster_scale':value})
        self.assertEqual(self.source.read_bytes(),before);self.assertFalse((self.root/'out.pdf').exists())

    def test_save_print_copy_is_atomic_on_failure_and_refuses_original(self):
        prepared=self.root/'prepared.pdf';prepared.write_bytes(text_pdf(['new']))
        dest=self.root/'dest.pdf';dest.write_bytes(b'old')
        with patch.object(print_tasks.os,'replace',side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):print_tasks.publish_print_copy(prepared,dest,self.source)
        self.assertEqual(dest.read_bytes(),b'old')
        self.assertFalse(list(self.root.glob('.linuxit-print-*')))
        with self.assertRaises(ValueError):print_tasks.publish_print_copy(prepared,self.source,self.source)
        print_tasks.publish_print_copy(prepared,dest,self.source)
        self.assertEqual(dest.read_bytes(),prepared.read_bytes())


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK and X display')
class PrintPreparationGUITests(unittest.TestCase):
    def test_cancelling_preparation_never_calls_printer_submission(self):
        from main import PDFWindow,Gtk
        from test_gui import wait_for
        entered=threading.Event();release=threading.Event()
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            path=Path(directory)/'gui.pdf';path.write_bytes(text_pdf(['alpha']))
            window=PDFWindow(str(path))
            def delayed(*args):
                entered.set();release.wait(8);return None
            try:
                wait_for(lambda:window.displayed_page==0)
                with patch('main.prepare_print',side_effect=delayed),patch('main.cups.print_file') as submit:
                    window._submit_print_job({'destination':'printer','printer':'synthetic'})
                    wait_for(entered.is_set)
                    dialog=next(w for w in Gtk.Window.list_toplevels() if isinstance(w,Gtk.MessageDialog)
                                and w.get_transient_for() is window)
                    event=window.print_cancel;dialog.response(Gtk.ResponseType.CANCEL)
                    self.assertTrue(event.is_set());release.set()
                    self.assertIsNone(window.print_cancel);submit.assert_not_called()
            finally:
                release.set();window.destroy()
