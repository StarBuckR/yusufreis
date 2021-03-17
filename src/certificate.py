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

class Certificate(object):
    def __init__(self, network):
        self.is_window_open = False
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Certificate"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(300, 200)
        self.window.set_resizable(False)
        self.network = network

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)
    
    def show_window(self):
        if self.is_window_open == True:
            return

        separator = Gtk.Separator()
        self.grid.attach(separator, 0, 0, 4, 1)

        cert_details = self.get_certificate_details().split("\n")
        # converting (issuer=DC = lab, DC = elleriana, CN = elleriana-WIN16-DC01-CA) into DC=lab, DC=elleriana, CN=elleriana-WIN16-DC01-CA
        issuer = "".join(cert_details[0].split("=")[1:]).replace("  ", "=")
        # converting (subject=CN = par1941-2.elleriana.lab) into CN=par1941-2.elleriana.lab
        subject = "".join(cert_details[1].split("=")[1:]).replace("  ", "=")
        label_a = summary.create_label_and_attach(self.grid, issuer, _("Issuer: "), separator)
        label_a = summary.create_label_and_attach(self.grid, subject, _("Subject: "), label_a)
        label_a = summary.create_label_and_attach(self.grid, "".join(cert_details[2].split("=")[1:]), _("Start Date: "), label_a)
        label_a = summary.create_label_and_attach(self.grid, "".join(cert_details[3].split("=")[1:]), _("End Date: "), label_a)
        
        for detail in cert_details[5:]:
            label_a = summary.create_label_and_attach(self.grid, "".join(detail).strip(), _("Extension SAN: "), label_a)
        
        self.window.set_icon_from_file(summary.ICONDomain)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.is_advanced_open = False
        self.window.add(self.grid)
        self.window.show_all()

    def get_certificate_details(self):
        if network.get_if_identity_is_user(self.network.combobox.get_active_text()):
            return controls.execute("pkexec hvlcert -user " + network.get_identity(self.network.combobox.get_active_text()) + \
                 " -show | openssl x509 -noout -issuer -subject -startdate -enddate -ext subjectAltName")
        else:
            return controls.execute("pkexec hvlcert -show | openssl x509 -noout -issuer -subject -startdate -enddate -ext subjectAltName")
        
    def on_delete_event(self, control, button):
        self.is_window_open = False
