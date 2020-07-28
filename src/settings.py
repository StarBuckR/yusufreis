import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

import summary
import gettext
import base64

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

class Settings(object):
    def __init__(self):
        self.is_window_open = False

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Settings"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(400, 200)
        self.window.set_resizable(False)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)

    def show_window(self):
        if self.is_window_open == True:
            return
        
        button_label = ""
        label = ""
        is_in_domain = False
        if (summary.getDomain() != ""):
            is_in_domain = True
            label = _("User is in domain")
            button_label = _("Leave Domain")
        else:
            label = _("User is not in domain")
            button_label = _("Join Domain")

        label = Gtk.Label(label=("<b>"+ label +"</b>"), use_markup=True)
        self.grid.attach(label, 0, 0, 4, 1)

        separator1 = Gtk.Separator()
        self.grid.attach_next_to(separator1, label, Gtk.PositionType.BOTTOM, 4, 1)

        button = Gtk.Button(label=button_label)
        button.set_size_request(80, 30)

        label = Gtk.Label(label=_("Local Username:"))
        label.set_halign(Gtk.Align.END)
        label2 = Gtk.Label(label=_("Local Password:"))
        label2.set_halign(Gtk.Align.END)

        self.local_username_entry = Gtk.Entry()
        self.local_pass_entry = Gtk.Entry()
        self.local_pass_entry.set_visibility(False)

        self.grid.attach_next_to(label, separator1, Gtk.PositionType.BOTTOM, 1, 2)
        self.grid.attach_next_to(self.local_username_entry, label, Gtk.PositionType.RIGHT, 3, 2)
        self.grid.attach_next_to(label2, label, Gtk.PositionType.BOTTOM, 1, 2)
        self.grid.attach_next_to(self.local_pass_entry, label2, Gtk.PositionType.RIGHT, 3, 2)

        separator1 = label2 # little hack for grid attachment correction

        if is_in_domain == False: # this will be false in release
            separator2 = Gtk.Separator()

            label3 = Gtk.Label(label=_("Domain Username:"))
            label3.set_halign(Gtk.Align.END)

            label4 = Gtk.Label(label=_("Domain Password:"))
            label4.set_halign(Gtk.Align.END)

            self.domain_username_entry = Gtk.Entry()
            self.domain_pass_entry = Gtk.Entry()
            self.domain_pass_entry.set_visibility(False)

            self.grid.attach_next_to(separator2, label2, Gtk.PositionType.BOTTOM, 4, 1)

            label5 = Gtk.Label(label=_("Domain Name:"))
            label5.set_halign(Gtk.Align.END)
            self.domain_name_entry = Gtk.Entry()

            label6 = Gtk.Label(label=_("Hostname:"))
            label6.set_halign(Gtk.Align.END)
            self.hostname_entry = Gtk.Entry()

            self.grid.attach_next_to(label5, separator2, Gtk.PositionType.BOTTOM, 1, 2)
            self.grid.attach_next_to(self.domain_name_entry, label5, Gtk.PositionType.RIGHT, 3, 2)
            self.grid.attach_next_to(label6, label5, Gtk.PositionType.BOTTOM, 1, 2)
            self.grid.attach_next_to(self.hostname_entry, label6, Gtk.PositionType.RIGHT, 3, 2)

            self.grid.attach_next_to(label3, label6, Gtk.PositionType.BOTTOM, 1, 2)
            self.grid.attach_next_to(self.domain_username_entry, label3, Gtk.PositionType.RIGHT, 3, 2)
            self.grid.attach_next_to(label4, label3, Gtk.PositionType.BOTTOM, 1, 2)
            self.grid.attach_next_to(self.domain_pass_entry, label4, Gtk.PositionType.RIGHT, 3, 2)

            separator1 = label4 # little hack for grid attachment correction
            button.connect("clicked", self.on_join_button_clicked)
        else:
            button.connect("clicked", self.on_leave_button_clicked)

        self.grid.attach_next_to(button, separator1, Gtk.PositionType.BOTTOM, 4, 2)

        self.window.set_icon_from_file(summary.ICONComputer)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.window.add(self.grid)
        self.window.show_all()

    def on_delete_event(self, control, button):
        self.is_window_open = False
    
    def on_join_button_clicked(self, button):
        print(self.local_username_entry.get_text())
        print(self.local_pass_entry.get_text())
        print(self.domain_username_entry.get_text())
        print(self.domain_pass_entry.get_text())
        print(self.domain_name_entry.get_text())
        print(self.hostname_entry.get_text())
    
    def on_leave_button_clicked(self, button):
        print(self.local_username_entry.get_text())
        print(self.local_pass_entry.get_text())