"""Own copy-only PDF edits; never overwrite inputs or execute PDF actions."""
from contextlib import contextmanager
from local_files import publish_copy
import hashlib
import math
from pathlib import Path
import re
import shutil
import tempfile

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Text, Rectangle, Highlight
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NullObject, NumberObject, TextStringObject, FloatObject
from pdf_form_controls import inspect_controls, fill_controls
from pdf_annotations import ANNOTATION_KINDS, create_annotation, create_ink
from pdf_comments import COMMENT_TYPES
from pdf_form_events import inspect_form_events, calculate_form_values, format_form_values
from annotation_geometry import EXTRA_KINDS, create_extra_annotation, move_annotation, conversation_members
from annotation_style import STYLEABLE, current_style, restyle_annotation
from pdf_xfa import XFAError, field_data_path, inspect_xfa, write_field_values
from pdf_edit_security import edit_auth, authorize_operations, preserve_encryption, permissions as edit_permissions

MAX_OPERATIONS = 1000
MAX_TEXT_BYTES = 64 * 1024


def _sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _require(value, message):
    if not value:
        raise ValueError(message)


def _text(value, name, limit=MAX_TEXT_BYTES):
    _require(isinstance(value, str) and value.strip() and len(value.encode('utf-8')) <= limit,
             f'{name} vazio, inválido ou acima do limite.')
    return value


def _inherited(field, name, default=None):
    reference = getattr(field, 'indirect_reference', None)
    _require(reference is not None, 'Campos diretos sem referência PDF ainda não são suportados.')
    current = reference.get_object()
    seen = set()
    while current is not None:
        _require(id(current) not in seen and len(seen) < 64, 'Hierarquia de campo inválida ou muito profunda.')
        seen.add(id(current))
        if name in current:
            return current[name]
        parent = current.get('/Parent')
        current = parent.get_object() if parent is not None else None
        if isinstance(current, NullObject):
            current = None
    return default


def _terminal(field):
    raw = field.indirect_reference.get_object()
    kids = raw.get('/Kids')
    if kids is None:
        return True
    kids = kids.get_object()
    if isinstance(kids, NullObject):
        return True
    _require(isinstance(kids, ArrayObject), 'Subcampos do formulário inválidos.')
    children = [child.get_object() for child in kids]
    _require(all(isinstance(child, DictionaryObject) for child in children), 'Subcampo de formulário inválido.')
    return not any('/T' in child for child in children)


XFA_OPERATIONS = {'fill-text-fields', 'fill-form-events'}


def _xfa_state(reader, allow_xfa):
    """None without XFA; for hybrid forms the read-only XFA description (E07)."""
    form = reader.root_object.get('/AcroForm')
    if form is None or isinstance(form.get_object(), NullObject) or '/XFA' not in form.get_object():
        return None
    if not allow_xfa:
        raise NotImplementedError('Gravação de formulários XFA ainda não é suportada.')
    try:
        info = inspect_xfa(reader)
    except XFAError as exc:
        raise NotImplementedError(f'Formulário XFA não pode ser gravado: {exc}') from None
    if info['error']:
        raise NotImplementedError('Formulário XFA não pode ser gravado: ' + info['error'])
    if not info['hybrid']:
        raise NotImplementedError('Formulários somente XFA (sem campos AcroForm) não podem ser preenchidos.')
    return info


def _text_values(document):
    return {name: str(field['/V']) for name, field in (document.get_fields() or {}).items()
            if _inherited(field, '/FT') == '/Tx' and isinstance(field.get('/V'), str)}


@contextmanager
def _editable(path, expected=None, password=None, recover=False, allow_xfa=False):
    path = Path(path)
    identity = _sha(path)
    if expected is not None:
        _require(isinstance(expected, str) and re.fullmatch('[0-9a-f]{64}', expected),
                 'Informe o SHA-256 atual do PDF.')
        _require(identity == expected, 'O PDF mudou. Leia o documento novamente.')
    with path.open('rb') as stream:
        reader = PdfReader(stream, strict=not recover)
        if reader.is_encrypted:
            if password is None:raise NotImplementedError('Gravação de cópias de PDFs criptografados exige uma sessão autenticada.')
            try:role=int(reader.decrypt(password))
            except Exception:raise ValueError('Não foi possível autenticar a edição do PDF.') from None
            if not role:raise ValueError('Credencial de edição inválida.')
            reader._linuxit_owner=role==2
        fields = reader.get_fields() or {}
        if '/Perms' in reader.root_object or any(_inherited(f, '/FT') == '/Sig' for f in fields.values()):
            raise NotImplementedError('Gravação de documentos com assinatura ou campos de assinatura ainda não é suportada.')
        reader._linuxit_xfa = _xfa_state(reader, allow_xfa)
        if '/Collection' in reader.root_object:
            raise NotImplementedError('Gravação de portfólios ainda não é suportada.')
        yield reader, fields, identity


def _outline_nodes(reader):
    root = reader.root_object.get('/Outlines')
    if root is None:return []
    rows, seen = [], set()
    title_bytes = 0
    def walk(parent, prefix):
        nonlocal title_bytes
        _require(len(prefix) < 32, 'Árvore de marcadores acima do limite de 32 níveis.')
        current = parent.get('/First');index = 0
        while current is not None:
            node = current.get_object()
            _require(isinstance(node, DictionaryObject) and id(node) not in seen and len(rows) < 2048,
                     'Árvore de marcadores inválida ou acima do limite de 2048 entradas.')
            seen.add(id(node));path = prefix + [index]
            title = node.get('/Title', '')
            _require(isinstance(title, str) and len(title.encode('utf-8')) <= 4096, 'Título de marcador inválido ou acima do limite.')
            title_bytes += len(title.encode('utf-8'))
            _require(title_bytes <= 1024**2, 'Títulos de marcadores acima do limite total de 1 MiB.')
            rows.append((path, node))
            if '/First' in node:walk(node, path)
            current = node.get('/Next');index += 1
    walk(root.get_object(), [])
    return rows


def _note_records(reader):
    rows, truncated, text_bytes = [], False, 0
    for page_index, page in enumerate(reader.pages):
        annots = page.get('/Annots')
        if annots is None or not isinstance(annots.get_object(), ArrayObject):continue
        for index, ref in enumerate(annots.get_object()):
            note = ref.get_object()
            if not isinstance(note, DictionaryObject) or note.get('/Subtype') != '/Text':continue
            text, author = note.get('/Contents', ''), note.get('/T', '')
            if int(note.get('/F', 0)) & (64 | 128 | 512):continue
            if not isinstance(text, str) or not isinstance(author, str) or len(text.encode('utf-8')) > MAX_TEXT_BYTES or len(author.encode('utf-8')) > 4096:continue
            cost = len(text.encode('utf-8')) + len(author.encode('utf-8'))
            if len(rows) >= 2000 or text_bytes + cost > 1024**2:truncated = True;continue
            text_bytes += cost
            rows.append({'page':page_index,'index':index,'text':text,'author':author})
    return rows, truncated


def _annotation_rect(page, rect):
    left, bottom, right, top = map(float, page.cropbox)
    _require(isinstance(rect, list) and len(rect) == 4 and all(type(v) in (int, float) and math.isfinite(v) for v in rect),
             'Retângulo de anotação inválido.')
    _require(all(math.isfinite(v) for v in (left, bottom, right, top))
             and left <= rect[0] < rect[2] <= right and bottom <= rect[1] < rect[3] <= top,
             'A anotação deve ficar dentro do CropBox, em coordenadas PDF.')
    return rect


def _removable_annotation(note):
    return (isinstance(note, DictionaryObject) and note.get('/Subtype') in
            ('/Text', '/Square', '/Highlight', '/Underline', '/StrikeOut', '/Squiggly', '/Circle', '/Line', '/Ink', '/Polygon', '/PolyLine', '/Caret', '/FreeText', '/Stamp')
            and not int(note.get('/F', 0)) & (64 | 128 | 512)
            and not any(key in note for key in ('/IRT', '/Popup', '/Parent')))


def _annotation_has_dependants(reader, note):
    for page in reader.pages:
        annots = page.get('/Annots')
        if annots is None or not isinstance(annots.get_object(), ArrayObject):continue
        for ref in annots.get_object():
            other = ref.get_object()
            if not isinstance(other, DictionaryObject):continue
            for key in ('/IRT', '/Parent'):
                related = other.get(key)
                if related is not None and related.get_object() is note:return True
    return False


def _annotation_records(reader):
    rows, size, truncated = [], 0, False
    for page_index, page in enumerate(reader.pages):
        annots = page.get('/Annots')
        if annots is None or not isinstance(annots.get_object(), ArrayObject):continue
        for index, ref in enumerate(annots.get_object()):
            note = ref.get_object()
            if not _removable_annotation(note):continue
            text, author = note.get('/Contents', ''), note.get('/T', '')
            if (not isinstance(text, str) or not isinstance(author, str)
                    or len(text.encode('utf-8')) > MAX_TEXT_BYTES or len(author.encode('utf-8')) > 4096):continue
            cost = len(text.encode('utf-8')) + len(author.encode('utf-8'))
            if len(rows) >= 2000 or size + cost > 1024**2:truncated = True;continue
            size += cost
            color, opacity = current_style(note)
            rows.append({'page':page_index, 'index':index, 'subtype':str(note['/Subtype']), 'text':text, 'author':author,
                         'styleable':note['/Subtype'] in STYLEABLE, 'color':color, 'opacity':opacity})
    return rows, truncated


def _bookmark_path(value, allow_root=False):
    _require(isinstance(value, list) and (0 if allow_root else 1) <= len(value) <= 32
             and all(type(i) is int and 0 <= i < 2048 for i in value), 'Caminho de marcador inválido.')
    return tuple(value)


def _change_outline(writer, operation):
    moving = operation['kind'] == 'move-bookmark'
    _require(set(operation) == ({'kind','path','parent','position'} if moving else {'kind','path'}),
             'Opções de marcador inválidas.')
    source = _bookmark_path(operation['path'])
    rows = _outline_nodes(writer)
    objects, children = {tuple(p):n for p,n in rows}, {():[]}
    for path, node in rows:
        key = tuple(path);children[key] = []
        children[key[:-1]].append(node)
    _require(source in objects, 'Marcador não encontrado no documento atual.')
    if moving:
        target = _bookmark_path(operation['parent'], allow_root=True)
        _require(not target or target in objects, 'Pasta de marcadores não encontrada.')
        _require(target[:len(source)] != source, 'Não é possível mover um marcador para sua própria subárvore.')
        position = operation['position']
        target_size = len(children[target]) - int(target == source[:-1])
        _require(type(position) is int and 0 <= position <= target_size,
                 'Posição inválida; ela é medida depois de retirar o marcador da origem.')
    children[source[:-1]].pop(source[-1])
    if moving:children[target].insert(position, objects[source])
    by_node = {id(objects[key]):value for key,value in children.items() if key}
    root = writer.root_object['/Outlines']
    if getattr(root, 'indirect_reference', None) is None:
        writer.root_object[NameObject('/Outlines')] = writer._add_object(root)
    def link(parent, siblings):
        if not siblings:
            for key in ('/First','/Last','/Count'):parent.pop(key, None)
            return 0
        refs = [n.indirect_reference if getattr(n, 'indirect_reference', None) is not None else writer._add_object(n) for n in siblings]
        parent[NameObject('/First')], parent[NameObject('/Last')] = refs[0], refs[-1]
        visible = 0
        for index, node in enumerate(siblings):
            opened = int(node.get('/Count', 0)) >= 0
            for key, value in (('/Parent',parent.indirect_reference),('/Prev',refs[index-1] if index else None),
                               ('/Next',refs[index+1] if index+1 < len(refs) else None)):
                if value is None:node.pop(key, None)
                else:node[NameObject(key)] = value
            descendants = link(node, by_node[id(node)])
            if descendants:node[NameObject('/Count')] = NumberObject(descendants if opened else -descendants)
            visible += 1 + (descendants if opened else 0)
        return visible
    visible = link(root, children[()])
    root[NameObject('/Count')] = NumberObject(visible)
    _outline_nodes(writer)  # Enforce depth/shape limits after a move as well.


def inspect_editable_document(path, *, auth=None):
    """Describe the bounded edit contract without decoding embedded payloads."""
    password,recover=edit_auth(auth)
    with _editable(path,password=password,recover=recover,allow_xfa=True) as (reader, fields, identity):
        result = {'schema': 'linuxit-copy-edit-info-v1', 'source_sha256': identity,
                  'pages': len(reader.pages), 'text_fields': [], 'edit_permissions':edit_permissions(reader),
                  'page_boxes':[list(map(float, page.cropbox)) for page in reader.pages]}
        for name, field in fields.items():
            if _inherited(field, '/FT') == '/Tx' and _terminal(field):
                value = _inherited(field, '/V', '')
                if isinstance(value, NullObject):
                    value = ''
                _require(isinstance(value, str), 'Valor original de campo de texto inválido.')
                result['text_fields'].append({'name': name, 'value': value,
                                             'read_only': bool(int(_inherited(field, '/Ff', 0)) & 1)})
        result['bookmarks'] = [{'path':p, 'title':n.get('/Title', '')} for p, n in _outline_nodes(reader)]
        result['notes'], result['notes_truncated'] = _note_records(reader)
        result['form_controls'], result['unsupported_controls'] = inspect_controls(reader, fields)
        result['form_events'] = inspect_form_events(reader)
        result['xfa'] = None
        if reader._linuxit_xfa is not None:
            paths = {f['path'] for f in reader._linuxit_xfa['fields']}
            bound = []
            for record in result['text_fields']:
                try:
                    if field_data_path(record['name']) in paths:bound.append(record['name'])
                except XFAError:
                    pass
            result['xfa'] = {'hybrid': True, 'operations': sorted(XFA_OPERATIONS), 'bound_text_fields': bound}
        result['annotations'], result['annotations_truncated'] = _annotation_records(reader)
        result['reply_targets'] = []
        result['conversation_comments']=[];result['conversation_comments_truncated']=False;comment_bytes=0
        for page_index,page in enumerate(reader.pages):
            annots=page.get('/Annots');annots=annots.get_object() if annots is not None else []
            for index,ref in enumerate(annots):
                note=ref.get_object()
                if (len(result['reply_targets']) < 2000 and isinstance(note,DictionaryObject)
                        and note.get('/Subtype') in COMMENT_TYPES and not int(note.get('/F',0)) & (64|128|512)):
                    result['reply_targets'].append(dict(page=page_index,index=index,
                        text=str(note.get('/Contents',''))[:180],subtype=str(note['/Subtype'])))
                    text=note.get('/Contents','');author=note.get('/T','')
                    if isinstance(text,str) and isinstance(author,str):
                        size=len(text.encode('utf-8'))+len(author.encode('utf-8'))
                        if len(text.encode('utf-8'))<=MAX_TEXT_BYTES and len(author.encode('utf-8'))<=4096 and comment_bytes+size<=1024**2:
                            result['conversation_comments'].append(dict(page=page_index,index=index,text=text,author=author,subtype=str(note['/Subtype'])))
                            comment_bytes+=size
                        else:result['conversation_comments_truncated']=True
    _require(_sha(path) == identity, 'O PDF foi alterado durante a leitura.')
    return result


def _page(writer, index):
    _require(type(index) is int and 0 <= index < len(writer.pages), 'Página inválida; índices usam base zero.')
    return writer.pages[index]


def _apply(writer, operation):
    _require(isinstance(operation, dict), 'Cada alteração deve ser um objeto JSON.')
    kind = operation.get('kind')
    _require(isinstance(kind, str), 'Tipo de alteração inválido.')
    if kind in ('move-bookmark', 'delete-bookmark'):
        _change_outline(writer, operation)
    elif kind == 'fill-form-events':
        _require(set(operation)=={'kind','values'},'Opções de formulário inválidas.')
        values=calculate_form_values(writer,operation['values'])
        fields=writer.get_fields() or {};flags={}
        try:
            for name in values:
                raw=fields[name].indirect_reference.get_object()
                flags[name]=raw.get('/Ff')
                raw[NameObject('/Ff')]=NumberObject(int(_inherited(fields[name],'/Ff',0)) & ~1)
            # Formatted numbers go to the appearance only; /V keeps the unformatted value.
            display=format_form_values(writer,values)
            _apply(writer,dict(kind='fill-text-fields',values={**values,**display}))
            for name in display:
                fields[name].indirect_reference.get_object()[NameObject('/V')]=TextStringObject(values[name])
        finally:
            for name,value in flags.items():
                raw=fields[name].indirect_reference.get_object()
                if value is None:raw.pop('/Ff',None)
                else:raw[NameObject('/Ff')]=value
    elif kind == 'set-layer-visibility':
        _require(set(operation)=={'kind','visible'},'Alteração de camadas inválida.')
        from pdf_layers import apply_visibility
        apply_visibility(writer,operation['visible'])
    elif kind == 'fill-form-controls':
        _require(set(operation) == {'kind', 'values'}, 'Opções de formulário inválidas.')
        fill_controls(writer, operation['values'])
    elif kind in EXTRA_KINDS:
        geometry='points' if kind in ('add-polygon','add-polyline') else 'rect'
        _require(set(operation)=={'kind','page',geometry,'text'},'Opções de anotação inválidas.')
        page=_page(writer,operation['page'])
        writer.add_annotation(operation['page'],create_extra_annotation(writer,list(map(float,page.cropbox)),operation))
    elif kind in ('move-annotation','update-comment','delete-conversation','set-popup'):
        expected={'kind','page','index'}|({'dx','dy'} if kind=='move-annotation' else {'text','author'} if kind=='update-comment' else {'rect','open'} if kind=='set-popup' else set())
        _require(set(operation)==expected,'Opções de comentário inválidas.')
        page=_page(writer,operation['page']);annots=page.get('/Annots',[]);index=operation['index']
        _require(type(index) is int and 0<=index<len(annots),'Comentário não encontrado.')
        note=annots[index].get_object()
        _require(isinstance(note,DictionaryObject) and note.get('/Subtype') in COMMENT_TYPES and not int(note.get('/F',0))&(64|128|512),'Comentário bloqueado ou não suportado.')
        if kind=='move-annotation':
            _require(_removable_annotation(note) and not _annotation_has_dependants(writer,note),'Movimentação exige anotação simples sem vínculos.')
            move_annotation(page,note,operation['dx'],operation['dy'])
        elif kind=='delete-conversation':
            members=conversation_members(writer,page,index)
            page[NameObject('/Annots')]=ArrayObject(ref for ref in annots if id(ref.get_object()) not in members)
        elif kind=='set-popup':
            from pypdf.generic import BooleanObject
            _require(type(operation['open']) is bool,'Estado de popup inválido.')
            rect=_annotation_rect(page,operation['rect']);existing=note.get('/Popup')
            if existing is None:
                target=annots[index]
                if not hasattr(target,'idnum'):target=writer._add_object(note);annots[index]=target
                popup=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Popup'),NameObject('/Parent'):target})
                popupref=writer._add_object(popup);annots.append(popupref);note[NameObject('/Popup')]=popupref
            else:
                popup=existing.get_object()
                _require(isinstance(popup,DictionaryObject) and popup.get('/Subtype')=='/Popup' and popup.get('/Parent') is not None and popup['/Parent'] is note and not int(popup.get('/F',0))&(64|128|512),'Popup bloqueado ou incompatível.')
            popup[NameObject('/Rect')]=ArrayObject(FloatObject(v) for v in rect);popup[NameObject('/Open')]=BooleanObject(operation['open'])
            if note.get('/Subtype')=='/Text':note[NameObject('/Open')]=BooleanObject(operation['open'])
        else:
            text=operation['text'];author=operation['author']
            _require(isinstance(text,str) and len(text.encode('utf-8'))<=MAX_TEXT_BYTES and isinstance(author,str) and len(author.encode('utf-8'))<=4096,'Comentário ou autor inválido.')
            if note.get('/Subtype') in ('/FreeText','/Stamp'):
                replacement=create_extra_annotation(writer,list(map(float,page.cropbox)),dict(kind='add-freetext' if note['/Subtype']=='/FreeText' else 'add-stamp',rect=list(map(float,note['/Rect'])),text=text))
                note[NameObject('/AP')]=replacement['/AP']
            note[NameObject('/Contents')]=TextStringObject(text)
            if author:note[NameObject('/T')]=TextStringObject(author)
            else:note.pop('/T',None)
    elif kind == 'add-ink':
        _require(set(operation)=={'kind','page','paths','text'},'Opções de desenho inválidas.')
        page=_page(writer,operation['page'])
        note=create_ink(list(map(float,page.cropbox)),operation['paths'],operation['text'])
        note['/AP'][NameObject('/N')]=writer._add_object(note['/AP']['/N'])
        writer.add_annotation(operation['page'],note)
    elif kind == 'add-reply':
        _require(set(operation)=={'kind','page','index','text','author'},'Opções de resposta inválidas.')
        page=_page(writer,operation['page']);annots=page.get('/Annots')
        annots=annots.get_object() if annots is not None else []
        index=operation['index']
        _require(type(index) is int and 0 <= index < len(annots),'Comentário de destino inválido.')
        target=annots[index].get_object()
        _require(isinstance(target,DictionaryObject) and target.get('/Subtype') in COMMENT_TYPES
                 and not int(target.get('/F',0)) & (64|128|512),'Comentário bloqueado ou não suportado.')
        current=target;seen=set();members={id(ref.get_object()) for ref in annots}
        while current is not None:
            _require(id(current) in members and id(current) not in seen and len(seen)<64,
                     'Conversa cíclica, entre páginas ou profunda demais.')
            seen.add(id(current));parent=current.get('/IRT');current=parent.get_object() if parent is not None else None
        author=operation['author'];_require(isinstance(author,str) and len(author.encode('utf-8'))<=4096,'Autor inválido.')
        rect=_annotation_rect(page,list(map(float,target.get('/Rect',page.cropbox))))
        note=Text(rect=tuple(rect),text=_text(operation['text'],'Resposta'))
        _require(hasattr(annots[index],'idnum'),'Comentário direto sem referência indireta não é suportado.')
        note[NameObject('/IRT')]=annots[index];note[NameObject('/RT')]=NameObject('/R')
        note[NameObject('/T')]=TextStringObject(author);note[NameObject('/F')]=NumberObject(4)
        writer.add_annotation(operation['page'],note)
    elif kind == 'style-annotation':
        # E12: colour and opacity of an existing simple annotation, appearance regenerated.
        _require(set(operation) == {'kind', 'page', 'index', 'color', 'opacity'}, 'Opções de estilo inválidas.')
        page = _page(writer, operation['page']);annots = page.get('/Annots')
        _require(annots is not None and isinstance(annots.get_object(), ArrayObject), 'Página sem anotações suportadas.')
        annots = annots.get_object();index = operation['index']
        _require(type(index) is int and 0 <= index < len(annots), 'Índice de anotação inválido.')
        annotation = annots[index].get_object()
        _require(_removable_annotation(annotation) and not _annotation_has_dependants(writer, annotation),
                 'Anotação bloqueada, com respostas/popup ou de tipo não suportado.')
        restyle_annotation(writer, annotation, operation['color'], operation['opacity'])
    elif kind in ('delete-annotation', 'update-annotation'):
        _require(set(operation) == ({'kind', 'page', 'index'} if kind == 'delete-annotation'
                                    else {'kind', 'page', 'index', 'text', 'author'}), 'Opções de anotação inválidas.')
        page = _page(writer, operation['page']);annots = page.get('/Annots')
        _require(annots is not None and isinstance(annots.get_object(), ArrayObject), 'Página sem anotações suportadas.')
        annots = annots.get_object();index = operation['index']
        _require(type(index) is int and 0 <= index < len(annots), 'Índice de anotação inválido.')
        annotation = annots[index].get_object()
        _require(_removable_annotation(annotation) and not _annotation_has_dependants(writer, annotation),
                 'Anotação bloqueada, com respostas/popup ou de tipo não suportado.')
        if kind == 'delete-annotation':
            del annots[index]
        else:
            text, author = operation['text'], operation['author']
            if annotation.get('/Subtype') in ('/FreeText','/Stamp'):
                _apply(writer,dict(kind='update-comment',page=operation['page'],index=index,text=text,author=author))
                return
            _require(isinstance(text, str) and len(text.encode('utf-8')) <= MAX_TEXT_BYTES,
                     'Comentário inválido ou acima do limite de 64 KiB.')
            _require(isinstance(author, str) and len(author.encode('utf-8')) <= 4096, 'Autor inválido.')
            annotation[NameObject('/Contents')] = TextStringObject(text)
            if author:annotation[NameObject('/T')] = TextStringObject(author)
            else:annotation.pop('/T', None)
    elif kind in ANNOTATION_KINDS:
        geometry_key = 'points' if kind == 'add-line' else 'rect'
        _require(set(operation) == {'kind', 'page', geometry_key, 'text'}, 'Opções de anotação inválidas.')
        page = _page(writer, operation['page'])
        note = create_annotation(kind, list(map(float, page.cropbox)), operation[geometry_key], operation['text'])
        note['/AP'][NameObject('/N')] = writer._add_object(note['/AP']['/N'])
        writer.add_annotation(operation['page'], note)
    elif kind in ('add-highlight', 'add-rectangle'):
        _require(set(operation) == {'kind', 'page', 'rect', 'text'}, 'Opções de anotação inválidas.')
        page = _page(writer, operation['page']);rect = _annotation_rect(page, operation['rect'])
        text = operation['text']
        _require(isinstance(text, str) and len(text.encode('utf-8')) <= MAX_TEXT_BYTES, 'Texto da anotação inválido.')
        if kind == 'add-highlight':
            x0, y0, x1, y1 = rect
            note = Highlight(rect=tuple(rect), highlight_color='ffff00', quad_points=ArrayObject(FloatObject(v) for v in (x0,y1,x1,y1,x0,y0,x1,y0)))
        else:note = Rectangle(rect=tuple(rect))
        note[NameObject('/Contents')] = TextStringObject(text)
        note[NameObject('/F')] = NumberObject(4)
        writer.add_annotation(operation['page'], note)
    elif kind == 'rotate-page':
        _require(set(operation) == {'kind','page','angle'} and type(operation['angle']) is int
                 and operation['angle'] in (-270,-180,-90,90,180,270), 'Rotação inválida; use múltiplos de 90 graus até 270.')
        _page(writer, operation['page']).rotate(operation['angle'])
    elif kind == 'rename-bookmark':
        _require(set(operation) == {'kind','path','title'}, 'Opções de marcador inválidas.')
        path = operation['path']
        _require(isinstance(path, list) and 1 <= len(path) <= 32 and all(type(i) is int and 0 <= i < 2048 for i in path), 'Caminho de marcador inválido.')
        matches = [node for address, node in _outline_nodes(writer) if address == path]
        _require(len(matches) == 1, 'Marcador não encontrado no documento atual.')
        matches[0][NameObject('/Title')] = TextStringObject(_text(operation['title'], 'Título', 4096))
    elif kind == 'update-note':
        _require(set(operation) == {'kind','page','index','text','author'}, 'Opções de nota inválidas.')
        page = _page(writer, operation['page']);annots = page.get('/Annots')
        _require(annots is not None and isinstance(annots.get_object(), ArrayObject), 'A página não possui anotações suportadas.')
        annots = annots.get_object();index = operation['index']
        _require(type(index) is int and 0 <= index < len(annots), 'Índice de anotação inválido.')
        note = annots[index].get_object()
        _require(isinstance(note, DictionaryObject) and note.get('/Subtype') == '/Text'
                 and not (int(note.get('/F', 0)) & (64 | 128 | 512)), 'A anotação deve ser uma nota Text sem bloqueio de edição.')
        note[NameObject('/Contents')] = TextStringObject(_text(operation['text'], 'Texto'))
        author = operation['author']
        _require(isinstance(author, str) and len(author.encode('utf-8')) <= 4096, 'Autor inválido.')
        if author:note[NameObject('/T')] = TextStringObject(author)
        else:note.pop('/T', None)
    elif kind == 'add-bookmark':
        _require(set(operation) == {'kind', 'title', 'page'}, 'Opções de marcador inválidas.')
        _page(writer, operation['page'])
        writer.add_outline_item(_text(operation['title'], 'Título', 4096), operation['page'])
    elif kind == 'add-note':
        _require({'kind', 'text', 'page', 'rect'} <= operation.keys()
                 and set(operation) <= {'kind', 'text', 'page', 'rect', 'author'}, 'Opções de nota inválidas.')
        page = _page(writer, operation['page'])
        rect = operation['rect']
        left, bottom, right, top = map(float, page.cropbox)
        if rect is None:
            width, height = right - left, top - bottom
            _require(all(math.isfinite(v) for v in (left, bottom, right, top)) and width > 0 and height > 0,
                     'Dimensões da página inválidas.')
            margin = min(10, width / 10, height / 10)
            rect = [left + margin, top - margin - min(20, height - margin * 2),
                    left + margin + min(20, width - margin * 2), top - margin]
        _require(isinstance(rect, list) and len(rect) == 4 and all(
            type(v) in (int, float) and math.isfinite(v) for v in rect), 'Retângulo de nota inválido.')
        _require(left <= rect[0] < rect[2] <= right and bottom <= rect[1] < rect[3] <= top,
                 'A nota deve ficar dentro do CropBox da página, em coordenadas PDF.')
        author = operation.get('author')
        if author is not None:
            author = _text(author, 'Autor', 4096)
        note = Text(rect=tuple(rect), text=_text(operation['text'], 'Texto'), title_bar=author)
        # The PDF annotation flag key is /F; normalize the library helper's key.
        note.pop('/Flags', None)
        note[NameObject('/F')] = NumberObject(4)
        writer.add_annotation(operation['page'], note)
    elif kind == 'fill-text-fields':
        _require(set(operation) == {'kind', 'values'}, 'Opções de formulário inválidas.')
        values = operation['values']
        _require(isinstance(values, dict) and 0 < len(values) <= 256, 'Informe de 1 a 256 campos de texto.')
        fields = writer.get_fields() or {}
        for name, value in values.items():
            _require(name in fields and _inherited(fields[name], '/FT') == '/Tx', 'Campo de texto não encontrado.')
            field = fields[name]
            _require(_terminal(field), 'Selecione um campo de texto terminal, sem subcampos nomeados.')
            _require(not (int(_inherited(field, '/Ff', 0)) & 1), 'Campo somente leitura não pode ser alterado.')
            _require(isinstance(value, str) and len(value.encode('utf-8')) <= MAX_TEXT_BYTES, 'Valor de campo inválido.')
            # get_fields() presents a reduced Field view which omits /MaxLen.
            limit = _inherited(field, '/MaxLen')
            if limit is not None:
                _require(isinstance(limit, int) and limit >= 0, 'Limite de caracteres do campo inválido.')
                _require(len(value) <= int(limit), 'Valor acima do limite de caracteres do campo.')
            raw = field.indirect_reference.get_object()
            if '/FT' not in raw:
                # Materialize the equivalent inherited type for combined child widgets.
                raw[NameObject('/FT')] = NameObject('/Tx')
        writer.update_page_form_field_values(None, values, auto_regenerate=None)
        updated = writer.get_fields() or {}
        _require(all(updated[name].get('/V') == value for name, value in values.items()),
                 'O formulário não possui widgets de página suportados para todos os campos.')
    else:
        raise ValueError('Tipo de alteração não suportado.')


def save_edited_copy(path, destination, *, source_sha256, operations, auth=None):
    """Apply a bounded batch to a clone and create a new PDF exclusively."""
    _require(isinstance(operations, list) and 0 < len(operations) <= MAX_OPERATIONS,
             f'Informe de 1 a {MAX_OPERATIONS} alterações.')
    destination = Path(destination)
    _require(destination.parent.is_dir(), 'A pasta de destino deve existir.')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    temporary = None
    created = False
    password,recover=edit_auth(auth)
    try:
        with _editable(path, source_sha256,password=password,recover=recover,allow_xfa=True) as (reader, fields, identity):
            authorize_operations(reader,operations)
            xfa = reader._linuxit_xfa
            if xfa is not None and not all(isinstance(op, dict) and op.get('kind') in XFA_OPERATIONS for op in operations):
                raise NotImplementedError('Em formulários XFA só o preenchimento de campos de texto é suportado.')
            writer = PdfWriter(clone_from=reader)
            before = _text_values(writer) if xfa is not None else {}
            for operation in operations:
                _apply(writer, operation)
            changed = {}
            if xfa is not None:
                # Every changed text value (typed or calculated) is mirrored into datasets.
                changed = {name: value for name, value in _text_values(writer).items() if before.get(name) != value}
                if changed:
                    write_field_values(writer, changed)
            preserve_encryption(writer,reader)
            with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-copy-', suffix='.pdf', delete=False) as stream:
                temporary = Path(stream.name)
                writer.write(stream)
            with temporary.open('rb') as stream:
                check=PdfReader(stream,strict=True)
                if reader.is_encrypted:
                    _require(check.is_encrypted and check.decrypt(password),'A cópia gerada não preservou a autenticação.')
                    _require(check.trailer['/Encrypt']['/P']==reader.trailer['/Encrypt']['/P'],'A cópia alterou as permissões originais.')
                _require(len(check.pages) == len(reader.pages), 'A cópia gerada não preservou as páginas.')
                if changed:
                    data = {f['path']: f['value'] for f in inspect_xfa(check)['fields']}
                    reopened = _text_values(check)
                    _require(all(data.get(field_data_path(name)) == reopened.get(name) == value for name, value in changed.items()),
                             'A cópia gerada não manteve AcroForm e dados XFA coerentes.')
        _require(_sha(path) == identity, 'O PDF foi alterado durante a preparação da cópia.')
        def unchanged():
            _require(_sha(path) == identity, 'O PDF foi alterado durante a preparação da cópia.')
        publish_copy(temporary,destination,unchanged)
        created = True
        return {'schema': 'linuxit-copy-edit-result-v1', 'source_sha256': identity,
                'output_sha256': _sha(destination), 'path': str(destination),
                'pages': len(writer.pages), 'operations_applied': len(operations),
                'xfa_synced_fields': sorted(changed)}
    except BaseException:
        if created:
            destination.unlink()
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
