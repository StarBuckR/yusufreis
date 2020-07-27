#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

# Libraries
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

from gi.repository import Gio, Gtk, GdkPixbuf, AppIndicator3 as appindicator
import os
import sys
import subprocess

import gettext
import locale
import controls

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

CURRDIR = os.path.dirname(os.path.abspath(__file__))
# this maindir is for development, the commented one is for release
MAINDIR = "/usr/share/hvl/yusufreis/"
ICONDomain = os.path.join(MAINDIR+"images/", 'Domain-icon.png')
ICONLocal = os.path.join(MAINDIR+"images/", 'Local-icon.png')

def getDomain():
    return controls.execute("net ads info 2> /dev/null | grep Realm | cut -d':' -f2 | tr -d ' ' | tr -d '\n'")
    # cmd_domainname = "net ads info 2> /dev/null | grep Realm | cut -d':' -f2 | tr -d ' ' | tr -d '\n'"
    # domainname = subprocess.check_output((cmd_domainname), shell=True)
    # domainname = domainname.decode('UTF-8')
    # return(domainname)

def getWorkgroup():
    return controls.execute("net ads workgroup | cut -d':' -f2 | tr -d ' ' | tr -d '\n'")

def getHostname():
    return controls.execute("hostname | tr -d '\n'")

def getCPU():
    cpumodel = controls.execute("lscpu | grep 'Model name:' | cut -d':' -f2 | sed -e 's/^[[:space:]]*//'| tr -d '\n'")
    cpucore = controls.execute("lscpu | grep '^CPU(s):' | cut -d':' -f2 | sed -e 's/^[[:space:]]*//'| tr -d '\n'")
    return(cpumodel + " - " + cpucore)

def getRAM():
    memory = controls.execute("awk '/MemTotal/ {print $2}' /proc/meminfo")
    memory = round(int(memory)/1024/1000, 2)
    return(str(memory)+" GB")

def getDist():
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
        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title(_("Summary"))
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.set_border_width(32)
        window.set_icon_from_file(ICONDomain)
        window.set_default_size(400, 400)
        window.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_direction(Gtk.TextDirection.LTR)

        window.add(grid)

        label1 = Gtk.Label(("<b>"+getHostname()+"</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)
        grid.attach(label1, 0, 0, 4, 1)


        if (getDomain() != ""):
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
        grid.attach_next_to(image1, label1, Gtk.PositionType.BOTTOM, 4, 2)

        separator1 = Gtk.Separator()
        grid.attach_next_to(separator1, image1, Gtk.PositionType.BOTTOM, 4, 2)

        label_a = create_label_and_attach(grid, getDist(), _("OS:"), separator1)
        label_a = create_label_and_attach(grid, getCPU(), _("CPU:"), label_a)
        label_a = create_label_and_attach(grid, getRAM(), _("RAM:"), label_a)

        separator = Gtk.Separator()
        grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        domain = getDomain()
        if(domain == ""):
            domain = _("Domain could not found")
            workgroup = ""
        else:
            workgroup = getWorkgroup()

        label_a = create_label_and_attach(grid, domain, _("Domain:"), separator)
        
        if(workgroup == ""):
            workgroup = _("Workgroup could not found")
        
        label_a = create_label_and_attach(grid, workgroup, _("Workgroup:"), label_a)
        grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        quitBtn = Gtk.Button(label=_("Settings"))
        quitBtn.set_size_request(80, 30)
        quitBtn.connect("clicked", self.on_button_clicked)

        separator = Gtk.Separator()
        grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(quitBtn, separator, Gtk.PositionType.BOTTOM, 4, 2)

        window.show_all()

    def on_button_clicked(self, widget):
        print("Settings")
        #Gtk.main_quit()

    def on_degisim_ornekozellik(self, settings, key, check_button):
        check_button.set_active(settings.get_boolean("ornekozellik"))

    def on_kontrol_ornekozellik(self, button, settings):
        settings.set_boolean("ornekozellik", button.get_active())
