import serial
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from matplotlib.figure import Figure
from numpy import arange, sin, cos
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(1000, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(self.hbox)

        self.create_left_panel()

        self.sep = Gtk.Separator()
        self.sep.set_orientation(Gtk.Orientation.VERTICAL)
        self.sep.get_style_context().add_class("sidebar-separator")
        self.hbox.pack_start(self.sep, False, True, 0)

        self.create_graph()

        self.show_all()

    def create_left_panel(self):
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.hbox.pack_start(self.vbox, False, True, 10)

        self.spacer1 = Gtk.Label()
        self.vbox.pack_start(self.spacer1, False, True, 15)

        self.temperature = Gtk.Label()
        self.temperature.set_markup('Temperature')
        self.vbox.pack_start(self.temperature, False, True, 0)

        self.temperature = Gtk.Label()
        self.temperature.set_markup('<span font="30">23.4 °C</span>')
        self.vbox.pack_start(self.temperature, False, True, 0)

        self.spacer2 = Gtk.Label()
        self.vbox.pack_start(self.spacer2, False, True, 10)

        self.temperature = Gtk.Label()
        self.temperature.set_markup('Rel. Humidity')
        self.vbox.pack_start(self.temperature, False, True, 0)

        self.relHumidity = Gtk.Label()
        self.relHumidity.set_markup('<span font="30">48 %</span>')
        self.vbox.pack_start(self.relHumidity, False, True, 0)

    def create_graph(self):
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111, xlabel="Temps [s]")
        ax.set_ylabel('Temperature [°C]', color='C0')
        ax2 = ax.twinx()
        ax2.set_ylabel('Relative Humidity [%]', color='r')

        t = arange(0.01, 10.0, 0.01)
        s1 = sin(t)
        s2 = cos(t)

        ax.plot(t, s1)
        ax2.plot(t, s2, 'r')

        sw = Gtk.ScrolledWindow()
        vbox_graph = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox_graph.pack_start(sw, True, True, 10)
        canvas = FigureCanvas(fig)
        canvas.set_size_request(400, 400)
        sw.add_with_viewport(canvas)
        self.hbox.pack_start(vbox_graph, True, True, 5)


if __name__ == "__main__":
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

# configure the serial connections (the parameters differs on the device you are connecting to)
'''
ser = serial.Serial(
    port='COM8',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
'''
