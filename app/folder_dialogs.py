"""GTK local folder shortcuts; a native folder picker can use desktop portals."""
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GLib
from local_files import read_folders, remember_folder, preferred_folder


def prepare_chooser(dialog, operation='open', source=None):
    folder = preferred_folder(operation,source)
    if folder:
        try:dialog.set_current_folder(folder)
        except GLib.Error:pass
    shortcut = read_folders().get('sync_folder')
    if shortcut:
        try:dialog.add_shortcut_folder(shortcut)
        except GLib.Error:pass


def remember_selection(path, operation='open'):
    if not path:return
    from pathlib import Path
    try:remember_folder('last_save' if operation=='save' else 'last_open',str(Path(path).parent))
    except (OSError,ValueError):pass  # An unavailable preference store must not prevent file access.


def choose_sync_folder(parent):
    dialog = Gtk.FileChooserNative.new('Escolher pasta local sincronizada',parent,
        Gtk.FileChooserAction.SELECT_FOLDER,'Usar esta pasta','Cancelar')
    dialog.set_modal(True);dialog.set_local_only(True)
    folder = preferred_folder()
    if folder:dialog.set_current_folder(folder)
    try:
        if dialog.run() != Gtk.ResponseType.ACCEPT:return None
        path = dialog.get_filename()
        if not path:raise ValueError('Selecione uma pasta local disponível pelo desktop.')
        remember_folder('sync_folder',path)
        return path
    finally:dialog.destroy()
