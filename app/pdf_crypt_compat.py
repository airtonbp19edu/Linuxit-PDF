"""Honour /EncryptMetadata false in the pinned pypdf (E18).

With the Standard security handler, V4/V5 documents may leave metadata streams
(/Type /Metadata) in clear and mark them with the Identity crypt filter (PDF 2.0,
7.6.5 and 7.6.6). The pinned pypdf decrypts such streams anyway (garbling them)
and cannot decode the /Crypt filter. This adapter, installed once by
pdf_dependency.configure_pdf_library:

- reading: leaves those streams undecrypted and drops the Identity /Crypt
  filter from the in-memory object, so their bytes are the clear XMP;
- writing with a preserved encryption dictionary: writes them in clear again,
  with the Identity crypt filter first in the filter chain.

Documents whose encryption dictionary does not say /EncryptMetadata false are
not affected.
"""
import copy

_INSTALLED = False


def _clear_metadata(encryption, obj):
    from pypdf.generic import StreamObject
    return (getattr(encryption, 'EncryptMetadata', True) is False and isinstance(obj, StreamObject)
            and obj.get('/Type') == '/Metadata')


def _without_identity_filter(obj):
    from pypdf.generic import ArrayObject, NameObject
    filters, params = obj.get('/Filter'), obj.get('/DecodeParms')
    if filters is None:return
    filters = filters.get_object()
    params = params.get_object() if params is not None else None
    if filters == '/Crypt':
        obj.pop('/Filter', None);obj.pop('/DecodeParms', None)
        if hasattr(obj, 'decoded_self'):
            # pypdf decodes an encoded stream only through its filters; with none left the raw bytes are the data.
            from pypdf.generic import DecodedStreamObject
            decoded = DecodedStreamObject();decoded.set_data(obj._data)
            for key, value in obj.items():
                if key != '/Length':decoded[key] = value
            obj.decoded_self = decoded
        return
    if isinstance(filters, list) and filters and filters[0] == '/Crypt':
        rest = ArrayObject(filters[1:]);obj[NameObject('/Filter')] = rest if len(rest) != 1 else rest[0]
        if isinstance(params, list) and params:
            more = ArrayObject(params[1:])
            if any(p is not None and getattr(p, 'get_object', lambda: p)() is not None for p in more):
                obj[NameObject('/DecodeParms')] = more if len(more) != 1 else more[0]
            else:obj.pop('/DecodeParms', None)


def _with_identity_filter(obj):
    from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NullObject
    identity = DictionaryObject({NameObject('/Type'): NameObject('/CryptFilterDecodeParms'), NameObject('/Name'): NameObject('/Identity')})
    filters, params = obj.get('/Filter'), obj.get('/DecodeParms')
    if filters is None:
        obj[NameObject('/Filter')] = NameObject('/Crypt');obj[NameObject('/DecodeParms')] = identity;return obj
    filters = filters.get_object();params = params.get_object() if params is not None else None
    names = list(filters) if isinstance(filters, list) else [filters]
    if names and names[0] == '/Crypt':return obj
    values = list(params) if isinstance(params, list) else [params if params is not None else NullObject()] * 1
    values += [NullObject()] * (len(names) - len(values))
    obj[NameObject('/Filter')] = ArrayObject([NameObject('/Crypt')] + names)
    obj[NameObject('/DecodeParms')] = ArrayObject([identity] + values)
    return obj


def install():
    global _INSTALLED
    if _INSTALLED:return
    from pypdf._encryption import Encryption
    decrypt, encrypt = Encryption.decrypt_object, Encryption.encrypt_object

    def decrypt_object(self, obj, idnum, generation, *args, **kwargs):
        if _clear_metadata(self, obj):
            _without_identity_filter(obj);return obj
        return decrypt(self, obj, idnum, generation, *args, **kwargs)

    def encrypt_object(self, obj, idnum, generation):
        if _clear_metadata(self, obj):
            return _with_identity_filter(copy.copy(obj))
        return encrypt(self, obj, idnum, generation)

    Encryption.decrypt_object, Encryption.encrypt_object = decrypt_object, encrypt_object
    _INSTALLED = True
