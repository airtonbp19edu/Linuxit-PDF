"""Temporary-folder cleanup for GTK tests that is safe on Windows.

On Windows a file stays locked until the destroyed widgets, Poppler documents and file monitors
that referenced it are finalized. Those releases happen after pending main-loop events and
garbage collection, so a cleanup right after destroy() can fail with WinError 32 even though
nothing is leaked. Elsewhere the cleanup is unchanged and any error is raised at once.
"""
import gc
import os
import time


def cleanup_temp(temp, timeout=10):
    deadline = time.monotonic() + timeout
    while True:
        try:
            temp.cleanup();return
        except PermissionError:
            if os.name != 'nt' or time.monotonic() > deadline:raise
            try:
                from gi.repository import GLib
                context = GLib.MainContext.default()
                while context.pending():context.iteration(False)
            except (ImportError, ValueError):pass
            gc.collect();time.sleep(.1)
