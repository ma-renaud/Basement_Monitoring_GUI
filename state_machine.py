class StateMachine:
    def __init__(self, initial_state):
        self.currentState = initial_state

    # Template method:
    def process(self, inputs):
        for i in inputs:
            self.currentState.run(i)
