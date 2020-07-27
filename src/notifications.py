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
        self.get_notifications_address = settings.get_string("get-notifications")
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
        self.sw = Gtk.ScrolledWindow()
        self.grid = Gtk.Grid()

        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)

        self.sw.set_size_request(400, 400)

        if self.count > 0:
            self.create_notifications()

        self.sw.add(self.grid)

        self.window.add(self.sw)
        self.window.show_all()

    def create_notifications(self):
        separator = ""
        for i in range(self.count):
            overlay = Gtk.Overlay()
            box = Gtk.Box()
            
            label_text = self.response['notifications'][i]['message']
            label = Gtk.Label(
                "<b><span font='10' foreground='#000000'>{}</span></b>".format(label_text))
            label.set_use_markup(True)
            label.set_line_wrap(True)
            label.set_line_wrap_mode(0)
            label.set_direction(Gtk.TextDirection.LTR)
            label.set_alignment(0, 0)
            label.set_vexpand(True)
            
            button = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
            button.set_relief(Gtk.ReliefStyle.NONE)
            button.set_receives_default(True)
            button.set_size_request(1, 1)
            button.connect("clicked", self.on_close_notification_click, label_text, i)

            box.add(label)
            box.add(button)
            overlay.add(box)
            if i == 0:
                self.grid.attach(overlay, 0, 0, 3, 2)
            else:
                self.grid.attach_next_to(overlay, separator, Gtk.PositionType.BOTTOM, 3, 2)
            separator = Gtk.Separator()
            self.grid.attach_next_to(separator, overlay, Gtk.PositionType.BOTTOM, 4, 1)
            

    def get_notifications(self, tray):
        try:
            hostname = controls.execute("hostname")
            data = {
                "machine_name": hostname
            }
            self.response = (requests.post(self.get_notifications_address, data=data)).json()
            self.count = self.response['count']
            if(self.count > 0):
                tray.set_from_file(summary.MAINDIR + "images/notification.png")
            else:
                tray.set_from_file(summary.MAINDIR + "images/notification.png")
            tray.is_server_up = True
        except Exception as e:
            tray.is_server_up = False
            tray.set_from_file(summary.MAINDIR + "images/notification.png")
            message.log_error("Exception occurred: " + str(e))

    def on_close_notification_click(self, button, notification_text, notification_index):
        try:
            hostname = controls.execute("hostname")
            data = {
                "machine_name": hostname,
                "message": notification_text,
                "index": notification_index
            }

            resp = requests.delete(self.notifications_address, data=data).json()
            message.log_info(resp)
        except Exception as e:
            message.log_error("Exception occurred: " + str(e))