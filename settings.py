from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import GdkPixbuf
import os


_name_option = 1

def rename(path, artist, title, album, fileExtension):
  if _name_option == 1:
    filename = artist + " - " + title
  elif _name_option == 2:
    filename = title + " - " + artist
  else: 
    filename = title + " - " + artist + " - " + album
  os.rename(path, os.path.dirname(path) + "/" + filename + fileExtension)
