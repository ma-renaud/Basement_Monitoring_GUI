import os
import configparser

from serial_config import SerialConfig


class ConfigManager:
    def __init__(self, path):
        self.path = path

    def create_config(self):

        config = configparser.ConfigParser()
        config.add_section("Serial")
        config.set("Serial", "Line", "COM1")
        config.set("Serial", "Speed", "9600")
        config.set("Serial", "Data Bits", "8")
        config.set("Serial", "Stop Bits", "1")
        config.set("Serial", "Parity", "0")
        config.set("Serial", "Flow", "2")

        with open(self.path, "wt", encoding='utf8') as config_file:
            config.write(config_file)

    def get_config(self):
        if not os.path.exists(self.path):
            self.create_config()

        config = configparser.ConfigParser()
        config.read(self.path)
        return config

    def read_serial_config(self):
        serial_config = SerialConfig()

        config = self.get_config()
        config.read(self.path)

        serial_config.line = config.get("Serial", "Line", fallback="COM1")
        serial_config.speed = config.getint("Serial", "Speed", fallback="9600")
        serial_config.data_bits = config.getint("Serial", "Data Bits", fallback="8")
        serial_config.stop_bits = config.getint("Serial", "Stop Bits", fallback="1")
        serial_config.parity = config.getint("Serial", "Parity", fallback="0")
        serial_config.flow = config.getint("Serial", "Flow", fallback="2")
        return serial_config

    def write_serial_config(self, serial_config):
        config = self.get_config()
        config.set("Serial", "Line", serial_config.line)
        config.set("Serial", "Speed", str(serial_config.speed))
        config.set("Serial", "Data Bits", str(serial_config.data_bits))
        config.set("Serial", "Stop Bits", str(serial_config.stop_bits))
        config.set("Serial", "Parity", str(serial_config.parity))
        config.set("Serial", "Flow", str(serial_config.flow))

        with open(self.path, "wt", encoding='utf8') as config_file:
            config.write(config_file)
