"""Own bounded image/TIFF-sequence to RGB PDF creation; inputs stay intact."""
from io import BytesIO
from local_files import publish_copy
import hashlib
import math
from pathlib import Path
import re
import shutil
import tempfile
import warnings

from PIL import Image, ImageOps
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, NumberObject
from search_tasks import run_search_worker

MAX_IMAGES = 100
MAX_PAGES = 100
MAX_SOURCE_BYTES = 64 * 1024**2
MAX_TOTAL_BYTES = 256 * 1024**2
MAX_IMAGE_PIXELS = 45_000_000
MAX_TOTAL_PIXELS = 150_000_000
MAX_OUTPUT_BYTES = 128 * 1024**2
SUPPORTED_FORMATS = frozenset({'PNG','JPEG','BMP','WEBP','TIFF'})


def _require(value, message):
    if not value:
        raise ValueError(message)


def _sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def validate_request(request):
    _require(isinstance(request, dict) and set(request) == {'paths', 'dpi'}, 'Pedido de criação inválido.')
    paths, dpi = request['paths'], request['dpi']
    _require(type(dpi) is int and 72 <= dpi <= 600, 'A resolução deve ser um inteiro de 72 a 600 DPI.')
    _require(isinstance(paths, list) and 1 <= len(paths) <= MAX_IMAGES,
             f'Escolha de 1 a {MAX_IMAGES} arquivos PNG/JPEG/BMP/WebP/TIFF.')
    _require(all(isinstance(p, str) and p and '\x00' not in p for p in paths), 'Caminho de imagem inválido.')
    resolved = [Path(p).resolve() for p in paths]
    _require(len(set(resolved)) == len(resolved), 'Remova as imagens repetidas da lista.')
    return resolved, dpi


def _tiff_page_count(data, limit):
    """Bound the main IFD chain before Pillow decodes any frame.

    This checks directory structure/count only. Pillow remains responsible for
    tag values, compression and image decoding; no recursive SubIFD traversal.
    """
    _require(len(data) >= 8 and data[:2] in (b'II', b'MM'), 'Cabeçalho TIFF inválido.')
    order = 'little' if data[:2] == b'II' else 'big'
    def uint(offset, width):
        _require(0 <= offset <= len(data) - width, 'Diretório TIFF truncado ou fora do arquivo.')
        return int.from_bytes(data[offset:offset+width], order)
    version = uint(2, 2)
    if version == 42:
        count_size, entry_size, pointer_size, minimum = 2, 12, 4, 8
        offset = uint(4, 4)
    elif version == 43:
        _require(uint(4, 2) == 8 and uint(6, 2) == 0, 'Cabeçalho BigTIFF não suportado.')
        count_size, entry_size, pointer_size, minimum = 8, 20, 8, 16
        offset = uint(8, 8)
    else:
        raise ValueError('Versão TIFF não suportada.')
    seen = set()
    while offset:
        _require(len(seen) < limit, f'O PDF pode ter no máximo {MAX_PAGES} páginas, somando todos os arquivos.')
        _require(offset >= minimum and offset not in seen, 'Encadeamento de páginas TIFF inválido ou cíclico.')
        seen.add(offset)
        count = uint(offset, count_size)
        _require(count > 0, 'Diretório TIFF sem imagem.')
        offset = uint(offset + count_size + count * entry_size, pointer_size)
    _require(seen, 'O TIFF não contém páginas.')
    return len(seen)


def _image_page(writer, rgb, dpi):
    width, height = rgb.size
    points = (width * 72 / dpi, height * 72 / dpi)
    page = writer.add_blank_page(*points)
    raw = DecodedStreamObject()
    raw.set_data(rgb.tobytes())
    image = raw.flate_encode()
    image.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Image'),
                  NameObject('/Width'): NumberObject(width), NameObject('/Height'): NumberObject(height),
                  NameObject('/ColorSpace'): NameObject('/DeviceRGB'), NameObject('/BitsPerComponent'): NumberObject(8)})
    from pypdf.generic import DictionaryObject
    page[NameObject('/Resources')] = DictionaryObject({NameObject('/XObject'): DictionaryObject({
        NameObject('/Im1'): writer._add_object(image)})})
    content = DecodedStreamObject()
    content.set_data(f'q {points[0]:.9f} 0 0 {points[1]:.9f} 0 0 cm /Im1 Do Q\n'.encode('ascii'))
    page[NameObject('/Contents')] = writer._add_object(content)
    return points


def create_pdf_from_images(destination, request):
    paths, dpi = validate_request(request)
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    destination = destination.resolve()
    _require(destination.suffix.lower() == '.pdf', 'O destino deve ter extensão .pdf.')
    _require(destination.parent.is_dir(), 'A pasta de destino deve existir.')
    _require(destination not in paths, 'O destino não pode ser uma imagem fonte.')
    writer = PdfWriter()
    writer.add_metadata({'/Title': 'PDF criado de imagens', '/Creator': 'Linuxit PDF'})
    sources, identities, total_bytes, total_pixels = [], [], 0, 0
    temporary, created = None, False
    try:
        for source_number, path in enumerate(paths, 1):
            _require(path.is_file(), 'Uma imagem selecionada não está disponível.')
            _require(path.stat().st_size <= MAX_SOURCE_BYTES, 'Uma imagem excede o limite de 64 MiB.')
            with path.open('rb') as stream:
                data = stream.read(MAX_SOURCE_BYTES + 1)
            _require(len(data) <= MAX_SOURCE_BYTES, 'Uma imagem excede o limite de 64 MiB.')
            total_bytes += len(data)
            _require(total_bytes <= MAX_TOTAL_BYTES, 'As imagens excedem o limite total de 256 MiB.')
            identity = hashlib.sha256(data).hexdigest()
            identities.append((path, identity))
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('error', Image.DecompressionBombWarning)
                    with Image.open(BytesIO(data)) as source:
                        format_ = source.format
                        _require(format_ in SUPPORTED_FORMATS, 'Formato não suportado; use PNG, JPEG, BMP, WebP ou TIFF.')
                        if format_ == 'TIFF':
                            frames = _tiff_page_count(data, MAX_PAGES - len(sources))
                        else:
                            frames = getattr(source, 'n_frames', 1)
                            _require(frames == 1, 'Imagens animadas ou com múltiplos quadros não TIFF não são suportadas.')
                        _require(len(sources) + frames <= MAX_PAGES, f'O PDF pode ter no máximo {MAX_PAGES} páginas, somando todos os arquivos.')
                        for frame in range(frames):
                            source.seek(frame)
                            pixels = source.width * source.height
                            _require(0 < pixels <= MAX_IMAGE_PIXELS, 'Uma página de imagem excede o limite de 45 megapixels.')
                            total_pixels += pixels
                            _require(total_pixels <= MAX_TOTAL_PIXELS, 'As imagens excedem o limite total de 150 megapixels.')
                            source.load()
                            with ImageOps.exif_transpose(source) as oriented:
                                with oriented.convert('RGBA') as rgba, Image.new('RGB', oriented.size, 'white') as rgb:
                                    with rgba.getchannel('A') as alpha:
                                        rgb.paste(rgba, mask=alpha)
                                    points = _image_page(writer, rgb, dpi)
                                    sources.append({'path': str(path), 'sha256': identity,
                                                    'format': format_, 'pixels': list(rgb.size),
                                                    'page_points': list(points), 'input': source_number,
                                                    'frame': frame + 1, 'frame_count': frames})
            except (OSError, EOFError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
                raise ValueError('Não foi possível decodificar uma imagem válida dentro dos formatos e limites suportados.') from exc
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-images-', suffix='.pdf', delete=False) as stream:
            temporary = Path(stream.name)
            writer.write(stream)
        _require(temporary.stat().st_size <= MAX_OUTPUT_BYTES, 'O PDF gerado excede o limite de 128 MiB.')
        with temporary.open('rb') as stream:
            reader = PdfReader(stream, strict=True)
            _require(len(reader.pages) == len(sources) and not reader.is_encrypted, 'O PDF gerado não preservou as páginas esperadas.')
            for page, source in zip(reader.pages, sources):
                _require(all(math.isclose(float(v), expected, abs_tol=1e-5) for v, expected in
                             zip((page.mediabox.width, page.mediabox.height), source['page_points'])), 'Dimensões inválidas no PDF gerado.')
        def unchanged():
            for path, identity in identities:
                _require(_sha(path) == identity, 'Uma imagem mudou durante a criação. Selecione as fontes novamente.')
        unchanged()
        publish_copy(temporary,destination,unchanged)
        created = True
        return {'schema': 'linuxit-image-pdf-result-v1', 'path': str(destination), 'pages': len(sources),
                'input_count': len(paths),
                'dpi': dpi, 'sources': sources, 'output_sha256': _sha(destination)}
    except BaseException:
        if created:
            destination.unlink(missing_ok=True)
        raise
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def invoke_image_creation(destination, request, cancel=None, timeout=120):
    paths, dpi = validate_request(request)
    result = run_search_worker('images-to-pdf', destination, request, cancel, timeout)
    if result is None:
        return None
    try:
        _require(result['schema'] == 'linuxit-image-pdf-result-v1' and result['dpi'] == dpi
                 and type(result['pages']) is int and 1 <= result['pages'] <= MAX_PAGES
                 and type(result['input_count']) is int and result['input_count'] == len(paths)
                 and Path(result['path']).resolve() == Path(destination).resolve()
                 and re.fullmatch('[0-9a-f]{64}', result['output_sha256'])
                 and isinstance(result['sources'], list) and len(result['sources']) == result['pages'],
                 'Incomplete image creation result')
        rows, cursor, total_pixels = result['sources'], 0, 0
        for number, path in enumerate(paths, 1):
            first = rows[cursor]
            count, format_, identity = first['frame_count'], first['format'], first['sha256']
            _require(type(count) is int and 1 <= count <= MAX_PAGES and cursor + count <= len(rows)
                     and format_ in SUPPORTED_FORMATS and (count == 1 or format_ == 'TIFF')
                     and re.fullmatch('[0-9a-f]{64}', identity), 'Invalid image frame inventory')
            for frame, row in enumerate(rows[cursor:cursor+count], 1):
                _require(Path(row['path']).resolve() == path and row['sha256'] == identity
                         and type(row['input']) is int and row['input'] == number
                         and type(row['frame']) is int and row['frame'] == frame
                         and type(row['frame_count']) is int and row['frame_count'] == count
                         and row['format'] == format_, 'Invalid image frame order')
                pixels, points = row['pixels'], row['page_points']
                _require(isinstance(pixels, list) and len(pixels) == 2
                         and all(type(v) is int and v > 0 for v in pixels)
                         and pixels[0] * pixels[1] <= MAX_IMAGE_PIXELS
                         and isinstance(points, list) and len(points) == 2
                         and all(type(v) in (int, float) and math.isfinite(v) and v > 0 for v in points)
                         and all(math.isclose(v, px * 72 / dpi, abs_tol=1e-5) for v, px in zip(points, pixels)),
                         'Invalid image frame dimensions')
                total_pixels += pixels[0] * pixels[1]
            cursor += count
        _require(cursor == len(rows) and total_pixels <= MAX_TOTAL_PIXELS, 'Incomplete image source inventory')
        return result
    except (IndexError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError('O worker não retornou uma confirmação de criação válida.') from exc
