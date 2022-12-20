import os
from pathlib import Path
from typing import List


def process_input() -> List[int]:
    with open(
        os.path.join(Path(__file__).parent.absolute(), "input.txt"), "r"
    ) as input_file:
        elves = []
        calories = 0
        for line in input_file:
            if line and line != "\n":
                calories += int(line)
            else:
                elves.append(calories)
                calories = 0

    return elves


def top_calorie_carriers(elves: List[int], n: int = 1) -> int:
    return sorted(elves, key=lambda x: -x)[:n]


if __name__ == "__main__":
    elves = process_input()
    print("1: ", top_calorie_carriers(elves)[0])
    print("2: ", sum(top_calorie_carriers(elves, n=3)))
