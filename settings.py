## @package settings
#  Graphical interface for settings.
##

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import GdkPixbuf
import os
import sys

_name_option = 1


def rename(path, artist, title, album, fileExtension):
    if _name_option == 1:
        filename = artist + " - " + title
    elif _name_option == 2:
        filename = title + " - " + artist
    else:
        filename = title + " - " + artist + " - " + album
    os.rename(path, os.path.dirname(path) + "/" + filename + fileExtension)
    return os.path.dirname(path) + "/" + filename + fileExtension


def save_format_callback(action, builder, mainwin=None):
    checks = [builder.get_object('artist_title'),
              builder.get_object('title_artist'),
              builder.get_object('title_artist_album')]
    for i in range(len(checks)):
        if checks[i].get_active():
            global _name_option
            _name_option = i + 1
    if mainwin is None:
        builder.get_object('format_window').destroy()


def change_format(action, parameter):
    """
        Shows format costumizer's window.
    """
    builder = Gtk.Builder()
    try:
        builder.add_from_file("format.glade")
    except:
        print("file not found")
        sys.exit()
    checks = [builder.get_object('artist_title'),
              builder.get_object('title_artist'),
              builder.get_object('title_artist_album')]
    checks[_name_option - 1].set_active(True)
    builder.get_object('ok_button').connect('clicked', save_format_callback, builder)
    builder.get_object('format_window').show_all()
