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
import summary, controls, certificate

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

INTERFACE_CONF_DIRECTORY = "/usr/share/hvlcert/"
INTERFACES_DIRECTORY = "/etc/network/interfaces.d/"
SWITCHER_DIRECTORY = "/usr/share/hvlcert/"

def get_ip_address(interface_name):
    ip_address = controls.execute("ip a | grep " + interface_name + " | grep inet")
    if not ip_address:
        return None
    
    ip_address = ip_address.split(" ")[1]
    return ip_address

def get_interfaces():
    return controls.execute("cat /etc/network/interfaces | grep iface | awk -F ' ' '{print$2}'")

def is_interface_up(interface_name):
    returned_value = controls.execute("ip a | grep " + interface_name.strip() + " | grep ' UP '")
    return returned_value if returned_value != "" else False

def is_interface_configured(interface_name):
    returned_value = controls.execute("cat " + INTERFACES_DIRECTORY + interface_name.strip() + " | grep wpa_" + interface_name.strip()  + ".conf")
    return True if returned_value != "" else False

def is_interface_exists(interface_name):
    return True if controls.execute("ip link show | grep " + interface_name) else False

def get_ssid(name):
    return controls.execute("cat " + INTERFACE_CONF_DIRECTORY + "wpa_" + name + ".conf | grep 'ssid' | awk -F '=' '{print $2}' | awk -F '\"' '{print $2}'")

def get_domain_suffix_match(name):
    return controls.execute("cat " + INTERFACE_CONF_DIRECTORY + "wpa_" + name + ".conf | grep 'domain_suffix_match' | awk -F '=' '{print $2}'")

def get_identity(name):
    return controls.execute("cat " + INTERFACE_CONF_DIRECTORY + "wpa_" + name + ".conf | grep 'identity' | awk -F '=' '{print $2}'")

def get_if_identity_is_user(name):
    returned_value = controls.execute("cat " + INTERFACE_CONF_DIRECTORY + "wpa_" + name + ".conf | grep 'identity' | grep host")
    return False if returned_value != "" else True

def get_working_ethernets():
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
        self.window.set_resizable(False)

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
        
        for filename in os.listdir(INTERFACES_DIRECTORY):
            if filename.startswith(("w", "e")) and is_interface_configured(filename) and is_interface_exists(filename):
                if is_interface_up(filename):
                    interface = filename
                    label_a = summary.create_label_and_attach(self.grid, interface, _("Interface Name: "), separator)
                    label_a = summary.create_label_and_attach(self.grid, get_ip_address(interface), _("IP Address: "), label_a)
                    label_a = summary.create_label_and_attach(self.grid, get_ssid(interface), _("ssid: "), label_a)
                    label_a = summary.create_label_and_attach(self.grid, get_domain_suffix_match(interface), _("Domain Suffix Match: "), label_a)
                    label_a = summary.create_label_and_attach(self.grid, get_identity(interface), _("Identity: "), label_a)
                else:
                    label_a = summary.create_label_and_attach(self.grid, interface, _("Interface Name: "), separator)
                    label_down = Gtk.Label(label=("<b> <span color='red'> " + _("Interface is DOWN, Click to elevate") + "</span> </b>"), use_markup=True)
                    label_down.set_halign(Gtk.Align.CENTER)
                    down_button = Gtk.Button(label=_("Interface is DOWN, click to elevate"))
                    down_button.connect("clicked", self.on_down_button_clicked, interface)

                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                        filename=summary.ICONLocal,
                        width=36,
                        height=36,
                        preserve_aspect_ratio=True)

                    image1 = Gtk.Image.new_from_pixbuf(pixbuf)

                    self.grid.attach_next_to(image1, label_a, Gtk.PositionType.BOTTOM, 4, 2)
                    self.grid.attach_next_to(down_button, image1, Gtk.PositionType.BOTTOM, 4, 1)
                    
                    # must do this in order to separator to not break and collide with "down" label
                    label_a = down_button

                separator = Gtk.Separator()
                self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        self.advanced_button = Gtk.Button(label=_("Advanced Settings"))
        self.advanced_button.set_size_request(80, 30)
        self.advanced_button.connect("clicked", self.on_advanced_clicked)
        self.grid.attach_next_to(self.advanced_button, separator, Gtk.PositionType.BOTTOM, 4, 2)
        
        self.window.set_icon_from_file(summary.ICONDomain)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.is_advanced_open = False
        self.window.add(self.grid)
        self.window.show_all()

    def on_cert_button_clicked(self, button):
        certificate_window = certificate.Certificate(self)
        certificate_window.show_window()

    def on_down_button_clicked(self, button, interface_name):
        print(interface_name)

    def on_advanced_clicked(self, button):
        if self.is_advanced_open:
            return

        combobox = Gtk.ComboBoxText()
        for item in get_working_ethernets().split("\n"):
            try:
                if int(item.split(":")[0]):
                    name = item.split(":")[1].strip()
                    if name.startswith(tuple(["e", "w"])):
                        combobox.append_text(name)
            except ValueError:
                pass

        combobox.set_active(0)
        name = combobox.get_active_text()
        # connecting combobox here to bypass an AttributeError
        combobox.connect("changed", self.on_combobox_changed)

        self.grid.attach_next_to(combobox, button, Gtk.PositionType.BOTTOM, 2, 2)
        self.switch = Gtk.Switch()
        self.switch.props.valign = Gtk.Align.CENTER
        self.switch_handler_id = self.switch.connect("notify::active", self.switch_network_interface)
        self.grid.attach_next_to(self.switch, combobox, Gtk.PositionType.RIGHT, 1, 2)
        self.reconfigure_switch(name)

        cert_button = Gtk.Button(label=_("Get Certificate"))
        cert_button.connect("clicked", self.on_cert_button_clicked)
        self.grid.attach_next_to(cert_button, combobox, Gtk.PositionType.BOTTOM, 4, 2)

        self.combobox = combobox
        self.is_advanced_open = True
        self.window.show_all()

    def on_combobox_changed(self, combobox):
        self.reconfigure_switch(combobox.get_active_text())

    def switch_network_interface(self, button, active):
        if self.switch.get_active():
            #print(controls.execute("pkexec echo Enabled"))
            controls.execute("pkexec " + SWITCHER_DIRECTORY + "switcher.sh -a -e -i " + self.combobox.get_active_text())
        else:
            #print(controls.execute("pkexec echo Disabled"))
            controls.execute("pkexec " + SWITCHER_DIRECTORY + "switcher.sh -a -d -i " + self.combobox.get_active_text())
        
    def reconfigure_switch(self, name):
        # these block contains a little workaround to not emit a signal when changing 
        # switch's current state by simply blocking and unblocking emit handler
        if is_interface_configured(name):
            self.switch.handler_block(self.switch_handler_id)
            self.switch.set_state(True)
            self.switch.handler_unblock(self.switch_handler_id)
        else:
            self.switch.handler_block(self.switch_handler_id)
            self.switch.set_state(False)
            self.switch.handler_unblock(self.switch_handler_id)

    def on_delete_event(self, control, button):
        self.is_window_open = False
