"""E24/D05 decision (21/10/2026): result order and bookmark-result behaviour follow what was
observed in Foxit. Own GTK checks; the Foxit observation itself is in
testes/resultados/vm-2026-10-21-e24/observations.json."""
from gtk_cleanup import cleanup_temp
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_search_extensions_gtk import Gtk, wait_for
from test_search_scopes import scoped_pdf


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')), 'Requires GTK3 and X11')
class FoxitOrderGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-foxit-order-');self.root = Path(self.temp.name)
        self.source = self.root/'scopes.pdf';scoped_pdf(self.source, unresolved=True)
        self.original = self.source.read_bytes();self.errors = []
        self.hook = patch.object(sys, 'excepthook', lambda *args: self.errors.append(args));self.hook.start()
        self.quit = patch.object(Gtk, 'main_quit');self.quit.start()
        load_css();self.window = PDFWindow(str(self.source))
        wait_for(lambda: self.window.current_pixbuf is not None and self.window.displayed_page == 0)

    def tearDown(self):
        self.window.destroy();self.quit.stop();self.hook.stop();cleanup_temp(self.temp)
        self.assertEqual(self.errors, [])

    def search_all(self):
        w = self.window;w._show_find();w.find_results_toggle.set_active(True)
        w.find_options['include_bookmarks'].set_active(True);w.find_options['include_comments'].set_active(True)
        w.find_entry.set_text('alvo')
        wait_for(lambda: len(w.search_hits) == 6 and not w.search_running)
        return w

    def test_results_list_bookmarks_then_page_text_then_comments(self):
        w = self.search_all()
        self.assertEqual([hit['source'] for hit in w.search_hits],
                         ['bookmark', 'bookmark', 'page_text', 'page_text', 'page_text', 'comment'])
        self.assertEqual([hit['text'] for hit in w.search_hits[:2]], ['ALVO marcador', 'alvo externo'])

    def test_bookmark_result_selects_bookmark_without_changing_page(self):
        w = self.search_all()
        self.assertEqual(w.search_hits[0]['page'], 1)  # the bookmark's destination is page 2
        w._select_search_hit(0)
        wait_for(lambda: w.bookmark_list.get_selected_row() is not None)
        for _ in range(10):
            wait_for(lambda: True)
        self.assertEqual(w.page, 0);self.assertEqual(w.displayed_page, 0)
        self.assertEqual(getattr(w.bookmark_list.get_selected_row(), 'item_id', None), w.search_hits[0]['item_id'])
        # A page-text result still moves the view to its own page and the bookmark row itself
        # still navigates when activated, as in Foxit.
        w._select_search_hit(2);self.assertEqual(w.page, 0)
        row = w.bookmark_list.get_selected_row();w._bookmark_activated(w.bookmark_list, row)
        wait_for(lambda: w.displayed_page == 1)
        self.assertEqual(self.source.read_bytes(), self.original)


if __name__ == '__main__':
    unittest.main()
