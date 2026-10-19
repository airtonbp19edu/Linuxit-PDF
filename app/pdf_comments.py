"""Bounded markup/reply inspection. No appearance, script or external action runs."""
from html.parser import HTMLParser

COMMENT_TYPES = {
    '/Text': 'Nota', '/FreeText': 'Texto', '/Highlight': 'Destaque',
    '/Underline': 'Sublinhado', '/StrikeOut': 'Tachado', '/Squiggly': 'Ondulado',
    '/Stamp': 'Carimbo', '/Ink': 'Desenho', '/Line': 'Linha', '/Square': 'Retângulo',
    '/Circle': 'Elipse', '/Polygon': 'Polígono', '/PolyLine': 'Polilinha',
    '/FileAttachment': 'Anexo', '/Caret': 'Inserção', '/Redact': 'Redação',
}
MAX_ANNOTATIONS = 50000
MAX_TEXT = 65536
MAX_THREAD_DEPTH = 64


def _obj(value):
    return value.get_object() if hasattr(value, 'get_object') else value


def _key(ref):
    indirect = ref if hasattr(ref, 'idnum') else getattr(ref, 'indirect_reference', None)
    return ('object', indirect.idnum, indirect.generation) if indirect is not None else ('direct', id(ref))


class _PlainRichText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.hidden = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.hidden += 1
        elif tag in ('br', 'p', 'div', 'li'):
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.hidden = max(0, self.hidden - 1)
        elif tag in ('p', 'div', 'li'):
            self.parts.append(' ')

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)


def inspect_comments(reader, cancel=None, max_annotations=MAX_ANNOTATIONS):
    """Keep distinct comments, deduplicate object aliases, expose invalid links.

    Explicit /Annots order wins. A same-page /IRT parent omitted from /Annots is
    included after explicit entries. Cross-page, cyclic and overdeep relations
    are reported rather than guessed. Bounds are after PDF object decoding.
    """
    records, by_key, queue, notices = [], {}, [], []
    scanned = 0

    def stopped():
        return cancel is not None and cancel.is_set()

    def notice(reason):
        if reason not in notices and len(notices) < 32:
            notices.append(reason)

    def text(value):
        value = '' if value is None else str(value)
        if len(value) > MAX_TEXT:
            notice('Texto de comentário truncado em 65536 caracteres.')
        return value[:MAX_TEXT].strip()

    def add(ref, page, inferred=False):
        key = _key(ref)
        if key in by_key:
            if by_key[key]['page'] != page:
                notice('Objeto de anotação compartilhado entre páginas; mantida a primeira página.')
            return
        annot = _obj(ref)
        if not hasattr(annot, 'get') or str(annot.get('/Subtype')) not in COMMENT_TYPES:
            return
        subtype = str(annot.get('/Subtype'))
        comment_id = f'p{page}:o{key[1]}:{key[2]}' if key[0] == 'object' else f'p{page}:a{len(records)}'
        contents = text(annot.get('/Contents'))
        if not contents and annot.get('/RC') is not None:
            rich = _obj(annot['/RC'])
            # Stream decoding can allocate before bounds: leave this case explicit.
            if hasattr(rich, 'get_data'):
                notice('Rich text em stream não inspecionado; conteúdo parcial.')
            else:
                parser = _PlainRichText()
                parser.feed(text(rich))
                contents = ' '.join(''.join(parser.parts).split())
        author, subject = text(annot.get('/T')), text(annot.get('/Subj'))
        item = dict(page=page, type=COMMENT_TYPES[subtype], author=author,
                    text=subject or contents or COMMENT_TYPES[subtype], contents=contents,
                    subject=subject, comment_id=comment_id, parent_comment_id=None,
                    relationship=None, is_reply=False, thread_depth=0,
                    inferred_from_reply=inferred, _key=key, _annot=annot)
        by_key[key] = item
        records.append(item)
        queue.append(item)

    for page_index, page in enumerate(reader.pages):
        if stopped():
            break
        try:
            annots = _obj(page.get('/Annots')) or []
            for ref in annots:
                if stopped() or scanned >= max_annotations:
                    break
                scanned += 1
                try:
                    add(ref, page_index)
                except Exception:
                    notice('Anotação ilegível omitida.')
        except Exception:
            notice('Lista de anotações ilegível omitida.')
        if scanned >= max_annotations:
            notice('Limite de anotações atingido; conteúdo parcial.')
            break

    cursor = 0
    while cursor < len(queue) and not stopped():
        item = queue[cursor]
        cursor += 1
        parent = item['_annot'].get('/IRT')
        if parent is None:
            continue
        key = _key(parent)
        if key not in by_key and scanned < max_annotations:
            scanned += 1
            try:
                add(parent, item['page'], True)
            except Exception:
                pass
        target = by_key.get(key)
        if target is None or target['page'] != item['page']:
            notice('Resposta com pai ausente ou em outra página; vínculo omitido.')
            continue
        relation = str(item['_annot'].get('/RT', '/R'))
        if relation not in ('/R', '/Group'):
            notice('Tipo de vínculo de comentário desconhecido; vínculo omitido.')
            continue
        item['parent_comment_id'] = target['comment_id']
        item['relationship'] = relation[1:]
        item['is_reply'] = relation == '/R'

    parents = {item['comment_id']: item['parent_comment_id'] for item in records}
    for item in records:
        seen, parent, depth = {item['comment_id']}, item['parent_comment_id'], 0
        while parent is not None:
            if parent in seen or depth >= MAX_THREAD_DEPTH:
                notice('Ciclo ou profundidade excessiva em comentários; vínculo omitido.')
                item.update(parent_comment_id=None, relationship=None, is_reply=False)
                depth = 0
                break
            seen.add(parent)
            depth += 1
            parent = parents[parent]
        item['thread_depth'] = depth
    for item in records:
        item.pop('_key'); item.pop('_annot')
    if stopped():
        notice('Inspeção de comentários interrompida; conteúdo parcial.')
    return records, notices
