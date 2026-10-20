"""Executable own acceptance cases S12 that need the real GTK window and a display.

They drive PDFWindow/PresentationWindow through the same methods the widgets
call. Configuration and cache folders are redirected to the case folder so a
run never touches the user's preferences. Not Foxit observations.
"""
import os
from pathlib import Path
import threading
import time
from unittest.mock import patch

from casos import OWN, SCOPES, check

CASES = {}


def case(case_id, boundary):
    def register(function):
        CASES[case_id] = dict(function=function, boundary=boundary, needs_display=True)
        return function
    return register


def _gtk():
    import gi
    gi.require_version('Gtk', '3.0');gi.require_version('Gdk', '3.0')
    from gi.repository import Gdk, GLib, Gtk
    return Gtk, Gdk, GLib


def wait_for(predicate, timeout=20):
    _, _, GLib = _gtk()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        context = GLib.MainContext.default()
        while context.pending():
            context.iteration(False)
        if predicate():
            return True
        time.sleep(.02)
    return False


def settle(seconds):
    wait_for(lambda: False, seconds)


class Window:
    """Open one document in an isolated PDFWindow and always destroy it."""

    def __init__(self, ctx, document=None):
        self.ctx, self.document = ctx, document

    def __enter__(self):
        Gtk, _, _ = _gtk()
        self.saved = {k: os.environ.get(k) for k in ('XDG_CONFIG_HOME', 'XDG_CACHE_HOME', 'XDG_DATA_HOME')}
        for key, name in (('XDG_CONFIG_HOME', 'config'), ('XDG_CACHE_HOME', 'cache'), ('XDG_DATA_HOME', 'data')):
            folder = self.ctx.work / name;folder.mkdir(exist_ok=True);os.environ[key] = str(folder)
        self.quit = patch.object(Gtk, 'main_quit');self.quit.start()
        from main import PDFWindow, load_css
        load_css()
        self.errors = []
        self.window = PDFWindow()
        self.window._error = self.errors.append
        if self.document is not None:
            self.window.open_document(str(self.document))
            check(wait_for(lambda: self.window.page_count > 0 and self.window.current_pixbuf is not None),
                  'documento não abriu na janela')
            # Let the initial final-width render and neighbour prefetch finish before acting.
            wait_for(lambda: not self.window._render_pending);settle(.8)
        return self.window

    def __exit__(self, *_):
        try:
            self.window.destroy();settle(.2)
        finally:
            self.quit.stop()
            for key, value in self.saved.items():
                if value is None:os.environ.pop(key, None)
                else:os.environ[key] = value


def _clipboard_text():
    Gtk, Gdk, _ = _gtk()
    return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).wait_for_text()


def _set_clipboard(text):
    Gtk, Gdk, _ = _gtk()
    Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD).set_text(text, -1)
    settle(.1)


# 02 — navigation

@case('S12-02-1', 'PDFWindow.goto_page/_rotate')
def navigate_and_rotate(ctx):
    with Window(ctx, ctx.fixture(SCOPES)) as w:
        w.goto_page(1)
        check(wait_for(lambda: w.page == 1 and w.displayed_page == 1), 'segunda página não exibida')
        w._rotate(90)
        check(wait_for(lambda: w.displayed_rotation == 90 and w.displayed_page == 1), 'rotação não exibida')
        width, height = w.current_pixbuf.get_width(), w.current_pixbuf.get_height()
        page_w, page_h = w.page_sizes[1]
        ratio, expected = width / height, page_h / page_w
        check(abs(ratio - expected) / expected < .03, f'proporção exibida {ratio:.3f} != página girada {expected:.3f}')
        return dict(page=2, rotation=90, displayed_ratio=round(ratio, 3), rotated_page_ratio=round(expected, 3))


@case('S12-02-2', 'PDFWindow.request_render callbacks')
def obsolete_render(ctx):
    with Window(ctx, ctx.fixture(OWN + 'oito-paginas.pdf')) as w:
        release, slow_started, produced, outcome = threading.Event(), threading.Event(), {}, {}
        original = w._reader_pixbuf

        def reader(path, page, *rest):  # DocumentSession.call passes the private reading path first
            if page == 5:
                slow_started.set();release.wait(10)
            try:
                pixbuf = original(path, page, *rest)
            except Exception as exc:  # noqa: BLE001 - the application may cancel the obsolete task
                outcome.setdefault(page, type(exc).__name__ + ': ' + str(exc));raise
            produced.setdefault(page, pixbuf);outcome.setdefault(page, 'finished')
            return pixbuf

        w._reader_pixbuf = reader
        # Page index 5 is far from the opened first page, so it is neither cached nor prefetched.
        w.goto_page(5)
        check(wait_for(slow_started.is_set), 'render da página anterior não começou')
        w.goto_page(2)
        release.set()
        check(wait_for(lambda: 5 in outcome and 2 in produced and w.displayed_page == 2), 'renders não terminaram')
        settle(.8)
        check(w.page == 2 and w.displayed_page == 2, f'página exibida {w.displayed_page}')
        check(w.rendered_pixbuf is not produced.get(5) and (w.rendered_pixbuf is produced[2]
              or w.page_cache.get(w._render_request_key) is w.rendered_pixbuf), 'imagem exibida não é a da página atual')
        check('Falha' not in w.status_file.get_text(), 'falha do render obsoleto exibida: ' + w.status_file.get_text())
        return dict(current_page=3, obsolete_page=6, obsolete_outcome=outcome[5], display_kept=True)


# 03 — presentation

def _presentation(ctx, w):
    from presentation import PresentationWindow
    p = PresentationWindow(w, w.runner, str(w.filepath), w.page_sizes, 0, w.cache_dir)
    p.resize(1000, 600)
    check(wait_for(lambda: p.pixbuf is not None and not p._loading), 'apresentação não carregou')
    return p


@case('S12-03-1', 'PresentationWindow fit/fill')
def presentation_modes(ctx):
    with Window(ctx, ctx.fixture(SCOPES)) as w:
        p = _presentation(ctx, w)
        try:
            width, height = p._canvas_size();available = height - p._controls_height()
            check(width > available, f'viewport não é paisagem: {width}×{available}')
            fit = (p.pixbuf.get_width(), p.pixbuf.get_height())
            check(fit[0] <= width and available * .88 <= fit[1] <= available, f'ajustar página: {fit} em {width}×{available}')
            check((p.pan_x, p.pan_y) == (0, 0), 'ajustar página fora do centro')
            p.fit_combo.set_active_id('fill')
            check(wait_for(lambda: not p._loading and p.pixbuf.get_width() >= width - 30), 'preencher não ocupou a largura')
            fill = (p.pixbuf.get_width(), p.pixbuf.get_height())
            return dict(viewport=[width, available], fit=list(fit), fill=list(fill), centered=True)
        finally:
            p.destroy()


@case('S12-03-2', 'PresentationWindow render failure')
def presentation_failure(ctx):
    with Window(ctx, ctx.fixture(SCOPES)) as w:
        p = _presentation(ctx, w)
        try:
            with patch.object(p, '_load_page_pixbuf', side_effect=RuntimeError('falha sintética de imagem')):
                p._goto(1)
                check(wait_for(lambda: p._render_error is not None), 'falha não entregue à apresentação')
            check('falha sintética' in p._render_error and p.get_visible(), 'estado de falha ausente ou janela inválida')
            p._goto(0)
            check(wait_for(lambda: p._render_error is None and p.pixbuf is not None and not p._loading),
                  'janela não se recuperou depois da falha')
            return dict(error_shown=True, window_alive=True, recovered=True)
        finally:
            p.destroy()


# 05 — bookmark search hits selected in the window

def _bookmark_search(w):
    for key, button in w.find_options.items():
        if key.startswith('include_'):
            button.set_active(key == 'include_bookmarks')
    w.find_entry.set_text('alvo')
    check(wait_for(lambda: not w.search_running and len(w.search_hits) == 2), f'hits de marcador: {len(w.search_hits)}')
    return w.search_hits


@case('S12-05-1', 'PDFWindow find bar + _select_search_hit')
def bookmark_hits(ctx):
    with Window(ctx, ctx.fixture(SCOPES)) as w:
        hits = _bookmark_search(w)
        summary = [(h['source'], h['page'], h['rects']) for h in hits]
        check(summary == [('bookmark', 1, []), ('bookmark', None, [])], f'hits: {summary}')
        w._select_search_hit(0)
        check(wait_for(lambda: w.page == 1 and w.displayed_page == 1), 'hit de marcador não levou à segunda página')
        w._select_search_hit(1)
        settle(.5)
        check(w.page == 1 and w.search_pos == 1, 'hit sem destino moveu a página')
        return dict(hits=[[s, None if p is None else p + 1, r] for s, p, r in summary], selected_pages=[2, 2])


@case('S12-05-2', 'PDFWindow _select_search_hit')
def bookmark_without_destination(ctx):
    with Window(ctx, ctx.fixture(SCOPES)) as w:
        hits = _bookmark_search(w)
        unresolved = [i for i, h in enumerate(hits) if h['page'] is None]
        check(len(unresolved) == 1, 'hit sem destino ausente')
        settle(.5)
        before = (w.page, w.displayed_page)  # the finished search already shows its first hit
        w._select_search_hit(unresolved[0])
        settle(.5)
        hit = w.search_hits[w.search_pos]
        check((w.page, w.displayed_page) == before and hit['rects'] == [] and not w._search_scroll_pending,
              f'destino ou destaque fabricado: {before} -> {(w.page, w.displayed_page)}')
        return dict(page_kept=before[0] + 1, rects=[], scroll_pending=False)


# 10 — text selection and clipboard

def _word(path, text):
    from rendering import extract_page_words
    data = extract_page_words(str(path), 0)
    word = next(item for item in data['words'] if item['text'] == text)
    return data, (word['x0'], word['y0'], word['x1'], word['y1'])


@case('S12-10-1', 'PDFWindow _finish_text_selection + clipboard')
def select_and_copy(ctx):
    path = ctx.fixture(SCOPES)
    data, rect = _word(path, 'alvo')
    with Window(ctx, path) as w:
        copied = []
        for rotation in (0, 90):
            if rotation:
                w._rotate(90)
                check(wait_for(lambda: w.displayed_rotation == 90), 'rotação não exibida')
            _set_clipboard('sentinela')
            w._finish_text_selection(w._pdf_rect_to_display(rect, data))
            check(wait_for(lambda: bool(w.selected_words)), f'seleção vazia na rotação {rotation}')
            copied.append(_clipboard_text())
        check(copied == ['alvo', 'alvo'], f'área de transferência: {copied}')
        return dict(clipboard=copied, rotations=[0, 90])


@case('S12-10-2', 'PDFWindow _finish_text_selection')
def select_empty(ctx):
    path = ctx.fixture(SCOPES)
    data, _ = _word(path, 'alvo')
    with Window(ctx, path) as w:
        _set_clipboard('sentinela')
        empty = (data['width'] * .1, data['height'] * .8, data['width'] * .6, data['height'] * .95)
        w._finish_text_selection(w._pdf_rect_to_display(empty, data))
        check(wait_for(lambda: 'Nenhum texto' in w.status_file.get_text()), f'status: {w.status_file.get_text()!r}')
        check(w.selected_words == [] and _clipboard_text() == 'sentinela', 'conteúdo fictício copiado')
        return dict(status=w.status_file.get_text(), clipboard_unchanged=True)


# 15 — forms

@case('S12-15-9', 'PDFWindow _xfa_dialog')
def xfa_dialog(ctx):
    with Window(ctx, ctx.fixture(OWN + 'formulario-xfa.pdf')) as w:
        check(wait_for(lambda: getattr(w, 'xfa_state', None) == 'ready'), 'painéis não carregaram')
        dialog = w._xfa_dialog(w.xfa_info, w.xfa_state)
        try:
            rows = [tuple(row) for row in dialog.xfa_store]
            summary = dialog.xfa_summary.get_text()
        finally:
            dialog.destroy()
        check(rows[0] == ('form1[0].nome[0]', 'Ana Souza') and len(rows) == 4, f'linhas {rows}')
        check('híbrido' in summary and 'não são executados' in summary, f'resumo {summary!r}')
    with Window(ctx, ctx.fixture(OWN + 'formulario.pdf')) as w:
        check(wait_for(lambda: getattr(w, 'xfa_state', None) == 'ready'), 'painéis não carregaram')
        dialog = w._xfa_dialog(w.xfa_info, w.xfa_state)
        try:
            plain = dialog.get_property('secondary-text')
        finally:
            dialog.destroy()
        check(plain == 'Este PDF não contém formulário XFA.', f'sem XFA: {plain!r}')
    return dict(rows=len(rows), first=list(rows[0]), summary=summary.splitlines()[0], without_xfa=plain)


# 20 — viewer ruler

@case('S12-20-1', 'PDFWindow _finish_measure')
def measure_inch(ctx):
    with Window(ctx, ctx.fixture(SCOPES)) as w:
        page_w, _ = w._page_dimensions_rotated();display_w, _ = w.page_image.display_size
        dx = 72 * display_w / page_w
        w._finish_measure((10, 40, 10 + dx, 40))
        check(w.measure_result == '2,54 cm', f'resultado {w.measure_result!r}')
        return dict(result=w.measure_result, decimals=2, decimal_separator='vírgula')


@case('S12-20-2', 'PDFWindow _finish_measure')
def measure_without_page(ctx):
    with Window(ctx) as w:
        w.measure_result = None
        w._finish_measure((0, 0, 100, 0))
        check(w.measure_result is None, f'medida publicada sem página: {w.measure_result!r}')
        return dict(measure_result=None)
