from collections import deque
from environmental_data import EnvironmentalData
from numpy import sum
from enum import Enum


class TimeScale(Enum):
    SECONDS = 1
    MINUTES = 2
    HOURS = 3


class EnvironmentalDataHistory:
    def __init__(self):
        self.seconds_buffer = list()
        self.hours_buffer = list()
        self.last_five_minute = deque(maxlen=320)
        self.last_hour = deque(maxlen=60)
        self.last_day = deque(maxlen=24)
        self.current_scale = TimeScale.SECONDS

    @property
    def last(self):
        return self.last_five_minute[-1]

    @property
    def time_scale(self):
        return self.current_scale

    def set_time_scale(self):
        if len(self.last_day) > 5:
            self.current_scale = TimeScale.HOURS
        elif len(self.last_hour) > 5:
            self.current_scale = TimeScale.MINUTES
        else:
            self.current_scale = TimeScale.SECONDS

    def get_history(self, scale):
        if scale is TimeScale.HOURS:
            return self.last_day
        if scale is TimeScale.MINUTES:
            return self.last_hour
        return self.last_five_minute

    def append(self, environmental_data):
        self.seconds_buffer.append(environmental_data)
        self.average_history()
        self.set_time_scale()

    def average_history(self):
        self.average_last_minute()
        self.average_last_hour()

    def average_last_minute(self):
        if len(self.seconds_buffer) > 1:
            self.last_five_minute.append(self.seconds_buffer[-1])

            seconds_diff = (self.seconds_buffer[-1].datetime - self.seconds_buffer[0].datetime).total_seconds()
            if seconds_diff >= 60:
                self.last_hour.append(self.average_data(self.seconds_buffer, self.hours_buffer))
                self.seconds_buffer.clear()

    def average_last_hour(self):
        if len(self.hours_buffer) > 1:
            minutes_diff = (self.hours_buffer[-1].datetime - self.hours_buffer[0].datetime).total_seconds() / 60.0

            if minutes_diff >= 60:
                self.average_data(self.hours_buffer, self.last_day)
                self.hours_buffer.clear()

    @staticmethod
    def average_data(container_from, container_to):
        sum_temp = sum([o.temperature for o in container_from])
        sum_hum = sum([o.rel_humidity for o in container_from])
        env = EnvironmentalData(sum_temp / len(container_from), sum_hum / len(container_from))
        container_to.append(env)
        return env
