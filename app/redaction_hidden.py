"""Opt-in removal of marked words from explicitly selected hidden PDF data.

Words come from Poppler geometry, never a guessed text/rectangle association.
This is deliberately not a document-wide sanitiser or an OCR engine.
"""
from io import BytesIO
from pathlib import Path
import math
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET

from platform_runtime import subprocess_options
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject, DecodedStreamObject

MAX_XML = 8 * 1024**2
MAX_TEXT = 2 * 1024**2
TEXT_SUFFIXES = {'.txt', '.csv', '.md', '.log', '.json', '.xml'}


def options(request):
    flags = request.get('hidden', {})
    if not isinstance(flags, dict) or set(flags) - {'metadata', 'bookmarks', 'attachments'} or any(type(v) is not bool for v in flags.values()):
        raise ValueError('Opções de redação de dados ocultos inválidas.')
    return flags


def words_from_bbox(raw, page, boxes):
    if len(raw) > MAX_XML or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('Geometria de palavras acima do limite ou XML não permitido.')
    root = ET.fromstring(raw)
    pages = [n for n in root.iter() if n.tag.rsplit('}', 1)[-1] == 'page']
    if len(pages) != 1:
        raise ValueError('Geometria de palavras sem página única.')
    media = page.mediabox
    width, height = (float(pages[0].get(k, 'nan')) for k in ('width', 'height'))
    if not all(math.isfinite(v) for v in (width, height)) or abs(width - float(media.width)) > .02 or abs(height - float(media.height)) > .02:
        raise ValueError('Dimensões da geometria de palavras divergentes.')
    terms, count = set(), 0
    for node in pages[0].iter():
        if node.tag.rsplit('}', 1)[-1] != 'word':
            continue
        count += 1
        if count > 100000:
            raise ValueError('Página acima do limite de palavras.')
        from math import isfinite
        coords = [float(node.attrib[k]) for k in ('xMin', 'yMin', 'xMax', 'yMax')]
        if not all(isfinite(v) for v in coords) or coords[0] >= coords[2] or coords[1] >= coords[3]:
            raise ValueError('Retângulo de palavra inválido.')
        x0, y0, x1, y1 = coords
        rect = (float(media.left)+x0, float(media.top)-y1, float(media.left)+x1, float(media.top)-y0)
        if any(rect[0] < b[2] and b[0] < rect[2] and rect[1] < b[3] and b[1] < rect[3] for b in boxes):
            # Keep punctuation too: matching a word as a substring errs toward
            # removal, and covers names such as segredo.txt and segredo_2026.
            word = unicodedata.normalize('NFC', ''.join(node.itertext())).strip()
            if word:
                if len(word) > 256:
                    raise ValueError('Palavra marcada acima de 256 caracteres.')
                terms.add(word)
    return terms


def marked_words(reader, plan, work):
    terms = set()
    for index, item in plan.items():
        single = PdfWriter()
        page = single.add_page(reader.pages[index])
        page.pop('/Annots', None)
        page[NameObject('/Rotate')] = NumberObject(0)
        page.cropbox = page.mediabox
        source, output = work/'words.pdf', work/'words.xml'
        single.write(source)
        try:
            result = subprocess.run(['pdftotext', '-bbox', '-enc', 'UTF-8', str(source), str(output)],
                                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    timeout=60, **subprocess_options())
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ValueError('Dados ocultos requerem pdftotext com geometria de palavras; nenhuma cópia publicada.') from exc
        if result.returncode or not output.is_file() or output.stat().st_size > MAX_XML:
            raise ValueError('Não foi possível obter palavras sob as marcas; nenhuma cópia publicada.')
        raw = output.read_bytes()
        # Poppler emits the XHTML public DOCTYPE itself. Remove ONLY its exact
        # fixed declaration before the strict XML parser; arbitrary DTDs fail.
        raw = raw.replace(b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', b'')
        terms.update(words_from_bbox(raw, page, [b for _, areas, _ in item['marks'] for b in areas]))
        if len(terms) > 4096:
            raise ValueError('Acima de 4096 palavras marcadas para dados ocultos.')
        source.unlink();output.unlink()
    if not terms:
        raise ValueError('Nenhuma palavra extraível sob as marcas. Dados ocultos não foram considerados limpos; OCR não é executado.')
    return terms


def sanitise(writer, terms, flags):
    """Modify a disposable clone only. Unhandled attachment data aborts it."""
    if not terms or len(terms) > 4096 or any(not isinstance(t,str) or not t or len(t)>256 for t in terms):
        raise ValueError('Conjunto de palavras de redação inválido.')
    pattern = re.compile('|'.join(re.escape(t) for t in sorted(terms, key=lambda t: (-len(t), t))), re.IGNORECASE)
    def clean(text):
        return pattern.sub('[REDACTED]', unicodedata.normalize('NFC', str(text)))
    report = dict(metadata_removed=False, bookmark_titles_changed=0, attachments_checked=0,
                  attachment_strings_changed=0, attachment_contents_changed=0)
    root = writer.root_object
    if flags.get('metadata'):
        # Remove Info and XMP in full, rather than leave alternative encodings,
        # custom properties or XMP attributes containing a marked word.
        writer.metadata = None
        root.pop('/Metadata', None)
        report['metadata_removed'] = True
    if flags.get('bookmarks'):
        outline = root.get('/Outlines')
        stack = [outline.get_object().get('/First')] if outline else []
        seen = set()
        while stack:
            ref = stack.pop()
            if ref is None:
                continue
            node = ref.get_object()
            if not isinstance(node, DictionaryObject) or id(node) in seen or len(seen) >= 10000:
                raise ValueError('Árvore de marcadores inválida ou acima do limite.')
            seen.add(id(node))
            if '/Title' in node:
                if not isinstance(node['/Title'], str):
                    raise ValueError('Título de marcador não textual.')
                before = str(node['/Title']);after = clean(before)
                node[NameObject('/Title')] = TextStringObject(after)
                report['bookmark_titles_changed'] += before != after
            stack.extend([node.get('/Next'), node.get('/First')])
    if flags.get('attachments'):
        from pdf_attachments import _all_entries
        # Associated-file graphs outside the supported catalog/page-annotation
        # enumeration must not be silently certified as sanitised.
        if '/AF' in root or any('/AF' in p for p in writer.pages):
            raise ValueError('Anexos associados /AF não são suportados pela redação de texto.')
        entries = []
        for item in _all_entries(writer):
            if len(entries) >= 100:raise ValueError('A redação aceita até 100 anexos de texto.')
            entries.append(item)
        seen, catalog, total = set(), [], 0
        for entry, origin, _ in entries:
            spec = entry.pdf_object
            catalog_name = clean(entry.name)
            if origin == 'catalog':
                catalog.append((catalog_name, spec.indirect_reference or spec))
            if id(spec) in seen:
                continue
            seen.add(id(spec))
            name = str(spec.get('/UF') or spec.get('/F') or entry.name)
            if Path(name).suffix.lower() not in TEXT_SUFFIXES:
                raise ValueError('Redação de conteúdo só aceita anexos txt/csv/md/log/json/xml em UTF-8; outros formatos exigem revisão separada.')
            ef = spec.get('/EF')
            ef = ef.get_object() if ef else None
            if not isinstance(ef, DictionaryObject) or set(ef) - {'/F', '/UF'}:
                raise ValueError('Representação de anexo não suportada.')
            streams = {}
            for ref in ef.values():
                stream = ref.get_object()
                streams[id(stream)] = stream
            if not streams:
                raise ValueError('Anexo sem conteúdo incorporado.')
            for stream in streams.values():
                raw = stream.get_data()
                total += len(raw)
                if len(raw) > MAX_TEXT or total > 8 * MAX_TEXT:
                    raise ValueError('Conteúdo dos anexos acima do limite de redação.')
                try:
                    text = raw.decode('utf-8-sig', errors='strict')
                except UnicodeError as exc:
                    raise ValueError('Anexo não é texto UTF-8; nenhuma cópia publicada.') from exc
                if '\x00' in text:
                    raise ValueError('Anexo contém dados binários.')
                after = clean(text).encode('utf-8')
                replacement = DecodedStreamObject();replacement.set_data(after)
                replacement[NameObject('/Type')] = NameObject('/EmbeddedFile')
                new_ref = writer._add_object(replacement)
                for key, ref in list(ef.items()):
                    if ref.get_object() is stream:
                        ef[NameObject(key)] = new_ref
                report['attachment_contents_changed'] += after != raw
            for key in ('/F', '/UF', '/Desc'):
                if key in spec:
                    if not isinstance(spec[key], str):
                        raise ValueError('Nome/descrição de anexo não textual.')
                    before = str(spec[key]);after = clean(before)
                    spec[NameObject(key)] = TextStringObject(after)
                    report['attachment_strings_changed'] += before != after
            report['attachments_checked'] += 1
        if catalog:
            keys = [name for name, _ in catalog]
            if len(set(keys)) != len(keys):
                raise ValueError('A redação produziria nomes de anexos duplicados.')
            pairs = ArrayObject()
            for name, ref in sorted(catalog, key=lambda p: TextStringObject(p[0]).get_encoded_bytes()):
                pairs.extend([TextStringObject(name), ref])
            root['/Names'][NameObject('/EmbeddedFiles')] = writer._add_object(DictionaryObject({NameObject('/Names'): pairs}))
    return report
