"""Shared detection of the real OCR/media runtime for tests on Linux and native Windows."""
import os
from pathlib import Path
import shutil
import sys

OCR_TOOLS = ('tesseract', 'pdftocairo', 'pdftotext')


def ocr_tools():
    return all(shutil.which(name) for name in OCR_TOOLS)


def gui_display():
    """Linux needs an X11/Wayland display; native Windows GUI runs are opted in by the CI."""
    if os.name == 'nt':
        return bool(os.environ.get('LINUXIT_WINDOWS_GUI_TESTS'))
    return bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))


def font_path():
    candidates = [Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
                  Path(sys.prefix) / 'share/fonts/TTF/DejaVuSans.ttf',
                  Path('/app/share/fonts/DejaVuSans.ttf'),
                  Path('/usr/share/fonts/dejavu/DejaVuSans.ttf')]
    windows = os.environ.get('WINDIR') or os.environ.get('SystemRoot')
    if windows:
        candidates += [Path(windows) / 'Fonts' / name for name in ('arial.ttf', 'segoeui.ttf', 'tahoma.ttf')]
    for path in candidates:
        if path.is_file():
            return str(path)
    # Fontconfig knows where a usable TrueType font is in Flatpak runtimes and other
    # layouts whose paths are not fixed. Ask it for a scalable, non-bitmap face.
    import shutil as _shutil
    import subprocess as _subprocess
    if _shutil.which('fc-match'):
        try:
            found = _subprocess.run(['fc-match', '-f', '%{file}', ':scalable=true:outline=true'],
                                    stdout=_subprocess.PIPE, stderr=_subprocess.DEVNULL, timeout=15).stdout.decode().strip()
        except (OSError, _subprocess.SubprocessError):
            found = ''
        if found and found.lower().endswith(('.ttf', '.otf')) and Path(found).is_file():
            return found
    return None


def scan_font(size):
    from PIL import ImageFont
    path = font_path()
    if path is None:
        raise unittest_skip('No TrueType font available for the synthetic scan')
    return ImageFont.truetype(path, size)


def unittest_skip(message):
    import unittest
    return unittest.SkipTest(message)


def gstreamer_available():
    try:
        import gi
        gi.require_version('Gst', '1.0')
        from gi.repository import Gst
        Gst.init(None)
        return all(Gst.ElementFactory.find(name) is not None for name in ('filesrc', 'decodebin', 'fakesink', 'audioconvert'))
    except (ImportError, ValueError):
        return False
