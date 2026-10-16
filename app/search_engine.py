"""Page-wise text search using the same geometry as reader selection."""
from collections import OrderedDict
from pathlib import Path
from dataclasses import dataclass

from pdf_panels import inspect_document_panels
import threading
import unicodedata

from rendering import document_info, extract_page_words


def normalized(text, match_case=False, ignore_accents=False):
    text = unicodedata.normalize('NFC', text)
    if not match_case:
        text = text.casefold()
    if ignore_accents:
        text = ''.join(c for c in unicodedata.normalize('NFD', text)
                       if unicodedata.category(c) != 'Mn')
    return text


@dataclass(frozen=True)
class SearchOptions:
    """Independent Linuxit contract; not a recovered Foxit structure layout."""
    match_case: bool = False
    whole_words: bool = False
    ignore_accents: bool = False
    join_hyphens: bool = False
    include_page_text: bool = True
    include_bookmarks: bool = False
    include_comments: bool = False

    def text_options(self):
        return {key: getattr(self, key) for key in
                ('match_case', 'whole_words', 'ignore_accents', 'join_hyphens')}


def literal_spans(text, needle, whole_words=False):
    """Non-overlapping literal matches on normalized strings; no regex execution."""
    if not needle:
        return
    def is_word(character):
        return character == '_' or unicodedata.category(character)[0] in 'LNM'
    start = 0
    while True:
        pos = text.find(needle, start)
        if pos < 0:
            return
        end = pos + len(needle)
        bounded = ((pos == 0 or not is_word(text[pos - 1]))
                   and (end == len(text) or not is_word(text[end])))
        if not whole_words or bounded:
            yield pos, end
        start = end


def page_hits(data, query, page_index, match_case=False, whole_words=False,
              ignore_accents=False, join_hyphens=False):
    needle = ' '.join(normalized(query, match_case, ignore_accents).split())
    if not needle:
        return []
    blocks = {}
    for word in data['words']:
        blocks.setdefault(word['block'], []).append(word)
    hits = []
    for words in blocks.values():
        chars, owners = [], []
        for idx, word in enumerate(words):
            join = (idx > 0 and join_hyphens and word['line'] != words[idx - 1]['line']
                    and words[idx - 1]['text'].endswith(('-', '\u00ad')))
            if join:
                if chars and chars[-1] in ('-', '\u00ad'):
                    chars.pop(); owners.pop()
            elif idx:
                chars.append(' '); owners.append(None)
            folded = normalized(word['text'], match_case, ignore_accents)
            chars.extend(folded); owners.extend([idx] * len(folded))
        text = ''.join(chars)
        for pos, end in literal_spans(text, needle, whole_words):
            selected = sorted({owner for owner in owners[pos:end] if owner is not None})
            if not selected:
                continue
            hits.append({'page': page_index, 'width': data['width'], 'height': data['height'],
                         'source': 'page_text',
                         'rects': [[words[i][key] for key in ('x0', 'y0', 'x1', 'y1')] for i in selected],
                         'text': ' '.join(words[i]['text'] for i in selected),
                         'snippet': ' '.join(w['text'] for w in words[max(0, min(selected)-5):max(selected)+9])[:180]})
    return hits


class TextSearchIndex:
    """Retain at most 64 page maps; searches can stop between page extractions."""
    def __init__(self, path, page_count=None, max_cached_pages=64, page_sizes=None):
        self.path = str(Path(path).resolve())
        self.identity = self._identity()
        if page_sizes is None:
            info = document_info(self.path)
            page_sizes = info['sizes']
        self.page_sizes = page_sizes
        self.page_count = page_count if page_count is not None else len(page_sizes)
        self.max_cached_pages = max(1, int(max_cached_pages))
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        self.panel_cache = None

    def _identity(self):
        stat = Path(self.path).stat()
        return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns

    def page(self, index):
        if self._identity() != self.identity:
            raise RuntimeError('O PDF foi alterado. Reabra o documento para pesquisar.')
        with self.lock:
            data = self.cache.get(index)
            if data is not None:
                self.cache.move_to_end(index)
                return data
        data = extract_page_words(self.path, index, page_size=self.page_sizes[index])
        if self._identity() != self.identity:
            raise RuntimeError('O PDF foi alterado durante a pesquisa. Reabra o documento.')
        with self.lock:
            self.cache[index] = data
            self.cache.move_to_end(index)
            while len(self.cache) > self.max_cached_pages:
                self.cache.popitem(last=False)
        return data

    def _panels(self):
        if self._identity() != self.identity:
            raise RuntimeError('O PDF foi alterado. Reabra o documento para pesquisar.')
        with self.lock:
            cached = self.panel_cache
        if cached is not None:
            return cached
        data = inspect_document_panels(self.path)
        if self._identity() != self.identity:
            raise RuntimeError('O PDF foi alterado durante a pesquisa. Reabra o documento.')
        with self.lock:
            self.panel_cache = data
        return data

    def _metadata_hits(self, query, options, cancel):
        if cancel is not None and cancel.is_set():
            return
        data = self._panels()
        needle = ' '.join(normalized(query, options.match_case, options.ignore_accents).split())
        sources = []
        if options.include_bookmarks:
            sources.append(('bookmark', data['bookmarks']))
        if options.include_comments:
            sources.append(('comment', data['comments']))
        for source, items in sources:
            for item in items:
                if cancel is not None and cancel.is_set():
                    return
                text = item['title'] if source == 'bookmark' else ' '.join(
                    value for value in (item.get('subject', ''), item.get('contents', '')) if value)
                haystack = ' '.join(normalized(text, options.match_case, options.ignore_accents).split())
                page = item.get('page')
                if not isinstance(page, int) or not 0 <= page < self.page_count:
                    page = None
                width, height = self.page_sizes[page] if page is not None else (0, 0)
                for _ in literal_spans(haystack, needle, options.whole_words):
                    if cancel is not None and cancel.is_set():
                        return
                    yield {'source': source, 'page': page, 'width': width, 'height': height,
                           'rects': [], 'text': text, 'snippet': ' '.join(text.split())[:180]}

    def search(self, query, max_hits=5000, cancel=None, on_page=None, **kwargs):
        if len(query) > 256:
            raise ValueError('A pesquisa deve ter no máximo 256 caracteres.')
        options = SearchOptions(**kwargs)
        if not query.strip() or max_hits <= 0 or (cancel is not None and cancel.is_set()):
            return []
        if self._identity() != self.identity:
            raise RuntimeError('O PDF foi alterado. Reabra o documento para pesquisar.')
        hits = []
        if options.include_page_text:
            for index in range(self.page_count):
                if cancel is not None and cancel.is_set():
                    return hits
                data = self.page(index)
                if cancel is not None and cancel.is_set():
                    return hits
                batch = page_hits(data, query, index, **options.text_options())[:max_hits - len(hits)]
                hits.extend(batch)
                if on_page is not None:
                    on_page(index + 1, batch)
                if len(hits) >= max_hits:
                    return hits
        if options.include_bookmarks or options.include_comments:
            for hit in self._metadata_hits(query, options, cancel):
                if cancel is not None and cancel.is_set():
                    break
                hits.append(hit)
                if on_page is not None:
                    on_page(self.page_count if options.include_page_text else 0, [hit])
                if len(hits) >= max_hits:
                    break
        return hits
