import os
import re

from pathlib import Path
from collections import defaultdict


class SystemState:

    def __init__(self, X=1):
        self.X = X
        self.clock = 0
        self.cycle_history = defaultdict(int)

    def tick(self):
        self.clock += 1
        self.cycle_history[self.clock] = self.X        

    def _execute_add_command(self, value):
        for _ in range(2):
            self.tick()
        self.X = self.X + value
        # self.tick()

    def _execute_noop_command(self):
        self.tick()

    def execute_command(self, command):
        if command == "noop":
            self._execute_noop_command()
        else:
            self._execute_add_command(int(command.split(" ")[1]))


    def get_signal_strength(self, start=20, step=40):
        strength = 0
        for idx in range(20, len(self.cycle_history), step):
            strength += (self.cycle_history[idx] * idx)
        return strength

class CRTDisplay:

    def __init__(self, state):
        self.state = state
    
    def render_screen(self):
        for idx in range(0, len(self.state.cycle_history)):
            if idx % 40 == 0:
                print("")
            X_register = state.cycle_history[idx + 1]

            if (idx % 40) in range(X_register - 1, X_register + 2):
                print("#", end="")
            else:
                print(".", end="")
            

def process_input(input_path):
    commands = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            commands.append(line.strip())
    return commands

if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    commands = process_input(input_path)
    
    state = SystemState()
    for command in commands:
        state.execute_command(command)
    state.tick()
    
    crt = CRTDisplay(state)

    print("1: ", state.get_signal_strength())
    print("2:")
    crt.render_screen()
