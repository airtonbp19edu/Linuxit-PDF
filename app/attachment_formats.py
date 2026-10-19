"""Passive text extraction from HTML and selected XML bodies in DOCX/ODT."""
from html.parser import HTMLParser
from io import BytesIO
import re
import zipfile
from xml.etree import ElementTree

MAX_EXPANDED = 2 * 1024 * 1024
OFFICE_SUFFIXES = {'.docx', '.odt', '.xlsx', '.pptx'}
HTML_SUFFIXES = {'.html', '.htm', '.xhtml'}
OTHER_PASSIVE_SUFFIXES={'.rtf'}


def _xml(raw):
    text=raw.decode('utf-8-sig',errors='strict')
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():raise ValueError('Declarações DTD/entidade não são aceitas.')
    tree=ElementTree.fromstring(text);pending=[(tree,0)]
    while pending:
        node,depth=pending.pop()
        if depth>128:raise ValueError('XML Office excede 128 níveis.')
        pending.extend((child,depth+1) for child in node)
    return tree


def _flatten(tree):
    parts=[];size=0
    def append(value):
        nonlocal size
        size+=len(value.encode('utf-8'))
        if size>MAX_EXPANDED:raise ValueError('Texto Office excede 2MiB.')
        parts.append(value)
    def walk(node):
        tag=node.tag.rsplit('}',1)[-1]
        if tag in ('del','instrText','object','OLEObject','drawing'):return
        if tag in ('p','h','tab','br','line-break','table-cell'):append(' ')
        if node.text:append(node.text)
        for child in node:
            walk(child)
            if child.tail:append(child.tail)
        if tag in ('p','h','table-cell'):append(' ')
    walk(tree);return ' '.join(''.join(parts).split())


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
    if suffix=='.rtf':
        from attachment_rtf import extract_rtf
        return extract_rtf(payload)
    if suffix not in OFFICE_SUFFIXES:
        raise ValueError('Formato não suportado pelo extrator passivo.')
    try:
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            entries = archive.infolist()
            if len(entries) > 2000 or sum(e.file_size for e in entries) > MAX_EXPANDED:
                raise ValueError('Contêiner Office excede 2000 entradas ou 2 MiB expandidos.')
            def read(name):
                matches=[e for e in entries if e.filename==name]
                if len(matches)!=1 or matches[0].flag_bits&1:raise ValueError('Parte Office ausente, repetida ou criptografada.')
                with archive.open(matches[0]) as stream:raw=stream.read(MAX_EXPANDED+1)
                if len(raw)>MAX_EXPANDED:raise ValueError('XML Office excede 2MiB.')
                return _xml(raw)
            if suffix=='.docx':
                names=['word/document.xml']+sorted(e.filename for e in entries if re.fullmatch(r'word/(?:header\d*|footer\d*|footnotes|endnotes|comments)\.xml',e.filename))
            elif suffix=='.odt':names=['content.xml']+(['styles.xml'] if any(e.filename=='styles.xml' for e in entries) else [])
            elif suffix=='.pptx':
                names=sorted(e.filename for e in entries if re.fullmatch(r'ppt/(?:slides/slide\d+|notesSlides/notesSlide\d+)\.xml',e.filename))
                if not any('/slides/' in n for n in names):raise ValueError('Apresentação sem slides suportados.')
            else:names=sorted(e.filename for e in entries if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',e.filename))
            if not names or len(names)>256:raise ValueError('Contêiner Office sem partes suportadas ou acima de 256 partes.')
            parts=[];size=0
            def append(text):
                nonlocal size
                size+=len(text.encode('utf-8'))+1
                if size>MAX_EXPANDED:raise ValueError('Texto Office excede 2MiB.')
                parts.append(text)
            if suffix=='.xlsx':
                shared=[]
                if any(e.filename=='xl/sharedStrings.xml' for e in entries):
                    shared=[''.join(n.itertext()) for n in read('xl/sharedStrings.xml') if n.tag.rsplit('}',1)[-1]=='si']
                for name in names:
                    for cell in read(name).iter():
                        if cell.tag.rsplit('}',1)[-1]!='c':continue
                        values=[n.text or '' for n in cell if n.tag.rsplit('}',1)[-1]=='v']
                        value=values[0] if values else ''
                        if cell.get('t')=='s':
                            if not value.isdecimal() or not 0<=int(value)<len(shared):raise ValueError('Referência de texto XLSX inválida.')
                            value=shared[int(value)]
                        elif cell.get('t')=='inlineStr':value=''.join(n.text or '' for n in cell.iter() if n.tag.rsplit('}',1)[-1]=='t')
                        if value:append(value)
            else:
                for name in names:append(_flatten(read(name)))
            result=' '.join(' '.join(parts).split())
            if len(result.encode('utf-8')) > MAX_EXPANDED:
                raise ValueError('Texto Office excede 2 MiB.')
            return result, 'Office: texto do corpo e partes estruturadas suportadas; desenhos/objetos, layout, formatação e cálculo de fórmulas não inspecionados.'
    except (zipfile.BadZipFile, ElementTree.ParseError, RuntimeError, NotImplementedError) as exc:
        raise ValueError('Contêiner Office inválido ou não suportado.') from exc
