import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk

import requests
import subprocess

import gettext

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

class Window(Gtk.Builder):
    def __init__(self):
        Gtk.Builder.__init__(self)
        builder = Gtk.Builder()
        builder.add_from_file("popup.glade")

        note_label = builder.get_object("note")
        note_label.set_label(_("Note"))

        send_button = builder.get_object("send_button")
        send_button.set_label(_("Send"))

        self.image_window = builder.get_object("image")
        self.textview = builder.get_object("textview")
        
        send_button.connect("clicked", self.on_send_clicked)
        
        self.window = builder.get_object("popup_window")
        self.window.set_title(_("Send"))
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

    def on_send_clicked(self, button):
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

        response = requests.post('http://localhost:3000/users', files=files, data=data)
        #response = requests.get('http://localhost:3000/users')
        print(response.text)

        self.window.close()

    def on_destroy(self, window):
        self.window.close()

if __name__ == "__main__":
    window = Window()

    Gtk.main()
