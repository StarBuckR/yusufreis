import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import logging, summary
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename=summary.MAINDIR + "logs/yusufreis.log")
console = logging.StreamHandler()

def log_error(error):
    console.setLevel(logging.ERROR)
    logging.error(error)

def log_warning(warning):
    console.setLevel(logging.WARNING)
    logging.warning(warning)

def log_info(info):
    console.setLevel(logging.INFO)
    logging.info(info)

def log_debug(debug):
    console.setLevel(logging.DEBUG)
    logging.debug(debug)

class MessageDialogWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="MessageDialog Example")

    def info_dialog(self):
        dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK,
            "This is an INFO MessageDialog",
        )
        dialog.format_secondary_text(
            "And this is the secondary text that explains things."
        )
        dialog.run()
        print("INFO dialog closed")

        dialog.destroy()

    def error_dialog(self, message, secondary):
        dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CLOSE,
            message,
        )
        dialog.format_secondary_text(
            secondary
        )
        dialog.run()
        print("ERROR dialog closed")

        dialog.destroy()

    def warn_dialog(self, widget):
        dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL,
            "This is an WARNING MessageDialog",
        )
        dialog.format_secondary_text(
            "And this is the secondary text that explains things."
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("WARN dialog closed by clicking OK button")
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()

    def question_dialog(self, widget):
        dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO,
            "This is an QUESTION MessageDialog",
        )
        dialog.format_secondary_text(
            "And this is the secondary text that explains things."
        )
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
        elif response == Gtk.ResponseType.NO:
            print("QUESTION dialog closed by clicking NO button")

        dialog.destroy()


# win = MessageDialogWindow()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()