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
MAINDIR = "./"
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

class Summary(object):
    def __init__(self):

        # ana pencere bileşeni
        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title('PiriReis')
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.set_border_width(32)
        window.set_icon_from_file(ICONDomain)
        window.set_default_size(400, 400)
        window.set_resizable(False)

        #window.connect_after('destroy', self.on_cikis_pencere)
        # window.add(check_button)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_direction(Gtk.TextDirection.LTR)

        window.add(grid)

        quitBtn = Gtk.Button(label=_("Settings"))
        quitBtn.set_size_request(80, 30)
        quitBtn.connect("clicked", self.on_button_clicked)

        label1 = Gtk.Label(("<b>"+getHostname()+"</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)

        separator1 = Gtk.Separator()

        label2 = Gtk.Label(getDist())
        label2.set_halign(Gtk.Align.START)
        label2.set_direction(Gtk.TextDirection.LTR)
        label2_a = Gtk.Label(_("OS:"))
        label2_a.set_halign(Gtk.Align.END)
        label2_a.set_direction(Gtk.TextDirection.LTR)

        label3 = Gtk.Label(getCPU())
        label3.set_halign(Gtk.Align.START)
        label3.set_direction(Gtk.TextDirection.LTR)
        label3_a = Gtk.Label(_("CPU:"))
        label3_a.set_halign(Gtk.Align.END)
        label3_a.set_direction(Gtk.TextDirection.LTR)

        label4 = Gtk.Label(getRAM())
        label4.set_halign(Gtk.Align.START)
        label4.set_direction(Gtk.TextDirection.LTR)
        label4_a = Gtk.Label(_("RAM:"))
        label4_a.set_halign(Gtk.Align.END)
        label4_a.set_direction(Gtk.TextDirection.LTR)

        separator2 = Gtk.Separator()

        domain = getDomain()
        label5 = Gtk.Label(domain)
        if(domain == ""):
            label5 = Gtk.Label(_("Domain could not found"))

        label5.set_halign(Gtk.Align.START)
        label5.set_direction(Gtk.TextDirection.LTR)
        label5_a = Gtk.Label(_("Domain:"))
        label5_a.set_halign(Gtk.Align.END)
        label5_a.set_direction(Gtk.TextDirection.LTR)

        workgroup = getWorkgroup()
        label6 = Gtk.Label(workgroup)
        if(workgroup == ""):
            label6 = Gtk.Label(_("Workgroup could not found"))

        label6.set_halign(Gtk.Align.START)
        label6.set_direction(Gtk.TextDirection.LTR)
        label6_a = Gtk.Label(_("Workgroup:"))
        label6_a.set_halign(Gtk.Align.END)
        label6_a.set_direction(Gtk.TextDirection.LTR)

        separator3 = Gtk.Separator()

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

        grid.attach(label1, 0, 0, 4, 1)
        grid.attach_next_to(image1, label1, Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(separator1, image1, Gtk.PositionType.BOTTOM, 4, 2)

        grid.attach_next_to(label2_a, separator1,
                            Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label2, label2_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label3_a, label2_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label3, label3_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label4_a, label3_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label4, label4_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(separator2, label4_a,
                            Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(label5_a, separator2,
                            Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label5, label5_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label6_a, label5_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label6, label6_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(separator3, label6_a,
                            Gtk.PositionType.BOTTOM, 4, 2)

        grid.attach_next_to(quitBtn, separator3, Gtk.PositionType.BOTTOM, 4, 2)

        window.show_all()

    def on_button_clicked(self, widget):
        print("Settings")
        #Gtk.main_quit()

    def on_degisim_ornekozellik(self, settings, key, check_button):
        check_button.set_active(settings.get_boolean("ornekozellik"))

    def on_kontrol_ornekozellik(self, button, settings):
        settings.set_boolean("ornekozellik", button.get_active())
