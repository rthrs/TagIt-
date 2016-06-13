import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
import sys
import os
import threading

class Animation(Gtk.Window):

  builder = Gtk.Builder()

  def __init__(self, parent):
    try:
      self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/spinner.glade")
      self.parent = parent
    except:
      print("file not found")
      sys.exit()


class Spinner(Animation):

    def show(self):
      self.builder.get_object("spinner").set_transient_for(self.parent)
      self.builder.get_object("spinner").show_all()

    def destroy(self):
      self.builder.get_object("spinner").destroy()


class Progress(Animation):

    def show(self):
      self.builder.get_object("progress").set_transient_for(self.parent)
      self.builder.get_object("progress").show_all()

    def destroy(self):
      self.builder.get_object("progress").destroy()


class HeavyWork:

  def __init__(self, parent, todo, args, callback):
    self.todo = todo
    self.args = args
    self.callback = callback
    self.parent = parent

  def __end__(self, answer):
    if not self.aborted[0]:
      self.aborted[0] = True
      self.t.join()
      self.s.destroy()
      self.parent.software_liststore.clear()
      self.parent.currentDir()
      self.callback(*((answer, ) + self.args))
    return False

  def __run__(self):
    self.aborted = [False]
    answer = self.todo(*self.args)
    GObject.idle_add(self.__end__, answer)


class WorkSpinner(HeavyWork):

  def run(self):
    self.s = Spinner(self.parent)
    self.s.show()
    self.t = threading.Thread(target=self.__run__)
    self.t.deamon = True
    self.t.start()

class WorkProgress(HeavyWork):

  def __run__(self):
    self.aborted = [False]
    answer = self.todo(*(self.args + (self.update_bar, self.aborted)))
    GObject.idle_add(self.__end__, answer)

  def abort_cb(self, window):
    if not self.aborted[0]:
      print "Stop"
      self.aborted[0] = True
      self.t.join()
      print "it now"
      self.s.destroy()

  def update_bar(self, fraction):
    print str(fraction) + " kek"
    GObject.idle_add(self.s.builder.get_object("bar").set_fraction, fraction)

  def run(self):
    self.s = Progress(self.parent)
    self.s.show()
    self.s.builder.get_object("progress").connect("destroy", self.abort_cb)
    self.s.builder.get_object("abort").connect("clicked", self.abort_cb)
    self.t = threading.Thread(target=self.__run__)
    self.t.deamon = True
    self.t.start()
