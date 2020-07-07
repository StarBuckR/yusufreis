#!/usr/bin/env python

# found on <http://files.majorsilence.com/rubbish/pyGtk-book/pyGtk-notebook-html/pyGtk-notebook-latest.html#SECTION00430000000000000000>
# simple example of a tray icon application using PyGtk

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.set_from_icon_name('help-about')

        self.set_tooltip_text("Tray Icon")

        self.set_has_tooltip(True)
        self.set_visible(True)
        self.connect("popup_menu", self.on_secondary_click)
        self.connect("activate", self.on_click)

    def on_click(button, time):
        print("Left click")

    def on_secondary_click(self, widget, button, time):
        menu = Gtk.Menu()

        menu_item1 = Gtk.MenuItem("Send")
        menu_item1.connect("activate", self.on_send_click)
        menu.append(menu_item1)

        menu_item2 = Gtk.MenuItem("Quit")
        menu.append(menu_item2)
        menu_item2.connect("activate", Gtk.main_quit)

        menu.show_all()
        menu.popup(None, None, None, self, 3, time)
    
    def on_send_click(button, time):
        print("Send click")
    
if __name__ == '__main__':
    tray = TrayIcon()

    Gtk.main()