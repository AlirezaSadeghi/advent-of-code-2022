import os
from collections import defaultdict

from pathlib import Path


class Grid:

    def __init__(self, snapshot, has_floor=False):
        self.grid = defaultdict(lambda: ".")

        for row in snapshot:
            for (sj, si), (ej, ei) in zip(row, row[1:]):
                if sj == ej:
                    for idx in range(min(si, ei), max(si, ei) + 1):
                        self.grid[(idx, sj)] = "#"
                if si == ei:
                    for jdx in range(min(sj, ej), max(sj, ej) + 1):
                        self.grid[(si, jdx)] = "#"

        self.min_i = min(map(lambda x: x[0], self.grid.keys()))
        self.max_i = max(map(lambda x: x[0], self.grid.keys()))
        self.min_j = min(map(lambda x: x[1], self.grid.keys()))
        self.max_j = max(map(lambda x: x[1], self.grid.keys()))

        self.floor_height = None
        if has_floor:
            self.floor_height = self.max_i + 2
            for jdx in range(0, self.max_j * 2):
                self.grid[(self.floor_height, jdx)] = "#"

    def insert_sand(self, j, i):
        while True:
            if self.floor_height:
                if self.grid[(i, j)] == "o":
                    return False
            elif i >= self.max_i:
                return False

            if self.grid[(i + 1, j)] not in ["#", "o"]:
                i += 1
            elif self.grid[(i + 1, j - 1)] not in ["#", "o"]:
                i += 1
                j -= 1
            elif self.grid[(i + 1, j + 1)] not in ["#", "o"]:
                i += 1
                j += 1
            else:
                self.grid[(i, j)] = "o"
                break
        return True

    def visualize(self):
        for idx in range(self.min_i, ((self.floor_height or self.max_i) + 1)):
            for jdx in range(self.min_j, self.max_j + 1):
                print(self.grid[(idx, jdx)], end="")
            print()


def process_input(input_path):
    snapshot = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            snapshot.append([eval(item) for item in line.strip().split(" -> ")])
    return snapshot


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    vertical_snapshot = process_input(input_path)
    g = Grid(snapshot=vertical_snapshot)
    count = 0
    while g.insert_sand(500, 0):
        count += 1
    print("1: ", count)

    g2 = Grid(snapshot=vertical_snapshot, has_floor=True)
    count = 0
    while g2.insert_sand(500, 0):
        count += 1
    print("2: ", count)
