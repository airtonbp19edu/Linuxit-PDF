"""Real GTK/worker paths for embedded, advanced and persistent collection search."""
from gtk_cleanup import cleanup_temp
from io import BytesIO
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from test_attachment_search import text_pdf
from pypdf import PdfWriter

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib, Gdk
except (ImportError, ValueError):Gtk = GLib = Gdk = None


def wait_for(predicate, timeout=20):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        context = GLib.MainContext.default()
        while context.pending():context.iteration(False)
        if predicate():return
        time.sleep(.02)
    raise AssertionError('Search extension GTK timeout')


def capture(window, name):
    destination = os.environ.get('LINUXIT_SEARCH_CAPTURE_DIR')
    if not destination:return
    # Worker/model completion precedes GTK's next painted frame. Preserve a
    # rendered result, rather than the previously displayed busy state.
    settled = []
    def settle():settled.append(True);return False
    window.queue_draw()
    GLib.timeout_add(160, settle)
    wait_for(lambda: bool(settled))
    folder = Path(destination);folder.mkdir(parents=True, exist_ok=True)
    allocation = window.get_allocation()
    pixbuf = Gdk.pixbuf_get_from_window(window.get_window(), 0, 0, allocation.width, allocation.height)
    path = folder/(name+'.png');pixbuf.savev(str(path), 'png', [], [])
    (folder/(name+'.json')).write_text(json.dumps({'scope': 'Own GTK UI, not Foxit observation',
        'width': allocation.width, 'height': allocation.height,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}, indent=2)+'\n', encoding='utf-8')


@unittest.skipUnless(Gtk is not None and bool(os.environ.get('DISPLAY')), 'Requires GTK3 and X11')
class SearchExtensionGTKTests(unittest.TestCase):
    def setUp(self):
        from main import PDFWindow, load_css
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-search-ui-');self.root = Path(self.temp.name)
        self.source = self.root/'host.pdf'
        writer = PdfWriter(clone_from=BytesIO(text_pdf(['alpha x beta alphabet', 'other'])))
        writer.add_attachment('notes.txt', b'alvo alvoextra');writer.add_attachment('unsupported.bin', b'alvo')
        writer.write(self.source)
        self.original = self.source.read_bytes();self.errors = [];self.children = []
        self.hook = patch.object(sys, 'excepthook', lambda *args: self.errors.append(args));self.hook.start()
        self.quit = patch.object(Gtk, 'main_quit');self.quit.start()
        load_css();self.window = PDFWindow(str(self.source));self.collections = []
        wait_for(lambda: self.window.current_pixbuf is not None and self.window.displayed_page == 0)

    def tearDown(self):
        for window in self.collections:
            if not window.closed:window.destroy()
        self.window.destroy();self.quit.stop();self.hook.stop()
        for child in self.children:
            if child.poll() is None:child.kill();child.wait()
        cleanup_temp(self.temp);self.assertEqual(self.errors, [])

    def collection(self, opener=None):
        from collection_window import CollectionWindow
        window = CollectionWindow(self.window, opener or (lambda path, page: self.window.open_document(path, initial_page=page)))
        self.collections.append(window);window.show_all()
        return window

    def test_attachment_scope_displays_partial_coverage_and_distinct_identity(self):
        w = self.window;w._show_find();w.find_results_toggle.set_active(True)
        w.find_options['include_page_text'].set_active(False);w.find_options['include_attachments'].set_active(True)
        w.find_entry.set_text('alvo')
        wait_for(lambda: len(w.search_hits) == 2 and not w.search_running)
        self.assertIn('parciais', w.find_status.get_text())
        self.assertIn('unsupported.bin', w.find_status.get_tooltip_text())
        self.assertTrue(all(h['page'] is None and h['rects'] == [] for h in w.search_hits))
        self.assertIn('notes.txt', w.find_results_list.get_row_at_index(0).get_child().get_text())
        self.assertEqual(w.displayed_page, 0);self.assertEqual(self.source.read_bytes(), self.original)
        capture(w, 'attachment-search')

    def test_mode_controls_geometry_distance_and_bad_syntax(self):
        w = self.window;w._show_find();w.find_results_toggle.set_active(True)
        w.find_mode.set_active_id('wildcard');w.find_entry.set_text('alp*')
        wait_for(lambda: len(w.search_hits) == 2 and not w.search_running)
        self.assertTrue(all(hit['rects'] for hit in w.search_hits))
        w.find_mode.set_active_id('proximity');w.find_distance.set_value(1);w.find_entry.set_text('alpha beta')
        wait_for(lambda: len(w.search_hits) == 1 and not w.search_running)
        self.assertTrue(w.find_distance.get_sensitive());capture(w, 'proximity-search')
        w.find_distance.set_value(0)
        wait_for(lambda: not w.search_running and not w.search_hits and 'Nenhuma' in w.find_status.get_text())
        w.find_mode.set_active_id('wildcard');w.find_entry.set_text('*')
        wait_for(lambda: 'Erro:' in w.find_status.get_text())
        self.assertFalse(w.search_hits)

    def test_old_attachment_results_do_not_repopulate_another_document(self):
        import attachment_search
        w = self.window;entered = threading.Event()
        def delayed(path, query, options, limit, cancel):
            entered.set();cancel.wait(5)
            return {'hits': [{'source':'attachment','page':None,'rects':[],'snippet':'stale','attachment_name':'old.txt'}],
                    'omissions':[], 'limit_reached':False}
        other = self.root/'new.pdf';other.write_bytes(text_pdf(['new document']))
        with patch.object(attachment_search, 'invoke_attachment_search', side_effect=delayed):
            w.find_options['include_page_text'].set_active(False);w.find_options['include_attachments'].set_active(True)
            w.find_entry.set_text('alvo');wait_for(entered.is_set)
            w.open_document(str(other));wait_for(lambda: w.displayed_page == 0 and not w.search_running)
            self.assertEqual(w.filepath, str(other));self.assertEqual(w.search_hits, [])

    def test_collection_build_query_and_open_result_on_its_actual_page(self):
        first, second = self.root/'one.pdf', self.root/'two.pdf'
        first.write_bytes(text_pdf(['nothing']));second.write_bytes(text_pdf(['other', 'alpha target']))
        output = self.root/'selected.linuxit-index.json';w = self.collection()
        with patch.object(w, '_choose', side_effect=[[str(first), str(second)], str(output)]):w._build()
        wait_for(lambda: not w.busy and output.exists())
        self.assertIn('2 PDFs', w.status.get_text());w.query.set_text('alpha');w._search()
        wait_for(lambda: not w.busy and len(w.hits) == 1)
        self.assertEqual(w.hits[0]['page'], 1);capture(w, 'collection-search')
        w._activate(None, w.results.get_row_at_index(0))
        wait_for(lambda: self.window.filepath == str(second) and self.window.displayed_page == 1)
        self.assertEqual(self.window.page_count, 2)

    def test_collection_changed_result_is_refused_before_opening(self):
        from collection_index import build_index
        output = self.root/'selected.linuxit-index.json';build_index(output, {'paths':[str(self.source)]})
        opened = [];w = self.collection(lambda *args: opened.append(args))
        w.index_entry.set_text(str(output));w.query.set_text('alpha');w._search()
        wait_for(lambda: not w.busy and len(w.hits) == 2)
        self.source.write_bytes(text_pdf(['replacement']))
        w._activate(None, w.results.get_row_at_index(0))
        wait_for(lambda: not w.busy and 'mudou' in w.status.get_text())
        self.assertEqual(opened, [])

    def test_closing_collection_terminates_pending_worker_without_callbacks(self):
        import search_tasks
        original = subprocess.Popen
        def delayed(argv, **kwargs):
            if 'index-search' not in argv:return original(argv, **kwargs)
            child = original([sys.executable, '-c', 'import time;time.sleep(30)'], **kwargs)
            self.children.append(child);return child
        w = self.collection();w.index_entry.set_text(str(self.root/'index.linuxit-index.json'));w.query.set_text('alpha')
        with patch.object(search_tasks.subprocess, 'Popen', side_effect=delayed):
            w._search();wait_for(lambda: bool(self.children));w.destroy()
            wait_for(lambda: self.children[0].poll() is not None)
        self.assertTrue(w.closed)


if __name__ == '__main__':unittest.main()
