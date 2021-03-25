#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

# Libraries
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gio, Gtk, GdkPixbuf
import os
import sys
import subprocess

import gettext
import locale
import controls, network
import socket

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

CURRDIR = os.path.dirname(os.path.abspath(__file__))
MAINDIR = "/usr/share/hvl/yusufreis/"
ICONDomain = os.path.join(MAINDIR+"images/", 'Domain.png')
ICONLocal = os.path.join(MAINDIR+"images/", 'Local.png')
ICONComputer = os.path.join(MAINDIR+"images/", 'Computer.png')

def get_domain():
    return controls.execute("net ads info 2> /dev/null | grep Realm | cut -d':' -f2 | tr -d ' ' | tr -d '\n'")

def get_workgroup():
    return controls.execute("net ads workgroup | cut -d':' -f2 | tr -d ' ' | tr -d '\n'")

def get_hostname():
    return controls.execute("hostname | tr -d '\n'")

def get_CPU():
    cpumodel = controls.execute("lscpu | grep 'Model name:' | cut -d':' -f2 | sed -e 's/^[[:space:]]*//'| tr -d '\n'")
    cpucore = controls.execute("lscpu | grep '^CPU(s):' | cut -d':' -f2 | sed -e 's/^[[:space:]]*//'| tr -d '\n'")
    return(cpumodel + " - " + cpucore)

def get_RAM():
    memory = controls.execute("awk '/MemTotal/ {print $2}' /proc/meminfo")
    memory = round(int(memory)/1024/1000, 2)
    return(str(memory)+" GB")

def get_distro():
    return controls.execute("lsb_release -ir | cut -d':' -f2| sed -e 's/^[[:space:]]*//'| tr '\n' ' '")

def create_label_and_attach(grid, label_text, label_a_text, attach_next_to):
        label = Gtk.Label(label_text)
        label.set_halign(Gtk.Align.START)
        label.set_direction(Gtk.TextDirection.LTR)
        label_a = Gtk.Label(label_a_text)
        label_a.set_halign(Gtk.Align.END)
        label_a.set_direction(Gtk.TextDirection.LTR)

        grid.attach_next_to(label_a, attach_next_to, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label, label_a, Gtk.PositionType.RIGHT, 3, 2)

        return label_a

class Summary(object):
    def __init__(self):
        self.is_window_open = False

        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Summary"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_icon_from_file(ICONDomain)
        self.window.set_default_size(400, 400)
        self.window.set_resizable(False)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)

    def show_window(self, tray):
        if self.is_window_open == True:
            return

        label1 = Gtk.Label(label=("<b>"+get_hostname()+"</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)
        self.grid.attach(label1, 0, 0, 4, 1)

        if (get_domain() != ""):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=ICONDomain,
                width=96,
                height=96,
                preserve_aspect_ratio=True)
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=ICONLocal,
                width=96,
                height=96,
                preserve_aspect_ratio=True)

        image1 = Gtk.Image.new_from_pixbuf(pixbuf)
        self.grid.attach_next_to(image1, label1, Gtk.PositionType.BOTTOM, 4, 2)

        separator1 = Gtk.Separator()
        self.grid.attach_next_to(separator1, image1, Gtk.PositionType.BOTTOM, 4, 2)

        label_a = create_label_and_attach(self.grid, get_distro(), _("OS:"), separator1)
        label_a = create_label_and_attach(self.grid, get_CPU(), _("CPU:"), label_a)
        label_a = create_label_and_attach(self.grid, get_RAM(), _("RAM:"), label_a)

        separator = Gtk.Separator()
        self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        domain = get_domain()
        if(domain == ""):
            domain = _("Domain could not found")
            workgroup = ""
        else:
            workgroup = get_workgroup()

        label_a = create_label_and_attach(self.grid, domain, _("Domain:"), separator)
        
        if(workgroup == ""):
            workgroup = _("Workgroup could not found")
        
        label_a = create_label_and_attach(self.grid, workgroup, _("Workgroup:"), label_a)
        self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        quitBtn = Gtk.Button(label=_("Settings"))
        quitBtn.set_size_request(80, 30)
        quitBtn.connect("clicked", self.on_settings_clicked, tray)

        separator = Gtk.Separator()
        self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)
        self.grid.attach_next_to(quitBtn, separator, Gtk.PositionType.BOTTOM, 4, 2)

        self.window.set_icon_from_file(ICONComputer)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.window.add(self.grid)
        self.window.show_all()

    def on_delete_event(self, control, button):
        self.is_window_open = False

    def on_settings_clicked(self, widget, tray):
        tray.show_settings_window()

    def on_degisim_ornekozellik(self, settings, key, check_button):
        check_button.set_active(settings.get_boolean("ornekozellik"))

    def on_kontrol_ornekozellik(self, button, settings):
        settings.set_boolean("ornekozellik", button.get_active())
