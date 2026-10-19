"""Versioned local indexes, preservation, freshness and failure recovery."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_attachment_search import text_pdf, request
import collection_index as index
from pypdf import PdfWriter
from pypdf._page import PageObject


class CollectionIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='linuxit-index-')
        self.root = Path(self.temp.name)
        self.first, self.second = self.root/'one.pdf', self.root/'two.pdf'
        self.first.write_bytes(text_pdf(['other', 'alpha x beta']))
        self.second.write_bytes(text_pdf(['second term']))
        self.output = self.root/'collection.linuxit-index.json'

    def tearDown(self):self.temp.cleanup()

    def build(self, paths=None):return index.build_index(self.output, {'paths': [str(p) for p in (paths or [self.first, self.second])]})

    def test_build_reopen_worker_and_query_preserve_sources_and_real_pages(self):
        before = [p.read_bytes() for p in (self.first, self.second)]
        result = index.invoke_collection('index-build', self.output, {'paths': [str(self.first), str(self.second)]})
        self.assertEqual((result['documents'], result['pages']), (2, 3))
        data, identity = index.load_index(self.output)
        self.assertEqual(identity, result['index_sha256'])
        hits = index.invoke_collection('index-search', self.output, request('alpha'))['hits']
        self.assertEqual([(h['path'], h['page']) for h in hits], [(str(self.first.resolve()), 1)])
        self.assertEqual(before, [p.read_bytes() for p in (self.first, self.second)])
        self.assertEqual(set(p.name for p in self.root.iterdir()), {'one.pdf', 'two.pdf', self.output.name})

    def test_changed_missing_sources_are_excluded_until_explicit_rebuild(self):
        self.build();self.first.write_bytes(text_pdf(['replacement alpha']))
        result = index.search_index(self.output, request('alpha'))
        self.assertEqual(result['hits'], []);self.assertEqual(len(result['stale']), 1)
        self.build()
        self.assertEqual(index.search_index(self.output, request('alpha'))['hits'][0]['page'], 0)
        self.second.unlink()
        self.assertEqual(len(index.search_index(self.output, request('second'))['stale']), 1)

    def test_update_failure_preserves_old_index_and_removes_temporary(self):
        self.build();before = self.output.read_bytes()
        with patch.object(index.os, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):self.build()
        self.assertEqual(self.output.read_bytes(), before)
        self.assertFalse(list(self.root.glob('.linuxit-index-*')))

    def test_partial_creation_failure_removes_the_new_destination(self):
        def publication_failed(temporary, destination):
            # Staged content must already be complete before exclusive publication.
            body, identity = index.load_index(temporary)
            self.assertEqual(len(body['documents']), 2)
            self.assertFalse(destination.exists())
            raise OSError('disk full')
        with patch.object(index, '_publish_new_index', side_effect=publication_failed), self.assertRaises(OSError):self.build()
        self.assertFalse(self.output.exists());self.assertFalse(list(self.root.glob('.linuxit-index-*')))

    def test_concurrent_change_to_existing_index_is_preserved(self):
        self.build();original = index.verify_document;replacement = None
        def other_writer(path, identity):
            nonlocal replacement
            if replacement is None:
                body = json.loads(self.output.read_bytes());body.pop('body_sha256')
                body['created_at_utc'] = '2026-10-17T00:00:00+00:00';body['body_sha256'] = index._body_hash(body)
                replacement = json.dumps(body).encode();self.output.write_bytes(replacement)
            return original(path, identity)
        with patch.object(index, 'verify_document', side_effect=other_writer), self.assertRaisesRegex(ValueError, 'índice mudou'):
            self.build()
        self.assertEqual(self.output.read_bytes(), replacement)

    def test_unknown_destination_tampering_and_source_destination_are_refused(self):
        self.output.write_bytes(b'keep unrelated file')
        with self.assertRaises(ValueError):self.build()
        self.assertEqual(self.output.read_bytes(), b'keep unrelated file')
        self.output.unlink();self.build()
        body = json.loads(self.output.read_bytes());body['documents'][0]['pages'][0] = 'tampered'
        self.output.write_text(json.dumps(body), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'hash'):index.load_index(self.output)
        disguised_source = self.root/'pdf.linuxit-index.json';disguised_source.write_bytes(self.first.read_bytes())
        with self.assertRaises(ValueError):index.build_index(disguised_source, {'paths': [str(disguised_source)]})

    def test_limits_and_duplicate_paths_are_rejected_without_index_replacement(self):
        self.build();before = self.output.read_bytes()
        for name, value in [('MAX_PAGES', 2), ('MAX_INPUT_BYTES', 1), ('MAX_TEXT_BYTES', 2), ('MAX_DOCUMENTS', 1)]:
            with patch.object(index, name, value), self.assertRaises(ValueError):self.build()
            self.assertEqual(before, self.output.read_bytes())
        with self.assertRaises(ValueError):self.build([self.first, self.first])
        self.assertEqual(before, self.output.read_bytes())

    def test_encrypted_and_invalid_pdf_do_not_replace_valid_index(self):
        self.build();before = self.output.read_bytes()
        encrypted = PdfWriter();encrypted.add_blank_page(20, 20);encrypted.encrypt('secret');encrypted.write(self.second)
        with self.assertRaisesRegex(ValueError, 'criptografado'):self.build()
        self.assertEqual(before, self.output.read_bytes())
        self.second.write_bytes(b'invalid PDF')
        with self.assertRaises(Exception):self.build()
        self.assertEqual(before, self.output.read_bytes())

    def test_sources_changed_after_extraction_abort_before_publication(self):
        self.build();before = self.output.read_bytes();original = PageObject.extract_text;calls = 0
        def change_source(page, *args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:self.first.write_bytes(text_pdf(['changed source']))
            return original(page, *args, **kwargs)
        with patch.object(PageObject, 'extract_text', change_source), self.assertRaisesRegex(ValueError, 'fonte'):
            self.build()
        self.assertEqual(before, self.output.read_bytes())

    def test_all_query_modes_limit_and_stale_after_matching(self):
        self.build()
        self.assertEqual(len(index.search_index(self.output, request('alp*', mode='wildcard'))['hits']), 1)
        self.assertEqual(len(index.search_index(self.output, request('alpha beta', mode='proximity', proximity_distance=1))['hits']), 1)
        result = index.search_index(self.output, request('term', max_hits=1))
        self.assertTrue(result['limit_reached']);self.assertEqual(len(result['hits']), 1)
        original = index.verify_document;calls = 0
        def change_after_match(path, identity):
            nonlocal calls
            calls += 1
            if calls == 3:self.first.write_bytes(text_pdf(['different']))
            return original(path, identity)
        with patch.object(index, 'verify_document', side_effect=change_after_match):
            result = index.search_index(self.output, request('alpha'))
        self.assertFalse(result['hits']);self.assertEqual(len(result['stale']), 1)

    def test_invalid_schema_even_with_matching_hash_is_not_loaded(self):
        self.build();original = json.loads(self.output.read_bytes())
        for change in ('duplicate', 'relative', 'pages', 'unknown'):
            body = json.loads(json.dumps(original))
            if change == 'duplicate':body['documents'].append(body['documents'][0])
            elif change == 'relative':body['documents'][0]['path'] = 'relative.pdf'
            elif change == 'pages':body['documents'][0]['pages'] = [False]
            else:body['schema'] = 'unknown'
            body.pop('body_sha256');body['body_sha256'] = index._body_hash(body)
            self.output.write_text(json.dumps(body), encoding='utf-8')
            with self.subTest(change=change), self.assertRaises(ValueError):index.load_index(self.output)

    def test_index_changed_during_query_is_not_a_successful_report(self):
        self.build();original = index.query_spans;changed = False
        def mutate(*args, **kwargs):
            nonlocal changed
            if not changed:
                with self.output.open('ab') as stream:stream.write(b'\n')
                changed = True
            yield from original(*args, **kwargs)
        with patch.object(index, 'query_spans', mutate), self.assertRaisesRegex(ValueError, 'índice mudou'):
            index.search_index(self.output, request('alpha'))


if __name__ == '__main__':unittest.main()
