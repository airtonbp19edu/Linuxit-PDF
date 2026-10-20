"""S12-25 acceptance cases through the real desktop portal (ephemeral X11 desktop).

The application's own 'Abrir pelo seletor do sistema' action runs in a child
process with GTK_USE_PORTAL=1; the parent drives the portal dialog with xdotool.
Registered only when a display, xdotool, openbox and xdg-desktop-portal exist.
Configuration folders are redirected to the case folder. Not Foxit observations.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from casos import OWN, SCOPES, check, sha256

CASES = {}
CHILD = Path(__file__).resolve().parent / 'portal_cliente.py'
TITLE = '^Abrir PDF pelo seletor do sistema$'


def available():
    portal = any(Path(p).exists() for p in ('/usr/libexec/xdg-desktop-portal', '/usr/lib/xdg-desktop-portal'))
    tools = all(shutil.which(t) for t in ('xdotool', 'openbox', 'dbus-update-activation-environment'))
    return bool(os.environ.get('DISPLAY')) and portal and tools


def case(case_id, boundary):
    def register(function):
        if available():
            CASES[case_id] = dict(function=function, boundary=boundary, needs_display=True)
        return function
    return register


def _xdotool(*args):
    return subprocess.run(['xdotool', *args], capture_output=True, text=True, timeout=10)


def _drive(ctx, action, chosen=None):
    current = ctx.copy(SCOPES, 'atual.pdf')
    env = {**os.environ, 'GTK_USE_PORTAL': '1', 'XDG_CURRENT_DESKTOP': 'GNOME', 'G_DBUS_DEBUG': 'message',
           'PYTHONUTF8': '1'}
    for key, name in (('XDG_CONFIG_HOME', 'config'), ('XDG_CACHE_HOME', 'cache'), ('XDG_DATA_HOME', 'data')):
        folder = ctx.work / name;folder.mkdir(exist_ok=True);env[key] = str(folder)
    subprocess.run(['dbus-update-activation-environment', 'DISPLAY', 'XAUTHORITY', 'XDG_CURRENT_DESKTOP'],
                   env=env, check=True, timeout=10)
    manager = None
    if subprocess.run(['pgrep', '-u', str(os.getuid()), '-x', 'openbox'], capture_output=True).returncode != 0:
        manager = subprocess.Popen(['openbox', '--sm-disable'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log = ctx.work / 'cliente.log'
    try:
        with log.open('wb') as output:
            child = subprocess.Popen([sys.executable, str(CHILD), str(ctx.app), str(current)],
                                     stdout=output, stderr=subprocess.STDOUT, env=env)
            window, deadline = None, time.monotonic() + 30
            while window is None and time.monotonic() < deadline and child.poll() is None:
                found = _xdotool('search', '--onlyvisible', '--name', TITLE).stdout.split()
                window = found[-1] if found else None
                time.sleep(.1)
            check(window is not None, 'diálogo do portal não apareceu')
            _xdotool('windowactivate', '--sync', window)
            if action == 'select':
                _xdotool('key', '--clearmodifiers', 'ctrl+l')
                _xdotool('type', '--clearmodifiers', '--', str(chosen))
                _xdotool('key', '--clearmodifiers', 'Return')
            else:
                _xdotool('key', '--clearmodifiers', 'Escape')
            try:
                child.wait(timeout=30)
            except subprocess.TimeoutExpired:
                if action == 'select':_xdotool('key', '--clearmodifiers', 'Return')
                child.wait(timeout=15)
    finally:
        if 'child' in locals() and child.poll() is None:child.kill();child.wait()
        if manager is not None:manager.terminate();manager.wait(timeout=10)
    raw = log.read_text(encoding='utf-8', errors='replace')
    line = next((l for l in raw.splitlines() if l.startswith('LINUXIT_PORTAL_CASE ')), None)
    check(line is not None, 'cliente terminou sem resultado: ' + raw[-400:])
    result = json.loads(line.partition(' ')[2])
    result['portal_call'] = 'org.freedesktop.portal.FileChooser' in raw and 'OpenFile' in raw
    result['portal_response'] = 'org.freedesktop.portal.Request' in raw and 'Response' in raw
    return current, result


@case('S12-25-1', 'PDFWindow._choose_open_native via xdg-desktop-portal')
def portal_open(ctx):
    chosen = ctx.copy(OWN + 'oito-paginas.pdf', 'autorizado.pdf')
    other = ctx.copy(OWN + 'proximidade.pdf', 'outro.pdf')
    current, result = _drive(ctx, 'select', chosen)
    check(result['portal_call'] and result['portal_response'], 'a escolha não passou pelo portal')
    check(result['after'] == str(chosen) and result['pages'] == 8, f"documento aberto: {result['after']} ({result['pages']} páginas)")
    check(result['after'] != str(other) and result['errors'] == [], 'recurso não autorizado ou erro')
    check(sha256(current) == ctx.fixtures[SCOPES], 'documento anterior alterado')
    return dict(opened='autorizado.pdf', pages=8, portal_call=True, portal_response=True, other_file_opened=False)


@case('S12-25-2', 'PDFWindow._choose_open_native via xdg-desktop-portal')
def portal_cancel(ctx):
    current, result = _drive(ctx, 'cancel')
    check(result['portal_call'] and result['portal_response'], 'o cancelamento não passou pelo portal')
    check(result['after'] == result['before'] == str(current) and result['pages'] == 2,
          f"documento corrente trocado: {result['before']} -> {result['after']}")
    check(result['errors'] == [] and 'aberto' not in result['status'].lower(), 'erro ou sucesso falso: ' + result['status'])
    return dict(current_document_kept=True, pages=2, errors=[], status=result['status'])
