#!/usr/bin/env python

import message
import summary
import controls
import gettext
import requests
from gi.repository import Gtk, Gio
import gi
gi.require_version("Gtk", "3.0")


el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext


class Notifications(object):
    BASE_KEY = "apps.gsettings-projectx"

    def __init__(self):
        settings = Gio.Settings.new(self.BASE_KEY)
        self.notifications_address = settings.get_string("notifications")

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Notifications"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(400, 400)
        self.window.set_resizable(False)

        self.count = 0
        self.response = ""

    def show_window(self):
        sw = Gtk.ScrolledWindow()
        self.grid = Gtk.Grid()

        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)

        # vp.set_size_request(300,400)
        sw.set_size_request(400, 400)

        for i in range(self.count):
            self.create_label(self.response['notifications'][i]['message'], i)

        sw.add(self.grid)
        # vp.add(box)

        # sw.add(vp)
        self.window.add(sw)
        self.window.show_all()

    def create_label(self, label_text, i):
        label = Gtk.Label(
            "<b><span font='20' background='#ebebeb' foreground='#000000'>{}</span></b>".format(label_text))
        label.set_use_markup(True)
        label.set_line_wrap(True)

        label.set_direction(Gtk.TextDirection.LTR)
        label.set_halign(Gtk.Align.CENTER)
        label.set_vexpand(True)

        self.grid.attach(label, 0, i, 1, 1)

    def get_notifications(self, tray):
        try:
            hostname = controls.execute("hostname")
            data = {
                "machine_name": hostname
            }
            self.response = (requests.post(self.notifications_address, data=data)).json()
            self.count = self.response['count']
            if(self.count > 0):
                tray.set_from_file(summary.MAINDIR + "images/notification.png")
            else:
                tray.set_from_file(summary.MAINDIR + "images/notification.png")
        except Exception as e:
            message.log_error("Exception occurred: " + str(e))
