import sys

from main_window import MainWindow
from serial_window import SerialWindow
from serial_config import SerialConfig
import configparser
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

# This would typically be its own file
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <submenu>
      <attribute name="label">Application</attribute>
      <section>
        <item>
          <attribute name="action">app.quit</attribute>
          <attribute name="label" translatable="yes">_Quit</attribute>
          <attribute name="accel">&lt;Primary&gt;q</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label">Serial</attribute>
      <section>
        <item>
          <attribute name="action">app.serialConfig</attribute>
          <attribute name="label" translatable="yes">Settings</attribute>
        </item>
        <item>
          <attribute name="action">app.serialConnect</attribute>
          <attribute name="label" translatable="yes">Connect</attribute>
        </item>
      </section>
    </submenu>
  </menu>
</interface>
"""

class Application(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(application_id="org.example.myapp", **kwargs)
        self.window = None
        self.serial_config = None
        self.config_path = "config.ini"

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.read_config()

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("serialConfig", None)
        action.connect("activate", self.on_serial_config)
        self.add_action(action)

        action = Gio.SimpleAction.new("serialConnect", None)
        action.connect("activate", self.on_serial_connect)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_menubar(builder.get_object("app-menu"))

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

        #voir https://www.blog.pythonlibrary.org/2013/10/25/python-101-an-intro-to-configparser/
        config = self.get_config()
        config.set("Serial", "Line", self.serial_config.line)
        config.set("Serial", "Speed", str(self.serial_config.speed))
        config.set("Serial", "Data Bits", str(self.serial_config.data_bits))
        config.set("Serial", "Stop Bits", str(self.serial_config.stop_bits))
        config.set("Serial", "Parity", str(self.serial_config.parity))
        config.set("Serial", "Flow", str(self.serial_config.flow))

        with open(self.config_path, "wt", encoding='utf8') as config_file:
            config.write(config_file)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(application=self, title="Monitoring")

        self.window.present()

    def create_config(self):

        config = configparser.ConfigParser()
        config.add_section("Serial")
        config.set("Serial", "Line", "COM1")
        config.set("Serial", "Speed", "9600")
        config.set("Serial", "Data Bits", "8")
        config.set("Serial", "Stop Bits", "1")
        config.set("Serial", "Parity", "0")
        config.set("Serial", "Flow", "2")

        with open(self.config_path, "wt", encoding='utf8') as config_file:
            config.write(config_file)

    def get_config(self):
        if not os.path.exists(self.config_path):
            self.create_config()

        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config

    def read_config(self):
        if not self.serial_config:
            self.serial_config = SerialConfig()

        config = self.get_config()
        config.read('config.ini')

        self.serial_config.line = config.get("Serial", "Line", fallback="COM1")
        self.serial_config.speed = config.getint("Serial", "Speed", fallback="9600")
        self.serial_config.data_bits = config.getint("Serial", "Data Bits", fallback="8")
        self.serial_config.stop_bits = config.getint("Serial", "Stop Bits", fallback="1")
        self.serial_config.parity = config.getint("Serial", "Parity", fallback="0")
        self.serial_config.flow = config.getint("Serial", "Flow", fallback="2")

    def on_serial_config(self, action, param):
        win = SerialWindow(self.serial_config)
        win.show()

    def on_serial_connect(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
