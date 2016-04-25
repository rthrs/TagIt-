#-*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import GdkPixbuf
import eyed3 


def sNone(obj):
  if obj is None:
    return ''
  else:
    return obj

def iNone(obj):
  if obj is None:
    return 0
  else:
    return obj

class TagEditor:

    builder = Gtk.Builder()
    def __init__(self, filename):
      self.filename = filename
      try:
        self.builder.add_from_file("edit.glade")
      except:
        print("file not found")
        sys.exit()

    def errorOpening(self):
        me = Gtk.MessageDialog(title = "Uups!",
                 message_type=Gtk.MessageType.ERROR, buttons = Gtk.ButtonsType.OK)
        me.format_secondary_text("Nie mogę otworzyć tego pliku. Sorki.")
        me.run()
        me.destroy()

    def cancel_callback(self, action, parameter):
      self.builder.get_object('tagEditor').destroy()

    def save_callback(self, action, fileh):
      fileh.tag.title = unicode(self.builder.get_object('title').get_text(), "UTF-8")
      fileh.tag.album = unicode(self.builder.get_object('album').get_text(), "UTF-8")
      fileh.tag.artist = unicode(self.builder.get_object('artist').get_text(), "UTF-8")
      year = int(self.builder.get_object('year_v').get_value())
      fileh.tag._setDate("TDRC", year)
      fileh.tag.original_release_date = eyed3.core.Date(year=year)
      fileh.tag.release_date = eyed3.core.Date(year=year)
      fileh.tag.track_num = (int(self.builder.get_object('track_v').get_value()), 
                             fileh.tag.track_num[1])
      fileh.tag.save()
      self.builder.get_object('tagEditor').destroy()

    def tagEditor(self):
      try:
        fileh = eyed3.load(self.filename)
      except:
        self.errorOpening()
        return

      if fileh.tag is None:
        self.errorOpening()
        return
      
      title = sNone(fileh.tag.title)
      album = sNone(fileh.tag.album)
      artist = sNone(fileh.tag.artist)
      date = fileh.tag.getBestDate()
      if date is None:
        date = eyed3.core.Date(year=1000)
      track = fileh.tag.track_num
      self.builder.get_object('title').set_text(title)
      self.builder.get_object('album').set_text(album)
      self.builder.get_object('artist').set_text(artist)
      self.builder.get_object('year_v').set_value(date.year)
      self.builder.get_object('track_v').set_value(iNone(track[0]))
      self.builder.get_object('cancel').connect('clicked', self.cancel_callback, None)
      self.builder.get_object('save').connect('clicked', self.save_callback, fileh)
      self.builder.get_object('tagEditor').show_all()

