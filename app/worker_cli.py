#!/usr/bin/env python3
import json
try:
    import resource
except ImportError:  # Windows has no POSIX resource module.
    resource = None
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from imposition import prepare_output
from rendering import document_info


def _rasterize_pdf_in_place(path, dpi):
    try:
        from PIL import Image
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError('Imprimir como imagem requer o pacote python3-pil.') from exc
    dpi = max(72, min(600, int(dpi)))
    with tempfile.TemporaryDirectory(prefix='winux-raster-') as td:
        # Render and encode one page at a time. The former all-pages list could
        # retain multiple gigabytes of decoded pixels for large print jobs.
        from rendering import document_info
        info = document_info(path)
        page_count = int(info['pages'])
        for w, h in info['sizes']:
            if w * h * (dpi / 72) ** 2 > 45_000_000:
                raise RuntimeError('Imprimir como imagem excede o limite de 45 MP por página.')
        page_pdfs = []
        for page_no in range(1, page_count + 1):
            prefix = os.path.join(td, f'page-{page_no:06d}')
            proc = subprocess.run(
                ['pdftocairo', '-f', str(page_no), '-l', str(page_no), '-singlefile',
                 '-png', '-r', str(dpi), path, prefix],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr.strip() or f'Falha ao rasterizar a página {page_no}.')
            png = prefix + '.png'
            if not os.path.isfile(png):
                raise RuntimeError(f'A rasterização da página {page_no} não gerou imagem.')
            page_pdf = prefix + '.pdf'
            with Image.open(png) as source:
                image = source.convert('RGB')
                image.save(page_pdf, 'PDF', resolution=float(dpi))
                image.close()
            page_pdfs.append(page_pdf)
            os.unlink(png)
        temp_pdf = str(Path(path).with_suffix('.raster.pdf'))
        try:
            os.unlink(temp_pdf)
        except FileNotFoundError:
            pass
        if len(page_pdfs) == 1:
            os.replace(page_pdfs[0], temp_pdf)
        elif page_pdfs:
            proc = subprocess.run(['pdfunite', *page_pdfs, temp_pdf],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, timeout=600)
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr.strip() or 'Falha ao juntar as páginas rasterizadas.')
        else:
            raise RuntimeError('O documento não contém páginas para rasterizar.')
        os.replace(temp_pdf, path)


def main(argv):
    # Bound untrusted PDF parsing/imposition CPU and memory in the worker.
    for limit, amount in (() if resource is None else
                          ((resource.RLIMIT_AS, 2 * 1024**3), (resource.RLIMIT_CPU, 540))):
        try:
            soft, hard = resource.getrlimit(limit)
            resource.setrlimit(limit, (min(soft, amount) if soft != resource.RLIM_INFINITY else amount,
                                       min(hard, amount) if hard != resource.RLIM_INFINITY else amount))
        except (OSError, ValueError):
            pass
    if len(argv) < 3:
        raise SystemExit(2)
    cmd = argv[1]
    if cmd == 'signature-info':
        from pdf_signatures import inspect_pdf_signatures
        raw = sys.stdin.buffer.read(16385)
        if len(raw) > 16384:raise ValueError('Pedido de assinaturas acima do limite.')
        print(json.dumps(inspect_pdf_signatures(argv[2],json.loads(raw)),ensure_ascii=True))
        return
    if cmd in {'security-info', 'protect-copy', 'accessible-text', 'owner-copy'}:
        # Never emit a traceback or library exception containing a password.
        from pdf_security import inspect_pdf_security, protect_pdf_copy, extract_accessible_text, unprotect_owner_copy, SecurityError
        try:
            raw = sys.stdin.buffer.read(16385)
            if len(raw) > 16384:raise SecurityError('Pedido de segurança acima do limite.')
            action = {'security-info':inspect_pdf_security, 'protect-copy':protect_pdf_copy, 'accessible-text':extract_accessible_text, 'owner-copy':unprotect_owner_copy}[cmd]
            result = action(argv[2], json.loads(raw))
        except SecurityError as exc:
            print('ValueError: ' + str(exc), file=sys.stderr);raise SystemExit(1) from None
        except Exception:
            print('ValueError: Não foi possível concluir a operação de segurança.', file=sys.stderr);raise SystemExit(1) from None
        print(json.dumps(result, ensure_ascii=True))
        return
    if cmd == 'images-to-pdf':
        from pdf_creation import create_pdf_from_images
        raw = sys.stdin.buffer.read(256 * 1024 + 1)
        if len(raw) > 256 * 1024:
            raise ValueError('Pedido de criação acima de 256 KiB.')
        print(json.dumps(create_pdf_from_images(argv[2], json.loads(raw)), ensure_ascii=True))
        return
    if cmd == 'info':
        info = document_info(argv[2])
        print(json.dumps(info, ensure_ascii=False))
        return
    if cmd == 'panels':
        from pdf_panels import inspect_document_panels
        print(json.dumps(inspect_document_panels(argv[2]), ensure_ascii=False))
        return
    if cmd in {'index-build', 'index-search'}:
        from collection_index import build_index, search_index
        raw = sys.stdin.buffer.read(256 * 1024 + 1)
        if len(raw) > 256 * 1024:
            raise ValueError('Pedido de coleção acima de 256 KiB.')
        action = build_index if cmd == 'index-build' else search_index
        print(json.dumps(action(argv[2], json.loads(raw)), ensure_ascii=True))
        return
    if cmd == 'search-attachments':
        from attachment_search import search_attachment_text
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536:
            raise ValueError('Pedido de busca acima de 64 KiB.')
        print(json.dumps(search_attachment_text(argv[2], json.loads(raw)), ensure_ascii=True))
        return
    if cmd == 'edit-info':
        from pdf_changes import inspect_editable_document
        print(json.dumps(inspect_editable_document(argv[2]), ensure_ascii=True))
        return
    if cmd == 'copy-edit':
        if len(argv) != 4:
            raise SystemExit(2)
        from pdf_changes import save_edited_copy
        raw = sys.stdin.buffer.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError('O pedido de alterações excede 1 MiB.')
        request = json.loads(raw.decode('utf-8'))
        if not isinstance(request, dict) or set(request) != {'source_sha256', 'operations'}:
            raise ValueError('Pedido de alterações inválido.')
        print(json.dumps(save_edited_copy(argv[2], argv[3], **request), ensure_ascii=True))
        return
    if cmd == 'attachments':
        from pdf_attachments import list_attachments
        print(json.dumps(list_attachments(argv[2]), ensure_ascii=True))
        return
    if cmd == 'extract-attachment':
        if len(argv) != 4:
            raise SystemExit(2)
        from pdf_attachments import extract_attachment
        try:
            request = json.load(sys.stdin)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RuntimeError('Opções de extração inválidas.') from exc
        if not isinstance(request, dict):
            raise ValueError('A extração requer um objeto JSON com index e source_sha256.')
        result = extract_attachment(argv[2], request.get('index'), argv[3],
                                    source_sha256=request.get('source_sha256'))
        print(json.dumps(result, ensure_ascii=True))
        return
    if cmd == 'prepare':
        if len(argv) < 4:
            raise SystemExit(2)
        input_path, output_path = argv[2], argv[3]
        try:
            job = json.load(sys.stdin)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RuntimeError('Opções de impressão inválidas.') from exc
        prepare_output(input_path, output_path, job)
        if job.get('print_as_image'):
            _rasterize_pdf_in_place(output_path, job.get('image_dpi', 300))
        print(output_path)
        return
    raise SystemExit(2)


if __name__ == '__main__':
    main(sys.argv)
