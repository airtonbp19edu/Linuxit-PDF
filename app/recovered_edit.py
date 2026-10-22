"""Normalize a consented damaged source before editing a new copy."""
from io import BytesIO
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def reader_for_edit(stream, recover):
    if not recover:
        return PdfReader(stream, strict=True)
    from document_session import MAX_BYTES, _rebuilt, _check_pages, _normalise_page_tree
    stream.seek(0)
    data=stream.read(MAX_BYTES+1)
    if not 0<len(data)<=MAX_BYTES:
        raise ValueError('A recuperação para edição aceita PDF de até256MiB.')
    reader=None
    for candidate in (data,*_rebuilt(data)):
        try:
            possible=PdfReader(BytesIO(candidate),strict=False)
            possible.root_object
            reader=possible;break
        except (PdfReadError,ValueError,KeyError):
            continue
    if reader is None:
        raise ValueError('Não foi possível reconstruir o PDF para editar uma cópia.')
    # Authentication/permission checks stay in the original edit path.
    if reader.is_encrypted:
        return reader
    _check_pages(reader,repair=True)
    writer=PdfWriter(clone_from=reader)
    _normalise_page_tree(writer)
    output=BytesIO();writer.write(output)
    normalized=PdfReader(BytesIO(output.getvalue()),strict=True)
    _check_pages(normalized,repair=False)
    return normalized
