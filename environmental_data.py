class EnvironmentalData(object):

    def __init__(self, temperature, rel_humidity):
        self.__temperature = 0;
        self.temperature = temperature
        self.rel_humidity = rel_humidity
        self.temperature_offset = 2

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, temperature):
        self.__temperature = temperature - EnvironmentalData.TEMPERATURE_OFFSET

EnvironmentalData.TEMPERATURE_OFFSET = 2
