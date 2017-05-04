import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from serial_config import SerialConfig


class SerialWindow(Gtk.Window):

    def __init__(self, serial_config):
        Gtk.Window.__init__(self, title="Serial Communication Settings")

        self.set_default_size(400, 300)
        self.set_border_width(15)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_modal(True)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box_outer.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 0, 0, 0))
        self.add(box_outer)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box_outer.pack_start(hbox, False, True, 0)
        label = Gtk.Label("Serial line to connect to", xalign=0)
        ed_comm_line = Gtk.Entry()
        ed_comm_line.set_text(serial_config.line)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(ed_comm_line, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box_outer.pack_start(hbox, False, True, 0)
        label = Gtk.Label("Speed (baud)", xalign=0)
        ed_speed = Gtk.Entry()
        ed_speed.set_text(str(serial_config.speed))
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(ed_speed, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box_outer.pack_start(hbox, False, True, 0)
        label = Gtk.Label("Data bits", xalign=0)
        ed_data = Gtk.Entry()
        ed_data.set_text(str(serial_config.data_bits))
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(ed_data, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box_outer.pack_start(hbox, False, True, 0)
        label = Gtk.Label("Stop bits", xalign=0)
        ed_stop = Gtk.Entry()
        ed_stop.set_text(str(serial_config.stop_bits))
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(ed_stop, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box_outer.pack_start(hbox, False, True, 0)
        label = Gtk.Label("Parity", xalign=0)
        combo_parity = Gtk.ComboBoxText()
        self.fill_combo_parity(combo_parity)
        combo_parity.set_active_id(str(serial_config.parity))
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo_parity, False, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        box_outer.pack_start(hbox, False, True, 0)
        label = Gtk.Label("Flow control", xalign=0)
        combo_flow = Gtk.ComboBoxText()
        self.fill_combo_flow(combo_flow)
        combo_flow.set_active_id(str(serial_config.flow))
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo_flow, False, True, 0)

        vbox = Gtk.VBox(False, 5)
        hbox = Gtk.HBox(True, 3)

        valign = Gtk.Alignment(xalign=0.0, yalign=1.0, xscale=0.0, yscale=0.0)
        vbox.pack_start(valign, True, True, 0)

        ok = Gtk.Button("Save")
        ok.set_size_request(70, 30)
        close = Gtk.Button("Cancel")

        hbox.add(ok)
        hbox.add(close)

        halign = Gtk.Alignment(xalign=1.0, yalign=0.0, xscale=0.0, yscale=0.0)
        halign.add(hbox)

        vbox.pack_start(halign, False, False, 0)
        box_outer.pack_start(vbox, True, True, 0)

        self.show_all()

    def fill_combo_parity(self, combo):
        combo.insert(0, "0", "None")
        combo.insert(1, "1", "Odd")
        combo.insert(2, "2", "Even")
        combo.insert(3, "3", "Mark")
        combo.insert(4, "4", "Space")

    def fill_combo_flow(self, combo):
        combo.insert(0, "0", "None (DTR/RTS enable)")
        combo.insert(1, "1", "None (DTR/RTS disable)")
        combo.insert(2, "2", "XON/XOFF")
        combo.insert(3, "3", "RTS/CTS")


if __name__ == "__main__":
    win = SerialWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
