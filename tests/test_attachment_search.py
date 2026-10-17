"""Real embedded bytes/PDFs, query modes and worker lifecycle on own data."""
from io import BytesIO
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch, PropertyMock

sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', Path(__file__).resolve().parents[1] / 'app'))))
import attachment_search as search
from search_engine import SearchOptions, TextSearchIndex
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, DecodedStreamObject, EmbeddedFile, NameObject, NumberObject


def text_pdf(texts):
    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')}))
    for text in texts:
        page = writer.add_blank_page(200, 200)
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject()
        stream.set_data(('BT /F1 12 Tf 10 100 Td (' + text + ') Tj ET').encode('ascii'))
        page[NameObject('/Contents')] = writer._add_object(stream)
    output = BytesIO();writer.write(output)
    return output.getvalue()


def request(query='alvo', **kwargs):
    result = {'query': query, 'match_case': False, 'ignore_accents': False, 'whole_words': False,
              'mode': 'literal', 'proximity_distance': 0, 'max_hits': 5000}
    result.update(kwargs)
    return result


class AttachmentSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-embedded-search-')
        self.root = Path(self.temp.name)
        self.pdf = self.root / 'source.pdf'

    def tearDown(self):self.temp.cleanup()

    def host(self, attachments):
        writer = PdfWriter();writer.add_blank_page(200, 200)
        for name, content in attachments:writer.add_attachment(name, content)
        writer.write(self.pdf)
        return writer

    def test_utf8_bom_case_accents_and_whole_words_preserve_source(self):
        self.host([('unicode.txt', '\ufeffÁLVO alvoextra alvo'.encode('utf-8'))])
        before = self.pdf.read_bytes()
        result = search.search_attachment_text(self.pdf, request(ignore_accents=True, whole_words=True))
        self.assertTrue(result['complete']);self.assertEqual(len(result['hits']), 2)
        self.assertEqual(result['source_sha256'], hashlib.sha256(before).hexdigest())
        self.assertTrue(all(hit['attachment_index'] == 0 and hit['page'] is None and hit['rects'] == [] for hit in result['hits']))
        self.assertEqual(len(search.search_attachment_text(self.pdf, request(match_case=True, whole_words=True))['hits']), 1)
        self.assertEqual(before, self.pdf.read_bytes());self.assertEqual(list(self.root.iterdir()), [self.pdf])

    def test_embedded_pdf_page_is_distinct_from_host_and_model_keeps_scope(self):
        self.host([('inside.pdf', text_pdf(['other', 'ALVO inside']))])
        options = SearchOptions(include_page_text=False, include_attachments=True)
        result = search.invoke_attachment_search(self.pdf, 'alvo', options, 5000)
        hit = result['hits'][0]
        self.assertEqual((hit['attachment_name'], hit['attachment_page'], hit['page']), ('inside.pdf', 1, None))
        index = TextSearchIndex(self.pdf, 1, page_sizes=[(200, 200)])
        notices = []
        hits = index.search('alvo', include_page_text=False, include_attachments=True, on_notice=notices.append)
        self.assertEqual(hits, result['hits']);self.assertFalse(notices[0]['omissions'])
        with patch('attachment_search.invoke_attachment_search', side_effect=AssertionError('unchecked scope must not decode')):
            self.assertEqual(index.search('alvo', include_page_text=False), [])

    def test_tree_and_annotation_references_keep_separate_indices(self):
        writer = self.host([('same.txt', b'alvo first'), ('same.txt', b'alvo second')])
        tree = writer.root_object['/Names']['/EmbeddedFiles'];pairs = tree.pop('/Names')
        tree[NameObject('/Kids')] = ArrayObject([writer._add_object(DictionaryObject({NameObject('/Names'): pairs}))])
        writer.pages[0][NameObject('/Annots')] = ArrayObject([writer._add_object(DictionaryObject({
            NameObject('/Subtype'): NameObject('/FileAttachment'), NameObject('/FS'): pairs[1]}))])
        writer.write(self.pdf)
        hits = search.search_attachment_text(self.pdf, request())['hits']
        self.assertEqual([h['attachment_index'] for h in hits], [0, 1, 2])
        self.assertEqual([h['attachment_origin'] for h in hits], ['catalog', 'catalog', 'annotation'])
        self.assertEqual(hits[-1]['attachment_host_page'], 0);self.assertIsNone(hits[-1]['page'])

    def test_unsupported_invalid_utf8_malformed_and_encrypted_pdf_report_omissions(self):
        encrypted = PdfWriter();encrypted.add_blank_page(20, 20);encrypted.encrypt('password');out = BytesIO();encrypted.write(out)
        self.host([('binary.exe', b'alvo'), ('bad.txt', b'\xffalvo'), ('broken.pdf', b'bad pdf'),
                   ('protected.pdf', out.getvalue()), ('good.txt', b'alvo')])
        result = search.search_attachment_text(self.pdf, request())
        self.assertFalse(result['complete']);self.assertEqual(len(result['omissions']), 4)
        self.assertEqual([h['attachment_name'] for h in result['hits']], ['good.txt'])

    def test_size_budget_declared_and_decoded_limits_do_not_hide_partial_state(self):
        writer = self.host([('a.txt', b'alvo'), ('b.txt', b'alvo more'), ('c.txt', b'alvo more')])
        with patch.object(search, 'MAX_FILE_BYTES', 5):
            result = search.search_attachment_text(self.pdf, request())
            self.assertEqual(len(result['hits']), 1);self.assertEqual(len(result['omissions']), 2)
        # A false small declared size still cannot bypass the decoded-content check.
        for entry in writer.attachment_list:entry.size = NumberObject(1)
        writer.write(self.pdf)
        with patch.object(search, 'MAX_FILE_BYTES', 5):
            result = search.search_attachment_text(self.pdf, request())
            self.assertEqual(len(result['hits']), 1);self.assertFalse(result['complete'])
        with patch.object(search, 'MAX_TOTAL_BYTES', 5):
            result = search.search_attachment_text(self.pdf, request())
            self.assertEqual(len(result['hits']), 1);self.assertEqual(len(result['omissions']), 2)

    def test_entry_page_and_hit_limits_are_explicit(self):
        self.host([('a.txt', b'alvo alvo alvo'), ('b.txt', b'alvo'), ('c.txt', b'alvo')])
        result = search.search_attachment_text(self.pdf, request(max_hits=2))
        self.assertEqual(len(result['hits']), 2);self.assertTrue(result['limit_reached']);self.assertFalse(result['complete'])
        with patch.object(search, 'MAX_FILES', 2):
            result = search.search_attachment_text(self.pdf, request())
            self.assertIsNone(result['omissions'][0]['index']);self.assertEqual(len(result['hits']), 4)
        self.host([('pages.pdf', text_pdf(['alvo', 'alvo']))])
        with patch.object(search, 'MAX_PAGES', 1):
            result = search.search_attachment_text(self.pdf, request())
            self.assertFalse(result['hits']);self.assertFalse(result['complete'])

    def test_advanced_modes_use_same_rules_in_attachment_worker(self):
        self.host([('terms.txt', b'alpha x beta alphabet beta')])
        self.assertEqual(len(search.search_attachment_text(self.pdf, request('alp*', mode='wildcard'))['hits']), 2)
        self.assertEqual(len(search.search_attachment_text(self.pdf, request('alpha beta', mode='proximity', proximity_distance=1))['hits']), 1)
        self.assertFalse(search.search_attachment_text(self.pdf, request('alpha beta', mode='proximity'))['hits'])

    def test_changed_source_during_decode_is_not_a_successful_report(self):
        self.host([('a.txt', b'alvo')])
        def changed():
            with self.pdf.open('ab') as stream:stream.write(b'\nchanged')
            return b'alvo'
        with patch.object(EmbeddedFile, 'content', new_callable=PropertyMock, side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'alterado'):search.search_attachment_text(self.pdf, request())

    def test_invalid_request_fails_before_opening_source(self):
        for value in ({}, request(max_hits=True), request(mode='wildcard', query='*'), request(match_case=1)):
            with self.assertRaises(ValueError):search.search_attachment_text(self.pdf, value)

    def _sleeping_worker(self, argv, **kwargs):
        child = self.original_popen([sys.executable, '-c', 'import time; time.sleep(30)'], **kwargs)
        self.children.append(child)
        return child

    def test_cancellation_terminates_the_actual_child_and_does_not_create_files(self):
        self.host([('a.txt', b'alvo')]);event = threading.Event();self.children = []
        self.original_popen = subprocess.Popen
        timer = threading.Timer(.15, event.set);timer.start()
        try:
            with patch.object(search.subprocess, 'Popen', side_effect=self._sleeping_worker):
                result = search.invoke_attachment_search(self.pdf, 'alvo', SearchOptions(), 100, event)
            self.assertEqual(result['hits'], []);self.assertIsNotNone(self.children[0].poll())
        finally:timer.join()
        self.assertEqual(list(self.root.iterdir()), [self.pdf])

    def test_timeout_terminates_the_actual_child_and_reports_failure(self):
        self.original_popen = subprocess.Popen;self.children = []
        with patch.object(search.subprocess, 'Popen', side_effect=self._sleeping_worker):
            with self.assertRaisesRegex(RuntimeError, 'tempo'):search.invoke_attachment_search(self.pdf, 'alvo', SearchOptions(), 100, timeout=.1)
        self.assertIsNotNone(self.children[0].poll())

    def test_cancellation_after_a_hit_stops_model_emission(self):
        self.host([('a.txt', b'alvo alvo alvo')]);index = TextSearchIndex(self.pdf, 1, page_sizes=[(200, 200)])
        event = threading.Event();seen = []
        def progress(_, batch):seen.extend(batch);event.set()
        hits = index.search('alvo', include_page_text=False, include_attachments=True, cancel=event, on_page=progress)
        self.assertEqual(len(hits), 1);self.assertEqual(hits, seen)


if __name__ == '__main__':unittest.main()
