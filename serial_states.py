from state import State


class WaitForStart(State):
    def run(self, _input):
        if _input == "<":
            self.context.reception_start()
            self.context.currentState = ReceiveData(self.context)


class ReceiveData(State):
    def run(self, _input):
        if _input == ">":
            self.context.append_received_data()
            self.context.reception_complete()
        elif _input == ",":
            self.context.append_received_data()
        else:
            self.context.receive_data()
