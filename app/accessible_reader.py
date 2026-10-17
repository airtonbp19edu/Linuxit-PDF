"""Read-only GTK text snapshot through ATK.Text; no speech, OCR or reading-order claim."""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Atk', '1.0')
from gi.repository import Gtk, Atk
from async_core import BackgroundRunner
from cancel_state import get_event
from pdf_security import invoke_accessible_text


class AccessibleTextWindow(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title='Texto da página', transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(700, 500)
        self.runner = BackgroundRunner(workers=1);self.closed = False
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8);box.set_border_width(12);self.add(box)
        self.heading = Gtk.Label(xalign=0);box.pack_start(self.heading, False, False, 0)
        hint = Gtk.Label(label='Texto extraído sem OCR. A ordem pode diferir da leitura visual.', xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint, False, False, 0)
        self.text = Gtk.TextView();self.text.set_editable(False);self.text.set_cursor_visible(True);self.text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text.get_accessible().set_name('Texto extraído da página PDF')
        scroll = Gtk.ScrolledWindow();scroll.add(self.text);box.pack_start(scroll, True, True, 0)
        self.status = Gtk.Label(xalign=0);self.status.set_line_wrap(True)
        self.status.get_accessible().set_role(Atk.Role.STATUSBAR);box.pack_start(self.status, False, False, 0)
        close = Gtk.Button(label='Fechar');close.connect('clicked', lambda *_:self.destroy());box.pack_start(close, False, False, 0)
        self.connect('destroy', self._destroy)

    def load(self, path, page, total):
        self.heading.set_text(f'Página {page + 1} de {total}')
        self.text.get_buffer().set_text('');self.status.set_text('Extraindo texto…')
        def task():
            return invoke_accessible_text(path, page, get_event())
        def done(text):
            if text is None:return
            self.text.get_buffer().set_text(text)
            self.status.set_text('Texto disponível para teclado e tecnologia assistiva.' if text.strip() else 'Esta página não forneceu texto. OCR não está incluído.')
            self.text.grab_focus()
        self.runner.submit('accessible-text', task, done, lambda e:self.status.set_text(str(e)), priority='background')

    def _destroy(self, *_):
        self.closed = True;self.runner.shutdown()
