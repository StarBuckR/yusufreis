#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import pyscreenshot as ImageGrab

import gui, message, summary
import subprocess, gettext, sys

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)

        self.set_from_icon_name('help-about')
        self.set_tooltip_text(_("Tray Icon"))

        self.set_has_tooltip(True)
        self.set_visible(True)
        self.connect("popup_menu", self.on_secondary_click)
        self.connect("activate", self.on_click)

        self.menu = Gtk.Menu()

        self.menu_item1 = Gtk.MenuItem(_("Summary"))
        self.menu_item1.connect("activate", self.on_summary_click)
        self.menu.append(self.menu_item1)

        self.menu_item1 = Gtk.MenuItem(_("Send"))
        self.menu_item1.connect("activate", self.on_send_click)
        self.menu.append(self.menu_item1)

        self.menu_item2 = Gtk.MenuItem(_("Quit"))
        self.menu.append(self.menu_item2)
        self.menu_item2.connect("activate", Gtk.main_quit)

    def on_click(self, button, time):
        print(_("Left clicked"))

    def on_summary_click(self, button):
        summary.Summary()

    def on_secondary_click(self, widget, button, time):
        self.menu.show_all()
        self.menu.popup(None, None, None, self, 3, time)

    def on_send_click(self, button):
        print(_("Send clicked"))

        image = ImageGrab.grab()
        image.save('image.jpg')

        self.gui_window = gui.Window()
        self.gui_window.show_popup_window()

def control():
    username = subprocess.getoutput("whoami")
    base_dir = subprocess.getoutput("getent passwd " + username + " | awk -F: ' { print $6} '")
    domain_name = subprocess.getoutput("dnsdomainname")
    
    if domain_name in base_dir:
        return True
    else:
        return False

if __name__ == '__main__':
    tray = TrayIcon()

    Gtk.main()
