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

def execute(command):
    try:
        proc = subprocess.Popen("timeout " + BASHTIMEOUT + " " + command, stdout=subprocess.PIPE, shell=True)
        (dist, err) = proc.communicate()
        dist = dist.decode('UTF-8')
        if(dist == ""):
            message.log_info(command + " " + "returning null")

        return(dist.strip())
    except Exception as e:
        message.log_error("Exception occurred")
        return("")

def getUsername():
    return execute("whoami")

def getBaseDir():
    return execute("getent passwd " + getUsername() + " | awk -F: ' { print $6} '")

def getDomainName():
    return execute("dnsdomainname")

def getPing():
    return execute("ping -c 1 " + getDomainName())

def getHost():
    return execute("host " + getDomainName())

def getKlist():
    return execute("klist")

def getLDAP():
    return execute("net ads info 2>/dev/null | grep 'LDAP server name' | awk -F: '{print $2}'")

def getNTPTime(host):
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

def getClientTime():
    return execute("date +'%a %b %d %T %Y'")

def getSssd():
    return execute("systemctl is-active sssd.service")
def getSmbd():
    return execute("systemctl is-active smbd.service")

def getPam():
    return execute("cat /etc/pam.d/common-session | grep  'session required pam_mkhomedir.so skel=/etc/skel umask=0077'")

class Controls(object):
    def __init__(self):
        # ana pencere bileşeni
        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title(_("Controls"))
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.set_border_width(32)
        window.set_default_size(400, 400)
        window.set_resizable(False)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_direction(Gtk.TextDirection.LTR)

        window.add(grid)

        label1 = Gtk.Label(("<b>" + summary.getHostname() + "</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)

        separator = Gtk.Separator()
        grid.attach(label1, 0, 0, 4, 1)
        grid.attach_next_to(separator, label1, Gtk.PositionType.BOTTOM, 4, 2)
        
        label_a = summary.create_label_and_attach(grid, getUsername(), _("Username: "), separator)
        label_a = summary.create_label_and_attach(grid, getBaseDir(), _("Getent control: "), label_a)

        domainname = getDomainName()
        if domainname != "":
            pass
        else:
            domainname = _("Fail")
        label_a = summary.create_label_and_attach(grid, domainname, _("Domain control: "), label_a)

        can_ping = getPing()
        if(can_ping != ""):
            can_ping = _("Success")
        else:
            can_ping = _("Fail")
        label_a = summary.create_label_and_attach(grid, can_ping, _("Ping control: "), label_a)

        can_host = getHost()
        if(can_host != ""):
            can_host = _("Success")
        else:
            can_host = _("Fail")
        label_a = summary.create_label_and_attach(grid, can_host, _("Host control: "), label_a)

        # # control if klist command exists
        if os.path.isfile("/etc/krb5.conf") is False:
            message.log_info("klist is not found")
        else:
            message.log_info("klist found")

        klist = getKlist()
        if(("no credentials cache found" in klist) or (klist == "")):
            klist = _("Fail")
        else:
            klist = _("Success")
        label_a = summary.create_label_and_attach(grid, klist, _("Klist control: "), label_a)

        # # control if pam exists
        if os.path.isfile("/etc/pam.d/common-session") is False:
            message.log_info("pam not found")
        else:
            message.log_info("pam found")

        pam = getPam()
        if(klist == ""):
            pam = _("Fail")
        else:
            pam = _("Success")
        label_a = summary.create_label_and_attach(grid, pam, _("Pam control: "), label_a)

        separator = Gtk.Separator()
        grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        label_a = summary.create_label_and_attach(grid, getNTPTime(getLDAP()), _("DC time: "), separator)
        label_a = summary.create_label_and_attach(grid, getClientTime(), _("Client time: "), label_a)

        separator = Gtk.Separator()
        grid.attach_next_to(separator, label_a, Gtk.PositionType.BOTTOM, 4, 2)

        sssd = getSssd()
        if sssd == "active":
            sssd = _("Active")
        else:
            sssd = _("Inactive")
        label_a = summary.create_label_and_attach(grid, sssd, _("Sssd service control: "), separator
        )

        smbd = getSmbd()
        if smbd == "active":
            smbd = _("Active")
        else:
            smbd = _("Inactive")
        label_a = summary.create_label_and_attach(grid, smbd, _("Smbd service control: "), label_a)

        window.show_all()
