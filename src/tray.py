#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from PIL import Image 

import send, message, summary, controls, notifications, settings, loading
import subprocess, gettext, sys, os

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

send_window = ""
summary_window = ""
controls_window = ""
notifications_window = ""
settings_window = ""

class TrayIcon(Gtk.StatusIcon):
    def __init__(self):
        Gtk.StatusIcon.__init__(self)
        self.is_server_up = False
        self.set_from_file(summary.MAINDIR + "images/Computer.png")
        self.set_tooltip_text("Yusufreis")
        self.set_title("Yusufreis")
        
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

        if self.is_server_up == True:
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

    def on_click(self, button):
        loading_window = loading.Loading()
        while Gtk.events_pending():
            Gtk.main_iteration(),

        summary_window.show_window(self)

        loading_window.destroy()

    def on_notifications_click(self, button):
        loading_window = loading.Loading()
        while Gtk.events_pending():
            Gtk.main_iteration()

        notifications_window.show_window()

        loading_window.destroy()

    def on_summary_click(self, button):
        loading_window = loading.Loading()
        while Gtk.events_pending():
            Gtk.main_iteration()

        summary_window.show_window(self)

        loading_window.destroy()
    
    def on_controls_click(self, button):
        loading_window = loading.Loading()
        while Gtk.events_pending():
            Gtk.main_iteration()
        
        controls_window.show_window()

        loading_window.destroy()

    def on_send_click(self, button):
        loading_window = loading.Loading()
        while Gtk.events_pending():
            Gtk.main_iteration()

        try:
            imagename = summary.MAINDIR + 'image.jpg'
            os.system("import -window root "+imagename)

            send_window.show_window()
        except Exception as e:
            message.log_error("Exception occured: " + str(e))
            message.MessageDialogWindow().error_dialog(_("Error"), 
                _("There has been an error while taking a screenshot. Please try again later"))
        
        loading_window.destroy()
        
    def show_settings_window(self):
        loading_window = loading.Loading()
        while Gtk.events_pending():
            Gtk.main_iteration()

        settings_window.show_window()

        loading_window.destroy()

if __name__ == '__main__':
    notifications_window = notifications.Notifications()
    summary_window = summary.Summary()
    send_window = send.Send()
    controls_window = controls.Controls()
    settings_window = settings.Settings()

    tray = TrayIcon()

    # control notifications every 5 seconds
    interval_ms = 5
    GLib.timeout_add_seconds(interval_ms, tray.get_notifications_interval)

    Gtk.main()
