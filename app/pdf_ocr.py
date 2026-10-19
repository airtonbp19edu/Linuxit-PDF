"""Bounded, offline raster-copy OCR. Original document and saved copies stay intact."""
from io import BytesIO
import hashlib
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile

from PIL import Image
from local_files import publish_copy
from pdf_dependency import configure_pdf_library
from platform_runtime import subprocess_options
from search_tasks import run_search_worker

configure_pdf_library()
from pypdf import PdfReader, PdfWriter

MAX_SOURCE_BYTES = 128 * 1024**2
MAX_OUTPUT_BYTES = 128 * 1024**2
MAX_PAGES = 20
MAX_PAGE_PIXELS = 45_000_000
MAX_TOTAL_PIXELS = 150_000_000
LANGUAGES = frozenset({'por', 'eng', 'por+eng'})


def _require(value, message):
    if not value:
        raise ValueError(message)


def source_identity(path):
    path = Path(path)
    _require(path.is_file() and path.stat().st_size <= MAX_SOURCE_BYTES,
             'OCR aceita um PDF local de até 128 MiB.')
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def validate_request(request):
    _require(isinstance(request, dict) and {'source_sha256', 'language', 'dpi'}<=set(request)<={'source_sha256','language','dpi','pages','psm'},
             'Pedido de OCR inválido.')
    _require(isinstance(request['source_sha256'], str) and re.fullmatch('[0-9a-f]{64}', request['source_sha256']),
             'Identidade do PDF inválida; reabra o documento.')
    _require(isinstance(request['language'], str) and request['language'] in LANGUAGES,
             'Escolha português, inglês ou português e inglês.')
    _require(type(request['dpi']) is int and request['dpi'] in (150, 300),
             'OCR aceita resolução de 150 ou 300 DPI.')
    _require(type(request.get('psm',3)) is int and request.get('psm',3) in (3,6,11),'OCR aceita layout automático, bloco único ou texto esparso.')
    if 'pages' in request:
        _require(isinstance(request['pages'],list) and 1<=len(request['pages'])<=MAX_PAGES and all(type(v) is int and 1<=v<=MAX_PAGES for v in request['pages']) and len(set(request['pages']))==len(request['pages']),'Selecione páginas únicas entre1e20.')
    return request['source_sha256'], request['language'], request['dpi']


def _run(argv, timeout=120):
    # Invoked inside a resource-limited worker process group. The caller kills
    # the group on cancellation, including Poppler/Tesseract grandchildren.
    env = os.environ.copy()
    env['OMP_THREAD_LIMIT'] = '1'
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                    timeout=timeout, env=env, **subprocess_options())
        except FileNotFoundError as exc:
            raise ValueError('OCR requer Poppler e Tesseract instalados com os idiomas escolhidos.') from exc
        except subprocess.TimeoutExpired as exc:
            raise ValueError('Uma página excedeu o tempo de OCR. Nenhuma cópia foi publicada.') from exc
        _require(result.returncode == 0,
                 'Falha no OCR local. Confira o PDF e os idiomas instalados no Tesseract.')
        out.seek(0)
        return out.read(16385).decode('utf-8', errors='replace')


def _page_sizes(reader, dpi):
    _require(not reader.is_encrypted, 'OCR não aceita PDF criptografado nesta versão.')
    _require(1 <= len(reader.pages) <= MAX_PAGES, f'OCR aceita de 1 a {MAX_PAGES} páginas por operação.')
    sizes, total = [], 0
    for page in reader.pages:
        _require(float(page.get('/UserUnit', 1)) == 1, 'OCR não aceita UserUnit diferente de 1 nesta versão.')
        coords = [float(v) for v in (*page.mediabox, *page.cropbox)]
        _require(all(math.isfinite(v) and abs(v) <= 14400 for v in coords), 'Caixas de página inválidas para OCR.')
        box, media = page.cropbox, page.mediabox
        _require(media.left <= box.left < box.right <= media.right and media.bottom <= box.bottom < box.top <= media.top,
                 'O CropBox deve estar contido no MediaBox para OCR.')
        rotation = int(page.rotation)
        _require(rotation % 90 == 0, 'Rotação de página inválida para OCR.')
        width, height = float(box.width), float(box.height)
        if rotation % 180:
            width, height = height, width
        pixels = math.ceil(width * dpi / 72) * math.ceil(height * dpi / 72)
        _require(0 < pixels <= MAX_PAGE_PIXELS, 'Uma página excede o limite de 45 megapixels para OCR.')
        total += pixels
        _require(total <= MAX_TOTAL_PIXELS, 'O documento excede o limite de 150 megapixels para OCR.')
        sizes.append((width, height))
    return sizes


def create_searchable_copy(source, destination, request):
    identity, language, dpi = validate_request(request)
    source, destination = Path(source).resolve(), Path(destination)
    _require(destination.suffix.lower() == '.pdf' and destination.parent.is_dir(),
             'Escolha um nome .pdf novo em uma pasta disponível.')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    destination = destination.resolve()
    _require(source != destination, 'O destino deve ser diferente do original.')
    _require(source.is_file() and source.stat().st_size <= MAX_SOURCE_BYTES, 'OCR aceita um PDF local de até 128 MiB.')
    with source.open('rb') as stream:
        data = stream.read(MAX_SOURCE_BYTES + 1)
    _require(len(data) <= MAX_SOURCE_BYTES, 'OCR aceita um PDF local de até 128 MiB.')
    _require(hashlib.sha256(data).hexdigest() == identity, 'O PDF mudou. Reabra o documento antes do OCR.')
    reader=PdfReader(BytesIO(data));sizes = _page_sizes(reader, dpi)
    chosen=set(request.get('pages',range(1,len(sizes)+1)))
    _require(chosen<=set(range(1,len(sizes)+1)),'Uma página selecionada não existe neste PDF.')
    writer = PdfWriter()
    writer.add_metadata({'/Creator': 'Linuxit PDF — OCR local', '/Title': 'Cópia rasterizada com OCR'})
    pages_info, total_page_bytes = [], 0
    with tempfile.TemporaryDirectory(prefix='linuxit-ocr-') as folder:
        work = Path(folder)
        pinned = work / 'source.pdf'
        pinned.write_bytes(data)
        del data
        available = _run(['tesseract', '--list-langs']).splitlines()
        _require(set(language.split('+')).issubset({line.strip() for line in available}),
                 'O idioma escolhido não está instalado no Tesseract local.')
        for index, (width, height) in enumerate(sizes, 1):
            if index not in chosen:
                writer.add_page(reader.pages[index-1])
                retained_text=(reader.pages[index-1].extract_text() or '').strip()
                pages_info.append({'page':index,'page_points':[width,height],'recognized_characters':len(retained_text),'text_detected':bool(retained_text),'ocr_applied':False})
                continue
            prefix = work / 'page'
            image, page_pdf = prefix.with_suffix('.png'), prefix.with_suffix('.pdf')
            _run(['pdftocairo', '-f', str(index), '-l', str(index), '-singlefile', '-cropbox',
                  '-png', '-r', str(dpi), str(pinned), str(prefix)])
            _require(image.is_file() and image.stat().st_size <= MAX_SOURCE_BYTES, 'A renderização de OCR não produziu uma imagem válida.')
            expected = (math.ceil(width * dpi / 72), math.ceil(height * dpi / 72))
            with Image.open(image) as rendered:
                _require(rendered.format == 'PNG' and rendered.size == expected, 'Dimensões inesperadas na renderização de OCR.')
                rendered.verify()
            _run(['tesseract', str(image), str(prefix), '-l', language, '--dpi', str(dpi),
                  '--oem', '1', '--psm', str(request.get('psm',3)), 'pdf'])
            _require(page_pdf.is_file(), 'O Tesseract não produziu a página PDF esperada.')
            total_page_bytes += page_pdf.stat().st_size
            _require(total_page_bytes <= MAX_OUTPUT_BYTES, 'O PDF de OCR excede o limite de 128 MiB.')
            page_reader = PdfReader(BytesIO(page_pdf.read_bytes()), strict=True)
            _require(not page_reader.is_encrypted and len(page_reader.pages) == 1, 'Página de OCR inválida.')
            page = page_reader.pages[0]
            _require(int(page.rotation) == 0 and all(math.isclose(float(a), b, abs_tol=1) for a, b in
                     zip((page.mediabox.width, page.mediabox.height), (width, height))), 'Geometria inesperada na página de OCR.')
            # Pixel rounding can change Tesseract's dimensions by a fraction of
            # a point. Scale both the raster and invisible text to the crop size.
            page.scale_to(width, height)
            writer.add_page(page)
            text = page.extract_text() or ''
            pages_info.append({'page': index, 'page_points': [width, height],
                               'recognized_characters': len(text.strip()), 'text_detected': bool(text.strip()),'ocr_applied':True})
            image.unlink()
            page_pdf.unlink()
        output = work / 'searchable.pdf'
        writer.write(output)
        _require(output.stat().st_size <= MAX_OUTPUT_BYTES, 'O PDF de OCR excede o limite de 128 MiB.')
        final = PdfReader(output, strict=True)
        _require(len(final.pages) == len(sizes) and not final.is_encrypted, 'PDF de OCR incompleto.')
        for page_index,(page, size) in enumerate(zip(final.pages, sizes),1):
            if page_index not in chosen:continue
            _require(all(math.isclose(float(a), b, abs_tol=1e-5) for a, b in
                         zip((page.mediabox.width, page.mediabox.height), size)), 'Dimensões finais inválidas no OCR.')
        output_hash = source_identity(output)
        def unchanged():
            _require(source_identity(source) == identity, 'O PDF mudou durante o OCR. Reabra o documento.')
        publish_copy(output, destination, unchanged)
    return {'schema': 'linuxit-ocr-copy-v1', 'path': str(destination), 'source_sha256': identity,
            'output_sha256': output_hash, 'pages': len(sizes), 'language': language, 'dpi': dpi,
            'rasterized': True, 'pages_info': pages_info,
            'rasterized_pages':sorted(chosen),'psm':request.get('psm',3),
            'pages_without_text': [p['page'] for p in pages_info if not p['text_detected']]}


def invoke_ocr(source, destination, request, cancel=None, timeout=600):
    identity, language, dpi = validate_request(request)
    result = run_search_worker('ocr-copy', source, request, cancel, timeout, destination=destination)
    if result is None:
        return None
    try:
        _require(result['schema'] == 'linuxit-ocr-copy-v1' and result['source_sha256'] == identity
                 and result['language'] == language and result['dpi'] == dpi and result['rasterized'] is True
                 and Path(result['path']).resolve() == Path(destination).resolve()
                 and re.fullmatch('[0-9a-f]{64}', result['output_sha256'])
                 and type(result['pages']) is int and 1 <= result['pages'] <= MAX_PAGES
                 and len(result['pages_info']) == result['pages'], 'Confirmação de OCR inválida.')
        missing = []
        for index, page in enumerate(result['pages_info'], 1):
            _require(type(page['page']) is int and page['page'] == index and type(page['recognized_characters']) is int
                     and page['recognized_characters'] >= 0
                     and type(page['text_detected']) is bool
                     and page['text_detected'] == (page['recognized_characters'] > 0), 'Página de OCR inválida.')
            _require(isinstance(page['page_points'], list) and len(page['page_points']) == 2
                     and all(type(v) in (int, float) and math.isfinite(v) and 0 < v <= 28800
                             for v in page['page_points']), 'Dimensões de OCR inválidas.')
            if not page['text_detected']:
                missing.append(index)
        _require(missing == result['pages_without_text'], 'Avisos de OCR inválidos.')
        return result
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError('O worker não retornou uma confirmação de OCR válida.') from exc
