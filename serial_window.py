import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SerialWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Serial Communication Settings")

        self.set_default_size(400, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_modal(True)


if __name__ == "__main__":
    win = SerialWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()