from state_machine import StateMachine
from serial_states import *


class SerialDecoder(StateMachine):
    def __init__(self):
        StateMachine.__init__(self, WaitForStart(self))
        self.decoded = list()
        self.completed = False
        self.reception_buffer = ""

    def decode(self, _inputs):
        StateMachine.process(self, _inputs)

    def reception_start(self):
        self.decoded = list()
        self.completed = False
        self.reception_buffer = ""

    def receive_data(self, _input):
        self.reception_buffer += _input

    def append_received_data(self):
        self.decoded.append(float(self.reception_buffer))
        self.reception_buffer = ""

    def reception_complete(self):
        self.completed = True
