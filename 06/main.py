import os
from pathlib import Path


def process_input(input_path):
    with open(input_path, "r") as input_file:
        return input_file.read().strip()


def find_closest_non_repeating_window(line, size=4):
    for idx in range(len(line) - size + 1):
        if len(set(line[idx : idx + size])) == size:
            return idx + size


if __name__ == "__main__":
    line = process_input(os.path.join(Path(__file__).parent.absolute(), "input.txt"))
    print("1: ", find_closest_non_repeating_window(line))
    print("2: ", find_closest_non_repeating_window(line, size=14))
