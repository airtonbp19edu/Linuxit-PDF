"""Apply pending redaction marks (E15) in a new copy.

Each page holding /Redact marks is rendered by Poppler without its
annotations, the marked areas are painted with the mark's fill colour (/IC,
black by default) in the raster, and the page content is replaced by that
single image. Text, vector drawings and images of the page are gone; pages
without marks keep their content byte for byte. Annotations that overlap a
marked area are removed with the marks; form fields under a mark are refused.
The structure tree is dropped when it exists, because it may carry the page's
text (ActualText/Alt) and its marked-content links would point to nothing.

Hidden data can be selected explicitly: Info/XMP removal, marked-word matching
in outline titles and UTF-8 text attachments. Other pages are not searched.
"""
from io import BytesIO
import hashlib
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zlib

from local_files import publish_copy
from pdf_dependency import configure_pdf_library
from platform_runtime import subprocess_options
from search_tasks import run_search_worker

configure_pdf_library()
from pypdf import PdfReader, PdfWriter  # noqa: E402
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,  # noqa: E402
                           NameObject, NumberObject)

SCHEMA = 'linuxit-redacted-copy-v1'
MAX_SOURCE_BYTES = 128 * 1024**2
MAX_OUTPUT_BYTES = 256 * 1024**2
MAX_REDACTED_PAGES = 50
MAX_MARKS = 512
MAX_PAGE_PIXELS = 45_000_000
MAX_TOTAL_PIXELS = 300_000_000
DPI_CHOICES = (150, 300)
IMAGE_NAME = '/LinuxitRedacted'


def _require(value, message):
    if not value:
        raise ValueError(message)


def validate_request(request):
    _require(isinstance(request, dict) and {'source_sha256', 'dpi'} <= set(request) <= {'source_sha256', 'dpi', 'mode', 'hidden'}, 'Pedido de redação inválido.')
    from redaction_hidden import options
    options(request)
    _require(request.get('mode', 'raster') in ('raster', 'vector'), 'Modo de redação inválido.')
    _require(isinstance(request['source_sha256'], str) and re.fullmatch('[0-9a-f]{64}', request['source_sha256']),
             'Identidade do PDF inválida; reabra o documento.')
    _require(type(request['dpi']) is int and request['dpi'] in DPI_CHOICES, 'A redação aceita 150 ou 300 DPI.')
    return request['source_sha256'], request['dpi']


def _number(value):
    value = float(value)
    _require(math.isfinite(value) and abs(value) <= 1_000_000, 'Geometria de marca de redação inválida.')
    return value


def _boxes(note):
    """Marked areas in page space: QuadPoints when present, otherwise /Rect."""
    quads = note.get('/QuadPoints')
    quads = quads.get_object() if quads is not None else None
    if isinstance(quads, list) and quads:
        values = [_number(v) for v in quads]
        _require(len(values) % 8 == 0 and len(values) // 8 <= 1024, 'QuadPoints de redação inválidos.')
        boxes = []
        for i in range(0, len(values), 8):
            xs, ys = values[i:i + 8:2], values[i + 1:i + 8:2]
            boxes.append((min(xs), min(ys), max(xs), max(ys)))
    else:
        x0, y0, x1, y1 = [_number(v) for v in note['/Rect']]
        boxes = [(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))]
    _require(all(b[2] > b[0] and b[3] > b[1] for b in boxes), 'Marca de redação com área vazia.')
    return boxes


def _fill(note):
    colour = note.get('/IC')
    colour = colour.get_object() if colour is not None else None
    if isinstance(colour, list) and len(colour) == 3:
        values = [_number(c) for c in colour]
        if all(0 <= c <= 1 for c in values):
            return tuple(round(c * 255) for c in values)
    return (0, 0, 0)


def _overlaps(rect, boxes):
    try:
        x0, y0, x1, y1 = [_number(v) for v in rect]
    except (TypeError, ValueError, KeyError):
        return True  # unreadable geometry is treated as overlapping
    x0, x1 = sorted((x0, x1));y0, y1 = sorted((y0, y1))
    return any(x0 < b[2] and b[0] < x1 and y0 < b[3] and b[1] < y1 for b in boxes)


def _plan(reader, dpi):
    """Marks, fills and annotations to remove for every page holding marks."""
    plan, total_marks, pixels = {}, 0, 0
    for index, page in enumerate(reader.pages):
        annots = page.get('/Annots')
        annots = annots.get_object() if annots is not None else []
        if not isinstance(annots, list):continue
        marks = []
        for ref in annots:
            note = ref.get_object()
            if isinstance(note, DictionaryObject) and note.get('/Subtype') == '/Redact':
                marks.append((note, _boxes(note), _fill(note)))
        if not marks:continue
        total_marks += len(marks)
        _require(total_marks <= MAX_MARKS, f'Acima de {MAX_MARKS} marcas de redação.')
        _require(len(plan) < MAX_REDACTED_PAGES, f'A redação aceita até {MAX_REDACTED_PAGES} páginas marcadas por cópia.')
        _require(float(page.get('/UserUnit', 1)) == 1, 'Redação não aceita UserUnit diferente de 1 nesta versão.')
        _require(int(page.rotation) % 90 == 0, 'Rotação de página inválida para redação.')
        box, media = page.cropbox, page.mediabox
        coords = [float(v) for v in (*box, *media)]
        _require(all(math.isfinite(v) and abs(v) <= 14400 for v in coords), 'Caixas de página inválidas para redação.')
        _require(media.left <= box.left < box.right <= media.right and media.bottom <= box.bottom < box.top <= media.top,
                 'O CropBox deve estar contido no MediaBox para a redação.')
        width, height = math.ceil(float(box.width) * dpi / 72), math.ceil(float(box.height) * dpi / 72)
        _require(width * height <= MAX_PAGE_PIXELS, 'Uma página marcada excede 45 megapixels nesta resolução.')
        pixels += width * height
        _require(pixels <= MAX_TOTAL_PIXELS, 'As páginas marcadas excedem o limite total de pixels; use 150 DPI.')
        areas = [b for _, boxes, _ in marks for b in boxes]
        removed, overlay = [], 0
        for ref in annots:
            note = ref.get_object()
            if not isinstance(note, DictionaryObject):continue
            if note.get('/Subtype') == '/Redact':
                removed.append(note);overlay += int('/OverlayText' in note or '/RO' in note)
            elif _overlaps(note.get('/Rect', [0, 0, 0, 0]), areas):
                _require(note.get('/Subtype') != '/Widget',
                         f'Há campo de formulário sob uma área marcada na página {index + 1}; a redação de campos não é suportada.')
                removed.append(note)
        # Popups and replies of a removed annotation go with it.
        changed = True
        while changed:
            changed = False
            for ref in annots:
                note = ref.get_object()
                if not isinstance(note, DictionaryObject) or any(note is r for r in removed):continue
                parent = note.get('/Parent') if note.get('/Subtype') == '/Popup' else note.get('/IRT')
                parent = parent.get_object() if parent is not None else None
                if parent is not None and any(parent is r for r in removed):
                    removed.append(note);changed = True
        plan[index] = dict(marks=marks, removed=removed, size=(width, height), overlay_ignored=overlay)
    _require(plan, 'Não há áreas marcadas para redação neste PDF.')
    return plan


def _run(argv, timeout=180):
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                    timeout=timeout, **subprocess_options())
        except FileNotFoundError as exc:
            raise ValueError('A redação requer o Poppler (pdftocairo) instalado.') from exc
        except subprocess.TimeoutExpired as exc:
            raise ValueError('Uma página excedeu o tempo de renderização. Nenhuma cópia foi publicada.') from exc
        _require(result.returncode == 0, 'Falha ao renderizar uma página marcada.')


def _render(work, data, index, dpi, size):
    """Render one page with no annotations and rotation neutralised (page space = image space)."""
    from PIL import Image
    reader = PdfReader(BytesIO(data))
    writer = PdfWriter()
    page = writer.add_page(reader.pages[index])
    page.pop('/Annots', None)
    page[NameObject('/Rotate')] = NumberObject(0)
    single = work / 'page.pdf'
    with single.open('wb') as stream:writer.write(stream)
    prefix = work / 'page'
    _run(['pdftocairo', '-png', '-singlefile', '-cropbox', '-r', str(dpi), str(single), str(prefix)])
    image_path = prefix.with_suffix('.png')
    _require(image_path.is_file(), 'A renderização não produziu a imagem da página.')
    with Image.open(image_path) as rendered:
        _require(rendered.format == 'PNG' and rendered.size == size, 'Dimensões inesperadas na renderização da redação.')
        image = rendered.convert('RGB')
    single.unlink();image_path.unlink()
    return image


def _paint(image, page, marks, dpi):
    from PIL import ImageDraw
    draw = ImageDraw.Draw(image)
    left, top = float(page.cropbox.left), float(page.cropbox.top)
    scale = dpi / 72
    width, height = image.size
    for _, boxes, fill in marks:
        for x0, y0, x1, y1 in boxes:
            # Round outwards and add one pixel: anti-aliased glyph edges must not survive.
            a = max(0, math.floor((x0 - left) * scale) - 1);b = max(0, math.floor((top - y1) * scale) - 1)
            c = min(width, math.ceil((x1 - left) * scale) + 1);d = min(height, math.ceil((top - y0) * scale) + 1)
            if c > a and d > b:draw.rectangle([a, b, c - 1, d - 1], fill=fill)
    return image


def _image_page(writer, page, image):
    raw = DecodedStreamObject();raw.set_data(image.tobytes())
    raw.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Image'),
                NameObject('/Width'): NumberObject(image.size[0]), NameObject('/Height'): NumberObject(image.size[1]),
                NameObject('/ColorSpace'): NameObject('/DeviceRGB'), NameObject('/BitsPerComponent'): NumberObject(8)})
    encoded = raw.flate_encode(level=9)
    box = page.cropbox
    content = DecodedStreamObject()
    content.set_data(f'q {float(box.width):.4f} 0 0 {float(box.height):.4f} {float(box.left):.4f} {float(box.bottom):.4f} cm '
                     f'{IMAGE_NAME} Do Q\n'.encode('ascii'))
    page[NameObject('/Contents')] = writer._add_object(content)
    page[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'): DictionaryObject(
        {NameObject(IMAGE_NAME): writer._add_object(encoded)})})
    for key in ('/Thumb', '/PieceInfo', '/StructParents', '/Group', '/SeparationInfo'):
        page.pop(key, None)


def redact_copy(source, destination, request):
    identity, dpi = validate_request(request)
    source, destination = Path(source).resolve(), Path(destination)
    _require(destination.suffix.lower() == '.pdf' and destination.parent.is_dir(),
             'Escolha um nome .pdf novo em uma pasta disponível.')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    destination = destination.resolve()
    _require(source != destination, 'O destino deve ser diferente do original.')
    _require(source.is_file() and source.stat().st_size <= MAX_SOURCE_BYTES, 'A redação aceita um PDF local de até 128 MiB.')
    with source.open('rb') as stream:data = stream.read(MAX_SOURCE_BYTES + 1)
    _require(len(data) <= MAX_SOURCE_BYTES, 'A redação aceita um PDF local de até 128 MiB.')
    _require(hashlib.sha256(data).hexdigest() == identity, 'O PDF mudou. Reabra o documento antes da redação.')
    reader = PdfReader(BytesIO(data), strict=True)
    if reader.is_encrypted:
        raise NotImplementedError('Redação de PDF protegido por senha ainda não é suportada; salve uma cópia sem senha antes.')
    root = reader.root_object
    if '/Perms' in root or any(f.get('/FT') == '/Sig' for f in (reader.get_fields() or {}).values()):
        raise NotImplementedError('A redação invalidaria as assinaturas deste PDF; remova-as ou use o original não assinado.')
    _require('/Collection' not in root, 'Redação de portfólios não é suportada.')
    acroform = root.get('/AcroForm')
    _require(acroform is None or '/XFA' not in acroform.get_object(), 'Redação de formulários XFA não é suportada.')
    plan = _plan(reader, dpi)
    writer = PdfWriter(clone_from=reader)
    removed_annotations = 0
    vector_mode = request.get('mode', 'raster') == 'vector'
    vector_counts = {'text_objects_removed':0,'paths_removed':0,'images_removed':0,'forms_removed':0}
    with tempfile.TemporaryDirectory(prefix='linuxit-redact-') as folder:
        work = Path(folder)
        from redaction_hidden import options, marked_words, sanitise
        hidden = options(request)
        hidden_report = sanitise(writer, marked_words(reader, plan, work), hidden) if any(hidden.values()) else None
        for index, item in plan.items():
            if not vector_mode:
                image = _paint(_render(work, data, index, dpi, item['size']), reader.pages[index], item['marks'], dpi)
            page = writer.pages[index]
            annots = page.get('/Annots')
            annots = annots.get_object() if annots is not None else ArrayObject()
            ids = {id(r) for r in item['removed']}
            # writer objects are clones; compare by the source object's indirect number.
            source_annots = reader.pages[index]['/Annots'].get_object()
            keep = ArrayObject(w for w, r in zip(annots, source_annots) if id(r.get_object()) not in ids)
            removed_annotations += len(annots) - len(keep)
            if keep:page[NameObject('/Annots')] = keep
            else:page.pop('/Annots', None)
            if vector_mode:
                from vector_redaction import redact_page
                counts = redact_page(writer,page,item['marks'])
                for key,value in counts.items():vector_counts[key]+=value
            else:
                _image_page(writer, page, image)
        structure_removed = '/StructTreeRoot' in writer._root_object
        if structure_removed:
            writer._root_object.pop('/StructTreeRoot', None)
            mark = writer._root_object.get('/MarkInfo')
            if mark is not None:writer._root_object.pop('/MarkInfo', None)
            for page in writer.pages:page.pop('/StructParents', None)
        writer.compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)
        output = work / 'redacted.pdf'
        with output.open('wb') as stream:writer.write(stream)
        _require(output.stat().st_size <= MAX_OUTPUT_BYTES, 'A cópia redigida excede 256 MiB.')
        final = PdfReader(output, strict=True)
        _require(len(final.pages) == len(reader.pages) and not final.is_encrypted, 'Cópia redigida incompleta.')
        for index, page in enumerate(final.pages):
            if index in plan:
                if not vector_mode:
                    _require(not (page.extract_text() or '').strip(), 'Ainda há texto numa página redigida.')
                notes = page.get('/Annots')
                notes = notes.get_object() if notes is not None else []
                _require(all(n.get_object().get('/Subtype') != '/Redact' for n in notes), 'Marca de redação não removida.')
            else:
                before, after = reader.pages[index].get_contents(), page.get_contents()
                _require((before is None and after is None) or (before is not None and after is not None
                         and before.get_data() == after.get_data()), 'Uma página sem marcas foi alterada.')
        output_hash = hashlib.sha256(output.read_bytes()).hexdigest()

        def unchanged():
            with source.open('rb') as stream:
                _require(hashlib.file_digest(stream, 'sha256').hexdigest() == identity, 'O PDF mudou durante a redação.')
        publish_copy(output, destination, unchanged)
    return {'schema': SCHEMA, 'path': str(destination), 'source_sha256': identity, 'output_sha256': output_hash,
            'pages': len(reader.pages), 'dpi': dpi, 'redacted_pages': [i + 1 for i in sorted(plan)],
            'marks_applied': sum(len(item['marks']) for item in plan.values()),
            'annotations_removed': removed_annotations,
            'overlay_text_ignored': sum(item['overlay_ignored'] for item in plan.values()),
            'structure_tree_removed': structure_removed, 'rasterized': not vector_mode,
            'mode':'vector' if vector_mode else 'raster', 'objects_removed':vector_counts if vector_mode else None,
            'hidden_data': hidden_report}


def invoke_redaction(source, destination, request, cancel=None, timeout=900):
    identity, dpi = validate_request(request)
    result = run_search_worker('redact-copy', source, request, cancel, timeout, destination=destination)
    if result is None:
        return None
    _require(isinstance(result, dict) and result.get('schema') == SCHEMA and result.get('source_sha256') == identity
             and result.get('dpi') == dpi and result.get('rasterized') is (request.get('mode','raster')!='vector')
             and Path(result.get('path', '')).resolve() == Path(destination).resolve()
             and isinstance(result.get('output_sha256'), str) and re.fullmatch('[0-9a-f]{64}', result['output_sha256'])
             and isinstance(result.get('redacted_pages'), list) and result['redacted_pages']
             and all(type(p) is int and 1 <= p <= result.get('pages', 0) for p in result['redacted_pages']),
             'Confirmação de redação inválida.')
    return result
