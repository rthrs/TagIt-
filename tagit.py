#-*- coding: utf-8 -*-
"""
  TagIt! GUI.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GObject
GObject.threads_init()
import sys
import tag
import edit
#import pylab
import settings
import collection
from gi.repository import GdkPixbuf
pixbuf = GdkPixbuf.Pixbuf.new_from_file('img/logo.png')
import gi
gi.require_version('Gtk', '3.0')
import os
import animation
from gi.repository.GdkPixbuf import Pixbuf

icons = ["go-previous","edit-cut", "edit-paste", "edit-copy"]

class MyWindow(Gtk.ApplicationWindow):
    path = "/home"



    def currentDir(self):
        for x in os.listdir(self.path):
            if x[0] != '.' and os.path.isdir(self.path + "/" + x):
                self.software_liststore.append([x, "folder"])
        for x in os.listdir(self.path):
            if x[0] != '.' and os.path.isfile(self.path + "/" + x) and os.path.splitext(x)[1] in (".mp3"):
                self.software_liststore.append([x, "audio-x-generic"])
                
    def __init__(self, app):
        Gtk.Window.__init__(self, title="TagIt!", application=app)
        self.set_default_size(900, 700)
        self.set_border_width(5)
        self.set_icon_from_file('img/icon_cpy.png')

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, str)
        self.currentDir()


        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(model=self.software_liststore)
        
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("", renderer_pixbuf, icon_name=1)
        Gtk.TreeViewColumn.set_fixed_width(column_pixbuf, 1)
        self.treeview.append_column(column_pixbuf)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Nazwa", renderer_text, text=0)
        self.treeview.append_column(column_text)        


        #get double clicks
        self.treeview.connect("row-activated", self.on_double_click);

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        pixbuf = Gtk.IconTheme.get_default().load_icon(icons[0], 64, 0)
        button = Gtk.Button.new_from_icon_name("go-previous", 4)
        self.buttons.append(button)
        #counter = 0
        for i in ["Otaguj automatycznie", "Otaguj recznie"]:
            if os.path.isdir and i=="Otaguj recznie":
                button = Gtk.Button("nic tu nie ma")
                self.buttons.append(button)
            else:
                button = Gtk.Button(i)
                #counter += 1
                self.buttons.append(button)
                
        self.buttons[0].connect("clicked", self.on_selection_button_clicked)
        self.buttons[1].connect("clicked", self.ButtonAutoTag_callback)
        #if counter == 2:
        self.buttons[2].connect("clicked", self.ButtonTagEdit_callback)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 2, 10)
        
        frame = Gtk.Frame(label="label")
        box = Gtk.Box()
        miniMenu = Gtk.Box()

                
        self.grid.attach_next_to(frame, self.scrollable_treelist, Gtk.PositionType.RIGHT, 2, 8)        
        #self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)        
        
        self.grid.attach_next_to(box, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        box.add(self.buttons[0])
        box.set_border_width(15)


        miniMenu.add(self.buttons[1])
        #if counter == 2:
        miniMenu.add(self.buttons[2])
        miniMenu.set_border_width(10)
                
        self.grid.attach_next_to(miniMenu, frame, Gtk.PositionType.BOTTOM, 1, 1)
        #self.grid.attach_next_to(self.buttons[2], self.buttons[1], Gtk.PositionType.BOTTOM, 1, 1)
        #for i, button in enumerate(self.buttons[2:]):
        #    self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.BOTTOM, 1, 1)
        self.scrollable_treelist.add(self.treeview)


        # the actions for the window menu, connected to the callback functions
        col_open_action = Gio.SimpleAction.new("col_open", None)
        col_open_action.connect("activate", self.col_open_callback)
        self.add_action(col_open_action)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.open_callback)
        self.add_action(open_action)
        
        dir_open_action = Gio.SimpleAction.new("dir_open", None)
        dir_open_action.connect("activate", self.dir_open_callback)
        self.add_action(dir_open_action)
        
        settings_action = Gio.SimpleAction.new("settings", None)
        settings_action.connect("activate", self.settings_callback)
        self.add_action(settings_action)
        
        settings_action = Gio.SimpleAction.new("tagEdit", None)
        settings_action.connect("activate", self.tagEdit_callback)
        self.add_action(settings_action)

        ButtonTagEdit_action = Gio.SimpleAction.new("ButtonTagEdit", None)
        ButtonTagEdit_action.connect("activate", self.ButtonTagEdit_callback)
        self.add_action(ButtonTagEdit_action)

        ButtonAutoTag_action = Gio.SimpleAction.new("ButtonAutoTag", None)
        ButtonAutoTag_action.connect("activate", self.ButtonAutoTag_callback)
        self.add_action(ButtonAutoTag_action)
                
        settings_action = Gio.SimpleAction.new("change_format", None)
        settings_action.connect("activate", settings.change_format)
        self.add_action(settings_action)

        # action with a state created
        about_action = Gio.SimpleAction.new("about", None)
        # action connected to the callback function
        about_action.connect("activate", self.about_callback)
        # action added to the application
        self.add_action(about_action)        


        self.show_all()

    def getFilePath(self):
        model, it = self.treeview.get_selection().get_selected()
        #sprawdzic, czy przypadkiem nie   [1]  !!!
        return self.path + "/" + model[it][0]

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        

        self.software_liststore.clear()
        self.path = os.path.split(self.path)[0]
        self.buttons[2].set_label("zmienilem sie")
        print("powinienem sie zmienic :c")
        self.currentDir()
        
    def on_double_click(self, widget, c, d):
        model, it = widget.get_selection().get_selected()
        print(model[it][0])
        if os.path.isdir(self.path + "/" + model[it][0]):
            self.path = self.path + "/" + model[it][0]
            self.software_liststore.clear()
            self.currentDir()
        
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

    
    #callback function for colection creating
    def col_open_done(self, answer, path):
        succ, un, t = answer
        s = ""
        for file in un:
            s += "\n" + file
        if succ > 0:
            me = edit.info("Zokończono tagowanie", "Liczba pominiętych plików: " + str(len(un)) + "\nOtagowanych: " + str(len(t)))
            print "Pominięto: " + s
        else:
          me = edit.info("Uups", "Coś poszło nie tak")
        me.run()
        me.destroy()


    # callback function for the dialog col_open_dialog
    def col_open_response_cb(self, dialog, response_id):
        col_open_dialog = dialog
        # if response is "ACCEPT" (the button "Open" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            # an empty string (provisionally)
            w = animation.WorkProgress(self, collection.createCollection, (col_open_dialog.get_filename(), ), self.col_open_done)
            w.run()
            print("new collection in: " + col_open_dialog.get_filename())
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            print("cancelled: FileChooserAction.OPEN")
        # destroy the FileChooserDialog
        dialog.destroy()


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

    # callback function for BUTTON tagEditor
    def ButtonTagEdit_callback(self, widget):    
        filename = self.getFilePath()
        print(filename) 
        edit.TagEditor(filename).tagEditor()
        
    # callback function for BUTTON  AutoTag
    def ButtonAutoTag_callback(self, widget):    
        filename = self.getFilePath()
        print(filename)
        if os.path.isdir(filename):
            print("It's directory")
        else:
            h = animation.WorkSpinner(self, tag.tagFile, (filename,), self.open_response_cb_done)
            h.run()
                        
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
        aboutdialog.set_icon_from_file('img/icon_cpy.png')

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
    
    def open_response_cb_done(self, answer, path):
      if answer == 0:
        me = edit.info("Udało się", "Plik został otagowany.")
        me.run()
        me.destroy()
      else:
        me = edit.ups_quest("Coś poszło nie tak.", "Czy chcesz poprawić tagi ręcznie?")
        response = me.run()
        me.destroy()
        if response == Gtk.ResponseType.OK:
          edit.TagEditor(path).tagEditor()


    # callback function for the dialog open_dialog
    def open_response_cb(self, dialog, response_id):
        """
            Callback function for the dialog open_dialog.
        """
        open_dialog = dialog
        # if response is "ACCEPT" (the button "Open" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            print("opened: " + open_dialog.get_filename())
            h = animation.WorkSpinner(self, tag.tagFile, (open_dialog.get_filename(),), self.open_response_cb_done)
            dialog.destroy()
            h.run()
                 
        # if response is "CANCEL" (the button "Cancel" has been clicked)
        elif response_id == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            print("cancelled: FileChooserAction.OPEN")
        # destroy the FileChooserDialog


    def dir_open_done(self, answer, path):
      s = ""
      for file in answer:
        s += "\n" + file
      if len(answer) > 0:
        me = edit.info("Zokończono tagowanie", "Liczba pominiętych plików: " + str(len(answer)))
        print "Pominięto: " + s
      else:
        me = edit.info("Zakończono tagowaniue", "Pomyślnie otagowano wszystkie pliki!")
      me.run()
      me.destroy()


    # callback function for the dialog dir_open_dialog
    def dir_open_response_cb(self, dialog, response_id):
        """
            Callback function for the dialog dir_open_dialog.
        """
        dir_open_dialog = dialog
        # if response is "ACCEPT" (the button "Open" has been clicked)
        if response_id == Gtk.ResponseType.ACCEPT:
            # an empty string (provisionally)
            w = animation.WorkProgress(self, tag.tagFolder, (dir_open_dialog.get_filename(), ), self.dir_open_done)
            w.run()
            #tag.tagFolder(dir_open_dialog.get_filename())
            print("opened: " + dir_open_dialog.get_filename())
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
        
'''

win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
'''

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
