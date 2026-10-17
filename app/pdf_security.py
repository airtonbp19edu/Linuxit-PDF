"""Own bounded authentication, AES-R6 copies and owner-authorized decryption."""
import os
from pathlib import Path
import re
import shutil
import tempfile

from pdf_changes import _editable, _sha, _inherited
from pdf_dependency import configure_pdf_library
configure_pdf_library()
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions as Permissions
from pypdf.errors import DependencyError
from search_tasks import run_search_worker

MAX_SOURCE_BYTES = 64 * 1024**2
MAX_OUTPUT_BYTES = 128 * 1024**2
MAX_PAGES = 1000
PERMISSION_FLAGS = {
    'print': ('print', 'print_to_representation'), 'copy': ('extract',),
    'modify': ('modify',), 'annotate': ('add_or_modify',),
    'fill_forms': ('fill_form_fields',), 'assemble': ('assemble_doc',),
}


class SecurityError(ValueError):
    """Only fixed, non-secret messages may cross the worker error channel."""


def _require(value, message):
    if not value:
        raise SecurityError(message)


def _source(path):
    path = Path(path).resolve()
    _require(path.is_file() and path.stat().st_size <= MAX_SOURCE_BYTES, 'Selecione um PDF disponível de até 64 MiB.')
    return path


def _password(value, creating=False):
    # Bound to printable ASCII so AES-R6 SASLprep never silently changes a new password.
    limit = (8, 64) if creating else (0, 127)
    _require(isinstance(value, str) and limit[0] <= len(value) <= limit[1]
             and (not creating or all(32 <= ord(c) <= 126 for c in value))
             and (not creating or bool(value.strip())),
             'Novas senhas devem ter 8–64 caracteres ASCII imprimíveis; a senha de inspeção aceita até 127 caracteres.')
    return value


def permission_bits(values):
    _require(isinstance(values, dict) and set(values) == set(PERMISSION_FLAGS)
             and all(type(v) is bool for v in values.values()), 'Opções de permissões inválidas.')
    flags = {'extract_text_and_graphics': True}  # Accessibility extraction is not disabled.
    for name, bits in PERMISSION_FLAGS.items():
        for bit in bits:flags[bit] = values[name]
    return Permissions.from_dict(flags)


def _permissions(number):
    flags = Permissions(int(number)).to_dict()
    return {name: all(flags[bit] for bit in bits) for name, bits in PERMISSION_FLAGS.items()}


def inspect_pdf_security(path, request):
    _require(isinstance(request, dict) and set(request) == {'password'}, 'Pedido de inspeção inválido.')
    password = _password(request['password'])
    path = _source(path);identity = _sha(path)
    try:
        with path.open('rb') as stream:
            reader = PdfReader(stream, strict=True)
            encrypted = reader.is_encrypted
            info = reader.trailer['/Encrypt'] if encrypted else {}
            role = int(reader.decrypt(password)) if encrypted else 2
            pages = len(reader.pages) if role else None
            _require(pages is None or 1 <= pages <= MAX_PAGES, 'Inspeção limitada a PDFs com 1–1000 páginas.')
            result = {'schema': 'linuxit-security-info-v1', 'source_sha256': identity,
                      'encrypted': encrypted, 'authenticated': bool(role),
                      'role': {0: None, 1: 'user', 2: 'owner'}[role] if encrypted else 'unprotected',
                      'pages': pages, 'permissions': _permissions(info.get('/P', int(Permissions.all()))),
                      'encryption_version': int(info.get('/V', 0)), 'revision': int(info.get('/R', 0)),
                      'bits': int(info.get('/Length', 0))}
    except SecurityError:raise
    except Exception:
        raise SecurityError('Não foi possível inspecionar este PDF ou seu método de proteção.') from None
    _require(_sha(path) == identity, 'O PDF mudou durante a inspeção. Leia o arquivo novamente.')
    return result


def protect_pdf_copy(path, request):
    keys = {'destination', 'source_sha256', 'user_password', 'owner_password', 'permissions'}
    _require(isinstance(request, dict) and set(request) == keys, 'Pedido de proteção inválido.')
    user, owner = _password(request['user_password'], True), _password(request['owner_password'], True)
    _require(user != owner, 'Use senhas diferentes para abertura e proprietário.')
    flags = permission_bits(request['permissions'])
    _require(isinstance(request['source_sha256'], str) and re.fullmatch('[0-9a-f]{64}', request['source_sha256']), 'Identidade do PDF inválida.')
    _require(isinstance(request['destination'], str) and '\x00' not in request['destination'], 'Destino inválido.')
    path = _source(path);destination = Path(request['destination'])
    _require(destination.suffix.lower() == '.pdf' and destination.parent.is_dir(), 'Escolha um destino .pdf em uma pasta existente.')
    if destination.exists() or destination.is_symlink():
        raise SecurityError('Escolha um nome novo; nenhum arquivo existente será substituído.')
    destination = destination.resolve();temporary = None;created = False
    try:
        # Encrypted, signed, XFA and portfolio sources remain explicitly unsupported.
        with _editable(path, request['source_sha256']) as (reader, _, identity):
            _require(1 <= len(reader.pages) <= MAX_PAGES, 'Proteção limitada a PDFs com 1–1000 páginas.')
            writer = PdfWriter(clone_from=reader)
            writer.encrypt(user, owner, permissions_flag=flags, algorithm='AES-256')
            with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-protect-', suffix='.pdf', delete=False) as stream:
                temporary = Path(stream.name);writer.write(stream)
            _require(temporary.stat().st_size <= MAX_OUTPUT_BYTES, 'O PDF gerado excede o limite de 128 MiB.')
            with temporary.open('rb') as stream:
                check = PdfReader(stream, strict=True)
                entry = check.trailer['/Encrypt']
                _require(check.is_encrypted and (entry['/V'], entry['/R'], entry['/Length']) == (5, 6, 256)
                         and entry['/CF']['/StdCF']['/CFM'] == '/AESV3', 'A cópia não apresentou a criptografia AES-256 esperada.')
                _require(not check.decrypt('') and int(check.decrypt(user)) == 1
                         and int(check.decrypt(owner)) == 2, 'Não foi possível verificar os dois níveis de senha.')
                _require(len(check.pages) == len(reader.pages) and _permissions(entry['/P']) == request['permissions'],
                         'A cópia não preservou páginas ou permissões esperadas.')
        _require(_sha(path) == identity, 'O PDF mudou durante a preparação da cópia.')
        with temporary.open('rb') as source:
            fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600);created = True
            with os.fdopen(fd, 'wb') as output:shutil.copyfileobj(source, output, 65536)
        return {'schema': 'linuxit-protected-copy-v1', 'path': str(destination), 'source_sha256': identity,
                'output_sha256': _sha(destination), 'pages': len(writer.pages),
                'algorithm': 'AES-256', 'permissions': dict(request['permissions'])}
    except SecurityError:raise
    except FileExistsError:
        raise SecurityError('Escolha um nome novo; nenhum arquivo existente será substituído.') from None
    except NotImplementedError:
        raise SecurityError('A proteção de cópias não aceita fontes criptografadas, assinadas, XFA ou portfólios.') from None
    except DependencyError:
        raise SecurityError('A criação AES-256 requer a dependência cryptography do runtime.') from None
    except Exception:
        raise SecurityError('Não foi possível criar e verificar a cópia protegida.') from None
    finally:
        # Remove outputs only when a handled exception is propagating.
        import sys
        if sys.exc_info()[0] is not None and created:destination.unlink(missing_ok=True)
        if temporary is not None:temporary.unlink(missing_ok=True)


def extract_accessible_text(path, request):
    _require(isinstance(request, dict) and set(request) == {'page'} and type(request['page']) is int, 'Página de leitura inválida.')
    info = inspect_pdf_security(path, {'password':''})
    _require(not info['encrypted'], 'A leitura de texto acessível de PDFs criptografados ainda não é suportada.')
    _require(0 <= request['page'] < info['pages'], 'Página de leitura inválida.')
    from rendering import extract_page_text
    text = extract_page_text(str(path), request['page'])
    _require(len(text.encode('utf-8')) <= 1024**2, 'O texto desta página excede o limite de 1 MiB.')
    _require(_sha(path) == info['source_sha256'], 'O PDF mudou durante a leitura de texto.')
    text = ''.join(c for c in text if c in '\t\n\r' or ord(c) >= 32)
    return {'schema':'linuxit-accessible-text-v1','page':request['page'],'source_sha256':info['source_sha256'],'text':text}


def unprotect_owner_copy(path, request):
    _require(isinstance(request, dict) and set(request) == {'destination','source_sha256','owner_password'}, 'Pedido de cópia inválido.')
    password = _password(request['owner_password'])
    _require(isinstance(request['source_sha256'], str) and re.fullmatch('[0-9a-f]{64}', request['source_sha256']), 'Identidade do PDF inválida.')
    _require(isinstance(request['destination'], str) and '\x00' not in request['destination'], 'Destino inválido.')
    path = _source(path);identity = _sha(path)
    _require(identity == request['source_sha256'], 'O PDF mudou. Inspecione o arquivo novamente.')
    destination = Path(request['destination'])
    _require(destination.suffix.lower() == '.pdf' and destination.parent.is_dir(), 'Escolha um destino .pdf em uma pasta existente.')
    _require(not destination.exists() and not destination.is_symlink(), 'Escolha um nome novo; nenhum arquivo existente será substituído.')
    destination = destination.resolve();temporary = None;created = False
    try:
        with path.open('rb') as stream:
            reader = PdfReader(stream, strict=True)
            _require(reader.is_encrypted and int(reader.decrypt(password)) == 2, 'Esta operação exige autenticação com a senha de proprietário.')
            fields = reader.get_fields() or {};root = reader.root_object
            _require('/Perms' not in root and '/Collection' not in root
                     and not any(_inherited(f, '/FT') == '/Sig' for f in fields.values()),
                     'Cópias de documentos assinados, com restrições especiais ou portfólios não são suportadas.')
            form = root.get('/AcroForm')
            _require(form is None or '/XFA' not in form.get_object(), 'Cópias de formulários XFA não são suportadas.')
            _require(1 <= len(reader.pages) <= MAX_PAGES, 'Cópia limitada a PDFs com 1–1000 páginas.')
            writer = PdfWriter(clone_from=reader)
            with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.linuxit-protect-', suffix='.pdf', delete=False) as output:
                temporary = Path(output.name);writer.write(output)
            _require(temporary.stat().st_size <= MAX_OUTPUT_BYTES, 'O PDF gerado excede o limite de 128 MiB.')
            with temporary.open('rb') as output:
                check = PdfReader(output, strict=True)
                _require(not check.is_encrypted and len(check.pages) == len(reader.pages), 'Não foi possível verificar a cópia sem senha.')
        _require(_sha(path) == identity, 'O PDF mudou durante a preparação da cópia.')
        with temporary.open('rb') as source:
            fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600);created = True
            with os.fdopen(fd, 'wb') as output:shutil.copyfileobj(source, output, 65536)
        return {'schema':'linuxit-owner-copy-v1','source_sha256':identity,'path':str(destination),
                'output_sha256':_sha(destination),'pages':len(writer.pages),'algorithm':'none'}
    except SecurityError:raise
    except Exception:raise SecurityError('Não foi possível criar e verificar a cópia autorizada pelo proprietário.') from None
    finally:
        import sys
        if sys.exc_info()[0] is not None and created:destination.unlink(missing_ok=True)
        if temporary is not None:temporary.unlink(missing_ok=True)


def invoke_accessible_text(path, page, cancel=None):
    result = run_search_worker('accessible-text', path, {'page':page}, cancel)
    if result is None:return None
    try:
        if (result['schema'] != 'linuxit-accessible-text-v1' or result['page'] != page
                or not re.fullmatch('[0-9a-f]{64}', result['source_sha256'])
                or not isinstance(result['text'], str) or len(result['text'].encode('utf-8')) > 1024**2):raise ValueError()
        return result['text']
    except (KeyError, TypeError, ValueError):
        raise SecurityError('O worker não retornou um texto de página válido.') from None


def invoke_security(command, path, request, cancel=None, timeout=120):
    _require(command in {'security-info', 'protect-copy', 'owner-copy'}, 'Comando de segurança inválido.')
    result = run_search_worker(command, path, request, cancel, timeout)
    if result is None:return None
    try:
        schema = {'security-info':'linuxit-security-info-v1','protect-copy':'linuxit-protected-copy-v1','owner-copy':'linuxit-owner-copy-v1'}[command]
        if result['schema'] != schema or not re.fullmatch('[0-9a-f]{64}', result['source_sha256']):raise ValueError()
        if command == 'security-info':
            if type(result['authenticated']) is not bool or type(result['encrypted']) is not bool:raise ValueError()
        elif (result['source_sha256'] != request['source_sha256']
              or result['algorithm'] != ('AES-256' if command == 'protect-copy' else 'none')
              or (command == 'protect-copy' and result['permissions'] != request['permissions']) or result['pages'] < 1
              or Path(result['path']).resolve() != Path(request['destination']).resolve()
              or not re.fullmatch('[0-9a-f]{64}', result['output_sha256'])):raise ValueError()
        return result
    except (KeyError, TypeError, ValueError):
        raise SecurityError('O worker não retornou uma confirmação de segurança válida.') from None
