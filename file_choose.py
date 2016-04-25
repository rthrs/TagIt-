#-*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
import sys
import tag
import edit
import pylab
import collection
from gi.repository import GdkPixbuf
pixbuf = GdkPixbuf.Pixbuf.new_from_file('logo.png')


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(
            self, title="TagIt!", application=app)
        self.set_default_size(500, 400)
        self.set_icon_from_file('icon_cpy.png')

        # the actions for the window menu, connected to the callback functions

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.open_callback)
        self.add_action(open_action)
        
        dir_open_action = Gio.SimpleAction.new("dir_open", None)
        dir_open_action.connect("activate", self.dir_open_callback)
        self.add_action(dir_open_action)
        
        col_open_action = Gio.SimpleAction.new("col_open", None)
        col_open_action.connect("activate", self.col_open_callback)
        self.add_action(col_open_action)
        
        settings_action = Gio.SimpleAction.new("tagEdit", None)
        settings_action.connect("activate", self.tagEdit_callback)
        self.add_action(settings_action)
                
        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.settings_callback)
        self.add_action(settings_action)

        # action with a state created
        about_action = Gio.SimpleAction.new("about", None)
        # action connected to the callback function
        about_action.connect("activate", self.about_callback)
        # action added to the application
        self.add_action(about_action)

        img = Gtk.Image()
        
        img.set_from_file("bg_light.png") 
        self.add(img)

    # callback function for tagEditor
    def tagEdit_callback(self, action, parameter):
      dialog = Gtk.FileChooserDialog(title="Wybierz plik",
               action=Gtk.FileChooserAction.OPEN,
               buttons=["Otwórz", Gtk.ResponseType.OK, 
              "Powrót", Gtk.ResponseType.CANCEL])

      filter = Gtk.FileFilter()
      filter.set_name("Pliki mp3")
      filter.add_pattern("*.mp3")
      dialog.add_filter(filter)

      response = dialog.run()
      filename = dialog.get_filename()
      dialog.destroy() 
      if response == Gtk.ResponseType.OK:
        edit.TagEditor(filename).tagEditor()
                
    # callback function for about (see the AboutDialog example)
    def about_callback(self, action, parameter):
        # a  Gtk.AboutDialog
        aboutdialog = Gtk.AboutDialog()

        # lists of authors and documenters (will be used later)
        authors = ["TagIt! Team"]
        documenters = ["TagIt! Team"]

        # we fill in the aboutdialog
        aboutdialog.set_program_name("TagIt!")
        aboutdialog.set_copyright(
            "Copyright \xc2\xa9 2016 TagIt! Team")
        aboutdialog.set_authors(authors)
        aboutdialog.set_documenters(documenters)
        aboutdialog.set_comments('Aplikacja umożliwiająca wygodne, '
        +'automatyczne tagowanie i nazywanie plików z muzyką, zapewniająca '
        +'przejrzystość w folderach. Dzięki niej można łatwo odnaleźć konkretny'
        +' utwór, czy też wszystkie utwory danego wykonawcy.')        
        aboutdialog.set_logo(pixbuf)
        aboutdialog.set_icon_from_file('icon_cpy.png')

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        aboutdialog.show()

    # a callback function to destroy the aboutdialog
    def on_close(self, action, parameter):
        action.destroy()

    # callback for settings
    def settings_callback(self, action, parameter):
        self.buffer.set_text("")
        print("Settings opened")

    # callback for open
    def open_callback(self, action, parameter):
        # create a filechooserdialog to open:
        # the arguments are: title of the window, parent_window, action,
        # (buttons, response)
        open_dialog = Gtk.FileChooserDialog("Pick a file", self,
                                            Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        # not only local files can be selected in the file selector
        open_dialog.set_local_only(False)
        # dialog always on top of the textview window
        open_dialog.set_modal(True)
        # connect the dialog with the callback function open_response_cb()
        open_dialog.connect("response", self.open_response_cb)
        # show the dialog
        open_dialog.show()

    # callback function for the dialog open_dialog
    def open_response_cb(self, dialog, response_id):
        open_dialog = dialog
        # if response is "ACCEPT" (the button "Open" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            res = tag.tagFile(open_dialog.get_filename())
            if res == -1:
				printf("file not found in our database")
            else:
				print("tagged: " + open_dialog.get_filename())
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.OPEN")
        # destroy the FileChooserDialog
        dialog.destroy()
        
    # callback for open a directory
    def dir_open_callback(self, action, parameter):
        # create a filechooserdialog to open:
        # the arguments are: title of the window, parent_window, action,
        # (buttons, response)
        dir_open_dialog = Gtk.FileChooserDialog("Pick a directory", self,
                                            Gtk.FileChooserAction.SELECT_FOLDER,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        # not only local files can be selected in the file selector
        dir_open_dialog.set_local_only(False)
        # dialog always on top of the textview window
        dir_open_dialog.set_modal(True)
        # connect the dialog with the callback function open_response_cb()
        dir_open_dialog.connect("response", self.dir_open_response_cb)
        # show the dialog
        dir_open_dialog.show()

    # callback function for the dialog dir_open_dialog
    def dir_open_response_cb(self, dialog, response_id):
        dir_open_dialog = dialog
        # if response is "ACCEPT" (the button "Open" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            # an empty string (provisionally)
            tag.tagFolder(dir_open_dialog.get_filename())
            print("tagged: " + dir_open_dialog.get_filename())
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.OPEN")
        # destroy the FileChooserDialog
        dialog.destroy()
        
    # callback for creatinc collection
    def col_open_callback(self, action, parameter):
        # create a filechooserdialog to open:
        # the arguments are: title of the window, parent_window, action,
        # (buttons, response)
        col_open_dialog = Gtk.FileChooserDialog("Pick a directory", self,
                                            Gtk.FileChooserAction.SELECT_FOLDER,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        # not only local files can be selected in the file selector
        col_open_dialog.set_local_only(False)
        # dialog always on top of the textview window
        col_open_dialog.set_modal(True)
        # connect the dialog with the callback function open_response_cb()
        col_open_dialog.connect("response", self.col_open_response_cb)
        # show the dialog
        col_open_dialog.show()

    # callback function for the dialog col_open_dialog
    def col_open_response_cb(self, dialog, response_id):
        col_open_dialog = dialog
        # if response is "ACCEPT" (the button "Open" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            # an empty string (provisionally)
            collection.createCollection(col_open_dialog.get_filename())
            print("new collection in: " + col_open_dialog.get_filename())
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.OPEN")
        # destroy the FileChooserDialog
        dialog.destroy()


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # app action quit, connected to the callback function
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_callback)
        self.add_action(quit_action)

        # get the menu from the ui file with a builder
        builder = Gtk.Builder()
        try:
            builder.add_from_file("filechooserdialog.ui")
        except:
            print("file not found")
            sys.exit()
        menu = builder.get_object("menubar")
        self.set_menubar(builder.get_object("menubar"))

    # callback function for quit
    def quit_callback(self, action, parameter):
        self.quit()

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
