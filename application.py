import sys

from main_window import MainWindow
from serial_window import SerialWindow

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

# This would typically be its own file
MENU_XML="""
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp", **kwargs)
        self.window = None

        #self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
        #                     GLib.OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

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

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(application=self, title="Monitoring")

        self.window.present()

    def on_serial_config(self, action, param):
        win = SerialWindow()
        win.show()

    def on_serial_connect(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)