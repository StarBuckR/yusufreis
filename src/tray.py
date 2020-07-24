#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

import pyscreenshot as ImageGrab

import send, message, summary, controls, notifications
import subprocess, gettext, sys

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext


class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)

        self.set_from_file(summary.MAINDIR + "images/no-notification.png")
        self.set_tooltip_text(_("Tray Icon"))

        self.set_has_tooltip(True)
        self.set_visible(True)
        self.connect("popup_menu", self.on_secondary_click)
        self.connect("activate", self.on_click)

    def on_secondary_click(self, widget, button, time):
        self.menu = Gtk.Menu()

        self.notifications_label = Gtk.Label(_("Notifications") + "({})".format(notifications_window.count))
        self.notifications_menu_item = Gtk.MenuItem(self.notifications_label.get_text())
        self.notifications_menu_item.connect("activate", self.on_notifications_click)
        self.menu.append(self.notifications_menu_item)

        self.menu_item1 = Gtk.MenuItem(label=_("Summary"))
        self.menu_item1.connect("activate", self.on_summary_click)
        self.menu.append(self.menu_item1)

        self.menu_item1 = Gtk.MenuItem(label=_("Controls"))
        self.menu_item1.connect("activate", self.on_controls_click)
        self.menu.append(self.menu_item1)

        self.menu_item1 = Gtk.MenuItem(label=_("Send"))
        self.menu_item1.connect("activate", self.on_send_click)
        self.menu.append(self.menu_item1)

        self.menu_item2 = Gtk.MenuItem(label=_("Quit"))
        self.menu.append(self.menu_item2)
        self.menu_item2.connect("activate", Gtk.main_quit)

        self.menu.show_all()
        self.menu.popup(None, None, None, self, 3, time)

    def get_notifications_interval(self):
        notifications_window.get_notifications(self)
        return True

    def on_click(self, button, time):
        print("Left clicked")

    def on_notifications_click(self, button):
        notifications_window.show_window()

    def on_summary_click(self, button):
        summary.Summary()
    
    def on_controls_click(self, button):
        controls.Controls()

    def on_send_click(self, button):
        try:
            image = ImageGrab.grab()
            image.save(summary.MAINDIR + 'image.jpg')

            self.send_window = send.Window()
            self.send_window.show_popup_window()
        except Exception as e:
            message.log_error("Exception occured: " + str(e))
            message.MessageDialogWindow().error_dialog(_("Error"), 
                _("There has been an error while taking a screenshot. Please try again later"))
            

if __name__ == '__main__':
    notifications_window = notifications.Notifications()
    
    tray = TrayIcon()

    # control notifications every 5 seconds
    interval_ms = 5
    GLib.timeout_add_seconds(interval_ms, tray.get_notifications_interval)

    Gtk.main()
