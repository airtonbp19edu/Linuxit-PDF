"""Real synthetic PDF reply graphs and independent Linuxit search contracts."""
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

APP = Path(os.environ.get('PRINT_VIEW_TEST_APP', Path(__file__).resolve().parents[1]/'app'))
sys.path.insert(0, str(APP))
sys.path.insert(0, str(APP/'vendor'))
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text
from pypdf.generic import ArrayObject, NameObject, TextStringObject
from pdf_comments import inspect_comments
from pdf_panels import inspect_document_panels
from search_engine import TextSearchIndex, page_hits


def thread_pdf(path, variant='normal'):
    writer = PdfWriter()
    writer.add_blank_page(width=600, height=800)
    writer.add_blank_page(width=600, height=800)
    writer.add_outline_item('destination marker', 1)
    for body in ('root body', 'reply target', 'reply target'):
        note = Text(rect=(20, 30, 60, 70), text=body)
        note[NameObject('/T')] = TextStringObject('Pessoa')
        writer.add_annotation(1, note)
    annots = writer.pages[1]['/Annots']
    root, reply, second = [r.get_object() for r in annots]
    reply[NameObject('/IRT')] = annots[0]
    second[NameObject('/IRT')] = annots[1]
    root[NameObject('/Subj')] = TextStringObject('lastword')
    root[NameObject('/Contents')] = TextStringObject('firstword root body')
    if variant == 'alias':
        annots.append(annots[1])
    elif variant == 'missing-parent':
        writer.pages[1][NameObject('/Annots')] = ArrayObject(annots[1:])
    elif variant == 'cycle':
        root[NameObject('/IRT')] = annots[1]
    elif variant == 'cross-page':
        writer.pages[0][NameObject('/Annots')] = ArrayObject([annots[0]])
        writer.pages[1][NameObject('/Annots')] = ArrayObject(annots[1:])
    elif variant == 'rich':
        reply.pop('/Contents')
        reply[NameObject('/RC')] = TextStringObject('<body><p>Rich &amp; target</p><script>hidden</script></body>')
    elif variant == 'group':
        reply[NameObject('/RT')] = NameObject('/Group')
    writer.write(path)


class CommentThreadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.pdf = self.root/'threads.pdf'

    def tearDown(self):
        self.temp.cleanup()

    def test_replies_keep_distinct_objects_and_alias_is_not_a_second_occurrence(self):
        thread_pdf(self.pdf, 'alias')
        data = inspect_document_panels(self.pdf)
        comments = data['comments']
        self.assertEqual(len(comments), 3)
        self.assertEqual([c['thread_depth'] for c in comments], [0, 1, 2])
        self.assertEqual(comments[2]['parent_comment_id'], comments[1]['comment_id'])
        hits = TextSearchIndex(self.pdf).search('target', include_page_text=False, include_comments=True)
        self.assertEqual(len(hits), 2)
        self.assertEqual(len({h['item_id'] for h in hits}), 2)
        self.assertTrue(all(h['page'] == 1 and h['is_reply'] and not h['rects'] for h in hits))
        self.assertEqual([c['comment_id'] for c in comments],
                         [c['comment_id'] for c in inspect_document_panels(self.pdf)['comments']])

    def test_subject_and_contents_do_not_create_a_cross_field_phrase(self):
        thread_pdf(self.pdf)
        index = TextSearchIndex(self.pdf)
        opts = dict(include_page_text=False, include_comments=True)
        self.assertEqual(index.search('lastword firstword', **opts), [])
        self.assertEqual(index.search('Pessoa', **opts)[0]['match_field'], 'author')
        self.assertEqual(index.search('root body', **opts)[0]['match_field'], 'contents')

    def test_parent_not_in_annots_is_included_once_and_marked(self):
        thread_pdf(self.pdf, 'missing-parent')
        data = inspect_document_panels(self.pdf)
        self.assertEqual(len(data['comments']), 3)
        self.assertTrue(data['comments'][-1]['inferred_from_reply'])
        self.assertEqual(data['comments'][0]['parent_comment_id'], data['comments'][-1]['comment_id'])

    def test_cycle_and_cross_page_parent_are_reported_without_guessed_destination(self):
        thread_pdf(self.pdf, 'cycle')
        data = inspect_document_panels(self.pdf)
        self.assertTrue(data['notices'])
        self.assertTrue(all(c['parent_comment_id'] is None for c in data['comments']))
        thread_pdf(self.pdf, 'cross-page')
        data = inspect_document_panels(self.pdf)
        self.assertEqual([c['page'] for c in data['comments']], [0, 1, 1])
        self.assertIsNone(data['comments'][1]['parent_comment_id'])
        self.assertTrue(data['notices'])

    def test_rich_text_fallback_is_plain_text_and_group_is_not_a_reply(self):
        thread_pdf(self.pdf, 'rich')
        data = inspect_document_panels(self.pdf)
        self.assertEqual(data['comments'][1]['contents'], 'Rich & target')
        thread_pdf(self.pdf, 'group')
        data = inspect_document_panels(self.pdf)
        self.assertFalse(data['comments'][1]['is_reply'])
        self.assertEqual(data['comments'][1]['relationship'], 'Group')

    def test_inspection_limit_and_cancel_are_explicit_and_partial_cache_is_not_retained(self):
        thread_pdf(self.pdf)
        comments, notices = inspect_comments(PdfReader(self.pdf), max_annotations=1)
        self.assertEqual(len(comments), 1); self.assertTrue(notices)
        event = threading.Event(); event.set()
        comments, notices = inspect_comments(PdfReader(self.pdf), event)
        self.assertEqual(comments, []); self.assertTrue(notices)
        index = TextSearchIndex(self.pdf)
        index._panels(event)
        self.assertIsNone(index.panel_cache)
        self.assertEqual(len(index._panels()['comments']), 3)

    def test_cancel_during_page_extraction_keeps_previous_batch_and_limit_bounds_geometry(self):
        thread_pdf(self.pdf)
        index = TextSearchIndex(self.pdf)
        event = threading.Event()
        page = dict(width=100, height=100, words=[dict(text='target target', block=0, line=0,
                    x0=0, y0=0, x1=90, y1=20)])
        def extract(number):
            if number:
                event.set()
                raise RuntimeError('cancelled subprocess')
            return page
        with patch.object(index, 'page', side_effect=extract):
            hits = index.search('target', cancel=event)
        self.assertEqual(len(hits), 2)
        self.assertEqual(len(page_hits(page, 'target', 0, max_hits=1)), 1)


@unittest.skipUnless(os.environ.get('DISPLAY'), 'Requires GTK and X display')
class CommentSearchGUITests(unittest.TestCase):
    def test_reply_and_bookmark_hits_select_the_actual_panel_row(self):
        from test_gui import wait_for
        from main import PDFWindow, Gtk
        with tempfile.TemporaryDirectory() as directory, patch.object(Gtk, 'main_quit'):
            path = Path(directory)/'gui.pdf'; thread_pdf(path)
            window = PDFWindow(str(path))
            try:
                wait_for(lambda: window.displayed_page == 0)
                window.find_options['include_page_text'].set_active(False)
                window.find_options['include_comments'].set_active(True)
                window.find_entry.set_text('target')
                wait_for(lambda: len(window.search_hits) == 2 and not window.search_running)
                wait_for(lambda: window.displayed_page == 1 and window.comment_list.get_selected_row() is not None)
                self.assertEqual(window.comment_list.get_selected_row().item_id, window.search_hits[0]['item_id'])
                window._find_next()
                self.assertEqual(window.comment_list.get_selected_row().item_id, window.search_hits[1]['item_id'])
                wait_for(lambda: not window._search_scroll_pending)
                window.find_options['include_comments'].set_active(False)
                window.find_options['include_bookmarks'].set_active(True)
                window.find_entry.set_text('marker')
                wait_for(lambda: len(window.search_hits) == 1 and not window.search_running)
                self.assertEqual(window.bookmark_list.get_selected_row().item_id, window.search_hits[0]['item_id'])
            finally:
                window.destroy()

    def test_stop_retains_delivered_hits_and_late_results_cannot_repopulate(self):
        from test_gui import wait_for
        from main import PDFWindow, Gtk
        with tempfile.TemporaryDirectory() as directory, patch.object(Gtk, 'main_quit'):
            path = Path(directory)/'gui.pdf'; thread_pdf(path)
            window = PDFWindow(str(path)); reached = threading.Event(); release = threading.Event()
            def delayed(index, query, cancel=None, on_page=None, **kwargs):
                hit = dict(source='bookmark', page=1, width=600, height=800, rects=[],
                           text='target', snippet='target', item_id='bookmark:0')
                on_page(0, [hit]); reached.set(); release.wait(8)
                on_page(0, [hit]); return [hit, hit]
            try:
                wait_for(lambda: window.displayed_page == 0)
                with patch.object(TextSearchIndex, 'search', delayed):
                    window.find_entry.set_text('target')
                    wait_for(lambda: reached.is_set() and len(window.search_hits) == 1)
                    window.find_stop.clicked()
                    self.assertTrue(window.search_cancel.is_set())
                    self.assertFalse(window.search_running)
                    self.assertIn('interrompida', window.find_status.get_text())
                    release.set()
                    # A subsequent search must still work and replace the partial results.
                    window.find_entry.set_text('not-found')
                wait_for(lambda: not window.search_running and window.search_timer is None)
                self.assertEqual(window.search_hits, [])
                self.assertFalse(window.search_stopped)
            finally:
                release.set(); window.destroy()
