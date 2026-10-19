"""Passive text extraction from HTML and selected XML bodies in DOCX/ODT."""
from html.parser import HTMLParser
from io import BytesIO
import zipfile
from xml.etree import ElementTree

MAX_EXPANDED = 2 * 1024 * 1024
OFFICE_SUFFIXES = {'.docx', '.odt'}
HTML_SUFFIXES = {'.html', '.htm', '.xhtml'}


class _HTMLText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.hidden = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        elif tag in ('p', 'br', 'div', 'li', 'td', 'tr', 'h1', 'h2', 'h3'):
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
        else:
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def extract_passive_text(payload, suffix):
    """No paths are extracted, no relationships/URLs/macros are evaluated.

    Returns text plus an optional partial-content notice. Office body only;
    drawings, equations, headers and embedded objects are outside this contract.
    """
    if suffix in HTML_SUFFIXES:
        parser = _HTMLText()
        parser.feed(payload.decode('utf-8-sig', errors='strict'))
        return ' '.join(''.join(parser.parts).split()), None
    if suffix not in OFFICE_SUFFIXES:
        raise ValueError('Formato não suportado pelo extrator passivo.')
    try:
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            entries = archive.infolist()
            if len(entries) > 2000 or sum(e.file_size for e in entries) > MAX_EXPANDED:
                raise ValueError('Contêiner Office excede 2000 entradas ou 2 MiB expandidos.')
            name = 'word/document.xml' if suffix == '.docx' else 'content.xml'
            matches = [e for e in entries if e.filename == name]
            if len(matches) != 1 or matches[0].flag_bits & 1:
                raise ValueError('Corpo Office ausente, repetido ou criptografado.')
            with archive.open(matches[0]) as stream:
                raw = stream.read(MAX_EXPANDED + 1)
            if len(raw) > MAX_EXPANDED:
                raise ValueError('XML Office excede 2 MiB.')
            # Reject declarations before parsing, including non-UTF8 evasions.
            text = raw.decode('utf-8-sig', errors='strict')
            if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
                raise ValueError('Declarações DTD/entidade não são aceitas.')
            tree = ElementTree.fromstring(text)
            parts = []
            def walk(node, depth=0):
                if depth > 128:
                    raise ValueError('XML Office excede 128 níveis.')
                tag = node.tag.rsplit('}', 1)[-1]
                if tag in ('p', 'h', 'tab', 'br', 'line-break', 'table-cell'):
                    parts.append(' ')
                if node.text: parts.append(node.text)
                for child in node:
                    walk(child, depth + 1)
                    if child.tail: parts.append(child.tail)
                if tag in ('p', 'h', 'table-cell'): parts.append(' ')
            walk(tree)
            result = ' '.join(''.join(parts).split())
            if len(result.encode('utf-8')) > MAX_EXPANDED:
                raise ValueError('Texto Office excede 2 MiB.')
            return result, 'Office: somente texto do corpo; cabeçalhos, desenhos, equações e objetos não inspecionados.'
    except (zipfile.BadZipFile, ElementTree.ParseError, RuntimeError, NotImplementedError) as exc:
        raise ValueError('Contêiner Office inválido ou não suportado.') from exc
