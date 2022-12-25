import os

from pathlib import Path
from itertools import zip_longest

DISTRESS_1 = [[2]]
DISTRESS_2 = [[6]]

def process_input(input_path):
    items = [[]]
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            if not line:
                items.append([])
                continue

            items[-1].append(eval(line))
    return items


def compare(left, right):
    for l, r in zip_longest(left, right):
        if l is None:
            return True
        if r is None:
            return False

        if isinstance(l, int) and isinstance(r, int):
            if l > r:
                return False
            if r > l:
                return True
        else:
            _can_detect = compare(
                l if isinstance(l, list) else [l],
                r if isinstance(r, list) else [r]
            )
            if _can_detect is not None:
                return _can_detect

def decode(packets):
    def peek(signal):
        if isinstance(signal, int):
            return signal
        elif isinstance(signal, list):
            if len(signal) == 0:
                return 0
            return peek(signal[0])

    packets = sorted(packets, key=lambda x: peek(x))
    return (packets.index(DISTRESS_1) + 1) * (packets.index(DISTRESS_2) + 1)


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    packets = process_input(input_path)

    flattened = [DISTRESS_1, DISTRESS_2]
    right_order_indexes = []
    for idx, (left, right) in enumerate(packets):
        if compare(left, right):
            right_order_indexes.append(idx + 1)
        flattened.append(left)
        flattened.append(right)

    print("1: ", sum(right_order_indexes))
    print("2: ", decode(flattened))


