"""Own paginated XFA flow renderer, not an Adobe/XFA layout implementation.

Supported templates use top-to-bottom subforms, normal named data binding,
repeatable subforms, text/numeric/date fields and static text. Scripts, FormCalc,
positioned layout, explicit bindings and unsupported controls are refused before
publication. Output contains new AcroForm widgets and matching XFA datasets.
"""
import copy
import hashlib
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET

from local_files import publish_copy
from pdf_xfa import XFAError, _parse, _require, _obj, _new_stream, xfa_source, MAX_BYTES, MAX_FIELDS, MAX_VALUE
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, BooleanObject, DecodedStreamObject, DictionaryObject,
                          FloatObject, NameObject, NumberObject, TextStringObject)

TEMPLATE_PREFIX = 'http://www.xfa.org/schema/xfa-template/'
DATA_NS = 'http://www.xfa.org/schema/xfa-data/1.0/'
MAX_PAGES = 100
MAX_NODES = 20000
MAX_PDF_BYTES = 64 * 1024**2
SEGMENT = re.compile(r'([A-Za-z_][A-Za-z_0-9-]*)\[(\d{1,4})\]')


def local(element):
    return element.tag.rsplit('}', 1)[-1]


def child(element, name):
    return next((node for node in element if local(node) == name), None)


def _xml(data):
    _parse(data)  # Expat preflight refuses DTD/entities and bounds depth/size.
    # Count before building an ElementTree: tiny XML elements can otherwise make
    # an 8-MiB packet consume much more memory than its byte size suggests.
    from xml.parsers import expat
    parser=expat.ParserCreate();count=0
    def node(_name,_attrs):
        nonlocal count
        count+=1
        _require(count<=MAX_NODES,'Pacote XFA acima do limite de nós.')
    parser.StartElementHandler=node;parser.Parse(data,True)
    return ET.fromstring(data)


def _packets(reader):
    source = xfa_source(reader)
    _require(source is not None, 'Este PDF não contém XFA.')
    names, parts = source
    if names:
        _require(names.count('template') == names.count('datasets') == 1, 'É necessário um template e um datasets XFA completos.')
        return parts[names.index('template')], parts[names.index('datasets')]
    root = _xml(parts[0])
    template = next((n for n in root.iter() if local(n) == 'template'), None)
    datasets = next((n for n in root.iter() if n.tag == '{'+DATA_NS+'}datasets'), None)
    _require(template is not None and datasets is not None, 'Template ou datasets XFA ausente.')
    return ET.tostring(template, encoding='utf-8'), ET.tostring(datasets, encoding='utf-8')


def _data_root(datasets):
    data = child(datasets, 'data')
    _require(datasets.tag == '{'+DATA_NS+'}datasets' and data is not None, 'Datasets XFA inválido.')
    return data


def _path(data, path):
    _require(isinstance(path, str) and len(path) <= 1024, 'Caminho XFA inválido.')
    current = data
    for segment in path.split('.'):
        match = SEGMENT.fullmatch(segment)
        _require(match is not None, 'Caminho XFA precisa de nomes e índices explícitos.')
        candidates = [node for node in current if local(node) == match[1]]
        index = int(match[2])
        _require(index < len(candidates), 'Caminho de dados XFA não encontrado: ' + path)
        current = candidates[index]
    return current


def _value(element):
    value = child(element, 'value')
    if value is None:
        return ''
    _require(len(value) <= 1, 'Valor XFA composto não suportado.')
    if len(value):
        _require(local(value[0]) in ('text', 'integer', 'decimal', 'float', 'date', 'dateTime'), 'Tipo de valor XFA não suportado.')
    text = ''.join(value.itertext())
    _require(len(text) <= MAX_VALUE, 'Valor XFA acima do limite.')
    return text


def _safe_template(template):
    _require(local(template) == 'template', 'Pacote template XFA inválido.')
    # A renderer must never silently accept an unimplemented layout instruction.
    allowed = {'template','subform','occur','field','draw','value','text','integer','decimal','float','date','dateTime',
               'caption','ui','textEdit','numericEdit','dateTimeEdit','font','margin','para','border','edge','fill','color',
               'pageSet','pageArea','medium','contentArea','extras','desc'}
    count = 0
    for node in template.iter():
        count += 1
        _require(count <= 20000, 'Template XFA acima do limite de nós.')
        _require(local(node) in allowed, 'Elemento XFA não suportado na cópia fluida: ' + local(node))
        if local(node) == 'subform':
            _require(node.get('layout', 'tb') == 'tb', 'A cópia fluida só aceita subformulários top-to-bottom (tb).')
        if local(node) in ('field', 'subform') and node.get('name') is not None:
            _require(re.fullmatch(r'[A-Za-z_][A-Za-z_0-9-]*', node.get('name')) is not None, 'Nome XFA fora do binding normal suportado.')
        _require(node.get('presence', 'visible') == 'visible', 'Presença condicional XFA não suportada.')
        if local(node)=='field':
            _require(node.get('access','open')=='open','Campo XFA com acesso protegido/somente leitura não suportado na cópia fluida.')
        _require(not any(key.rsplit('}',1)[-1] in ('href','use','usehref') for key in node.attrib), 'Referência externa XFA não suportada.')


def _bounds(node):
    occur = child(node, 'occur')
    if occur is None:
        return 1, 1, 1
    try:
        low, high, initial = (int(occur.get(k, d)) for k, d in (('min','1'), ('max','1'), ('initial','1')))
    except ValueError:
        raise XFAError('Ocorrência XFA inválida.') from None
    _require(0 <= low <= 1000 and (high == -1 or low <= high <= 1000) and low <= initial <= (1000 if high == -1 else high), 'Ocorrência XFA fora do limite.')
    return low, 1000 if high == -1 else high, initial


def _blank(node, budget=None):
    if budget is None:budget=[MAX_FIELDS]
    _require(budget[0]>0,'Instanciação XFA acima do orçamento de nós.')
    budget[0]-=1
    output = ET.Element(node.get('name'))
    if local(node) == 'field':
        output.text = _value(node)
    else:
        for item in node:
            if local(item) in ('subform','field'):
                for _ in range(_bounds(item)[2]):
                    if item.get('name'):
                        output.append(_blank(item,budget))
                    else:
                        _require(local(item) == 'subform', 'Campo XFA sem nome.')
                        for nested in item:
                            if local(nested) in ('subform','field'):
                                output.append(_blank(nested,budget))
    return output


def flow_model(reader, values=None, instances=None):
    """Validate and bind flow rows, allowing explicit data instance add/remove."""
    template_bytes, dataset_bytes = _packets(reader)
    template, datasets = _xml(template_bytes), _xml(dataset_bytes)
    _safe_template(template)
    data = _data_root(datasets)
    values = {} if values is None else values
    instances = [] if instances is None else instances
    _require(isinstance(values, dict) and len(values) <= 256, 'Até 256 valores XFA por cópia.')
    _require(isinstance(instances, list) and len(instances) <= 100, 'Até 100 alterações de instância XFA por cópia.')
    rows, groups = [], {}
    creation_budget=[MAX_FIELDS]

    def bind(parent_template, parent_data, prefix='', populate=False):
        for node in parent_template:
            kind = local(node)
            if kind == 'draw':
                rows.append(dict(kind='text', text=_value(node)))
                _require(len(rows)<=MAX_FIELDS,'Layout XFA acima de 5000 linhas.')
                continue
            if kind not in ('field','subform'):
                continue
            name = node.get('name')
            if not name:
                _require(kind == 'subform', 'Campo XFA sem nome.')
                bind(node, parent_data, prefix, populate)
                continue
            entries = [n for n in parent_data if local(n) == name]
            low, high, initial = _bounds(node)
            # Missing ordinary nodes are instantiated from template defaults.
            if not entries and initial and populate:
                entries = [_blank(node,creation_budget) for _ in range(initial)]
                parent_data.extend(entries)
            base = prefix + name
            _require(base not in groups, 'Binding XFA duplicado no template: ' + base)
            groups[base] = (parent_data, node, entries)
            _require(low <= len(entries) <= high, 'Quantidade de instâncias XFA fora de occur: ' + base)
            for index, entry in enumerate(entries):
                path = base + '[' + str(index) + ']'
                if kind == 'subform':
                    bind(node, entry, path + '.', populate)
                else:
                    _require(not len(entry), 'Dados XFA ricos/compostos não suportados na cópia fluida.')
                    ui = child(node, 'ui')
                    _require(ui is None or len(ui) == 1 and local(ui[0]) in ('textEdit','numericEdit','dateTimeEdit'), 'Controle XFA fora do subconjunto textual.')
                    caption = child(node, 'caption')
                    label = _value(caption) if caption is not None else name
                    rows.append(dict(kind='field', path=path, label=label, value=entry.text or ''))
                    _require(len(rows) <= MAX_FIELDS, 'Layout XFA acima de 5000 linhas.')
    bind(template, data, populate=True)
    for operation in instances:
        _require(isinstance(operation, dict) and set(operation) == {'action','path','index'}, 'Alteração de instância XFA inválida.')
        action, path, index = operation['action'], operation['path'], operation['index']
        _require(action in ('add','remove') and path in groups and type(index) is int, 'Instância XFA não encontrada.')
        parent, node, entries = groups[path]
        _require(local(node) == 'subform', 'Só subformulários repetidos admitem instâncias.')
        low, high, _ = _bounds(node)
        if action == 'add':
            _require(len(entries) < high and 0 <= index <= len(entries), 'Instância excede o máximo XFA.')
            new = _blank(node,creation_budget)
            position = list(parent).index(entries[index]) if index < len(entries) else (list(parent).index(entries[-1])+1 if entries else len(parent))
            parent.insert(position, new)
        else:
            _require(len(entries) > low and 0 <= index < len(entries), 'Instância viola o mínimo XFA.')
            parent.remove(entries[index])
        rows.clear(); groups.clear(); bind(template, data)
    known = {row['path'] for row in rows if row['kind'] == 'field'}
    for path, value in values.items():
        _require(path in known and isinstance(value, str) and len(value) <= MAX_VALUE, 'Campo ou valor XFA inválido.')
        _require(not any(ord(c) < 32 and c not in '\n\r\t' for c in value), 'Valor XFA contém controle XML inválido.')
        _path(data, path).text = value
    rows.clear(); groups.clear(); bind(template, data)
    _require(rows, 'Template XFA sem conteúdo fluido.')
    serialized = ET.tostring(datasets, encoding='utf-8', xml_declaration=True)
    _require(len(serialized) <= MAX_BYTES, 'Dados XFA acima de 8 MiB após as alterações.')
    return dict(rows=rows, groups=[dict(path=path,count=len(entries),minimum=_bounds(node)[0],maximum=_bounds(node)[1])
                for path, (_, node, entries) in sorted(groups.items()) if local(node)=='subform' and _bounds(node)[1] > 1],
                template=template_bytes, datasets=serialized)


def inspect_xfa_flow(source):
    _require(Path(source).stat().st_size<=MAX_PDF_BYTES,'PDF XFA acima do limite de 64 MiB.')
    reader = PdfReader(source)
    _require(not reader.is_encrypted, 'Abra uma cópia XFA sem cifra para o layout fluido.')
    model = flow_model(reader)
    return dict(source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
                fields=[row for row in model['rows'] if row['kind']=='field'],groups=model['groups'],
                original_layout_preserved=False,scripts_executed=False)


def _latin(text):
    # The portable layout uses an explicitly advertised PDF WinAnsi font. Never
    # replace unsupported Unicode with question marks and claim data fidelity.
    try:
        return text.encode('cp1252')
    except UnicodeEncodeError:
        raise XFAError('A cópia fluida portátil aceita texto Windows-1252; este valor exige outra fonte Unicode.') from None


def _render(model):
    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({NameObject('/Type'):NameObject('/Font'), NameObject('/Subtype'):NameObject('/Type1'),
                       NameObject('/BaseFont'):NameObject('/Helvetica'), NameObject('/Encoding'):NameObject('/WinAnsiEncoding')}))
    resources = DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/Helv'):font})})
    fields = ArrayObject();page = None;commands = [];y = 0
    def stream(data):
        value=DecodedStreamObject();value.set_data(data);return writer._add_object(value)
    def finish():
        if page is not None:
            page[NameObject('/Contents')]=stream(b'\n'.join(commands))
    def next_page():
        nonlocal page,y,commands
        finish();_require(len(writer.pages)<MAX_PAGES,'Layout XFA acima de 100 páginas.')
        page=writer.add_blank_page(595,842);page[NameObject('/Resources')]=resources
        page[NameObject('/Annots')]=ArrayObject();commands=[];y=800
    def text_line(text,x,baseline):
        commands.append(b'BT /Helv 11 Tf 0 g '+str(x).encode()+b' '+str(baseline).encode()+b' Td <'+_latin(text).hex().encode()+b'> Tj ET')
    for row in model['rows']:
        text = row['text'] if row['kind']=='text' else row['value']
        lines=[]
        for line in text.replace('\r\n','\n').replace('\r','\n').split('\n'):
            # Conservative fixed character width keeps even wide Helvetica
            # glyphs inside the 505-point text rectangle (11pt <= 11pt/char).
            lines.extend(line[i:i+45] for i in range(0,len(line),45)) if line else lines.append('')
        _require(len(lines)<=48,'Campo XFA acima de 48 linhas; divida o texto.')
        height=max(24,len(lines)*14+10)+(16 if row['kind']=='field' else 0)
        if page is None or y-height<36:next_page()
        if row['kind']=='text':
            for index,line in enumerate(lines):text_line(line,42,y-12-index*14)
        else:
            text_line(row['label'][:45],42,y-11);top=y-18;bottom=y-height
            _latin(row['value'])
            widget=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Widget'),
                NameObject('/FT'):NameObject('/Tx'),NameObject('/T'):TextStringObject(row['path']),NameObject('/V'):TextStringObject(row['value']),
                NameObject('/DA'):TextStringObject('/Helv 11 Tf 0 g'),NameObject('/Ff'):NumberObject(4096),NameObject('/F'):NumberObject(4),
                NameObject('/Rect'):ArrayObject(FloatObject(n) for n in (42,bottom,553,top)),NameObject('/P'):page.indirect_reference})
            appearance=[b'0.7 G 0 0 511 '+str(top-bottom).encode()+b' re S']
            for index,line in enumerate(lines):
                appearance.append(b'BT /Helv 11 Tf 0 g 4 '+str(top-bottom-14-index*14).encode()+b' Td <'+_latin(line).hex().encode()+b'> Tj ET')
            ap=DecodedStreamObject();ap.set_data(b'\n'.join(appearance));ap.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),
                NameObject('/BBox'):ArrayObject(FloatObject(n) for n in (0,0,511,top-bottom)),NameObject('/Resources'):resources})
            widget[NameObject('/AP')]=DictionaryObject({NameObject('/N'):writer._add_object(ap)})
            ref=writer._add_object(widget);fields.append(ref);page['/Annots'].append(ref)
        y-=height+12
    finish()
    form=DictionaryObject({NameObject('/Fields'):fields,NameObject('/DA'):TextStringObject('/Helv 11 Tf 0 g'),NameObject('/DR'):resources,
        NameObject('/XFA'):ArrayObject([TextStringObject('template'),_new_stream(writer,model['template']),TextStringObject('datasets'),_new_stream(writer,model['datasets'])])})
    writer.root_object[NameObject('/AcroForm')]=writer._add_object(form)
    writer.root_object[NameObject('/NeedsRendering')]=BooleanObject(False)
    writer.add_metadata({'/Producer':'Linuxit PDF — own XFA flow layout','/Subject':'Layout fluido próprio; não preserva a aparência original XFA'})
    return writer


def create_xfa_flow_copy(source, destination, request):
    _require(isinstance(request,dict) and set(request)=={'source_sha256','values','instances'}, 'Pedido de cópia XFA inválido.')
    source,destination=Path(source),Path(destination)
    _require(destination.suffix.lower()=='.pdf' and destination.parent.is_dir(),'Escolha um PDF novo em pasta disponível.')
    _require(source.stat().st_size<=MAX_PDF_BYTES,'PDF XFA acima do limite de 64 MiB.')
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    _require(request['source_sha256']==before,'O PDF mudou; leia o formulário novamente.')
    reader=PdfReader(source)
    _require(not reader.is_encrypted and '/Perms' not in reader.root_object,'Cópia fluida XFA não aceita documento cifrado/assinado.')
    fields=reader.get_fields() or {}
    _require(not any(field.get('/FT')=='/Sig' for field in fields.values()),'Cópia fluida XFA não aceita assinatura.')
    model=flow_model(reader,request['values'],request['instances'])
    writer=_render(model)
    with tempfile.TemporaryDirectory(prefix='linuxit-xfa-') as temp:
        staged=Path(temp)/'flow.pdf';writer.write(staged)
        verified=PdfReader(staged).get_fields() or {}
        expected={r['path']:r['value'] for r in model['rows'] if r['kind']=='field'}
        _require(all(name in verified and str(verified[name].get('/V',''))==value for name,value in expected.items()),'Campos XFA divergentes após renderizar.')
        def unchanged():
            _require(hashlib.sha256(source.read_bytes()).hexdigest()==before,'O PDF mudou durante a operação.')
        publish_copy(staged,destination,unchanged)
    return dict(schema='linuxit-xfa-flow-copy-v1',path=str(destination),pages=len(writer.pages),fields=len(expected),
                source_sha256=before,original_layout_preserved=False,scripts_executed=False)
