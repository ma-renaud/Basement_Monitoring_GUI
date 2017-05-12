from state_machine import StateMachine
from serial_states import *


class SerialDecoder(StateMachine):
    def __init__(self):
        StateMachine.__init__(self, WaitForStart(self))

    def decode(self, _inputs):
        StateMachine.process(self, _inputs)

    def reception_start(self): pass

    def receive_data(self): pass

    def append_received_data(self): pass

    def reception_complete(self): pass
