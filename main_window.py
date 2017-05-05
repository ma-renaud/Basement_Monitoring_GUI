import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(1000, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.unix_start_time = time.mktime(time.localtime())
        self.unixtimeArray = []
        self.temperatureArray = []
        self.humidityArray = []

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

    def update(self, environmental_data):
        self.temperature.set_markup('<span font="30">' + "{0:.1f}".format(environmental_data.temperature) +
                                    ' °C</span>')
        self.rel_humidity.set_markup('<span font="30">' + "{0:.1f}".format(environmental_data.rel_humidity) +
                                     ' %</span>')
        timestamp = (time.strftime("%H:%M:%S"))
        unixtime = self.unix_start_time - time.mktime(time.localtime())
        self.unixtimeArray.append(float(unixtime))
        self.temperatureArray.append(environmental_data.temperature)
        self.humidityArray.append(environmental_data.rel_humidity)

        self.axTemperature.clear()
        self.axTemperature.set_xscale('log')
        self.axTemperature.set_xlabel('Temps [s]')
        self.axTemperature.set_ylabel('Temperature [°C]', color='r')
        self.axTemperature.plot(self.unixtimeArray, self.temperatureArray, 'r')

        self.axHumidity.clear()
        self.axHumidity.plot(self.unixtimeArray, self.humidityArray, 'C0')
        self.axHumidity.set_ylabel('Relative Humidity [%]', color='C0')

        self.plot_canvas.draw()

    def create_left_panel(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.hbox.pack_start(vbox, False, True, 10)

        spacer1 = Gtk.Label()
        vbox.pack_start(spacer1, False, True, 15)

        temperature = Gtk.Label()
        temperature.set_markup('Temperature')
        vbox.pack_start(temperature, False, True, 0)

        self.temperature.set_markup('<span font="30">23.4 °C</span>')
        vbox.pack_start(self.temperature, False, True, 0)

        spacer2 = Gtk.Label()
        vbox.pack_start(spacer2, False, True, 10)

        humidity = Gtk.Label()
        humidity.set_markup('Rel. Humidity')
        vbox.pack_start(humidity, False, True, 0)

        self.rel_humidity.set_markup('<span font="30">48 %</span>')
        vbox.pack_start(self.rel_humidity, False, True, 0)

    def create_graph(self):
        fig = Figure()
        self.axTemperature = fig.add_subplot(111, xlabel="Temps [s]")
        self.axTemperature.set_ylabel('Temperature [°C]', color='r')
        self.axTemperature.autoscale_view(True, True, True)
        self.axHumidity = self.axTemperature.twinx()
        self.axHumidity.set_ylabel('Relative Humidity [%]', color='C0')
        self.axHumidity.autoscale_view(True, True, True)

        sw = Gtk.ScrolledWindow()
        vbox_graph = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox_graph.pack_start(sw, True, True, 10)
        self.plot_canvas = FigureCanvas(fig)
        self.plot_canvas.set_size_request(400, 400)
        sw.add_with_viewport(self.plot_canvas)
        self.hbox.pack_start(vbox_graph, True, True, 5)




if __name__ == "__main__":
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
