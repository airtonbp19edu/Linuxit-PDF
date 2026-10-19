"""Authorized encrypted edits preserve the existing encryption and permissions."""
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf.constants import UserAccessPermissions as Permissions


def edit_auth(request):
    if request is None:return None,False
    if (not isinstance(request,dict) or set(request)!={'password','recover'}
            or request['password'] is not None and (not isinstance(request['password'],str) or len(request['password'])>127)
            or type(request['recover']) is not bool):
        raise ValueError('Autorização de edição inválida.')
    return request['password'],request['recover']


def permissions(reader):
    if not reader.is_encrypted or getattr(reader,'_linuxit_owner',False):
        return dict(modify=True,annotate=True,fill_forms=True,assemble=True)
    flags=Permissions(int(reader.trailer['/Encrypt'].get('/P',0))).to_dict()
    return dict(modify=bool(flags.get('modify')),annotate=bool(flags.get('add_or_modify')),
                fill_forms=bool(flags.get('fill_form_fields') or flags.get('add_or_modify')),
                assemble=bool(flags.get('assemble_doc') or flags.get('modify')))


def authorize_operations(reader,operations):
    allowed=permissions(reader)
    for operation in operations:
        if not isinstance(operation,dict):raise ValueError('Alteração inválida.')
        kind=operation.get('kind','')
        if kind in ('fill-text-fields','fill-form-controls','fill-form-events'):permission='fill_forms'
        elif kind=='rotate-page':permission='assemble'
        elif kind in ('add-bookmark','rename-bookmark','move-bookmark','delete-bookmark'):permission='modify'
        else:permission='annotate'
        if not allowed[permission]:raise ValueError('A permissão do PDF não autoriza este tipo de alteração.')


def preserve_encryption(writer,reader):
    if not reader.is_encrypted:return
    # Adapter for the pinned pypdf6.20.1 writer contract. _encrypt_entry must be
    # the dictionary, so it is excluded from encryption itself during writing.
    # Existing /O /U /OE /UE /Perms and file ID retain both password identities.
    writer._encryption=reader._encryption
    entry=reader.trailer['/Encrypt'].clone(writer)
    writer._add_object(entry);writer._encrypt_entry=entry
    writer._ID=reader.trailer['/ID'].clone(writer)
