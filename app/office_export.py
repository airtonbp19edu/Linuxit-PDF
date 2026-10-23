"""Own export of PDF text to editable DOCX and ODT documents.

Reads blocks and lines from Poppler (`pdftotext -bbox-layout`), keeps the reading order
Poppler reports, turns every block into one paragraph with an approximate font size taken
from the line height, and starts every PDF page on a new document page. Output is plain
WordprocessingML / OpenDocument Text written here; no template or third-party document is
copied. Bounded: images, tables, columns, colours and exact fonts are not reproduced.
"""
import html
import re
import zipfile
from xml.sax.saxutils import escape

BLOCK = re.compile(r'<block xMin="[^"]*" yMin="([-0-9.]+)" xMax="[^"]*" yMax="([-0-9.]+)">(.*?)</block>', re.S)
LINE = re.compile(r'<line xMin="[^"]*" yMin="([-0-9.]+)" xMax="[^"]*" yMax="([-0-9.]+)">(.*?)</line>', re.S)
WORD = re.compile(r'<word [^>]*>(.*?)</word>', re.S)
PAGE = re.compile(r'<page [^>]*>(.*?)</page>', re.S)
CONTROL = re.compile('[\x00-\x08\x0b\x0c\x0e-\x1f]')
MAX_PARAGRAPHS = 50000


def _clean(text):
    return CONTROL.sub('', text)


def paragraphs_from_bbox(markup):
    """[[{'text', 'size'}...] per page] from pdftotext -bbox-layout XHTML."""
    pages, count = [], 0
    for page in PAGE.findall(markup):
        items = []
        for _, _, block in BLOCK.findall(page):
            lines, heights = [], []
            for y0, y1, line in LINE.findall(block):
                words = [_clean(html.unescape(w)) for w in WORD.findall(line)]
                if words:
                    lines.append(' '.join(words))
                    heights.append(max(1.0, float(y1) - float(y0)))
            if not lines:
                continue
            text = ' '.join(lines)
            text = re.sub(r'(\w)- (\w)', r'\1\2', text)  # join words hyphenated at line ends
            size = sorted(heights)[len(heights) // 2] * 0.85
            items.append({'text': text, 'size': max(6.0, min(72.0, round(size * 2) / 2))})
            count += 1
            if count > MAX_PARAGRAPHS:
                raise ValueError('Documento acima de 50.000 parágrafos para exportação editável.')
        pages.append(items)
    return pages


DOCX_TYPES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
              '</Types>')
DOCX_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
             '</Relationships>')
DOCUMENT_RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                 '</Relationships>')
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
DOCX_STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               f'<w:styles xmlns:w="{W}"><w:docDefaults><w:rPrDefault><w:rPr>'
               '<w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans" w:cs="Liberation Sans"/>'
               '<w:sz w:val="22"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr>'
               '</w:pPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
               '<w:name w:val="Normal"/></w:style></w:styles>')


def write_docx(pages, path):
    body = []
    for index, items in enumerate(pages):
        if not items:
            items = [{'text': '', 'size': 11.0}]
        for number, item in enumerate(items):
            page_break = '<w:pPr><w:pageBreakBefore/></w:pPr>' if index and number == 0 else ''
            half_points = int(round(item['size'] * 2))
            body.append(f'<w:p>{page_break}<w:r><w:rPr><w:sz w:val="{half_points}"/><w:szCs w:val="{half_points}"/></w:rPr>'
                        f'<w:t xml:space="preserve">{escape(item["text"])}</w:t></w:r></w:p>')
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:document xmlns:w="{W}"><w:body>{"".join(body)}'
                '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="0" w:footer="0" w:gutter="0"/>'
                '</w:sectPr></w:body></w:document>')
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('[Content_Types].xml', DOCX_TYPES)
        archive.writestr('_rels/.rels', DOCX_RELS)
        archive.writestr('word/_rels/document.xml.rels', DOCUMENT_RELS)
        archive.writestr('word/document.xml', document)
        archive.writestr('word/styles.xml', DOCX_STYLES)


ODF_NS = ('xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
          'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
          'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
          'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"')
ODT_MANIFEST = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">'
                '<manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.text"/>'
                '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>'
                '<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>'
                '</manifest:manifest>')
ODT_STYLES = ('<?xml version="1.0" encoding="UTF-8"?>'
              f'<office:document-styles {ODF_NS} office:version="1.2"><office:styles>'
              '<style:default-style style:family="paragraph"><style:paragraph-properties fo:margin-bottom="0.21cm"/>'
              '<style:text-properties style:font-name="Liberation Sans" fo:font-size="11pt"/></style:default-style>'
              '</office:styles><office:automatic-styles><style:page-layout style:name="pm1">'
              '<style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm" fo:margin-top="2cm" '
              'fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm"/></style:page-layout>'
              '</office:automatic-styles><office:master-styles>'
              '<style:master-page style:name="Standard" style:page-layout-name="pm1"/></office:master-styles>'
              '</office:document-styles>')


def write_odt(pages, path):
    sizes = sorted({item['size'] for items in pages for item in items} | {11.0})
    names = {size: f'P{index}' for index, size in enumerate(sizes, 1)}
    styles = []
    for size, name in names.items():
        styles.append(f'<style:style style:name="{name}" style:family="paragraph"><style:text-properties fo:font-size="{size:g}pt"/></style:style>'
                      f'<style:style style:name="{name}B" style:family="paragraph"><style:paragraph-properties fo:break-before="page"/>'
                      f'<style:text-properties fo:font-size="{size:g}pt"/></style:style>')
    body = []
    for index, items in enumerate(pages):
        if not items:
            items = [{'text': '', 'size': 11.0}]
        for number, item in enumerate(items):
            style = names[item['size']] + ('B' if index and number == 0 else '')
            body.append(f'<text:p text:style-name="{style}">{escape(item["text"])}</text:p>')
    content = ('<?xml version="1.0" encoding="UTF-8"?>'
               f'<office:document-content {ODF_NS} office:version="1.2">'
               f'<office:automatic-styles>{"".join(styles)}</office:automatic-styles>'
               f'<office:body><office:text>{"".join(body)}</office:text></office:body></office:document-content>')
    with zipfile.ZipFile(path, 'w') as archive:
        # The mimetype entry must be first and stored uncompressed (ODF 1.2, part 3).
        archive.writestr(zipfile.ZipInfo('mimetype'), 'application/vnd.oasis.opendocument.text', compress_type=zipfile.ZIP_STORED)
        archive.writestr('META-INF/manifest.xml', ODT_MANIFEST, compress_type=zipfile.ZIP_DEFLATED)
        archive.writestr('styles.xml', ODT_STYLES, compress_type=zipfile.ZIP_DEFLATED)
        archive.writestr('content.xml', content, compress_type=zipfile.ZIP_DEFLATED)


def verify_office(path, kind, expected_pages):
    """Parse the produced package back and count paragraphs and page starts."""
    import xml.etree.ElementTree as ET
    with zipfile.ZipFile(path) as archive:
        if kind == 'odt':
            first = archive.infolist()[0]
            if first.filename != 'mimetype' or first.compress_type != zipfile.ZIP_STORED:
                raise ValueError('ODT gerado sem mimetype inicial não comprimido.')
            root = ET.fromstring(archive.read('content.xml'))
            ET.fromstring(archive.read('styles.xml'))
            ns = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
            paragraphs = root.iter(ns + 'p')
            starts = 1 + sum(1 for p in root.iter(ns + 'p') if p.get(ns + 'style-name', '').endswith('B'))
        else:
            root = ET.fromstring(archive.read('word/document.xml'))
            ET.fromstring(archive.read('word/styles.xml'))
            paragraphs = root.iter('{%s}p' % W)
            starts = 1 + sum(1 for _ in root.iter('{%s}pageBreakBefore' % W))
        count = sum(1 for _ in paragraphs)
    if starts != expected_pages or count < expected_pages:
        raise ValueError('Documento editável gerado não confere com as páginas do PDF.')
    return count
