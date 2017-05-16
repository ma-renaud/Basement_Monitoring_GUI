from collections import deque
from environmental_data import EnvironmentalData
from numpy import sum


class EnvironmentalDataHistory:
    def __init__(self):
        self.input_buffer = list()
        self.last_five_minute = deque(maxlen=320)
        self.last_hour = deque(maxlen=60)
        self.last_day = deque(maxlen=24)

    def get_history(self):
        if len(self.last_day) > 5:
            return self.last_day
        if len(self.last_hour) > 5:
            return self.last_hour
        return self.last_five_minute

    def append(self, environmental_data):
        self.input_buffer.append(environmental_data)
        self.average_history()

    def average_history(self):
        self.average_last_minute()
        self.average_last_hour()

    def average_last_minute(self):
        if len(self.input_buffer) > 1:
            self.last_five_minute.append(self.input_buffer[-1])
            seconds_diff = (self.input_buffer[-1].datetime - self.input_buffer[0].datetime).total_seconds()

            if seconds_diff >= 60:
                self.average_data(self.input_buffer, self.last_hour)
                self.input_buffer.clear()

    def average_last_hour(self):
        if len(self.last_hour) > 1:
            minutes_diff = (self.last_hour[-1].datetime - self.last_hour[0].datetime).total_seconds() / 60.0

            if minutes_diff >= 60:
                self.average_data(self.last_hour, self.last_day)

    @staticmethod
    def average_data(container_from, container_to):
        sum_temp = sum([o.temperature for o in container_from])
        sum_hum = sum([o.rel_humidity for o in container_from])
        container_to.append(EnvironmentalData(sum_temp / len(container_from), sum_hum / len(container_from)))
