"""
  Animation module providing wrappers for tasks that might be 
  time-consuming and thus should be run simultaneously with some
  animation displayed to user.
"""
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
  """
    Base class for all kinds of animations.
  """
  builder = Gtk.Builder()

  def __init__(self, parent):
    try:
      self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/spinner.glade")
      self.parent = parent
    except:
      print("gtk builder error.")
      sys.exit()


class Spinner(Animation):
  """
    Class representing a single window with a spinner.
  """
  def show(self):
    self.builder.get_object("spinner").set_transient_for(self.parent)
    self.builder.get_object("spinner").show_all()

  def destroy(self):
    self.builder.get_object("spinner").destroy()


class Progress(Animation):
  """
    Class representing a single window with a progress bar.
  """
  def show(self):
    self.builder.get_object("progress").set_transient_for(self.parent)
    self.builder.get_object("progress").show_all()

  def destroy(self):
    self.builder.get_object("progress").destroy()


class HeavyWork:
  """
    Base class for ones that run specific task in a new thread.
  """
  def __init__(self, parent, todo, args, callback):
    """
      Takes parent window that displays list of files, particular task
      to do in a new thread, its arguments, and function that
      should be evoked after given task ends.
      [Callback] takes result of a task from thread 
      and arguments that task was given to thread-task.
    """
    self.todo = todo
    self.args = args
    self.callback = callback
    self.parent = parent

  def __end__(self, answer):
    """
      Callback function for the finished task.
    """
    if not self.aborted[0]:
      self.aborted[0] = True
      self.task.join()
      self.anim.destroy()
      self.parent.software_liststore.clear()
      self.parent.currentDir()
      self.callback(*((answer, ) + self.args))
    return False

  def __run__(self):
    self.aborted = [False]
    answer = self.todo(*self.args)
    GObject.idle_add(self.__end__, answer)


class WorkSpinner(HeavyWork):
  """
    Represents task for which should be displayed spinner.
  """
  def run(self):
    self.anim = Spinner(self.parent)
    self.anim.show()
    self.task = threading.Thread(target=self.__run__)
    self.task.deamon = True
    self.task.start()

class WorkProgress(HeavyWork):
  """
    Represents task for which progress bar should be displayed.
    Beyond standard arguments, task with progess bar should take
    two more args at the end: function that takes one argument - 
    float of current progess [0; 1] and a list with single bool 
    that is true when the task should be aborted if possible.
  """
  def __run__(self):
    self.aborted = [False]
    answer = self.todo(*(self.args + (self.update_bar, self.aborted)))
    GObject.idle_add(self.__end__, answer)

  def abort_cb(self, window):
    """
      Gtk signal callback - calls the run task to stop and waits 
      for its end; then closes the progess bar window. 
      Particularly hereafter status of progess bar won't be updated.
    """
    if not self.aborted[0]:
      print "Stop"
      self.aborted[0] = True
      self.task.join()
      print "it now"
      self.anim.destroy()

  def update_bar(self, fraction):
    print str(fraction)
    GObject.idle_add(self.anim.builder.get_object("bar").set_fraction, fraction)

  def run(self):
    self.anim = Progress(self.parent)
    self.anim.show()
    self.anim.builder.get_object("progress").connect("destroy", self.abort_cb)
    self.anim.builder.get_object("abort").connect("clicked", self.abort_cb)
    self.task = threading.Thread(target=self.__run__)
    self.task.deamon = True
    self.task.start()
