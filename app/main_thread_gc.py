"""Run Python's cyclic garbage collector only on the GTK main thread.

GTK 3 is not thread-safe. Python's automatic cyclic collector runs in
whichever thread happens to cross the allocation threshold, which is often a
background worker (search, rendering, indexing). Widgets kept in reference
cycles (signal closures that capture the window, for instance) were then
finalized off the main thread while the main thread was computing CSS styles.
A full test run showed hundreds of buttons, lists and whole windows freed by
worker threads, and Debian 13 CI crashed twice with
"_gtk_css_rgba_value_get_rgba" followed by SIGSEGV (step E27).

install() turns off the automatic collector and schedules the same
generational collection from a GLib timeout on the main context, keeping the
interpreter's thresholds. Plain reference counting is unchanged, so objects
without cycles are still freed immediately. Worker-only processes never call
this and keep the default collector.
"""
import gc
import threading

INTERVAL_MS = 250
_installed = False


def _generation():
    """Mirror CPython's threshold policy: the oldest generation that is due."""
    counts, thresholds = gc.get_count(), gc.get_threshold()
    if not thresholds[0] or counts[0] < thresholds[0]:
        return None
    if counts[1] >= thresholds[1]:
        return 2 if counts[2] >= thresholds[2] else 1
    return 0


def collect_due():
    """Collect the generation that is due, on the calling (main) thread."""
    generation = _generation()
    if generation is not None:
        gc.collect(generation)
    return True


def install(glib):
    """Idempotent. Must be called on the thread that runs the GLib main loop."""
    global _installed
    if _installed:
        return False
    if threading.current_thread() is not threading.main_thread():
        raise RuntimeError('main_thread_gc.install must run on the main thread')
    gc.disable()
    glib.timeout_add(INTERVAL_MS, collect_due, priority=glib.PRIORITY_LOW)
    _installed = True
    return True


def installed():
    return _installed
