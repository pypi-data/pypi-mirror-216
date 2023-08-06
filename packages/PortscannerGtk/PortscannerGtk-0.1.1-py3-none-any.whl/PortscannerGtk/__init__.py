#!/usr/bin/python3
import socket
import sys
import threading
from queue import Queue
import time
import gi
import os
import importlib
gi.require_version('Adw', '1')
from gi.repository import Adw, GLib, Gtk, Gio
gi.require_version('Gtk', '4.0')

#Only for Splash Screen on start after using pyinstaller -w -F 
if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
    import pyi_splash
    pyi_splash.update_text('... Loading ...')
    pyi_splash.close()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports_open = 0
        self.msg = ""
        self.q = Queue()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        GLib.set_application_name("Multithreading Portscanner Gtk")

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.box1)

        self.grid = Gtk.Grid()
        self.box1.append(self.grid)
        self.grid.set_row_homogeneous(True)

        self.button_scan = Gtk.Button(label="scan !")
        self.button_clear = Gtk.Button(label="clear")
        self.button_exit = Gtk.Button(label="exit")
        self.label1 = Gtk.Label(label="Target:")
        self.label2 = Gtk.Label(label="Ports:")
        self.target = Gtk.Entry()
        self.ports = Gtk.Entry()
        self.result = Gtk.TextView()
        self.grid.attach(self.label1, 0, 0, 1, 1)
        self.grid.attach(self.label2, 1, 0, 1, 1)
        self.grid.attach(self.button_scan, 2, 0, 1, 1)
        self.grid.attach(self.target, 0, 1, 1, 1)
        self.grid.attach(self.ports, 1, 1, 1, 1)
        self.grid.attach(self.button_clear, 2, 1, 1, 1)
        self.grid.attach(self.button_exit, 2, 2, 1, 1)
        self.text = Gtk.TextBuffer()
        self.result.set_buffer(self.text)
        sw = Gtk.ScrolledWindow()
        sw.set_child(self.result)
        self.box1.append(sw)
        self.box1.set_homogeneous(True)
        self.set_default_size(430, 380)
        self.set_resizable(False)

        self.box1.set_spacing(10)
        self.box1.set_margin_top(10)
        self.box1.set_margin_bottom(10)
        self.box1.set_margin_start(10)
        self.box1.set_margin_end(10)

        self.button_clear.connect('clicked', self.button_clear_clicked)
        self.button_exit.connect('clicked', self.button_exit_clicked)
        self.button_scan.connect('clicked', self.button_scan_clicked)

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        menu = Gio.Menu.new()

        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")

        self.header.pack_start(self.hamburger)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about)
        self.add_action(action)

        menu.append("About", "win.about")

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)
        self.about.set_modal(self)

        self.about.set_authors(["Lennart Martens"])
        self.about.set_copyright("Copyright 2023 Lennart Martens")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("skull-symbolic.svg")
        self.about.show()

    def button_clear_clicked(self, button):
        self.text.set_text("")        

    def button_exit_clicked(self, button):
        self.close()

    def button_scan_clicked(self, button):
        for x in range(int(self.ports.get_text())):
            self.q.put(x)
            
        self.ziel = self.target.get_text()
        self.start()
        time.sleep(2)
        self.msg += f"\n\n{self.ports_open} Port(s) open !"
        self.text.set_text(self.msg)

    def scan(self, port):
        try:
            conn = self.s.connect((self.ziel, port))
            return True
        except:
            return False

    def worker(self):
        while True:
            port = self.q.get()
            if self.scan(port):
                self.ports_open += 1
                self.msg += f"\n--------------------------->Port {port} is open !!!"
            else:
                self.msg += f"\nPort {port} is closed."

    def start(self):
        for x in range(10):
            t = threading.Thread(target=self.worker)
            t.start()


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp()
app.run(sys.argv)
