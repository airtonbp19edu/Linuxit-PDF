"""Own query semantics and geometry; no claims about the Foxit analyzer."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', Path(__file__).resolve().parents[1] / 'app'))))
from search_matching import normalized, query_spans, validate_query
from search_engine import TextSearchIndex, page_hits


class SearchModeTests(unittest.TestCase):
    def test_literal_preserves_punctuation_unicode_and_whole_words(self):
        self.assertEqual(list(query_spans('a*b aXb', 'a*b')), [(0, 3)])
        text = normalized('Árvore Straße')
        self.assertEqual(list(query_spans(text, normalized('STRASSE'))), [(7, 14)])
        self.assertEqual(list(query_spans('किताब', 'क', True)), [])
        self.assertEqual(normalized('Ac\u0327a\u0303o', ignore_accents=True), 'acao')
        expanded = normalized('ß' * 200)
        self.assertEqual(list(query_spans(expanded, expanded)), [(0, 400)])

    def test_wildcards_match_complete_unicode_words_without_regex(self):
        self.assertEqual(list(query_spans('alvo alvos xalvo aLvo', 'alv?', mode='wildcard')), [(0, 4)])
        self.assertEqual(list(query_spans('alvo alvos xalvo', 'alv*', mode='wildcard')), [(0, 4), (5, 10)])
        self.assertEqual(list(query_spans('a ab acb axxxb', 'a*b', mode='wildcard')), [(2, 4), (5, 8), (9, 14)])
        self.assertEqual(list(query_spans('café cafe', 'caf?', mode='wildcard')), [(0, 4), (5, 9)])

    def test_proximity_uses_total_intervening_words_and_query_order(self):
        text = 'alpha x beta y gamma alpha beta gamma'
        self.assertEqual(list(query_spans(text, 'alpha beta gamma', mode='proximity', proximity_distance=1)), [(21, 37)])
        self.assertEqual(list(query_spans(text, 'alpha beta gamma', mode='proximity', proximity_distance=2)), [(0, 20), (21, 37)])
        self.assertEqual(list(query_spans('beta alpha', 'alpha beta', mode='proximity', proximity_distance=50)), [])

    def test_repeated_terms_and_nonoverlapping_occurrences(self):
        self.assertEqual(list(query_spans('a a a a', 'a a', mode='proximity')), [(0, 3), (4, 7)])
        self.assertEqual(list(query_spans('a x a', 'a a', mode='proximity')), [])
        self.assertEqual(list(query_spans('a x a', 'a a', mode='proximity', proximity_distance=1)), [(0, 5)])

    def test_invalid_syntax_distance_and_expansion_are_rejected(self):
        for query in ('*', '?', 'a b', 'a.b', 'a' * 65, 'a' + '*' * 9):
            with self.subTest(query=query), self.assertRaises(ValueError):
                validate_query(query, 'wildcard')
        for query in ('one', 'a b c d e f g h i', 'a + b'):
            with self.assertRaises(ValueError):validate_query(query, 'proximity')
        for distance in (-1, 51, True, 1.5):
            with self.assertRaises(ValueError):validate_query('a b', 'proximity', distance)
        with self.assertRaises(ValueError):validate_query('word', 'stemming')

    def test_advanced_token_length_guard_does_not_change_literal_contract(self):
        text = 'a' * 4097
        with self.assertRaises(ValueError):list(query_spans(text, 'a*', mode='wildcard'))
        self.assertEqual(len(list(query_spans(text, 'a'))), 4097)

    def test_page_geometry_keeps_owner_rectangles_for_both_modes(self):
        words = [{'text': text, 'block': 0, 'line': 0, 'x0': i * 10, 'y0': 0, 'x1': i * 10 + 9, 'y1': 10}
                 for i, text in enumerate(('Alpha', 'between', 'beta', 'alphabet'))]
        page = {'width': 100, 'height': 100, 'words': words}
        wildcard = page_hits(page, 'alp*', 0, mode='wildcard')
        self.assertEqual([hit['rects'][0][0] for hit in wildcard], [0, 30])
        proximity = page_hits(page, 'alpha beta', 0, mode='proximity', proximity_distance=1)
        self.assertEqual(len(proximity), 1)
        self.assertEqual(len(proximity[0]['rects']), 3)
        self.assertEqual(proximity[0]['text'], 'Alpha between beta')

    def test_metadata_uses_same_modes_and_invalid_query_does_not_parse(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'source.pdf'
            path.write_bytes(b'identity only; metadata supplied by the test')
            index = TextSearchIndex(path, 1, page_sizes=[(100, 100)])
            panels = {'bookmarks': [{'title': 'Alpha beta', 'page': 0}], 'comments': []}
            with patch.object(index, '_panels', return_value=panels):
                hits = index.search('alp*', mode='wildcard', include_page_text=False, include_bookmarks=True)
                self.assertEqual([(h['source'], h['page']) for h in hits], [('bookmark', 0)])
                self.assertEqual(len(index.search('alpha beta', mode='proximity', include_page_text=False, include_bookmarks=True)), 1)
            with patch.object(index, '_panels', side_effect=AssertionError('must not parse invalid syntax')):
                with self.assertRaises(ValueError):index.search('*', mode='wildcard', include_bookmarks=True)


if __name__ == '__main__':unittest.main()
