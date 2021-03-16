#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

# Libraries
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gio, Gtk, GdkPixbuf as appindicator
import os
import sys
import subprocess

import gettext
import locale
import summary, controls

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

INTERFACE_DIRECTORY = "/usr/share/hvlcert/"

def get_ip_address(interface_name):
    ip_address = controls.execute("ip a | grep " + interface_name + " | grep inet")
    if not ip_address:
        return None
    
    ip_address = ip_address.split(" ")[1]
    return ip_address

def is_interface_up(interface_name):
    returned_value = controls.execute("ip a | grep " + interface_name.strip() + " | grep ' UP '")
    return returned_value if returned_value != "" else False

def is_interface_configured(interface_name):
    returned_value = controls.execute("cat /etc/network/interfaces | grep wpa_" + interface_name.strip()  + ".conf")
    return True if returned_value != "" else False

def is_interface_exists(interface_name):
    return True if controls.execute("ip link show | grep " + interface_name) else False

def get_ssid(name):
    return controls.execute("cat " + INTERFACE_DIRECTORY + "wpa_" + name + ".conf | grep 'ssid' | awk -F '=' '{print $2}' | awk -F '\"' '{print $2}'")

def get_domain_suffix_match(name):
    return controls.execute("cat " + INTERFACE_DIRECTORY + "wpa_" + name + ".conf | grep 'domain_suffix_match' | awk -F '=' '{print $2}'")

def get_identity(name):
    return controls.execute("cat " + INTERFACE_DIRECTORY + "wpa_" + name + ".conf | grep 'identity' | awk -F '=' '{print $2}'")

def get_working_interfaces():
    return controls.execute("ip link show")

class Network(object):
    def __init__(self):
        self.is_window_open = False
        # ana pencere bileşeni
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Network"))
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.set_border_width(32)
        self.window.set_default_size(400, 400)
        self.window.set_resizable(True)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(5)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_direction(Gtk.TextDirection.LTR)
    
    def show_window(self):
        if self.is_window_open == True:
            return
        
        label1 = Gtk.Label(label=("<b>" + _("Network") + "</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)

        separator = Gtk.Separator()
        self.grid.attach(label1, 0, 0, 4, 1)
        self.grid.attach_next_to(separator, label1, Gtk.PositionType.BOTTOM, 4, 2)

        for filename in os.listdir(INTERFACE_DIRECTORY):
            if filename.endswith(".conf"):
                # code below works such as wpa_eth0.conf -> eth0.conf -> eth0
                interface_name = filename.split("_")[1].split(".conf")[0]

                if is_interface_exists(interface_name) and is_interface_configured(interface_name):
                    label_a = summary.create_label_and_attach(self.grid, interface_name, _("Interface Name: "), separator)
                    label_a = summary.create_label_and_attach(self.grid, get_ip_address(interface_name), _("IP Address: "), label_a)
                    label_a = summary.create_label_and_attach(self.grid, get_ssid(interface_name), _("ssid: "), label_a)
                    label_a = summary.create_label_and_attach(self.grid, get_domain_suffix_match(interface_name), _("Domain Suffix Match: "), label_a)
                    label_a = summary.create_label_and_attach(self.grid, get_identity(interface_name), _("Identity: "), label_a)

                    separator = Gtk.Separator()
                    self.grid.attach(label1, 0, 0, 4, 1)
                    self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        self.advanced_button = Gtk.Button(label=_("Advanced"))
        self.advanced_button.set_size_request(80, 30)
        self.advanced_button.connect("clicked", self.on_advanced_clicked)
        self.grid.attach_next_to(self.advanced_button, separator, Gtk.PositionType.BOTTOM, 4, 2)
        
        self.window.set_icon_from_file(summary.ICONDomain)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.window.add(self.grid)
        self.window.show_all()

    def on_advanced_clicked(self, button):
        combobox = Gtk.ComboBoxText()
        combobox.connect("changed", self.on_combobox_changed)

        for item in get_working_interfaces().split("\n"):
            try:
                if int(item.split(":")[0]):
                    name = item.split(":")[1].strip()
                    if name.startswith(tuple(["e", "w"])):
                        combobox.append_text(name)
            except ValueError:
                pass

        combobox.set_active(0)
        name = combobox.get_active_text()

        self.grid.attach_next_to(combobox, button, Gtk.PositionType.BOTTOM, 4, 2)
        self.interface_enable_button = Gtk.Button(label=_("Enable"))
        self.interface_disable_button = Gtk.Button(label=_("Disable"))

        self.interface_enable_button.connect("clicked", self.on_network_changed, name, True)
        self.interface_disable_button.connect("clicked", self.on_network_changed, name, False)
        self.reconfigure_interface_buttons(name)

        self.grid.attach_next_to(self.interface_enable_button, combobox, Gtk.PositionType.BOTTOM, 1, 2)
        self.grid.attach_next_to(self.interface_disable_button, self.interface_enable_button, Gtk.PositionType.RIGHT, 3, 2)

        self.window.show_all()

    def on_network_changed(self, button, interface_name, enable:bool):
        """
        if enable:
            controls.execute("pkexec sudo switcher -a e -i " + interface_name)
        else:
            controls.execute("pkexec sudo switcher -a d -i " + interface_name)

        self.reconfigure_interface_buttons(interface_name)
        """
        print(interface_name + " -> interface_name", enable)

    def on_combobox_changed(self, combo):
        self.reconfigure_interface_buttons(combo.get_active_text())
    
    def reconfigure_interface_buttons(self, name):
        if is_interface_configured(name):
            self.interface_enable_button.set_sensitive(False)
            self.interface_disable_button.set_sensitive(True)
        else:
            self.interface_enable_button.set_sensitive(True)
            self.interface_disable_button.set_sensitive(False)

    def on_delete_event(self, control, button):
        self.is_window_open = False
