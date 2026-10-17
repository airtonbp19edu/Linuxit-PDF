"""Own bounded PNG/JPEG to RGB PDF creation, with no source modification."""
from io import BytesIO
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
MAX_SOURCE_BYTES = 64 * 1024**2
MAX_TOTAL_BYTES = 256 * 1024**2
MAX_IMAGE_PIXELS = 45_000_000
MAX_TOTAL_PIXELS = 150_000_000
MAX_OUTPUT_BYTES = 128 * 1024**2


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
             f'Escolha de 1 a {MAX_IMAGES} imagens PNG/JPEG.')
    _require(all(isinstance(p, str) and p and '\x00' not in p for p in paths), 'Caminho de imagem inválido.')
    resolved = [Path(p).resolve() for p in paths]
    _require(len(set(resolved)) == len(resolved), 'Remova as imagens repetidas da lista.')
    return resolved, dpi


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
    sources, total_bytes, total_pixels = [], 0, 0
    temporary, created = None, False
    try:
        for path in paths:
            _require(path.is_file(), 'Uma imagem selecionada não está disponível.')
            _require(path.stat().st_size <= MAX_SOURCE_BYTES, 'Uma imagem excede o limite de 64 MiB.')
            with path.open('rb') as stream:
                data = stream.read(MAX_SOURCE_BYTES + 1)
            _require(len(data) <= MAX_SOURCE_BYTES, 'Uma imagem excede o limite de 64 MiB.')
            total_bytes += len(data)
            _require(total_bytes <= MAX_TOTAL_BYTES, 'As imagens excedem o limite total de 256 MiB.')
            identity = hashlib.sha256(data).hexdigest()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('error', Image.DecompressionBombWarning)
                    with Image.open(BytesIO(data)) as source:
                        _require(source.format in {'PNG', 'JPEG'}, 'Somente imagens PNG e JPEG são suportadas.')
                        _require(getattr(source, 'n_frames', 1) == 1, 'Imagens animadas ou com múltiplos quadros não são suportadas.')
                        pixels = source.width * source.height
                        _require(0 < pixels <= MAX_IMAGE_PIXELS, 'Uma imagem excede o limite de 45 megapixels.')
                        total_pixels += pixels
                        _require(total_pixels <= MAX_TOTAL_PIXELS, 'As imagens excedem o limite total de 150 megapixels.')
                        source.load()
                        with ImageOps.exif_transpose(source) as oriented:
                            with oriented.convert('RGBA') as rgba, Image.new('RGB', oriented.size, 'white') as rgb:
                                with rgba.getchannel('A') as alpha:
                                    rgb.paste(rgba, mask=alpha)
                                points = _image_page(writer, rgb, dpi)
                                sources.append({'path': str(path), 'sha256': identity,
                                                'format': source.format, 'pixels': list(rgb.size),
                                                'page_points': list(points)})
            except (OSError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
                raise ValueError('Não foi possível decodificar uma imagem PNG/JPEG válida dentro dos limites.') from exc
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-images-', suffix='.pdf', delete=False) as stream:
            temporary = Path(stream.name)
            writer.write(stream)
        _require(temporary.stat().st_size <= MAX_OUTPUT_BYTES, 'O PDF gerado excede o limite de 128 MiB.')
        with temporary.open('rb') as stream:
            reader = PdfReader(stream, strict=True)
            _require(len(reader.pages) == len(paths) and not reader.is_encrypted, 'O PDF gerado não preservou as páginas esperadas.')
            for page, source in zip(reader.pages, sources):
                _require(all(math.isclose(float(v), expected, abs_tol=1e-5) for v, expected in
                             zip((page.mediabox.width, page.mediabox.height), source['page_points'])), 'Dimensões inválidas no PDF gerado.')
        for source in sources:
            _require(_sha(source['path']) == source['sha256'], 'Uma imagem mudou durante a criação. Selecione as fontes novamente.')
        with temporary.open('rb') as source, destination.open('xb') as output:
            created = True
            shutil.copyfileobj(source, output, 64 * 1024)
        return {'schema': 'linuxit-image-pdf-result-v1', 'path': str(destination), 'pages': len(paths),
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
        if (result['schema'] != 'linuxit-image-pdf-result-v1' or result['dpi'] != dpi
                or result['pages'] != len(paths) or Path(result['path']).resolve() != Path(destination).resolve()
                or not re.fullmatch('[0-9a-f]{64}', result['output_sha256'])
                or [Path(s['path']).resolve() for s in result['sources']] != paths
                or any(not re.fullmatch('[0-9a-f]{64}', s['sha256']) for s in result['sources'])):
            raise ValueError('Incomplete image creation result')
        return result
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError('O worker não retornou uma confirmação de criação válida.') from exc
