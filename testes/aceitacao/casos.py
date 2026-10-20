"""Executable own acceptance cases S12 (no display needed).

Each case follows the given/when/expected text of docs/especificacao-funcional.json
through a public boundary of the application: the worker command line used by
the interface, or the module the interface calls directly. A passing case is an
own-contract result for one revision; it is never a Foxit observation.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CASES = {}


def case(case_id, boundary):
    def register(function):
        CASES[case_id] = dict(function=function, boundary=boundary, needs_display=False)
        return function
    return register


class Failed(AssertionError):
    pass


def check(condition, message):
    if not condition:
        raise Failed(message)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Context:
    """Per-case work folder, fixture identity records and worker invocation."""

    def __init__(self, repository, app, work):
        self.repository, self.app, self.work = Path(repository), Path(app), Path(work)
        self.fixtures = {}

    def fixture(self, relative):
        path = self.repository / relative
        check(path.is_file(), 'Fixture ausente: ' + relative)
        self.fixtures[relative] = sha256(path)
        return path

    def copy(self, relative, name=None):
        target = self.work / (name or Path(relative).name)
        shutil.copyfile(self.fixture(relative), target)
        return target

    def unchanged(self):
        return {name: sha256(self.repository / name) == digest for name, digest in self.fixtures.items()}

    def worker(self, command, *args, request=None):
        process = subprocess.run([sys.executable, str(self.app / 'worker_cli.py'), command, *map(str, args)],
                                 input=b'' if request is None else json.dumps(request).encode('utf-8'),
                                 capture_output=True, timeout=300, cwd=str(self.work),
                                 env={**os.environ, 'PYTHONUTF8': '1'})
        result = None
        if process.returncode == 0 and process.stdout.strip():
            text = process.stdout.decode('utf-8').strip().splitlines()[-1]
            try:result = json.loads(text)
            except ValueError:result = text
        return dict(code=process.returncode, result=result, stderr=process.stderr.decode('utf-8', 'replace')[-600:])


SCOPES = 'testes/fixtures/busca-escopos.pdf'
ADVANCED = 'testes/fixtures/busca-avancada/'
OWN = 'testes/aceitacao/fixtures/'


def search_request(query, **changes):
    request = {'query': query, 'match_case': False, 'ignore_accents': False, 'whole_words': False,
               'mode': 'literal', 'proximity_distance': 0, 'max_hits': 5000}
    request.update(changes)
    return request


# 01 — open and render

@case('S12-01-1', 'worker info + rendering.render_page')
def open_and_render(ctx):
    from rendering import render_page
    path = ctx.fixture(SCOPES)
    info = ctx.worker('info', path)
    check(info['code'] == 0, 'info falhou: ' + info['stderr'])
    pages, sizes = info['result']['pages'], info['result']['sizes']
    check(pages == 2 and len(sizes) == 2 and all(w > 0 and h > 0 for w, h in sizes), f'páginas/tamanhos: {pages} {sizes}')
    other = ctx.work / 'outro.pdf'
    shutil.copyfile(ctx.fixture(OWN + 'oito-paginas.pdf'), other)
    cache = ctx.work / 'cache';cache.mkdir()
    images = [Path(render_page(str(path), index, 300, str(cache))) for index in range(2)]
    foreign = Path(render_page(str(other), 0, 300, str(cache)))
    digests = [sha256(p) for p in images]
    check(all(p.is_file() and p.stat().st_size > 0 for p in images), 'imagem de página ausente')
    check(len({*digests, sha256(foreign)}) == 3 and foreign not in images,
          'imagens de páginas/documentos diferentes coincidem no cache')
    return dict(pages=pages, sizes=sizes, page_image_sha256=digests, other_document_image_distinct=True)


@case('S12-01-2', 'worker info')
def open_invalid(ctx):
    missing = ctx.worker('info', ctx.work / 'nao-existe.pdf')
    invalid = ctx.worker('info', ctx.fixture('testes/fixtures/campaign18/invalido.pdf'))
    for label, run in (('inexistente', missing), ('inválido', invalid)):
        check(run['code'] != 0 and run['result'] is None, f'{label}: retornou página fictícia {run}')
    return dict(missing_exit=missing['code'], invalid_exit=invalid['code'])


# 04 — text search

@case('S12-04-1', 'search_engine.TextSearchIndex')
def text_search(ctx):
    from search_engine import TextSearchIndex
    index = TextSearchIndex(str(ctx.fixture(SCOPES)))
    plain, whole = index.search('alvo'), index.search('alvo', whole_words=True)
    check(len(plain) == 3, f'esperadas 3 ocorrências, obtidas {len(plain)}')
    check(len(whole) == 2, f'palavra inteira: esperadas 2, obtidas {len(whole)}')
    return dict(hits=len(plain), whole_word_hits=len(whole), pages=sorted({h['page'] for h in plain}))


@case('S12-04-2', 'search_engine.TextSearchIndex')
def text_search_limit(ctx):
    import search_engine
    index = search_engine.TextSearchIndex(str(ctx.fixture(SCOPES)))
    extracted = []
    original = search_engine.extract_page_words
    search_engine.extract_page_words = lambda *a, **k: extracted.append(a) or original(*a, **k)
    try:
        try:
            index.search('a' * 257)
            raised = False
        except ValueError:
            raised = True
    finally:
        search_engine.extract_page_words = original
    check(raised, 'consulta de 257 caracteres foi aceita')
    check(not extracted, 'páginas foram extraídas antes da recusa')
    return dict(value_error=True, pages_extracted=0)


# 06 — comments

@case('S12-06-1', 'search_engine.TextSearchIndex')
def comment_search(ctx):
    from search_engine import TextSearchIndex
    index = TextSearchIndex(str(ctx.fixture(SCOPES)))
    options = dict(include_page_text=False, include_comments=True)
    subject, target = index.search('assunto', **options), index.search('alvo', **options)
    check(len(subject) == 1 and len(target) == 1, f'assunto={len(subject)} alvo={len(target)}')
    check(all(h['source'] == 'comment' for h in subject + target), 'fonte diferente de comentário')
    from pdf_panels import inspect_document_panels
    note = inspect_document_panels(str(ctx.fixture(SCOPES)))['comments'][0]
    check(note['subject'] == 'Assunto separado' and note['contents'] == 'comentário alvo', 'assunto misturado ao conteúdo')
    return dict(subject_hits=1, contents_hits=1, subject=note['subject'], contents=note['contents'])


@case('S12-06-2', 'search_engine.TextSearchIndex')
def comment_author(ctx):
    from search_engine import TextSearchIndex
    hits = TextSearchIndex(str(ctx.fixture(SCOPES))).search('Autor', include_page_text=False, include_comments=True)
    check([(h['source'], h['page']) for h in hits] == [('comment', 0)], f'autor: {hits}')
    return dict(hits=[(h['source'], h['page'] + 1) for h in hits], page_numbering='um')


# 07 — attachments search

@case('S12-07-1', 'worker search-attachments')
def attachment_search(ctx):
    run = ctx.worker('search-attachments', ctx.fixture(ADVANCED + 'anexos.pdf'), request=search_request('alvo'))
    check(run['code'] == 0, run['stderr'])
    hits = run['result']['hits']
    check(hits and all(h['attachment_name'] == 'notas.txt' and h['attachment_index'] == 2 for h in hits), f'hits: {hits}')
    check(all(h['page'] is None and h['rects'] == [] for h in hits), 'destino principal fictício para hit de anexo')
    return dict(hits=len(hits), attachment=hits[0]['attachment_name'], index=hits[0]['attachment_index'],
                internal_page=hits[0]['attachment_page'], main_page=None)


@case('S12-07-2', 'worker search-attachments')
def attachment_search_omission(ctx):
    run = ctx.worker('search-attachments', ctx.fixture(ADVANCED + 'anexos.pdf'), request=search_request('alvo'))
    check(run['code'] == 0, run['stderr'])
    omitted = run['result']['omissions']
    check([o['name'] for o in omitted] == ['nao-suportado.bin'] and all(o['reason'] for o in omitted), f'omissões: {omitted}')
    check(run['result']['complete'] is False, 'resultado parcial anunciado como completo')
    return dict(omitted=omitted, complete=False)


# 08 — collection index

def _collection(ctx):
    first = ctx.copy(ADVANCED + 'colecao-um.pdf');second = ctx.copy(ADVANCED + 'colecao-dois.pdf')
    index = ctx.work / 'colecao.linuxit-index.json'
    run = ctx.worker('index-build', index, request={'paths': [str(first), str(second)]})
    check(run['code'] == 0, 'construção do índice falhou: ' + run['stderr'])
    return first, second, index, run['result']


@case('S12-08-1', 'worker index-build/index-search')
def collection_index(ctx):
    first, second, index, built = _collection(ctx)
    before = [sha256(first), sha256(second)]
    run = ctx.worker('index-search', index, request=search_request('target'))
    check(run['code'] == 0, run['stderr'])
    hits = [(Path(h['path']).name, h['page']) for h in run['result']['hits']]
    check(hits == [('colecao-dois.pdf', 0)], f'hits: {hits}')
    check([sha256(first), sha256(second)] == before, 'fontes alteradas pela indexação')
    return dict(documents=built['documents'], pages=built['pages'], hits=hits)


@case('S12-08-2', 'worker index-search')
def collection_stale(ctx):
    first, second, index, _ = _collection(ctx)
    second.write_bytes(first.read_bytes())
    run = ctx.worker('index-search', index, request=search_request('target'))
    check(run['code'] == 0, run['stderr'])
    stale = run['result']['stale']
    check(run['result']['hits'] == [], 'fonte alterada continuou nos resultados')
    check(len(stale) == 1 and Path(stale[0]['path'] if isinstance(stale[0], dict) else stale[0]).name == 'colecao-dois.pdf',
          f'fonte alterada não indicada: {stale}')
    return dict(hits=0, stale=len(stale))


# 09 — language modes

@case('S12-09-1', 'search_engine.TextSearchIndex')
def proximity(ctx):
    from search_engine import TextSearchIndex
    index = TextSearchIndex(str(ctx.fixture(OWN + 'proximidade.pdf')))
    near = lambda distance, query='alfa beta': len(index.search(query, mode='proximity', proximity_distance=distance))
    results = {'d1': near(1), 'd2': near(2), 'reverse_d50': near(50, 'beta alfa')}
    check(results == {'d1': 0, 'd2': 1, 'reverse_d50': 0}, f'proximidade: {results}')
    return results


@case('S12-09-2', 'search_engine.TextSearchIndex')
def wildcard_syntax(ctx):
    from search_engine import TextSearchIndex
    index = TextSearchIndex(str(ctx.fixture(SCOPES)))
    refused = {}
    for query, mode in (('alv[o]', 'wildcard'), ('alvo OR texto!', 'proximity')):
        try:
            hits = index.search(query, mode=mode)
            refused[query] = False
            check(False, f'{query!r} aceito em {mode}: {len(hits)} hits')
        except ValueError:
            refused[query] = True
    return dict(refused=refused, literal_fallback=False)


# 11 — print output

@case('S12-11-1', 'worker prepare-print')
def print_to_pdf(ctx):
    source = ctx.fixture(SCOPES);output = ctx.work / 'saida.pdf'
    run = ctx.worker('prepare-print', source, output, request={'print_mode': 'multiple', 'pages_per_sheet': 2})
    check(run['code'] == 0 and output.is_file(), 'preparação falhou: ' + run['stderr'])
    info = ctx.worker('info', output)['result']
    text = subprocess.run(['pdftotext', '-layout', str(output), '-'], capture_output=True, text=True).stdout
    check(info['pages'] == 1 and 'alvo' in text and 'outra' in text, f'plano N-up 2 não preservado: {info} {text[:120]!r}')
    return dict(output_pages=1, both_pages_on_sheet=True, physical_print=False)


@case('S12-11-2', 'cups_backend.print_file')
def print_without_lp(ctx):
    import cups_backend
    empty = ctx.work / 'sem-lp';empty.mkdir()
    previous = os.environ.get('PATH', '')
    os.environ['PATH'] = str(empty)
    try:
        try:
            cups_backend.print_file('fila-sintetica', str(ctx.fixture(SCOPES)), {'copies': 1})
            outcome = 'sent'
        except RuntimeError as exc:
            outcome = 'RuntimeError: ' + str(exc)
    finally:
        os.environ['PATH'] = previous
    check(outcome.startswith('RuntimeError'), 'envio sem lp reportado como sucesso')
    return dict(outcome=outcome)


# 12 — imposition

@case('S12-12-1', 'worker prepare-print (booklet)')
def booklet(ctx):
    from imposition import booklet_print_pairs
    source = ctx.fixture(OWN + 'oito-paginas.pdf');before = sha256(source);output = ctx.work / 'livreto.pdf'
    run = ctx.worker('prepare-print', source, output, request={'print_mode': 'booklet', 'booklet_sides': 'both'})
    check(run['code'] == 0, run['stderr'])
    faces = ctx.worker('info', output)['result']['pages']
    observed = []
    for page in range(1, faces + 1):
        text = subprocess.run(['pdftotext', '-layout', '-f', str(page), '-l', str(page), str(output), '-'],
                              capture_output=True, text=True).stdout.split()
        observed.append([int(word[4:]) for word in text if word.startswith('PAGE')])
    # (side, left, right) zero-based page indices; output words are one-based PAGEn labels.
    expected = [[left + 1, right + 1] for _side, left, right in booklet_print_pairs(list(range(8)), 'both')]
    check(faces == 4, f'faces: {faces}')
    check(observed == expected, f'ordem das duplas {observed} != {expected}')
    check(sha256(source) == before, 'original alterado')
    return dict(faces=faces, pairs=observed)


@case('S12-12-2', 'imposition.prepare_output')
def booklet_invalid(ctx):
    from imposition import prepare_output
    output = ctx.work / 'nao-criado.pdf'
    try:
        prepare_output(str(ctx.fixture(SCOPES)), str(output), {'print_mode': 'multiple', 'pages_per_sheet': 4.5})
        raised = False
    except ValueError:
        raised = True
    check(raised, 'pages_per_sheet=4.5 foi aceito')
    check(not output.exists(), 'saída criada apesar da recusa')
    return dict(value_error=True, output_created=False)


# 13/14 — panels

@case('S12-13-1', 'worker panels')
def bookmarks_panel(ctx):
    source = ctx.fixture(SCOPES);before = sha256(source)
    run = ctx.worker('panels', source)
    marks = [(b['title'], b['level'], b['page']) for b in run['result']['bookmarks']]
    check(marks == [('ALVO marcador', 0, 1), ('alvo externo', 0, None)], f'marcadores: {marks}')
    check(sha256(source) == before, 'PDF alterado pela inspeção')
    return dict(bookmarks=marks)


@case('S12-13-2', 'worker panels')
def bookmark_without_page(ctx):
    marks = ctx.worker('panels', ctx.fixture(SCOPES))['result']['bookmarks']
    external = [b for b in marks if b['title'] == 'alvo externo']
    check(len(external) == 1 and external[0]['page'] is None, f'destino atribuído: {external}')
    return dict(page=None)


@case('S12-14-1', 'worker panels')
def comment_fields(ctx):
    comments = ctx.worker('panels', ctx.fixture(SCOPES))['result']['comments']
    check(len(comments) == 1, f'comentários: {comments}')
    note = comments[0]
    fields = dict(page=note['page'], subject=note['subject'], contents=note['contents'], author=note['author'])
    check(fields == dict(page=0, subject='Assunto separado', contents='comentário alvo', author='Autor não pesquisável'),
          f'campos misturados: {fields}')
    return fields


@case('S12-14-2', 'worker panels')
def invalid_annotation(ctx):
    from pypdf import PdfWriter
    from pypdf.generic import IndirectObject, NumberObject
    writer = PdfWriter(clone_from=str(ctx.fixture(SCOPES)))
    writer.pages[0]['/Annots'].append(NumberObject(5))
    writer.pages[0]['/Annots'].append(IndirectObject(9999, 0, writer))
    broken = ctx.work / 'anotacao-invalida.pdf';writer.write(broken)
    run = ctx.worker('panels', broken)
    check(run['code'] == 0, 'leitura dos demais comentários falhou: ' + run['stderr'])
    contents = [c['contents'] for c in run['result']['comments']]
    check(contents == ['comentário alvo'], f'objeto inválido virou comentário: {contents}')
    return dict(comments=contents, invalid_entries=2)


# 15 — forms

def _form_request(path, values):
    return {'source_sha256': sha256(path), 'operations': [{'kind': 'fill-text-fields', 'values': values}]}


@case('S12-15-1', 'worker copy-edit')
def fill_text(ctx):
    from pypdf import PdfReader
    source = ctx.fixture(OWN + 'formulario.pdf');before = sha256(source);output = ctx.work / 'preenchido.pdf'
    run = ctx.worker('copy-edit', source, output, request=_form_request(source, {'nome': 'Linuxit aceitação'}))
    check(run['code'] == 0, run['stderr'])
    reader = PdfReader(str(output))
    value = reader.get_fields()['nome'].get('/V')
    check(value == 'Linuxit aceitação' and len(reader.pages) == 1, f'valor reaberto: {value!r}')
    check(sha256(source) == before, 'original alterado')
    return dict(reopened_value=value, pages=1, original_preserved=True)


@case('S12-15-2', 'worker copy-edit')
def fill_refused(ctx):
    source = ctx.fixture(OWN + 'formulario.pdf');before = sha256(source);outcomes = {}
    for label, values in (('readonly', {'fixo': 'novo'}), ('maxlen', {'curto': 'abcdef'})):
        output = ctx.work / f'{label}.pdf'
        run = ctx.worker('copy-edit', source, output, request=_form_request(source, values))
        check(run['code'] != 0 and not output.exists(), f'{label}: alteração aceita')
        outcomes[label] = 'refused'
    check(sha256(source) == before and not list(ctx.work.glob('.linuxit-copy-*')), 'original/temporários afetados')
    return outcomes


@case('S12-15-3', 'worker copy-edit (fill-form-events)')
def formatted_number(ctx):
    from pypdf import PdfReader
    source = ctx.fixture(OWN + 'formulario-numerico.pdf');before = sha256(source);output = ctx.work / 'numerico.pdf'
    request = {'source_sha256': before, 'operations': [{'kind': 'fill-form-events', 'values': {'preco': '1234,5', 'quantidade': '2'}}]}
    run = ctx.worker('copy-edit', source, output, request=request)
    check(run['code'] == 0, run['stderr'])
    reader = PdfReader(str(output));fields = reader.get_fields()
    raw = {name: str(fields[name]['/V']) for name in ('preco', 'quantidade', 'total')}
    check(raw == {'preco': '1234.5', 'quantidade': '2', 'total': '2469'}, f'valores gravados: {raw}')
    widget = next(a.get_object() for a in reader.pages[0]['/Annots'] if a.get_object()['/T'] == 'total')
    shown = widget['/AP']['/N'].get_object().get_data()
    check(b'R$ 2.469,00' in shown, 'aparência sem o número formatado')
    check(sha256(source) == before, 'original alterado')
    return dict(values=raw, appearance_text='R$ 2.469,00', javascript_executed=False)


@case('S12-15-4', 'worker copy-edit (fill-form-events)')
def formatted_date(ctx):
    from pypdf import PdfReader
    source = ctx.fixture(OWN + 'formulario-data.pdf');before = sha256(source);output = ctx.work / 'data.pdf'
    request = {'source_sha256': before, 'operations': [{'kind': 'fill-form-events', 'values': {'vencimento': '1/2/2026'}}]}
    run = ctx.worker('copy-edit', source, output, request=request)
    check(run['code'] == 0, run['stderr'])
    reader = PdfReader(str(output));value = str(reader.get_fields()['vencimento']['/V'])
    shown = reader.pages[0]['/Annots'][0].get_object()['/AP']['/N'].get_object().get_data()
    check(value == '1/2/2026' and b'01/02/2026' in shown, f'valor {value!r} ou aparência sem 01/02/2026')
    check(sha256(source) == before, 'original alterado')
    return dict(value=value, appearance_text='01/02/2026', javascript_executed=False)


@case('S12-15-5', 'worker copy-edit (fill-form-events)')
def impossible_date(ctx):
    source = ctx.fixture(OWN + 'formulario-data.pdf');before = sha256(source);output = ctx.work / 'data.pdf'
    request = {'source_sha256': before, 'operations': [{'kind': 'fill-form-events', 'values': {'vencimento': '31/02/2026'}}]}
    run = ctx.worker('copy-edit', source, output, request=request)
    check(run['code'] != 0 and not output.exists(), 'data inexistente aceita')
    check(sha256(source) == before and not list(ctx.work.glob('.linuxit-copy-*')), 'original/temporários afetados')
    return dict(refused=True, output_created=False)


@case('S12-15-6', 'worker copy-edit (fill-form-events)')
def masked_fields(ctx):
    from pypdf import PdfReader
    source = ctx.fixture(OWN + 'formulario-mascaras.pdf');before = sha256(source);output = ctx.work / 'mascaras.pdf'
    request = {'source_sha256': before, 'operations': [{'kind': 'fill-form-events', 'values': {'cep': '01310100', 'telefone': '5551234567'}}]}
    run = ctx.worker('copy-edit', source, output, request=request)
    check(run['code'] == 0, run['stderr'])
    reader = PdfReader(str(output));fields = reader.get_fields()
    values = {name: str(fields[name]['/V']) for name in ('cep', 'telefone')}
    check(values == {'cep': '01310-100', 'telefone': '5551234567'}, f'valores: {values}')
    # Visible page text: parentheses are escaped inside appearance string literals.
    shown = subprocess.run(['pdftotext', '-layout', str(output), '-'], capture_output=True, text=True).stdout
    check('01310-100' in shown and '(555) 123-4567' in shown, f'aparências sem máscara: {shown.strip()!r}')
    check(sha256(source) == before, 'original alterado')
    return dict(values=values, appearance={'cep': '01310-100', 'telefone': '(555) 123-4567'}, javascript_executed=False)


@case('S12-15-7', 'worker copy-edit (fill-form-events)')
def masked_refused(ctx):
    source = ctx.fixture(OWN + 'formulario-mascaras.pdf');before = sha256(source);outcomes = {}
    for label, values in (('cep_com_letra', {'cep': '0131010A'}), ('telefone_curto', {'telefone': '55512345'})):
        output = ctx.work / f'{label}.pdf'
        request = {'source_sha256': before, 'operations': [{'kind': 'fill-form-events', 'values': values}]}
        run = ctx.worker('copy-edit', source, output, request=request)
        outcomes[label] = run['code'] != 0 and not output.exists()
    check(all(outcomes.values()) and sha256(source) == before, f'recusas: {outcomes}')
    return outcomes


@case('S12-15-8', 'worker panels (XFA datasets) + copy-edit')
def xfa_read_only(ctx):
    source = ctx.fixture(OWN + 'formulario-xfa.pdf');before = sha256(source)
    run = ctx.worker('panels', source)
    check(run['code'] == 0 and isinstance(run['result'], dict), run['stderr'])
    xfa = run['result']['xfa']
    listed = [(f['path'], f['value']) for f in xfa['fields']]
    expected = [('form1[0].nome[0]', 'Ana Souza'), ('form1[0].itens[0].item[0]', 'Caneta'),
                ('form1[0].itens[0].item[1]', 'Caderno'), ('form1[0].obs[0]', '')]
    check(listed == expected and xfa['hybrid'] and xfa['error'] is None, f'campos XFA: {listed}')
    output = ctx.work / 'nao-gravar.pdf'
    edit = ctx.worker('copy-edit', source, output, request=_form_request(source, {'form1[0].nome[0]': 'Outro'}))
    check(edit['code'] != 0 and 'XFA' in edit['stderr'] and not output.exists(), 'gravação XFA aceita')
    check(sha256(source) == before, 'original alterado')
    return dict(fields=dict(listed), hybrid=True, write_refused=True, scripts_executed=False, original_preserved=True)


# 16 — attachments

@case('S12-16-1', 'worker attachments/extract-attachment')
def extract(ctx):
    source = ctx.fixture('testes/fixtures/anexos-simples.pdf')
    expected = json.loads(ctx.fixture('testes/fixtures/anexos-simples.json').read_text(encoding='utf-8'))['attachments'][0]
    listed = ctx.worker('attachments', source)['result']
    item = listed['attachments'][0]
    folder = ctx.work / 'destino';folder.mkdir()
    run = ctx.worker('extract-attachment', source, folder, request={'index': item['index'], 'source_sha256': listed['source_sha256']})
    check(run['code'] == 0, run['stderr'])
    saved = folder / expected['name']
    check(saved.is_file() and saved.stat().st_size == expected['size_bytes'] and sha256(saved) == expected['sha256'],
          'bytes extraídos diferem do manifesto')
    return dict(name=expected['name'], size=expected['size_bytes'], sha256=expected['sha256'])


@case('S12-16-2', 'worker attachments/extract-attachment')
def extract_dangerous(ctx):
    source = ctx.fixture(OWN + 'anexo-nome-perigoso.pdf')
    listed = ctx.worker('attachments', source)['result']
    item = listed['attachments'][0]
    check(item['name'] == '../fora.txt' and item['filename_allowed'] is False, f'listagem: {item}')
    folder = ctx.work / 'destino';folder.mkdir()
    run = ctx.worker('extract-attachment', source, folder, request={'index': 0, 'source_sha256': listed['source_sha256']})
    check(run['code'] != 0, 'extração aceita')
    check(not any(folder.iterdir()) and not (ctx.work / 'fora.txt').exists(), 'arquivo criado')
    return dict(filename_allowed=False, extraction='refused', files_created=0)


# 17 — signatures

def _identity(ctx):
    from datetime import datetime, timedelta, timezone
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Linuxit synthetic acceptance signer')])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=1)).sign(key, hashes.SHA256()))
    key_path, cert_path = ctx.work / 'chave.pem', ctx.work / 'certificado.pem'
    key_path.write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                           serialization.BestAvailableEncryption(b'senha-sintetica')))
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    return key_path, cert_path


def _signed(ctx):
    source = ctx.copy(SCOPES, 'origem.pdf');key, cert = _identity(ctx);signed = ctx.work / 'assinado.pdf'
    run = ctx.worker('sign-copy', source, request=dict(destination=str(signed), source_sha256=sha256(source),
                                                        certificate=str(cert), private_key=str(key), password='senha-sintetica'))
    check(run['code'] == 0 and signed.is_file(), 'assinatura falhou: ' + run['stderr'])
    return source, signed


@case('S12-17-1', 'worker sign-copy/signature-info')
def signature_integrity(ctx):
    source, signed = _signed(ctx)
    before = sha256(signed)
    info = ctx.worker('signature-info', signed, request={})
    check(info['code'] == 0, info['stderr'])
    item = info['result']['signatures'][0]
    check(item['integrity_verified'] and item['current_file_covered'], f'integridade: {item}')
    check(info['result']['trust_chain_verified'] is False and info['result']['network_used'] is False, 'confiança/rede indevidas')
    check(sha256(signed) == before, 'PDF alterado pela inspeção')
    return dict(integrity_verified=True, current_file_covered=True, trust_chain_verified=False, network_used=False)


@case('S12-17-2', 'worker signature-info')
def signature_malformed(ctx):
    _, signed = _signed(ctx)
    raw = signed.read_bytes()
    start = raw.index(b'/Contents <') + len(b'/Contents <')
    damaged = ctx.work / 'der-malformado.pdf'
    damaged.write_bytes(raw[:start] + b'00' * 64 + raw[start + 128:])
    tampered = ctx.work / 'alterado.pdf'
    tampered.write_bytes(raw.replace(b'alvo', b'ALVO', 1) if b'alvo' in raw else raw[:-40] + b'%' * 40)
    states = {}
    for label, path in (('der', damaged), ('bytes', tampered)):
        info = ctx.worker('signature-info', path, request={})
        items = info['result']['signatures'] if info['code'] == 0 else []
        approved = any(i.get('integrity_verified') for i in items)
        check(not approved, f'{label}: assinatura aprovada')
        states[label] = items[0]['status'] if items else f'exit {info["code"]}'
    return states


# 18/19 — security and accessible text

PASSWORDS = {'user_password': 'usuario-sintetico', 'owner_password': 'proprietario-sintetico'}


def _protected(ctx):
    from pdf_security import PERMISSION_FLAGS
    source = ctx.copy(SCOPES, 'origem.pdf');output = ctx.work / 'protegido.pdf'
    run = ctx.worker('protect-copy', source, request={'destination': str(output), 'source_sha256': sha256(source),
                                                       **PASSWORDS, 'permissions': {k: False for k in PERMISSION_FLAGS}})
    check(run['code'] == 0 and output.is_file(), 'proteção falhou: ' + run['stderr'])
    return source, output, run


@case('S12-18-1', 'worker protect-copy/security-info/owner-copy')
def security_roles(ctx):
    _, protected, created = _protected(ctx)
    user = ctx.worker('security-info', protected, request={'password': PASSWORDS['user_password']})
    owner = ctx.worker('security-info', protected, request={'password': PASSWORDS['owner_password']})
    check(user['code'] == 0 and owner['code'] == 0, user['stderr'] + owner['stderr'])
    dumped = json.dumps([created['result'], user['result'], owner['result']])
    check(not any(p in dumped for p in PASSWORDS.values()), 'senha presente no resultado')
    plain = ctx.work / 'aberto.pdf'
    unlocked = ctx.worker('owner-copy', protected, request={'destination': str(plain), 'source_sha256': sha256(protected),
                                                            'owner_password': PASSWORDS['owner_password']})
    check(unlocked['code'] == 0 and plain.is_file(), 'cópia sem criptografia do proprietário falhou: ' + unlocked['stderr'])
    roles = (user['result']['role'], owner['result']['role'])
    aes = (user['result']['encryption_version'], user['result']['revision'])
    check(roles == ('user', 'owner') and aes == (5, 6), f'papéis {roles}, criptografia V/R {aes}')
    reopened = ctx.worker('security-info', plain, request={'password': ''})['result']
    check(reopened['encrypted'] is False, 'cópia do proprietário continua cifrada')
    return dict(user_role=roles[0], owner_role=roles[1], aes256_v_r=list(aes), owner_plaintext_copy=True,
                passwords_in_results=False)


@case('S12-18-2', 'worker security-info/owner-copy/protect-copy')
def security_refusals(ctx):
    _, protected, _ = _protected(ctx)
    outcomes = {}
    wrong = ctx.worker('security-info', protected, request={'password': 'senha-errada'})
    outcomes['wrong_password'] = wrong['code'] != 0 or not wrong['result'].get('authenticated', False)
    plain = ctx.work / 'aberto.pdf'
    as_user = ctx.worker('owner-copy', protected, request={'destination': str(plain), 'source_sha256': sha256(protected),
                                                           'owner_password': PASSWORDS['user_password']})
    outcomes['user_plaintext'] = as_user['code'] != 0 and not plain.exists()
    existing = ctx.work / 'existente.pdf';existing.write_bytes(b'manter')
    again = ctx.worker('owner-copy', protected, request={'destination': str(existing), 'source_sha256': sha256(protected),
                                                         'owner_password': PASSWORDS['owner_password']})
    outcomes['existing_destination'] = again['code'] != 0 and existing.read_bytes() == b'manter'
    check(all(outcomes.values()), f'recusas: {outcomes}')
    check(not any(p in wrong['stderr'] + as_user['stderr'] for p in PASSWORDS.values()), 'senha em mensagem de erro')
    return outcomes


@case('S12-19-1', 'worker accessible-text')
def accessible_text(ctx):
    run = ctx.worker('accessible-text', ctx.fixture(SCOPES), request={'page': 0})
    check(run['code'] == 0, run['stderr'])
    text = run['result'].get('text', '')
    check('alvo' in text, f'texto: {text[:80]!r}')
    return dict(characters=len(text), contains_target=True)


@case('S12-19-2', 'worker accessible-text')
def accessible_text_encrypted(ctx):
    _, protected, _ = _protected(ctx)
    run = ctx.worker('accessible-text', protected, request={'page': 0})
    check(run['code'] != 0 and run['result'] is None, 'texto de PDF cifrado entregue sem senha')
    return dict(exit=run['code'], partial_text=None)


# 21 — layers

@case('S12-21-1', 'worker panels')
def layers(ctx):
    source = ctx.fixture(OWN + 'camadas.pdf');before = sha256(source)
    found = ctx.worker('panels', source)['result']['layers']
    names = [(l['name'], l['visible']) for l in found]
    check(names == [('Base', True), ('Notas', False)], f'camadas: {names}')
    check(sha256(source) == before, 'PDF alterado')
    return dict(layers=names)


@case('S12-21-2', 'worker panels')
def no_layers(ctx):
    found = ctx.worker('panels', ctx.fixture(SCOPES))['result']['layers']
    check(found == [], f'camada fictícia: {found}')
    return dict(layers=[])


# 22 — preferences

@case('S12-22-1', 'appearance.save_mode/read_mode')
def preferences(ctx):
    from appearance import read_mode, save_mode
    path = ctx.work / 'preferences.json'
    path.write_text(json.dumps({'appearance': 'dark', 'chave_futura': {'v': 1}}), encoding='utf-8')
    save_mode('light', path)
    stored = json.loads(path.read_text(encoding='utf-8'))
    check(read_mode(path) == 'light' and stored.get('chave_futura') == {'v': 1}, f'preferências: {stored}')
    return dict(mode='light', unknown_key_preserved=True)


@case('S12-22-2', 'appearance.save_mode')
def preferences_invalid(ctx):
    from appearance import save_mode
    path = ctx.work / 'preferences.json';path.write_text(json.dumps({'appearance': 'dark'}), encoding='utf-8')
    before = path.read_bytes()
    try:
        save_mode('neon', path);raised = False
    except ValueError:
        raised = True
    check(raised and path.read_bytes() == before, 'modo inventado aceito')
    return dict(value_error=True, file_unchanged=True)


# 24 — conversion

@case('S12-24-1', 'worker images-to-pdf')
def images_to_pdf(ctx):
    manifest = json.loads(ctx.fixture('testes/fixtures/criacao-imagens/manifest.json').read_text(encoding='utf-8'))
    images = [ctx.fixture('testes/fixtures/criacao-imagens/' + item['file']) for item in manifest['images']]
    before = [sha256(p) for p in images];output = ctx.work / 'imagens.pdf'
    run = ctx.worker('images-to-pdf', output, request={'paths': [str(p) for p in images], 'dpi': 72})
    check(run['code'] == 0, run['stderr'])
    info = ctx.worker('info', output)['result']
    expected = [list(item['page_points_at_72_dpi']) for item in manifest['images']]
    check(info['pages'] == 2 and [[round(v) for v in s] for s in info['sizes']] == expected, f'páginas: {info}')
    check([sha256(p) for p in images] == before, 'imagens fonte alteradas')
    return dict(pages=2, sizes=expected, order=[item['file'] for item in manifest['images']])


@case('S12-24-2', 'worker images-to-pdf')
def images_refused(ctx):
    from PIL import Image
    gif = ctx.work / 'animacao.gif'
    Image.new('RGB', (8, 8), 'red').save(gif, save_all=True, append_images=[Image.new('RGB', (8, 8), 'blue')])
    broken = ctx.work / 'quebrado.png';broken.write_bytes(b'\x89PNG\r\n\x1a\nnao e imagem')
    good = ctx.copy('testes/fixtures/criacao-imagens/transparencia.png')
    outcomes = {}
    for label, paths in (('gif', [good, gif]), ('png_invalido', [good, broken])):
        output = ctx.work / f'{label}.pdf'
        run = ctx.worker('images-to-pdf', output, request={'paths': [str(p) for p in paths], 'dpi': 72})
        outcomes[label] = run['code'] != 0 and not output.exists()
    existing = ctx.work / 'existente.pdf';existing.write_bytes(b'manter')
    run = ctx.worker('images-to-pdf', existing, request={'paths': [str(good)], 'dpi': 72})
    outcomes['existing_destination'] = run['code'] != 0 and existing.read_bytes() == b'manter'
    check(all(outcomes.values()), f'recusas: {outcomes}')
    return outcomes
