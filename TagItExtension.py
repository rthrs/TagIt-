#-*- coding: utf-8 -*-
"""
    Context menu extension for nautilus that enables either clicked song
    or directory tagging. Paste this file to the following directory:
    ~/.local/share/nautilus-python/extensions

    Crate directory if not exists (while TagIt! installation process) using:
    os.makedirs(expanduser('~/.local/share/nautilus-python/extensions'))
"""
from gi.repository import Nautilus, GObject, Gtk
import os
import sys
sys.path.insert(0, "/home/rth/Github/TagIt")
import tag
import edit
import animation

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def file_done(self, answer, path):
        me = None
        if answer == 0:
            me = edit.info("Udało się", "Plik został otagowany.")
        else:
            me = edit.info("Uups", "Coś poszło nie tak")
        me.run()
        me.destroy()

    def dir_done(self, answer, path):
        s = ""
        for file in answer:
            s += "\n" + file
        if len(answer) > 0:
            me = edit.info("Zakończono tagowanie", "Liczba pominiętych plików: " + str(len(answer)))
            print "Pominięto: " + s
        else:
            me = edit.info("Zakończono tagowanie", "Pomyślnie otagowano wszystkie pliki!")
        me.run()
        me.destroy()

    def menu_activate_cb(self, menu, file):
        path = file.get_location().get_path()
        #win = Gtk.ApplicationWindow()
        if file.is_directory():
            ret = tag.tagFolder(path)
            self.dir_done(ret, path)
            #w = animation.WorkProgress(win, tag.tagFolder, (path,), self.dir_done)
            #w.run()
        else:
            ret = tag.tagFile(path)
            self.file_done(ret, path)
            #h = animation.WorkSpinner(win, tag.tagFile, (path,), self.file_done)
            #h.run()
        #win.destroy()

    def get_file_items(self, window, files):
        if len(files) != 1:
            return

        file = files[0]
        name, ext = os.path.splitext(file.get_name())
        valid_exts = [".mp3"]

        if file.is_directory() or ext in valid_exts:
            item = Nautilus.MenuItem(
                name="SimpleMenuExtension::TagIt!",
                label="TagIt!",
                tip="TagIt!"
            )
            item.connect('activate', self.menu_activate_cb, file)

            return [item]
