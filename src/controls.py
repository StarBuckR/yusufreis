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
import summary

from socket import AF_INET, SOCK_DGRAM
import socket
import struct, time

import message

socket.setdefaulttimeout(5)
BASHTIMEOUT = str(3)

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext

def execute(command, environment=None):
    try:
        proc = subprocess.Popen("timeout " + BASHTIMEOUT + " " + command, stdout=subprocess.PIPE, shell=True, env=environment)
        (dist, err) = proc.communicate()
        dist = dist.decode('UTF-8')
        if(dist == ""):
            message.log_info(command + " " + "returning null")

        return(dist.strip())
    except Exception as e:
        message.log_error("Exception occurred")
        return("")

def execute_without_timeout(command):
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (dist, err) = proc.communicate()
        dist = dist.decode('UTF-8')
        if(dist.strip() == ""):
            message.log_info(command + " " + "returning null")

        return(dist.strip())
    except Exception as e:
        message.log_error("Exception occurred")
        return("")

def get_username():
    return execute("whoami")

def get_base_dir():
    return execute("getent passwd " + get_username() + " | awk -F: ' { print $6} '")

def get_domain_name():
    return execute("dnsdomainname")

def get_ping():
    return execute("ping -c 1 " + get_domain_name())

def get_host():
    return execute("host " + get_domain_name())

def get_klist():
    return execute("klist")

def get_LDAP():
    return execute("net ads info 2>/dev/null | grep 'LDAP server name' | awk -F: '{print $2}'")

def get_NTP_time(host):
    try:
        port = 123
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'

        TIME1970 = 2208988800 # 1970-01-01 00:00:00
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.sendto(msg.encode('utf-8'), address)
        msg, address = client.recvfrom( buf )

        t = struct.unpack( "!12I", msg )[10]
        t -= TIME1970

        return time.ctime(t).replace("  "," ")
    except socket.timeout:
        message.log_error(("Could not fetch time from NTP server"))
        return _("Fail")

def get_client_time():
    return execute("date +'%a %b %d %T %Y'")

def get_sssd():
    return execute("systemctl is-active sssd.service")
def get_smbd():
    return execute("systemctl is-active smbd.service")

def get_pam():
    return execute("cat /etc/pam.d/common-session | grep  'session required pam_mkhomedir.so skel=/etc/skel umask=0077'")

class Controls(object):
    def __init__(self):
        self.is_window_open = False
        # ana pencere bileşeni
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title(_("Controls"))
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
        
        label1 = Gtk.Label(label=("<b>" + summary.get_hostname() + "</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)

        separator = Gtk.Separator()
        self.grid.attach(label1, 0, 0, 4, 1)
        self.grid.attach_next_to(separator, label1, Gtk.PositionType.BOTTOM, 4, 2)
        
        label_a = summary.create_label_and_attach(self.grid, get_username(), _("Username: "), separator)
        label_a = summary.create_label_and_attach(self.grid, get_base_dir(), _("Getent control: "), label_a)

        domainname = get_domain_name()
        if domainname != "":
            pass
        else:
            domainname = _("Fail")
        label_a = summary.create_label_and_attach(self.grid, domainname, _("Domain control: "), label_a)

        can_ping = get_ping()
        if(can_ping != ""):
            can_ping = _("Success")
        else:
            can_ping = _("Fail")
        label_a = summary.create_label_and_attach(self.grid, can_ping, _("Ping control: "), label_a)

        can_host = get_host()
        if(can_host != ""):
            can_host = _("Success")
        else:
            can_host = _("Fail")
        label_a = summary.create_label_and_attach(self.grid, can_host, _("Host control: "), label_a)

        # # control if klist command exists
        if os.path.isfile("/etc/krb5.conf") is False:
            message.log_info("klist is not found")
        else:
            message.log_info("klist found")

        klist = get_klist()
        if(("no credentials cache found" in klist) or (klist == "")):
            klist = _("Fail")
        else:
            klist = _("Success")
        label_a = summary.create_label_and_attach(self.grid, klist, _("Klist control: "), label_a)

        # # control if pam exists
        if os.path.isfile("/etc/pam.d/common-session") is False:
            message.log_info("pam not found")
        else:
            message.log_info("pam found")

        pam = get_pam()
        if(klist == ""):
            pam = _("Fail")
        else:
            pam = _("Success")
        label_a = summary.create_label_and_attach(self.grid, pam, _("Pam control: "), label_a)

        separator = Gtk.Separator()
        self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        label_a = summary.create_label_and_attach(self.grid, get_NTP_time(get_LDAP()), _("DC time: "), separator)
        label_a = summary.create_label_and_attach(self.grid, get_client_time(), _("Client time: "), label_a)

        separator = Gtk.Separator()
        self.grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        sssd = get_sssd()
        if sssd == "active":
            sssd = _("Active")
        else:
            sssd = _("Inactive")
        label_a = summary.create_label_and_attach(self.grid, sssd, _("Sssd service control: "), separator
        )

        smbd = get_smbd()
        if smbd == "active":
            smbd = _("Active")
        else:
            smbd = _("Inactive")
        label_a = summary.create_label_and_attach(self.grid, smbd, _("Smbd service control: "), label_a)

        self.window.set_icon_from_file(summary.ICONComputer)
        self.window.connect('delete-event', self.on_delete_event)
        self.is_window_open = True
        self.window.add(self.grid)
        self.window.show_all()

    def on_delete_event(self, control, button):
        self.is_window_open = False
        