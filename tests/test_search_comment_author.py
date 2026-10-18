"""Author-search regression from the bounded offline Foxit observation."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(os.environ.get(
    'PRINT_VIEW_TEST_APP', Path(__file__).resolve().parents[1] / 'app'))))
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter
from pypdf.annotations import Text
from pypdf.generic import NameObject, TextStringObject
from search_engine import TextSearchIndex


class CommentAuthorTests(unittest.TestCase):
    def test_preserved_author_only_term_matches_the_recorded_page(self):
        source = Path(__file__).resolve().parents[1] / 'testes/fixtures/campaign18/busca-escopos.pdf'
        before = source.read_bytes()
        self.assertEqual(hashlib.sha256(before).hexdigest(),
                         '25b8f1cbb1b589a4460074144553869796f898b155c03527dc1e409d85217b01')
        index = TextSearchIndex(source, page_count=2, page_sizes=[(420, 595)] * 2)
        self.assertEqual(index.search('Autor', include_page_text=False), [])
        hits = index.search('Autor', include_page_text=False, include_comments=True)
        self.assertEqual([(h['source'], h['page'], h['rects']) for h in hits],
                         [('comment', 0, [])])
        self.assertIn('Autor não pesquisável', hits[0]['snippet'])
        self.assertEqual(source.read_bytes(), before)

    def test_author_matching_respects_case_whole_words_and_accents(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'author.pdf'
            writer = PdfWriter()
            writer.add_blank_page(width=420, height=595)
            note = Text(rect=(20, 20, 60, 60), text='body')
            note[NameObject('/T')] = TextStringObject('Álvaro ALVARO_EXTRA')
            writer.add_annotation(0, note)
            writer.write(source)
            index = TextSearchIndex(source, page_count=1, page_sizes=[(420, 595)])
            options = {'include_page_text': False, 'include_comments': True}
            self.assertEqual(index.search('álvaro', match_case=True, **options), [])
            self.assertEqual(len(index.search('Álvaro', match_case=True, **options)), 1)
            self.assertEqual(len(index.search('alvaro', whole_words=True,
                                              ignore_accents=True, **options)), 1)
            self.assertEqual(len(index.search('alvaro', ignore_accents=True, **options)), 2)
            self.assertEqual(index.search('alvaro', whole_words=True, **options), [])

    def test_comment_without_author_still_searches_subject_and_body(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'anonymous.pdf'
            writer = PdfWriter()
            writer.add_blank_page(width=420, height=595)
            note = Text(rect=(20, 20, 60, 60), text='conteúdo')
            note[NameObject('/Subj')] = TextStringObject('assunto')
            writer.add_annotation(0, note)
            writer.write(source)
            index = TextSearchIndex(source, page_count=1, page_sizes=[(420, 595)])
            options = {'include_page_text': False, 'include_comments': True}
            self.assertEqual(len(index.search('assunto', **options)), 1)
            self.assertEqual(len(index.search('conteúdo', **options)), 1)
            self.assertEqual(index.search('Autor', **options), [])
