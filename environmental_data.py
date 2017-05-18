import datetime as dt


class EnvironmentalData(object):

    def __init__(self, temperature, rel_humidity):
        self.temperature = temperature
        self.rel_humidity = rel_humidity
        self.datetime = dt.datetime.now()

    @staticmethod
    def get_adjusted_temperature(temperature):
        return temperature - EnvironmentalData.TEMPERATURE_OFFSET

EnvironmentalData.TEMPERATURE_OFFSET = 2
