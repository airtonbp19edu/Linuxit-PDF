#!/usr/bin/env python3
"""Count GObjects that Python's cyclic GC frees on worker threads during a test run (E27).

Runs scripts/run_tests.py in this process with gc.DEBUG_SAVEALL so each
collection's unreachable objects can be inspected before they are released.
Collections started on a non-main thread are counted with the GObject types
they free. A healthy GTK process frees no GObject off the main thread. The
probe slightly changes timing and memory use, so it is diagnostic only; the
test counts it prints are not validation evidence.

Usage: dbus-run-session -- xvfb-run -a python3 scripts/probe_gc_threads.py --report OUT.json -- [run_tests.py args]
"""
import collections
import gc
import json
from pathlib import Path
import runpy
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]


def main():
    if '--report' not in sys.argv or '--' not in sys.argv:
        raise SystemExit(__doc__)
    report = Path(sys.argv[sys.argv.index('--report') + 1])
    if report.exists():
        raise SystemExit('Use a new report path to preserve previous evidence')
    forwarded = sys.argv[sys.argv.index('--') + 1:]
    from gi.repository import GObject
    stats = collections.Counter()
    worker_types = collections.Counter()

    def on_gc(phase, info):
        if phase != 'stop':
            return
        thread = 'main' if threading.current_thread() is threading.main_thread() else 'worker'
        stats[thread + '_collections'] += 1
        stats[thread + '_collected'] += info['collected']
        if thread == 'worker':
            for item in gc.garbage:
                if isinstance(item, GObject.Object):
                    worker_types[type(item).__name__] += 1
        gc.garbage.clear()

    gc.set_debug(gc.DEBUG_SAVEALL)
    gc.callbacks.append(on_gc)
    sys.argv = [str(ROOT / 'scripts/run_tests.py')] + forwarded
    code = 0
    try:
        runpy.run_path(sys.argv[0], run_name='__main__')
    except SystemExit as exit_:
        code = exit_.code or 0
    finally:
        gc.callbacks.remove(on_gc)
        gc.set_debug(0)
        sys.path.insert(0, str(ROOT / 'app'))
        try:
            import main_thread_gc
            installed = main_thread_gc.installed()
        except ImportError:  # Revisions before E27 have no main-thread collector.
            installed = False
        data = {'schema': 'linuxit-gc-thread-probe-v1', 'run_tests_args': forwarded,
                'main_thread_gc_installed': installed,
                'collections': dict(stats), 'worker_freed_gobjects': sum(worker_types.values()),
                'worker_freed_gobject_types': dict(worker_types.most_common())}
        report.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({k: data[k] for k in ('main_thread_gc_installed', 'collections', 'worker_freed_gobjects')}))
    raise SystemExit(code)


if __name__ == '__main__':
    main()
