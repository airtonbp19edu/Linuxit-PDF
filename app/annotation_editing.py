"""Own bounded edits of markup annotations with reciprocal popup/reply links.

No PDF action runs. Relationships are validated before mutation, including links
from other pages. Form widgets, multimedia and unknown annotation types remain
outside this editing API. Deleting an attachment comment does not promise to
erase its payload or unrelated catalog attachments from the PDF.
"""
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, TextStringObject
from pdf_comments import COMMENT_TYPES

MAX_ANNOTATIONS = 50000
MAX_THREAD = 2000
MAX_DEPTH = 64
LOCK_FLAGS = 64 | 128 | 512


def _require(value, message):
    if not value:
        raise ValueError(message)


def _target(note, name):
    value = note.get(name)
    return value.get_object() if value is not None else None


def _inventory(document):
    entries = [];positions = {}
    for page_no, page in enumerate(document.pages):
        annots = page.get('/Annots')
        annots = annots.get_object() if annots is not None else []
        _require(isinstance(annots, list), 'Lista de anotações inválida.')
        for index, reference in enumerate(annots):
            _require(len(entries) < MAX_ANNOTATIONS, 'Documento acima de 50000 anotações.')
            note = reference.get_object()
            if not isinstance(note, DictionaryObject):
                continue
            entry = (page_no, index, reference, note)
            entries.append(entry);positions.setdefault(id(note), []).append(entry)
    return entries, positions


def _topology(document, page, index):
    entries, positions = _inventory(document)
    page_numbers = [i for i, candidate in enumerate(document.pages) if candidate is page]
    _require(len(page_numbers) == 1, 'Página de anotação ambígua.')
    page_no = page_numbers[0];annots = page.get('/Annots', [])
    annots = annots.get_object() if hasattr(annots, 'get_object') else annots
    _require(type(index) is int and 0 <= index < len(annots), 'Comentário não encontrado.')
    selected = annots[index].get_object()
    _require(isinstance(selected, DictionaryObject) and selected.get('/Subtype') in COMMENT_TYPES,
             'Tipo de anotação sem edição de comentário suportada.')
    # Gather the entire connected conversation in either direction. Even an
    # inbound cross-page reference makes edits ambiguous, not just outbound ones.
    members = {id(selected): selected}
    changed = True
    while changed:
        changed = False
        for _, _, _, note in entries:
            related = [_target(note, key) for key in ('/IRT', '/Parent', '/Popup')]
            if id(note) in members or any(value is not None and id(value) in members for value in related):
                for value in [note] + [v for v in related if v is not None]:
                    if id(value) not in members:
                        members[id(value)] = value;changed = True
        _require(len(members) <= MAX_THREAD, 'Conversa acima de 2000 objetos.')
    for key, note in members.items():
        locations = positions.get(key, [])
        _require(len(locations) == 1 and locations[0][0] == page_no,
                 'Conversa com referência ausente, repetida ou em outra página.')
        _require(isinstance(note, DictionaryObject) and note.get('/Subtype') in set(COMMENT_TYPES) | {'/Popup'},
                 'Conversa contém tipo de anotação não suportado.')
        _require(not int(note.get('/F', 0)) & LOCK_FLAGS, 'Conversa contém comentário bloqueado.')
        if note.get('/Subtype') == '/Popup':
            owner = _target(note, '/Parent')
            _require(owner is not None and owner.get('/Subtype') in COMMENT_TYPES and
                     _target(owner, '/Popup') is note and '/IRT' not in note and '/Popup' not in note,
                     'Popup sem proprietário recíproco válido.')
        else:
            _require('/Parent' not in note, 'Comentário com relação Parent não suportada.')
            popup = _target(note, '/Popup')
            if popup is not None:
                _require(popup.get('/Subtype') == '/Popup' and _target(popup, '/Parent') is note,
                         'Relação de popup não recíproca.')
            current = note;seen = set()
            while current is not None:
                _require(id(current) not in seen and len(seen) < MAX_DEPTH, 'Conversa cíclica ou acima de 64 níveis.')
                _require(current.get('/Subtype') in COMMENT_TYPES, 'Resposta aponta para objeto não suportado.')
                seen.add(id(current))
                if '/IRT' in current:
                    _require(current.get('/RT', '/R') == '/R', 'Grupos de anotação /RT Group ainda não são editáveis neste fluxo.')
                current = _target(current, '/IRT')
    return selected, members, annots


def _subtree(selected, members):
    result = {id(selected)}
    changed = True
    while changed:
        changed = False
        for key, note in members.items():
            parent = _target(note, '/IRT') or (_target(note, '/Parent') if note.get('/Subtype') == '/Popup' else None)
            if key not in result and parent is not None and id(parent) in result:
                result.add(key);changed = True
    return result


def conversation_members(document, page, index):
    """Validated selected comment + descendant replies/popups, preserving its parent."""
    selected, members, _ = _topology(document, page, index)
    removed = _subtree(selected, members)
    _require(not any('/StructParent' in members[key] for key in removed),
             'Excluir anotação ligada à árvore de acessibilidade ainda não é suportado.')
    return removed


def delete_annotation(document, page, index):
    """Delete one leaf reply/root and its popup; never leave descendant replies orphaned."""
    selected, members, annots = _topology(document, page, index)
    removed = _subtree(selected, members)
    _require(all(members[key].get('/Subtype') == '/Popup' for key in removed if key != id(selected)),
             'Comentário tem respostas dependentes; exclua a conversa explicitamente.')
    _require(not any('/StructParent' in members[key] for key in removed),
             'Excluir anotação ligada à árvore de acessibilidade ainda não é suportado.')
    page[NameObject('/Annots')] = ArrayObject(ref for ref in annots if id(ref.get_object()) not in removed)


def update_annotation_comment(document, page, index, text, author):
    """Update plain metadata; preserve reply links and graphical stamp/attachment APs."""
    selected, _, _ = _topology(document, page, index)
    _require(isinstance(text, str) and len(text.encode('utf-8')) <= 65536 and
             isinstance(author, str) and len(author.encode('utf-8')) <= 4096, 'Comentário ou autor inválido.')
    subtype = selected.get('/Subtype')
    if subtype == '/FreeText' or subtype == '/Stamp' and selected.get('/Name') == '/LinuxitCustom':
        _require(subtype != '/FreeText' or not any(key in selected for key in ('/CL', '/IT', '/RD')),
                 'Texto livre com chamada/intenção/margens especiais ainda não é refeito neste fluxo.')
        from annotation_geometry import create_extra_annotation
        replacement = create_extra_annotation(document, list(map(float, page.cropbox)), dict(
            kind='add-freetext' if subtype == '/FreeText' else 'add-stamp', rect=list(map(float, selected['/Rect'])), text=text))
        selected[NameObject('/AP')] = replacement['/AP']
    selected[NameObject('/Contents')] = TextStringObject(text)
    if author:
        selected[NameObject('/T')] = TextStringObject(author)
    else:
        selected.pop('/T', None)
    # Rich text would otherwise contradict the explicitly chosen plain contents
    # in viewers that prefer /RC. Non-content fields and relationships survive.
    selected.pop('/RC', None)


def move_related_annotation(document, page, index, dx, dy):
    selected, _, _ = _topology(document, page, index)
    from annotation_geometry import move_annotation
    popup = _target(selected, '/Popup')
    # Validate both operations on shallow geometry copies before mutating either.
    clones = [DictionaryObject(note) for note in (selected, popup) if note is not None]
    for copy in clones:
        move_annotation(page, copy, dx, dy)
    keys = ('/Rect', '/Vertices', '/QuadPoints', '/L', '/InkList')
    for note, copy in zip((selected, popup), clones):
        if note is not None:
            for key in keys:
                if key in copy:
                    note[NameObject(key)] = copy[key]


def style_related_annotation(document, page, index, color, opacity):
    selected, _, _ = _topology(document, page, index)
    from annotation_style import restyle_annotation
    return restyle_annotation(document, selected, color, opacity)


def resize_related_annotation(document, page, index, rect):
    selected, _, _ = _topology(document, page, index)
    from annotation_geometry import resize_annotation
    return resize_annotation(document, selected, rect)
