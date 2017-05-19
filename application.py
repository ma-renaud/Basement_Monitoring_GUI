import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk, GLib
from numpy import random

import os
import sys
import serial
import time
import threading

from main_window import MainWindow
from serial_window import SerialWindow
from environmental_data import EnvironmentalData
from environmental_data_history import EnvironmentalDataHistory, TimeScale
from serial_decoder import SerialDecoder
from config_manager import ConfigManager


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
        <item>
          <attribute name="action">app.serialDisconnect</attribute>
          <attribute name="label" translatable="yes">Disconnect</attribute>
        </item>
      </section>
    </submenu>
    <submenu>
      <attribute name="label">View</attribute>
      <section>
        <item>
          <attribute name="action">app.viewSeconds</attribute>
          <attribute name="label" translatable="yes">Last three minutes</attribute>
        </item>
        <item>
          <attribute name="action">app.viewMinutes</attribute>
          <attribute name="label" translatable="yes">Last hour</attribute>
        </item>
        <item>
          <attribute name="action">app.viewHours</attribute>
          <attribute name="label" translatable="yes">Last day</attribute>
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
        self.thread_data = None
        self.thread_values = None
        self.thread_graph = None
        self.thread_data_test = None
        self.connect_action = None
        self.disconnect_action = None
        self.seconds_action = None
        self.minutes_action = None
        self.hours_action = None
        self.serial_port = serial.Serial()
        self.config_path = ""
        self.environmental_data_history = EnvironmentalDataHistory()
        self.decoder = SerialDecoder()
        self.config_manager = None
        self.view_mode = TimeScale.SECONDS
        self.old_history_time_scale = self.environmental_data_history.time_scale

    def do_startup(self):
        Gtk.Application.do_startup(self)

        user_config_dir = os.path.expanduser("~") + os.path.sep + ".basement_monitoring"
        if not os.path.exists(user_config_dir):
            os.makedirs(user_config_dir)
        self.config_manager = ConfigManager(user_config_dir + os.path.sep + "user_config.ini")
        self.serial_config = self.config_manager.read_serial_config()

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        action = Gio.SimpleAction.new("serialConfig", None)
        action.connect("activate", self.on_serial_config)
        self.add_action(action)

        self.connect_action = Gio.SimpleAction.new("serialConnect", None)
        self.connect_action.connect("activate", self.on_serial_connect)
        self.add_action(self.connect_action)

        self.disconnect_action = Gio.SimpleAction.new("serialDisconnect", None)
        self.disconnect_action.connect("activate", self.on_serial_disconnect)
        self.disconnect_action.set_enabled(False)
        self.add_action(self.disconnect_action)

        self.seconds_action = Gio.SimpleAction.new("viewSeconds", None)
        self.seconds_action.connect("activate", self.on_view_seconds)
        self.add_action(self.seconds_action)

        self.minutes_action = Gio.SimpleAction.new("viewMinutes", None)
        self.minutes_action.connect("activate", self.on_view_minutes)
        self.minutes_action.set_enabled(False)
        self.add_action(self.minutes_action)

        self.hours_action = Gio.SimpleAction.new("viewHours", None)
        self.hours_action.connect("activate", self.on_view_hours)
        self.hours_action.set_enabled(False)
        self.add_action(self.hours_action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_menubar(builder.get_object("app-menu"))

        self.thread_data = threading.Thread(target=self.read_serial)
        self.thread_data.daemon = True

        self.thread_values = threading.Thread(target=self.update_values)
        self.thread_values.daemon = True

        self.thread_graph = threading.Thread(target=self.update_graph)
        self.thread_graph.daemon = True

        self.thread_data_test = threading.Thread(target=self.generate_test_data, args=[self.environmental_data_history])
        self.thread_data_test.daemon = True

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

        if self.serial_port.is_open:
            self.serial_port.close()

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(application=self, title="Monitoring")

        self.window.present()
        self.thread_data.start()
        self.thread_values.start()
        self.thread_graph.start()
        # self.thread_data_test.start()

    def on_serial_config(self, action, param):
        win = SerialWindow(self.serial_config, self.config_manager.write_serial_config)
        win.show()

    def on_serial_connect(self, action, param):
        if not self.serial_port.is_open:
            self.serial_port.baudrate = self.serial_config.speed
            self.serial_port.port = self.serial_config.line
            self.serial_port.bytesize = self.serial_config.data_bits
            self.serial_port.stopbits = self.serial_config.stop_bits
            self.serial_port.xonxoff = True
            self.serial_port.rtscts = False
            self.serial_port.timeout = 1
            self.serial_port.open()
            self.connect_action.set_enabled(False)
            self.disconnect_action.set_enabled(True)

    def on_serial_disconnect(self, action, param):
        if self.serial_port.is_open:
            self.serial_port.close()
            self.connect_action.set_enabled(True)
            self.disconnect_action.set_enabled(False)

    def on_view_seconds(self, action, param):
        self.view_mode = TimeScale.SECONDS
        GLib.idle_add(self.window.update_graph, self.environmental_data_history.get_history(self.view_mode),
                      self.view_mode)

    def on_view_minutes(self, action, param):
        self.view_mode = TimeScale.MINUTES
        GLib.idle_add(self.window.update_graph, self.environmental_data_history.get_history(self.view_mode),
                      self.view_mode)

    def on_view_hours(self, action, param):
        self.view_mode = TimeScale.HOURS
        GLib.idle_add(self.window.update_graph, self.environmental_data_history.get_history(self.view_mode),
                      self.view_mode)

    def on_quit(self, action, param):
        self.quit()

    def update_view_modes(self):
        if self.view_mode == self.old_history_time_scale and \
           self.old_history_time_scale != self.environmental_data_history.time_scale:
            self.view_mode = self.environmental_data_history.time_scale
            self.old_history_time_scale = self.environmental_data_history.time_scale

        if self.environmental_data_history.time_scale is TimeScale.HOURS:
            self.minutes_action.set_enabled(True)
            self.hours_action.set_enabled(True)
        if self.environmental_data_history.time_scale is TimeScale.MINUTES:
            self.minutes_action.set_enabled(True)

    def update_values(self):
        while True:
            if len(self.environmental_data_history.get_history(self.view_mode)) > 0:
                GLib.idle_add(self.window.update_values, self.environmental_data_history.last)

            self.update_view_modes()
            time.sleep(1)

    def update_graph(self):
        i = 0
        second_refresh = 2
        minute_refresh = 30
        hour_refresh = 1800
        refresh_needed = False
        while True:
            if len(self.environmental_data_history.get_history(self.view_mode)) > 0:
                if self.view_mode is TimeScale.SECONDS and i >= second_refresh:
                    refresh_needed = True
                elif self.view_mode is TimeScale.MINUTES and i >= minute_refresh:
                    refresh_needed = True
                elif i == hour_refresh:
                    refresh_needed = True

                if refresh_needed:
                    GLib.idle_add(self.window.update_graph, self.environmental_data_history.get_history(self.view_mode),
                                   self.view_mode)
                    i = 0
                    refresh_needed = False

            i = i+2
            time.sleep(2)

    def read_serial(self):
        while True:
            if self.serial_port.is_open:
                self.decoder.decode(self.serial_port.read().decode("utf-8"))
                if self.decoder.completed:
                    self.environmental_data_history.append(EnvironmentalData(self.decoder.decoded[0],
                                                                             self.decoder.decoded[1]))
            time.sleep(0.1)

    @staticmethod
    def generate_test_data(stack):
        while True:
            temp = 2 * random.random_sample() + 20
            hum = 5 * random.random_sample() + 48
            env = EnvironmentalData(temp, hum)
            stack.append(env)
            time.sleep(1)

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
