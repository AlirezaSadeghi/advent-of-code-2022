import os
import re

from copy import deepcopy
from pathlib import Path


class Monkey:
    def __init__(
        self,
        _id=None,
        items=None,
        operation_fn_str=None,
        test_fn_int=None,
        test_true=None,
        test_false=None,
        lcm_of_divisors=None
    ):
        self.id = _id
        self.items = items
        self.operation_fn_str = operation_fn_str
        self.test_fn_int = test_fn_int
        self.test_true = test_true
        self.test_false = test_false
        self.num_inspects = 0
        self.lcm_of_divisors = lcm_of_divisors

    @property
    def operation_fn(self):
        return lambda old: eval(self.operation_fn_str)

    @property
    def test_fn(self):
        return lambda x: x % self.test_fn_int == 0

    def adapt_worrieness(self, value):
        if self.lcm_of_divisors:
            return value % self.lcm_of_divisors

        return int(value / 3)

    def inspect(self):
        for idx in range(len(self.items)):
            self.num_inspects += 1
            self.items[idx] = self.adapt_worrieness(self.operation_fn(self.items[idx]))

    @property
    def throw_destinations(self):
        _results = []

        for item in self.items:
            if self.test_fn(item):
                _results.append(self.test_true)
            else:
                _results.append(self.test_false)

        return _results

    def clear(self):
        self.items = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.id + 1}: Inspects:{self.num_inspects} | {self.items}"


class State:
    def __init__(self, monkeys, worrisome=True):
        self.monekys = monkeys
        if not worrisome:
            lcm_of_divisors = 1
            for item in self.monekys:
                lcm_of_divisors *= item.test_fn_int
            for item in self.monekys:
                item.lcm_of_divisors = lcm_of_divisors

    def play_round(self):
        for monkey in self.monekys:
            monkey.inspect()
            for item, destination in zip(monkey.items, monkey.throw_destinations):
                self.monekys[destination].items.append(item)
            monkey.clear()

    @property
    def monkey_business(self):
        top_inspections = sorted(
            [item.num_inspects for item in self.monekys], key=lambda x: -x
        )
        return top_inspections[0] * top_inspections[1]


def process_input(input_path):
    monkeys = []

    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            if line.startswith("Monkey"):
                monkeys.append(Monkey(int(line.split()[1][:-1])))
            elif line.startswith("Starting items: "):
                monkeys[-1].items = list(
                    map(int, line.replace("Starting items: ", "").split(", "))
                )
            elif line.startswith("Operation: new = "):
                monkeys[-1].operation_fn_str = line.split("Operation: new = ")[1]
            elif line.startswith("Test: divisible by "):
                monkeys[-1].test_fn_int = int(line.split()[-1])
            elif line.startswith("If true"):
                monkeys[-1].test_true = int(line.split()[-1])
            elif line.startswith("If false"):
                monkeys[-1].test_false = int(line.split()[-1])

    return monkeys


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    monkeys = process_input(input_path)
    
    state = State(deepcopy(monkeys))
    for _ in range(20):
        state.play_round()
    print("1: ", state.monkey_business)

    state = State(deepcopy(monkeys), worrisome=False)
    for idx in range(10000):
        state.play_round()
    print("2: ", state.monkey_business)

