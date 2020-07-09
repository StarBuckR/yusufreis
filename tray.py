#!/usr/bin/env python

# found on <http://files.majorsilence.com/rubbish/pyGtk-book/pyGtk-notebook-html/pyGtk-notebook-latest.html#SECTION00430000000000000000>
# simple example of a tray icon application using PyGtk

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import pyscreenshot as ImageGrab

import gui

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)

        self.set_from_icon_name('help-about')

        self.set_tooltip_text("Tray Icon")

        self.set_has_tooltip(True)
        self.set_visible(True)
        self.connect("popup_menu", self.on_secondary_click)
        self.connect("activate", self.on_click)


        self.menu = Gtk.Menu()

        self.menu_item1 = Gtk.MenuItem("Send")
        self.menu_item1.connect("activate", self.on_send_click)
        self.menu.append(self.menu_item1)

        self.menu_item2 = Gtk.MenuItem("Quit")
        self.menu.append(self.menu_item2)
        self.menu_item2.connect("activate", Gtk.main_quit)

    def on_click(button, time):
        print("Left clicked")

    def on_secondary_click(self, widget, button, time):
        self.menu.show_all()
        self.menu.popup(None, None, None, self, 3, time)

    def on_send_click(self, button):
        print("Send clicked")

        image = ImageGrab.grab()
        image.save('image.jpg')

        self.gui_window = gui.Window()
        self.gui_window.show_popup_window()

if __name__ == '__main__':
    tray = TrayIcon()

    Gtk.main()