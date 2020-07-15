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

socket.setdefaulttimeout(5)

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext


def execute(command):
    try:
        proc = subprocess.Popen("timeout 3 " + command, stdout=subprocess.PIPE, shell=True)
        (dist, err) = proc.communicate()
        dist = dist.decode('UTF-8')
        return(dist.strip())
    except:
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
        return _("Fail")

def getClientTime():
    return execute("date +'%a %b %d %T %Y'")

def getSssd():
    return execute("systemctl is-active sssd.service")
def getSmdb():
    return execute("systemctl is-active smdb.service")

class Controls(object):
    def __init__(self):
        # ana pencere bileşeni
        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title('PiriReis')
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.set_border_width(32)
        #window.set_icon_from_file(summary.ICONDomain)
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

        separator1 = Gtk.Separator()

        label2 = Gtk.Label(getUsername())
        label2.set_halign(Gtk.Align.START)
        label2.set_direction(Gtk.TextDirection.LTR)
        label2_a = Gtk.Label(_("Username: "))
        label2_a.set_halign(Gtk.Align.END)
        label2_a.set_direction(Gtk.TextDirection.LTR)

        label3 = Gtk.Label(getBaseDir())
        label3.set_halign(Gtk.Align.START)
        label3.set_direction(Gtk.TextDirection.LTR)
        label3_a = Gtk.Label(_("Getent control: "))
        label3_a.set_halign(Gtk.Align.END)
        label3_a.set_direction(Gtk.TextDirection.LTR)

        label4 = Gtk.Label(getDomainName())
        label4.set_halign(Gtk.Align.START)
        label4.set_direction(Gtk.TextDirection.LTR)
        label4_a = Gtk.Label(_("Domain control: "))
        label4_a.set_halign(Gtk.Align.END)
        label4_a.set_direction(Gtk.TextDirection.LTR)

        can_ping = getPing()
        label5 = Gtk.Label(can_ping)
        if(can_ping != ""):
            label5 = Gtk.Label(_("Success"))
        else:
            label5 = Gtk.Label(_("Fail"))

        label5.set_halign(Gtk.Align.START)
        label5.set_direction(Gtk.TextDirection.LTR)
        label5_a = Gtk.Label(_("Ping control: "))
        label5_a.set_halign(Gtk.Align.END)
        label5_a.set_direction(Gtk.TextDirection.LTR)

        can_host = getHost()
        label6 = Gtk.Label(can_host)
        if(can_host != ""):
            label6 = Gtk.Label(_("Success"))
        else:
            label6 = Gtk.Label(_("Fail"))
        label6.set_halign(Gtk.Align.START)
        label6.set_direction(Gtk.TextDirection.LTR)
        label6_a = Gtk.Label(_("Host control: "))
        label6_a.set_halign(Gtk.Align.END)
        label6_a.set_direction(Gtk.TextDirection.LTR)

        klist = getKlist()
        label7 = Gtk.Label(klist)
        if(("no credentials cache found" in klist) or (klist == "")):
            label7 = Gtk.Label(_("Fail"))
        else:
            label7 = Gtk.Label(_("Success"))

        label7.set_halign(Gtk.Align.START)
        label7.set_direction(Gtk.TextDirection.LTR)
        label7_a = Gtk.Label(_("Klist control: "))
        label7_a.set_halign(Gtk.Align.END)
        label7_a.set_direction(Gtk.TextDirection.LTR)

        separator2 = Gtk.Separator()

        label8 = Gtk.Label(getNTPTime(getLDAP()))
        label8.set_halign(Gtk.Align.START)
        label8.set_direction(Gtk.TextDirection.LTR)
        label8_a = Gtk.Label(_("DC time: "))
        label8_a.set_halign(Gtk.Align.END)
        label8_a.set_direction(Gtk.TextDirection.LTR)

        label9 = Gtk.Label(getClientTime())
        label9.set_halign(Gtk.Align.START)
        label9.set_direction(Gtk.TextDirection.LTR)
        label9_a = Gtk.Label(_("Client time: "))
        label9_a.set_halign(Gtk.Align.END)
        label9_a.set_direction(Gtk.TextDirection.LTR)

        separator3 = Gtk.Separator()

        sssd = getSssd()
        label10 = Gtk.Label(sssd)
        if sssd == "active":
            label10 = Gtk.Label(_("Active"))
        else:
            label10 = Gtk.Label(_("Inactive"))

        label10.set_halign(Gtk.Align.START)
        label10.set_direction(Gtk.TextDirection.LTR)
        label10_a = Gtk.Label(_("Sssd service control: "))
        label10_a.set_halign(Gtk.Align.END)
        label10_a.set_direction(Gtk.TextDirection.LTR)

        smdb = getSmdb()
        label11 = Gtk.Label(smdb)
        if smdb == "active":
            label11 = Gtk.Label(_("Active"))
        else:
            label11 = Gtk.Label(_("Inactive"))

        label11.set_halign(Gtk.Align.START)
        label11.set_direction(Gtk.TextDirection.LTR)
        label11_a = Gtk.Label(_("Smdb service control: "))
        label11_a.set_halign(Gtk.Align.END)
        label11_a.set_direction(Gtk.TextDirection.LTR)

        grid.attach(label1, 0, 0, 4, 1)
        grid.attach_next_to(separator1, label1, Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(label1, separator1, Gtk.PositionType.BOTTOM, 3, 2)

        grid.attach_next_to(label2_a, separator1,
                            Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label2, label2_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label3_a, label2_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label3, label3_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label4_a, label3_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label4, label4_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label5_a, label4_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label5, label5_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label6_a, label5_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label6, label6_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label7_a, label6_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label7, label7_a, Gtk.PositionType.RIGHT, 3, 2)

        grid.attach_next_to(separator2, label7_a, Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(label8_a, separator2, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label8, label8_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label9_a, label8_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label9, label9_a, Gtk.PositionType.RIGHT, 3, 2)

        grid.attach_next_to(separator3, label9_a, Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(label10_a, separator3, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label10, label10_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label11_a, label10_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label11, label11_a, Gtk.PositionType.RIGHT, 3, 2)

        window.show_all()
