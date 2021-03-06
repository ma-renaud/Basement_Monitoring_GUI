import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
import matplotlib.dates as md
from environmental_data_history import TimeScale


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(1000, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(self.hbox)

        self.temperature = Gtk.Label()
        self.rel_humidity = Gtk.Label()
        self.create_left_panel()

        self.sep = Gtk.Separator()
        self.sep.set_orientation(Gtk.Orientation.VERTICAL)
        self.sep.get_style_context().add_class("sidebar-separator")
        self.hbox.pack_start(self.sep, False, True, 0)

        self.plot_canvas = None
        self.axTemperature = None
        self.axHumidity = None
        self.create_graph()

        self.show_all()

    def update_values(self, environmental_data_last):
        self.temperature.set_markup('<span font="30">' + "{0:.1f}".format(environmental_data_last.temperature) +
                                    ' °C</span>')
        self.rel_humidity.set_markup('<span font="30">' + "{0:.1f}".format(environmental_data_last.rel_humidity) +
                                     ' %</span>')

    def update_graph(self, environmental_data_history, time_scale):
        self.set_graph_axis(time_scale)
        time_array = [o.datetime for o in environmental_data_history]
        temp_array = [o.temperature for o in environmental_data_history]
        hum_array = [o.rel_humidity for o in environmental_data_history]

        self.axTemperature.plot(time_array, temp_array, 'r')
        self.axHumidity.plot(time_array, hum_array, 'C0')
        self.plot_canvas.draw()

    def create_left_panel(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.hbox.pack_start(vbox, False, True, 10)

        spacer1 = Gtk.Label()
        vbox.pack_start(spacer1, False, True, 15)

        temperature = Gtk.Label()
        temperature.set_markup('Temperature')
        vbox.pack_start(temperature, False, True, 0)

        self.temperature.set_markup('<span font="30">00.0 °C</span>')
        vbox.pack_start(self.temperature, False, True, 0)

        spacer2 = Gtk.Label()
        vbox.pack_start(spacer2, False, True, 10)

        humidity = Gtk.Label()
        humidity.set_markup('Rel. Humidity')
        vbox.pack_start(humidity, False, True, 0)

        self.rel_humidity.set_markup('<span font="30">00 %</span>')
        vbox.pack_start(self.rel_humidity, False, True, 0)

    def create_graph(self):
        fig = Figure()
        self.axTemperature = fig.add_subplot(111, xlabel="Temps [s]")
        self.axHumidity = self.axTemperature.twinx()
        self.set_graph_axis(TimeScale.SECONDS)

        sw = Gtk.ScrolledWindow()
        vbox_graph = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox_graph.pack_start(sw, True, True, 10)
        self.plot_canvas = FigureCanvas(fig)
        self.plot_canvas.set_size_request(400, 400)
        sw.add_with_viewport(self.plot_canvas)
        self.hbox.pack_start(vbox_graph, True, True, 5)

    def set_graph_axis(self, time_scale):
        if time_scale == TimeScale.SECONDS:
            xfmt = md.DateFormatter('%H:%M:%S')
        else:
            xfmt = md.DateFormatter('%m/%d %H:%M')

        self.axTemperature.clear()
        self.axTemperature.set_ylim([10, 40])
        self.axTemperature.set_ylabel('Temperature [°C]', color='r')
        self.axTemperature.xaxis_date()
        labels = self.axTemperature.get_xticklabels()
        for l in labels:
            l.update({'rotation': 25})
        self.axTemperature.xaxis.set_major_formatter(xfmt)

        self.axHumidity.clear()
        self.axHumidity.xaxis_date()
        self.axHumidity.set_ylim([35, 80])
        self.axHumidity.set_ylabel('Relative humidity [%]', color='C0')
        self.axHumidity.xaxis.set_major_formatter(xfmt)


if __name__ == "__main__":
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
