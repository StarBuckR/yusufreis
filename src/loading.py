import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import gettext
el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

import summary

from threading import Thread

class Loading(Thread):
    def __init__(self):
        super(Loading, self).__init__()

        self.window = Gtk.Window(Gtk.WindowType.POPUP)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_resizable(False)
        self.window.set_decorated(False)
        self.window.set_title(_("Loading..."))

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)

        label1 = Gtk.Label(label=("<b>"+ _("Loading...") +"</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)
        self.grid.attach(label1, 0, 0, 4, 1)

        # below lines commented out, because I couldn't pull off threading and gif animation got stuck
        # pixbuf_animation = GdkPixbuf.PixbufAnimation.new_from_file(summary.MAINDIR + "images/Loading.gif")
        
        # image = Gtk.Image()
        # image.set_from_animation(pixbuf_animation)
        # self.grid.attach_next_to(image, label1, Gtk.PositionType.BOTTOM, 4, 2)
        
        self.window.add(self.grid)

        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)
        
    def destroy(self):
        self.window.destroy()
