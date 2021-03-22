#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

# Libraries
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gio, Gtk, Gdk, GdkPixbuf
import os
import sys
import subprocess

import gettext
import locale
import summary, controls, network

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

class InterfaceDetails(object):
    def __init__(self):
        self.is_window_open = False
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Interface Details"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(400, 400)
        self.window.set_resizable(False)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)
    
    def create_and_show_window(self, details):
        if self.is_window_open == True:
            return

        separator = Gtk.Separator()
        self.grid.attach(separator, 0, 0, 4, 1)
        label_a = separator

        for detail in details.splitlines():
            splitted_detail = detail.split("=")
            label_a = summary.create_label_and_attach(self.grid, splitted_detail[1], splitted_detail[0] + ":", label_a)
        
        self.window.set_icon_from_file(summary.ICONDomain)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.is_advanced_open = False
        self.window.add(self.grid)
        self.window.show_all()

    def on_delete_event(self, control, button):
        self.is_window_open = False
