"""Read-only XFA detection and datasets field listing.

The XFA template is never interpreted and no script runs. Only the data
values in the ``datasets`` packet are listed, by their SOM-style path
(``form1[0].nome[0]``). Parsing is streaming and bounded: total size,
element depth, field count and value length are capped, and DOCTYPE or
entity declarations are refused before any expansion can happen.
"""
from xml.parsers import expat

from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.generic import ArrayObject, NullObject  # noqa: E402

DATA_NS = 'http://www.xfa.org/schema/xfa-data/1.0/'
MAX_BYTES = 8 * 1024 ** 2
MAX_PACKETS = 64
MAX_DEPTH = 64
MAX_FIELDS = 5000
MAX_VALUE = 4096
MAX_PATH = 1024


class XFAError(ValueError):
    pass


def _require(value, message):
    if not value:
        raise XFAError(message)


def _obj(value):
    return value.get_object() if hasattr(value, 'get_object') else value


def _stream_bytes(value):
    value = _obj(value)
    _require(hasattr(value, 'get_data'), 'Pacote XFA não é um fluxo.')
    data = value.get_data()
    _require(len(data) <= MAX_BYTES, 'Formulário XFA acima de 8 MiB.')
    return data


def xfa_source(reader):
    """Return (packet names, packet bytes) or None when the PDF has no XFA."""
    form = reader.root_object.get('/AcroForm')
    form = _obj(form) if form is not None else None
    if form is None or isinstance(form, NullObject) or not hasattr(form, 'get'):
        return None
    xfa = form.get('/XFA')
    if xfa is None:
        return None
    xfa = _obj(xfa)
    if isinstance(xfa, ArrayObject):
        _require(len(xfa) % 2 == 0 and len(xfa) <= 2 * MAX_PACKETS, 'Lista de pacotes XFA inválida.')
        names, parts, total = [], [], 0
        for index in range(0, len(xfa), 2):
            name = _obj(xfa[index])
            _require(isinstance(name, str) and len(name) <= 64, 'Nome de pacote XFA inválido.')
            data = _stream_bytes(xfa[index + 1])
            total += len(data)
            _require(total <= MAX_BYTES, 'Formulário XFA acima de 8 MiB.')
            names.append(str(name)); parts.append(data)
        return names, parts
    return [], [_stream_bytes(xfa)]


class _Collector:
    def __init__(self):
        self.stack = []          # frames: [local name, element uri, data frame or None]
        self.fields = []
        self.truncated = False
        self.datasets = False
        self.data_depth = None   # stack length once <xfa:data> is open
        self.root_counts = {}

    # Each data frame: {'name','counts','children','text','group','value','path'}
    def start(self, tag, attrs):
        _require(len(self.stack) < MAX_DEPTH, 'XFA com profundidade acima do limite.')
        uri, _, local = tag.rpartition(' ')
        frame = None
        parent = self.stack[-1][2] if self.stack else None
        if self.data_depth is not None and len(self.stack) >= self.data_depth:
            owner = next((f[2] for f in reversed(self.stack) if f[2] is not None and f[2]['value']), None)
            if owner is None:
                parent_data = parent if parent is not None and parent.get('path') is not None else None
                counts = parent_data['counts'] if parent_data is not None else self.root_counts
                if parent_data is not None:
                    parent_data['children'] = True
                index = counts.get(local, 0)
                counts[local] = index + 1
                prefix = parent_data['path'] + '.' if parent_data is not None else ''
                node = attrs.get(DATA_NS + ' dataNode')
                frame = {'name': local, 'counts': {}, 'children': False, 'text': [], 'size': 0,
                         'group': node == 'dataGroup',
                         'value': node == 'dataValue' or (DATA_NS + ' contentType') in attrs,
                         'path': (prefix + f'{local}[{index}]')[:MAX_PATH]}
        elif uri == DATA_NS and local == 'datasets':
            self.datasets = True
        elif uri == DATA_NS and local == 'data' and self.stack and self.stack[-1][:2] == ('datasets', DATA_NS):
            self.data_depth = len(self.stack) + 1
        self.stack.append((local, uri, frame))

    def text(self, value):
        owner = next((f[2] for f in reversed(self.stack) if f[2] is not None and f[2]['value']), None)
        target = owner or (self.stack[-1][2] if self.stack else None)
        if target is not None and target['size'] <= MAX_VALUE:
            target['text'].append(value); target['size'] += len(value)

    def end(self, _tag):
        local, uri, frame = self.stack.pop()
        if self.data_depth is not None and len(self.stack) + 1 == self.data_depth:
            self.data_depth = None
        if frame is None or frame['group'] or (frame['children'] and not frame['value']):
            return
        if len(self.fields) >= MAX_FIELDS:
            self.truncated = True
            return
        value = ''.join(frame['text'])
        self.fields.append({'path': frame['path'], 'name': frame['name'], 'value': value[:MAX_VALUE],
                            'value_truncated': len(value) > MAX_VALUE})


def _refuse(*_args):
    raise XFAError('XFA com DOCTYPE ou entidades não é aceito.')


def parse_datasets(xdp):
    """List data values in a bounded XDP document or bare datasets packet."""
    _require(isinstance(xdp, (bytes, bytearray)) and len(xdp) <= MAX_BYTES, 'Formulário XFA acima de 8 MiB.')
    collector = _Collector()
    parser = expat.ParserCreate(namespace_separator=' ')
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    parser.StartDoctypeDeclHandler = _refuse
    parser.EntityDeclHandler = _refuse
    parser.UnparsedEntityDeclHandler = _refuse
    parser.ExternalEntityRefHandler = _refuse
    parser.StartElementHandler = collector.start
    parser.EndElementHandler = collector.end
    parser.CharacterDataHandler = collector.text
    try:
        parser.Parse(bytes(xdp), True)
    except expat.ExpatError as exc:
        raise XFAError('XML do formulário XFA inválido.') from exc
    return collector.datasets, collector.fields, collector.truncated


def inspect_xfa(reader):
    """Describe the XFA form, or return None when the PDF has none."""
    source = xfa_source(reader)
    if source is None:
        return None
    packets, parts = source
    form = _obj(reader.root_object['/AcroForm'])
    fields = _obj(form.get('/Fields')) if form.get('/Fields') is not None else []
    needs = _obj(reader.root_object.get('/NeedsRendering'))
    result = {'packets': packets, 'hybrid': bool(fields) and not isinstance(fields, NullObject),
              'dynamic': needs is True or str(needs) == 'True', 'fields': [], 'truncated': False, 'error': None}
    if packets and 'datasets' not in packets:
        result['error'] = 'O formulário XFA não tem pacote de dados.'
        return result
    # A named datasets packet is normally a complete element; the joined
    # packets form the whole XDP when a writer split elements across streams.
    candidates = [parts[packets.index('datasets')]] if 'datasets' in packets else []
    candidates.append(b''.join(parts))
    for index, candidate in enumerate(candidates):
        try:
            found, result['fields'], result['truncated'] = parse_datasets(candidate)
            break
        except XFAError:
            if index == len(candidates) - 1:
                raise
    if not found:
        result['error'] = 'O formulário XFA não tem pacote de dados.'
    return result
