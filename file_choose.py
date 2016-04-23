#-*- coding: utf-8 -*-
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
from gi.repository import GdkPixbuf
import sys


class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(
            self, title="TagIt!", application=app)
        self.set_default_size(500, 400)

        # the actions for the window menu, connected to the callback functions
        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.new_callback)
        self.add_action(new_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.open_callback)
        self.add_action(open_action)
        
        dir_open_action = Gio.SimpleAction.new("dir_open", None)
        dir_open_action.connect("activate", self.dir_open_callback)
        self.add_action(dir_open_action)

        save_action = Gio.SimpleAction.new("save", None)
        save_action.connect("activate", self.save_callback)
        self.add_action(save_action)

        save_as_action = Gio.SimpleAction.new("save-as", None)
        save_as_action.connect("activate", self.save_as_callback)
        self.add_action(save_as_action)
        
        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.settings_callback)
        self.add_action(settings_action)
        
        # action with a state created
        about_action = Gio.SimpleAction.new("about", None)
        # action connected to the callback function
        about_action.connect("activate", self.about_callback)
        # action added to the application
        self.add_action(about_action)
        
        # the file
        self.file = None

        # the textview with the buffer
        self.buffer = Gtk.TextBuffer()
        textview = Gtk.TextView(buffer=self.buffer)
        textview.set_wrap_mode(Gtk.WrapMode.WORD)

        # a scrolled window for the textview
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.add(textview)
        self.scrolled_window.set_border_width(5)

        # add the scrolled window to the window
        self.add(self.scrolled_window)
        
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
        aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file('logo.jpg'))

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        aboutdialog.show()

    # a callback function to destroy the aboutdialog
    def on_close(self, action, parameter):
        action.destroy()

    # callback for new
    def new_callback(self, action, parameter):
        self.buffer.set_text("")
        print("New file created")

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
            # self.file is the file that we get from the FileChooserDialog
            self.file = open_dialog.get_file()
            # an empty string (provisionally)
            content = ""
            try:
                # load the content of the file into memory:
                # success is a boolean depending on the success of the operation
                # content is self-explanatory
                # etags is an entity tag (can be used to quickly determine if the
                # file has been modified from the version on the file system)
                [success, content, etags] = self.file.load_contents(None)
            except GObject.GError as e:
                print("Error: " + e.message)
            # set the content as the text into the buffer
            self.buffer.set_text(content, len(content))
            print("opened: " + open_dialog.get_filename())
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
            # self.file is the file that we get from the FileChooserDialog
            #self.file = dir_open_dialog.get_current_folder_file()
            # an empty string (provisionally)
            #content = ""
            #try:
                # load the content of the file into memory:
                # success is a boolean depending on the success of the operation
                # content is self-explanatory
                # etags is an entity tag (can be used to quickly determine if the
                # file has been modified from the version on the file system)
            #   [success, content, etags] = self.file.load_contents(None)
            #except GObject.GError as e:
            #    print("Error: " + e.message)
            # set the content as the text into the buffer
            #self.buffer.set_text(content, len(content))
            print("opened: " + dir_open_dialog.get_filename())
            
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.OPEN")
        # destroy the FileChooserDialog
        dialog.destroy()

    # callback function for save_as
    def save_as_callback(self, action, parameter):
        # create a filechooserdialog to save:
        # the arguments are: title of the window, parent_window, action,
        # (buttons, response)
        save_dialog = Gtk.FileChooserDialog("Pick a file", self,
                                            Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
        # the dialog will present a confirmation dialog if the user types a file name that
        # already exists
        save_dialog.set_do_overwrite_confirmation(True)
        # dialog always on top of the textview window
        save_dialog.set_modal(True)
        # if self.file has already been saved
        if self.file is not None:
            try:
                # set self.file as the current filename for the file chooser
                save_dialog.set_file(self.file)
            except GObject.GError as e:
                print("Error: " + e.message)
        # connect the dialog to the callback function save_response_cb()
        save_dialog.connect("response", self.save_response_cb)
        # show the dialog
        save_dialog.show()

    # callback function for the dialog save_dialog
    def save_response_cb(self, dialog, response_id):
        save_dialog = dialog
        # if response is "ACCEPT" (the button "Save" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            # self.file is the currently selected file
            self.file = save_dialog.get_file()
            # save to file (see below)
            self.save_to_file()
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.SAVE")
        # destroy the FileChooserDialog
        dialog.destroy()

    # callback function for save
    def save_callback(self, action, parameter):
        # if self.file is not already there
        if self.file is not None:
            self.save_to_file()
        # self.file is a new file
        else:
            # use save_as
            self.save_as_callback(action, parameter)

    # save_to_file
    def save_to_file(self):
        # get the content of the buffer, without hidden characters
        [start, end] = self.buffer.get_bounds()
        current_contents = self.buffer.get_text(start, end, False)
        # if there is some content
        if current_contents != "":
            # set the content as content of self.file.
            # arguments: contents, etags, make_backup, flags, GError
            try:
                self.file.replace_contents(current_contents,
                                           None,
                                           False,
                                           Gio.FileCreateFlags.NONE,
                                           None)
                print("saved: " + self.file.get_path())
            except GObject.GError as e:
                print("Error: " + e.message)
        # if the contents are empty
        else:
            # create (if the file does not exist) or overwrite the file in readwrite mode.
            # arguments: etags, make_backup, flags, GError
            try:
                self.file.replace_readwrite(None,
                                            False,
                                            Gio.FileCreateFlags.NONE,
                                            None)
                print("saved: " + self.file.get_path())
            except GObject.GError as e:
                print("Error: " + e.message)


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
