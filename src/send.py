import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk

import requests
import subprocess

import gettext

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

class Window(object):
    BASE_KEY = "apps.gsettings-projectx"
    def __init__(self):
        # GSettings key
        settings = Gio.Settings.new(self.BASE_KEY)
        self.post_address = settings.get_string("ipaddress")
        print(self.post_address)

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Send"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(400, 400)
        self.window.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_direction(Gtk.TextDirection.LTR)

        self.window.add(grid)

        self.textview = Gtk.TextView()
        self.textview.set_size_request(400, 200)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textbuffer = self.textview.get_buffer()
        textbuffer.set_text(_("Start typing your note here"))

        label = Gtk.Label(_("Note:"))
        label.set_direction(Gtk.TextDirection.LTR)
        label.set_halign(Gtk.Align.CENTER)

        send_button = Gtk.Button(label=_("Send"))
        send_button.set_size_request(80, 30)
        send_button.connect("clicked", self.on_send_click)

        cancel_button = Gtk.Button(label=_("Cancel"))
        cancel_button.set_size_request(80, 30)
        cancel_button.connect("clicked", self.on_cancel_click)

        grid.attach(label, 50, 10, 4, 1)
        grid.attach_next_to(self.textview, label, Gtk.PositionType.BOTTOM, 100, 30)
        grid.attach_next_to(send_button, self.textview, Gtk.PositionType.BOTTOM, 50, 10)
        grid.attach_next_to(cancel_button, send_button, Gtk.PositionType.RIGHT, 50, 10)
        
        self.window.show_all()
        self.window.connect("destroy", self.on_destroy)

    def show_popup_window(self):
        # pixbuf = GdkPixbuf.Pixbuf.new_from_file('image.jpg')

        # height = pixbuf.get_height() / 1.7
        # width = pixbuf.get_width() / 1.7
        # pixbuf = pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

        # image = Gtk.Image()
        # image.set_from_pixbuf(pixbuf)

        # self.image_window.set_from_pixbuf(pixbuf)
        self.window.show_all()

    def on_send_click(self, button):
        buffer = self.textview.get_buffer()
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        print(text)

        hostname = subprocess.getoutput("hostname")
        username = subprocess.getoutput("whoami")
        ip_adress = subprocess.getoutput("ip route get 1.2.3.4 | awk '{printf $7}'")

        files = {
            "image": open('image.jpg', 'rb')
        }

        data = {
            "note": text,
            "machine_name": hostname,
            "ip_adress": ip_adress,
            "username": username
        }

        response = requests.post(self.post_address, files=files, data=data)
        #response = requests.get('http://localhost:3000/users')
        print(response.text)

        self.window.close()

    def on_cancel_click(self, button):
        self.window.close()

    def on_destroy(self, window):
        self.window.close()

if __name__ == "__main__":
    window = Window()

    Gtk.main()
