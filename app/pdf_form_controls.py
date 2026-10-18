"""Bounded AcroForm button/choice edits, using existing button appearances."""
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import (ArrayObject, DictionaryObject, NameObject, NullObject,
                           NumberObject, StreamObject, TextStringObject)


def require(value, message):
    if not value:raise ValueError(message)


def inherited(field, name, default=None):
    reference = getattr(field, 'indirect_reference', None)
    require(reference is not None, 'Campos diretos sem referência PDF ainda não são suportados.')
    current, seen = reference.get_object(), set()
    while current is not None and not isinstance(current, NullObject):
        require(isinstance(current, DictionaryObject) and id(current) not in seen and len(seen) < 64,
                'Hierarquia de campo inválida ou muito profunda.')
        seen.add(id(current))
        if name in current:return current[name]
        parent = current.get('/Parent')
        current = parent.get_object() if parent is not None else None
    return default


def terminal(field):
    kids = field.indirect_reference.get_object().get('/Kids')
    if kids is None or isinstance(kids.get_object(), NullObject):return True
    kids = kids.get_object()
    require(isinstance(kids, ArrayObject), 'Subcampos do formulário inválidos.')
    children = [child.get_object() for child in kids]
    require(all(isinstance(child, DictionaryObject) for child in children), 'Subcampo de formulário inválido.')
    return not any('/T' in child for child in children)


def _widgets(document, field):
    raw = field.indirect_reference.get_object()
    require(terminal(field), 'Selecione um campo terminal.')
    widgets = [raw] if raw.get('/Subtype') == '/Widget' else [x.get_object() for x in _array(raw, '/Kids')]
    require(0 < len(widgets) <= 128 and len({id(w) for w in widgets}) == len(widgets),
            'Campo sem widgets suportados ou acima do limite.')
    pages = {id(a.get_object()) for p in document.pages for a in _array(p, '/Annots')}
    require(all(w.get('/Subtype') == '/Widget' and id(w) in pages for w in widgets),
            'Todos os widgets do campo devem pertencer a páginas do documento.')
    return raw, widgets


def _array(obj, key):
    value = obj.get(key)
    if value is None or isinstance(value.get_object(), NullObject):return []
    value = value.get_object()
    require(isinstance(value, ArrayObject), 'Lista de widgets inválida.')
    return value


def _string(value):
    require(isinstance(value, str) and len(value.encode('utf-8')) <= 4096, 'Opção de formulário inválida ou acima do limite.')
    return value


def describe_control(document, name, field):
    raw, widgets = _widgets(document, field)
    flags, kind = int(inherited(field, '/Ff', 0)), inherited(field, '/FT')
    record = {'name':name, 'read_only':bool(flags & 1)}
    if kind == '/Btn':
        require(not flags & (1 << 16), 'Botões de ação não são campos preenchíveis suportados.')
        states = []
        for widget in widgets:
            appearance = widget.get('/AP')
            appearance = appearance.get_object() if appearance is not None else None
            normal = appearance.get('/N') if isinstance(appearance, DictionaryObject) else None
            normal = normal.get_object() if normal is not None else None
            require(isinstance(normal, DictionaryObject) and '/Off' in normal and len(normal) == 2
                    and all(isinstance(v.get_object(), StreamObject) for v in normal.values()),
                    'Botão precisa de aparências Off e ligada já existentes.')
            on = next(key for key in normal if key != '/Off')
            require(isinstance(on, NameObject) and len(on.encode('utf-8')) <= 4096, 'Estado de botão inválido.')
            states.append(str(on))
        value = str(inherited(field, '/V', '/Off'))
        if flags & (1 << 15):
            require(len(set(states)) == len(states), 'Grupos radio com estados repetidos ainda não são suportados.')
            require(value in states + ['/Off'], 'Seleção radio original inválida.')
            record.update(kind='radio', value=value, options=states, allow_off=not bool(flags & (1 << 14)))
        else:
            require(len(set(states)) == 1 and value in (states[0], '/Off'), 'Estados de checkbox incompatíveis.')
            record.update(kind='checkbox', value=value != '/Off', on_state=states[0])
    elif kind == '/Ch':
        require(not flags & (1 << 18), 'Caixas de combinação com texto livre ainda não são suportadas.')
        options = inherited(field, '/Opt', [])
        require(isinstance(options, ArrayObject) and 0 < len(options) <= 512, 'Lista de opções inválida ou acima do limite.')
        pairs = []
        for option in options:
            option = option.get_object()
            if isinstance(option, str):pairs.append({'value':_string(option), 'label':_string(option)})
            else:
                require(isinstance(option, ArrayObject) and len(option) == 2, 'Opção de lista inválida.')
                pairs.append({'value':_string(option[0]), 'label':_string(option[1])})
        values = [p['value'] for p in pairs]
        require(len(set(values)) == len(values), 'Valores de opções duplicados não são suportados.')
        require(len({p['label'] for p in pairs}) == len(pairs), 'Rótulos de opções duplicados ainda não são suportados.')
        require(all(w is raw or '/V' not in w for w in widgets), 'Valores locais nos widgets de lista ainda não são suportados.')
        value = inherited(field, '/V', '')
        selected = list(value) if isinstance(value, ArrayObject) else [value] if value != '' else []
        multiple = bool(flags & (1 << 21))
        require(all(isinstance(v, str) and v in values for v in selected)
                and len(set(selected)) == len(selected) and (multiple or len(selected) <= 1),
                'Seleção original de lista inválida.')
        record.update(kind='choice', value=selected, options=pairs, multiple=multiple, combo=bool(flags & (1 << 17)))
    else:raise ValueError('Tipo de controle não suportado.')
    return record


def inspect_controls(document, fields):
    controls, unsupported = [], []
    for name, field in fields.items():
        if inherited(field, '/FT') not in ('/Btn', '/Ch'):continue
        require(len(controls) + len(unsupported) < 512, 'Formulário acima do limite de 512 controles adicionais.')
        try:controls.append(describe_control(document, name, field))
        except ValueError as exc:unsupported.append({'name':name, 'reason':str(exc)})
    return controls, unsupported


def fill_controls(writer, values):
    require(isinstance(values, dict) and 0 < len(values) <= 256, 'Informe de 1 a 256 controles.')
    fields = writer.get_fields() or {}
    for name, value in values.items():
        require(name in fields, 'Controle não encontrado.')
        field = fields[name];record = describe_control(writer, name, field)
        require(not record['read_only'], 'Campo somente leitura não pode ser alterado.')
        raw, widgets = _widgets(writer, field)
        if record['kind'] in ('checkbox', 'radio'):
            if record['kind'] == 'checkbox':
                require(type(value) is bool, 'Checkbox exige um valor booleano.')
                selected = record['on_state'] if value else '/Off'
            else:
                require(isinstance(value, str) and value in record['options'] + (['/Off'] if record['allow_off'] else []),
                        'Seleção radio inválida.')
                selected = value
            raw[NameObject('/V')] = NameObject(selected)
            for widget in widgets:
                normal = widget['/AP']['/N']
                widget[NameObject('/AS')] = NameObject(selected if selected in normal else '/Off')
                if widget is not raw:widget.pop('/V', None)
        else:
            require(isinstance(value, list) and all(isinstance(v, str) for v in value)
                    and len(set(value)) == len(value) and (record['multiple'] or len(value) <= 1), 'Seleção de lista inválida.')
            exports = [p['value'] for p in record['options']]
            require(all(v in exports for v in value), 'Valor ausente nas opções da lista.')
            # Reject the library's bare-name alias ambiguity before generating appearances.
            for page in writer.pages:
                for ref in _array(page, '/Annots'):
                    widget = ref.get_object()
                    parent = widget if '/FT' in widget and '/T' in widget else widget.get('/Parent', DictionaryObject()).get_object()
                    if writer._get_qualified_field_name(parent=parent) == name or parent.get('/T') == name:
                        require(any(widget is target for target in widgets), 'Nomes de campo ambíguos não são suportados.')
            for key in ('/FT', '/Ff', '/Opt'):
                item = inherited(field, key)
                if item is not None:raw[NameObject(key)] = item
            ordered = [v for v in exports if v in value]
            # pypdf6.20.1 expects plain /Opt strings during appearance generation.
            # Generate against display labels, then restore the actual export schema/value.
            options = raw['/Opt']
            labels = [p['label'] for p in record['options']]
            selected_labels = [labels[exports.index(v)] for v in ordered]
            raw[NameObject('/Opt')] = ArrayObject(TextStringObject(v) for v in labels)
            try:
                writer.update_page_form_field_values(None, {name:selected_labels if record['multiple'] else selected_labels[0] if selected_labels else ''}, auto_regenerate=None)
            finally:raw[NameObject('/Opt')] = options
            raw[NameObject('/V')] = ArrayObject(TextStringObject(v) for v in ordered) if record['multiple'] else TextStringObject(ordered[0] if ordered else '')
            raw[NameObject('/I')] = ArrayObject(NumberObject(exports.index(v)) for v in ordered)
            require(inherited((writer.get_fields() or {})[name], '/V') == (ordered if record['multiple'] else ordered[0] if ordered else ''),
                    'Não foi possível atualizar os widgets do campo.')
