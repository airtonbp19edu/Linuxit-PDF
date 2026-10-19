#!/usr/bin/env python3
"""Exercise actual GDK monitor routing on an explicitly virtual X11 desktop."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(os.environ.get('PRINT_VIEW_TEST_APP', ROOT / 'app'))))
import cairo
from main import PDFWindow, Gtk, Gdk, GLib
from presentation import PresentationWindow


def wait(predicate, timeout=20):
    deadline = time.monotonic() + timeout
    context = GLib.MainContext.default()
    while time.monotonic() < deadline:
        frame = time.monotonic() + .04
        while context.pending() and time.monotonic() < frame:context.iteration(False)
        if predicate():return
        time.sleep(.01)
    raise RuntimeError('Virtual monitor readiness timeout')


output = Path(sys.argv[1])
output.mkdir(parents=True, exist_ok=False)
report = {'schema':'linuxit-native-virtual-monitors-v1', 'virtual_desktop':True,
          'physical_monitor_validation':False, 'foxit_executed':False,
          'passed':False, 'monitors':[], 'transitions':[], 'errors':[]}
parent = presentation = None
try:
    display = Gdk.Display.get_default()
    for i in range(display.get_n_monitors()):
        geometry = display.get_monitor(i).get_geometry()
        report['monitors'].append({'index':i, 'x':geometry.x, 'y':geometry.y,
                                  'width':geometry.width, 'height':geometry.height})
    if len(report['monitors']) < 2:
        raise RuntimeError('The virtual desktop did not expose two GDK monitors')
    with tempfile.TemporaryDirectory(prefix='linuxit-native-monitors-') as directory, patch.object(Gtk, 'main_quit'):
        source = Path(directory) / 'monitor-fixture.pdf'
        surface = cairo.PDFSurface(str(source), 420, 595)
        context = cairo.Context(surface); context.set_font_size(24)
        context.move_to(30, 70); context.show_text('LINUXIT PRESENTATION'); context.show_page(); surface.finish()
        parent = PDFWindow(); parent._error = report['errors'].append; parent.open_document(str(source))
        wait(lambda:parent.displayed_page == 0)
        presentation = PresentationWindow(parent, parent.runner, parent.filepath, parent.page_sizes,
            0, parent.cache_dir, session=parent.document_session, monitor_index=0)
        for index in (0, 1, 0):
            presentation.monitor_combo.set_active_id(str(index))
            expected = report['monitors'][index]
            wait(lambda: not presentation._loading and presentation.fullscreen_active
                 and presentation.get_size() == (expected['width'], expected['height']))
            report['transitions'].append({'selected':index, 'fullscreen_active':presentation.fullscreen_active,
                'window_size':list(presentation.get_size()), 'page':presentation.page + 1})
            # Capture this visible window, never the occluded parent.
            presentation.canvas.queue_draw()
            settled=[]; GLib.timeout_add(180, lambda:(settled.append(True),False)[1]); wait(lambda:bool(settled))
            allocation = presentation.get_allocation()
            pixels = Gdk.pixbuf_get_from_window(presentation.get_window(),0,0,allocation.width,allocation.height)
            path = output / ('monitor-' + str(index) + '.png'); pixels.savev(str(path),'png',[],[])
        report['passed'] = not report['errors'] and len(report['transitions']) == 3
except Exception as exc:
    report['errors'].append(str(exc))
finally:
    if presentation is not None:presentation.destroy()
    if parent is not None:
        with patch.object(Gtk,'main_quit'):parent.destroy()
    report['app_files'] = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT/'app').glob('*.py')}
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:report[key] for key in ('passed','monitors','transitions','errors')}))
raise SystemExit(0 if report['passed'] else 1)
