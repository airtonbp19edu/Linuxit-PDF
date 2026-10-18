"""Independent search contracts on real PDFs; these are not Foxit differential tests."""
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from test_regressions import APP, make_pdf
sys.path.insert(0,str(APP))
from search_engine import TextSearchIndex, page_hits
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text
from pypdf.generic import NameObject, TextStringObject


def scoped_pdf(path, unresolved=False):
    raw=path.with_name('raw.pdf')
    make_pdf(raw,['alvo texto ALVO alvoextra','outra página'])
    writer=PdfWriter();writer.append(raw)
    writer.add_outline_item('ALVO marcador',1)
    if unresolved:writer.add_outline_item('alvo externo',None)
    note=Text(rect=(40,40,100,80),text='comentário alvo')
    note[NameObject('/Subj')]=TextStringObject('Assunto separado')
    note[NameObject('/T')]=TextStringObject('Autor não pesquisável')
    writer.add_annotation(0,note);writer.write(path)


class SearchScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.pdf=self.root/'scopes.pdf';scoped_pdf(self.pdf)
        self.index=TextSearchIndex(self.pdf)

    def tearDown(self):self.temp.cleanup()

    def test_real_document_scopes_are_independent_and_keep_destination(self):
        self.assertEqual(len(self.index.search('alvo')),3)
        bookmarks=self.index.search('alvo',include_page_text=False,include_bookmarks=True)
        self.assertEqual([(x['source'],x['page'],x['rects']) for x in bookmarks],[('bookmark',1,[])])
        comments=self.index.search('alvo',include_page_text=False,include_comments=True)
        self.assertEqual([(x['source'],x['page'],x['rects']) for x in comments],[('comment',0,[])])
        all_hits=self.index.search('alvo',include_bookmarks=True,include_comments=True,whole_words=True)
        self.assertEqual([x['source'] for x in all_hits],['page_text','page_text','bookmark','comment'])
        self.assertTrue(all(x['rects'] for x in all_hits[:2]))

    def test_comment_subject_contents_and_author_are_searchable(self):
        opts={'include_page_text':False,'include_comments':True}
        self.assertEqual(len(self.index.search('assunto',**opts)),1)
        self.assertEqual(len(self.index.search('comentário',**opts)),1)
        author=self.index.search('Autor',**opts)
        self.assertEqual([(hit['source'],hit['page'],hit['rects']) for hit in author],
                         [('comment',0,[])])
        self.assertEqual(self.index.search('Alvo',match_case=True,**opts),[])

    def test_global_limit_progress_and_cancel_cover_metadata(self):
        batches=[]
        hits=self.index.search('alvo',include_bookmarks=True,include_comments=True,max_hits=4,
                               on_page=lambda scanned,batch:batches.extend(batch))
        self.assertEqual(hits,batches);self.assertEqual(len(hits),4)
        self.assertEqual(hits[-1]['source'],'bookmark')
        event=threading.Event();seen=[]
        def on_hit(scanned,batch):seen.extend(batch);event.set()
        hits=self.index.search('alvo',include_page_text=False,include_bookmarks=True,
                               include_comments=True,cancel=event,on_page=on_hit)
        self.assertEqual(len(hits),1);self.assertEqual(hits,seen)
        with patch.object(self.index,'_panels',side_effect=AssertionError('Cancelled search parsed metadata')):
            self.assertEqual(self.index.search('alvo',include_comments=True,cancel=event),[])

    def test_cached_metadata_rejects_changed_document(self):
        self.index.search('alvo',include_page_text=False,include_bookmarks=True)
        make_pdf(self.pdf,['replacement'])
        with self.assertRaisesRegex(RuntimeError,'alterado'):
            self.index.search('alvo',include_page_text=False,include_bookmarks=True)

    def test_bookmark_without_local_page_is_not_given_a_fake_destination(self):
        scoped_pdf(self.pdf,unresolved=True)
        hits=TextSearchIndex(self.pdf).search('externo',include_page_text=False,include_bookmarks=True)
        self.assertEqual(len(hits),1);self.assertIsNone(hits[0]['page']);self.assertEqual(hits[0]['rects'],[])

    def test_unicode_combining_marks_are_word_characters(self):
        data={'width':100,'height':100,'words':[{'text':'किताब','block':0,'line':0,'x0':0,'y0':0,'x1':40,'y1':20}]}
        self.assertEqual(page_hits(data,'क',0,whole_words=True),[])
        self.assertEqual(len(page_hits(data,'किताब',0,whole_words=True)),1)


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires an X display')
class SearchScopeGUITests(unittest.TestCase):
    def test_ui_toggles_scopes_and_navigates_bookmark_result(self):
        from test_gui import wait_for
        from main import PDFWindow,Gtk
        with tempfile.TemporaryDirectory() as directory,patch.object(Gtk,'main_quit'):
            path=Path(directory)/'gui.pdf';scoped_pdf(path)
            w=PDFWindow(str(path))
            try:
                wait_for(lambda:w.displayed_page==0)
                w.find_options['include_page_text'].set_active(False)
                w.find_options['include_bookmarks'].set_active(True)
                w.find_entry.set_text('alvo')
                wait_for(lambda:len(w.search_hits)==1 and not w.search_running)
                self.assertEqual(w.search_hits[0]['source'],'bookmark')
                wait_for(lambda:w.displayed_page==1)
                w.find_options['include_bookmarks'].set_active(False)
                wait_for(lambda:'Selecione' in w.find_status.get_text())
                self.assertEqual(w.search_hits,[])
                w.find_options['include_comments'].set_active(True)
                wait_for(lambda:len(w.search_hits)==1 and not w.search_running)
                self.assertEqual(w.search_hits[0]['source'],'comment')
                wait_for(lambda:w.displayed_page==0)
                w.find_entry.set_text('Autor')
                wait_for(lambda:len(w.search_hits)==1 and not w.search_running
                         and 'Autor' in w.search_hits[0]['snippet'])
                self.assertEqual(w.search_hits[0]['source'],'comment')
                self.assertEqual(w.search_hits[0]['page'],0)
                self.assertEqual(w.search_hits[0]['rects'],[])
            finally:w.destroy()
