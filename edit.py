# -*- coding: utf-8 -*-
"""
    Graphical interface for manual tag editor.
"""

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import GdkPixbuf
import eyed3
import edit
import settings
import sys


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
    """
        Every instance of this class creates window that enables
        user to manually change tags for given file. Requires
        filepath passed to constructor.
    """
    builder = Gtk.Builder()

    def __init__(self, filename):
        self.filename = filename
        try:
            self.builder.add_from_file("edit.glade")
        except:
            print("file not found")
            sys.exit()

    def errorOpening(self):
        me = Gtk.MessageDialog(title="Uups!",
                               message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK)
        me.format_secondary_text("Nie mogę otworzyć tego pliku. Sorki.")
        me.run()
        me.destroy()

    def cancel_callback(self, action, parameter):
        self.builder.get_object('tagEditor').destroy()

    def save_callback(self, action, fileh):
        title = unicode(self.builder.get_object('title').get_text(), "UTF-8")
        album = unicode(self.builder.get_object('album').get_text(), "UTF-8")
        artist = unicode(self.builder.get_object('artist').get_text(), "UTF-8")
        if "" in [title, album, artist]:
            me = edit.info("Ups", "Pola nie mogą pozostać puste.")
            me.run()
            me.destroy()
        else:
            fileh.tag.title = title 
            fileh.tag.album = album
            fileh.tag.artist = artist
            year = int(self.builder.get_object('year_v').get_value())
            if self.builder.get_object('year_active').get_active():
                print year
                fileh.tag._setDate("TDRC", year)
                fileh.tag.original_release_date = eyed3.core.Date(year=year)
                fileh.tag.release_date = eyed3.core.Date(year=year)
            fileh.tag.track_num = (int(self.builder.get_object('track_v').get_value()),
                                       fileh.tag.track_num[1])
            fileh.tag.save()
            settings.rename(fileh.path, fileh.tag.artist, fileh.tag.title, fileh.tag.album, '.mp3')
            self.win.software_liststore.clear()
            self.win.currentDir()
        self.builder.get_object('tagEditor').destroy()

    def toggle_year_cb(self, action):
        state = self.builder.get_object('year_active').get_active()
        self.builder.get_object('year').set_editable(state)

    def tagEditor(self, win):
        """
          Shows editor's window.
        """
        try:
            fileh = eyed3.load(self.filename)
        except:
            self.errorOpening()
            return

        if fileh.tag is None:
            self.errorOpening()
            return
        
        self.win = win

        title = sNone(fileh.tag.title)
        album = sNone(fileh.tag.album)
        artist = sNone(fileh.tag.artist)
        date = fileh.tag.getBestDate()
        self.builder.get_object('year_active').connect('toggled',
                     self.toggle_year_cb)
        if date is not None:
            self.builder.get_object('year_active').set_active(True)
            self.builder.get_object('year_v').set_value(date.year)
        else:
            self.builder.get_object('year').set_editable(False)
        track = fileh.tag.track_num
        self.builder.get_object('title').set_text(title)
        self.builder.get_object('album').set_text(album)
        self.builder.get_object('artist').set_text(artist)
        self.builder.get_object('track_v').set_value(iNone(track[0]))
        self.builder.get_object('cancel').connect('clicked', self.cancel_callback, None)
        self.builder.get_object('save').connect('clicked', self.save_callback, fileh)
        self.builder.get_object('tagEditor').show_all()


# Messages

def info(title, message):
    me = Gtk.MessageDialog(title=title,
                           message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK)
    me.format_secondary_text(message)
    return me


def ups_quest(title, message):
    me = Gtk.MessageDialog(title=title,
                           message_type=Gtk.MessageType.QUESTION, buttons=
                           ["Tak", Gtk.ResponseType.OK,
                            "Zignoruj", Gtk.ResponseType.CANCEL])
    me.format_secondary_text(message)
    return me
