import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk

import requests
import subprocess
import glob, os, json, datetime

import base64
from io import BytesIO

import gettext
import message, controls, summary

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

class Send(object):
    BASE_KEY = "apps.gsettings-yusufreis"
    def __init__(self):
        self.is_window_open = False
        # GSettings key
        settings = Gio.Settings.new(self.BASE_KEY)
        self.post_address = settings.get_string("ipaddress")
        # print(self.post_address)

    def show_window(self):
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Send"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(400, 400)
        self.window.set_resizable(False)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)
        
        if self.is_window_open == True:
            return

        self.textview = Gtk.TextView()
        self.textview.set_size_request(400, 200)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textbuffer = self.textview.get_buffer()
        textbuffer.set_text(_(""))

        label = Gtk.Label(_("Note:"))
        label.set_direction(Gtk.TextDirection.LTR)
        label.set_halign(Gtk.Align.CENTER)

        send_button = Gtk.Button(label=_("Send"))
        send_button.set_size_request(80, 30)
        send_button.connect("clicked", self.on_send_click)

        cancel_button = Gtk.Button(label=_("Cancel"))
        cancel_button.set_size_request(80, 30)
        cancel_button.connect("clicked", self.on_cancel_click)

        self.grid.attach(label, 50, 10, 4, 1)
        self.grid.attach_next_to(self.textview, label, Gtk.PositionType.BOTTOM, 100, 30)
        self.grid.attach_next_to(send_button, self.textview, Gtk.PositionType.BOTTOM, 50, 10)
        self.grid.attach_next_to(cancel_button, send_button, Gtk.PositionType.RIGHT, 50, 10)
        
        self.window.set_icon_from_file(summary.ICONComputer)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.window.add(self.grid)
        self.window.show_all()

    def on_delete_event(self, control, button):
        self.is_window_open = False

    def on_send_click(self, button):
        try:
            buffer = self.textview.get_buffer()
            text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
            print(text)
 
            hostname = controls.execute("hostname")
            username = controls.execute("whoami")           


            list_of_files = glob.glob(summary.MAINDIR+'ss/*')
            latest_file = max(list_of_files, key=os.path.getctime)

            data = []
            data.append({
                "machine_name": hostname,
                "username": username,
                "note": text,
                "filename": latest_file
            })

            with open(summary.MAINDIR + "ss/main.json", "a") as outfile:
                json.dump(data, outfile)

            file_object = open(summary.MAINDIR + "ss/main.json", 'a')
            file_object.write("\n")
            file_object.close()

            # create new script that handles all api calls

            self.window.close()
        except Exception as e:
            message.log_error("Exception occurred: " + str(e))
            message.MessageDialogWindow().error_dialog(_("Error"), 
                _("There has been an error while sending information to the server. Please try again later"))
            
            self.window.close()
        return True
    
    def on_cancel_click(self, button):
        self.window.close()
        return True
