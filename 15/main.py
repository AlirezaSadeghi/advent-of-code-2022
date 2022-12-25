import os
import re
from collections import defaultdict

from pathlib import Path


def process_input(input_path):
    mapping = {}
    with open(input_path, "r") as input_file:
        for line in input_file:
            signal = line.strip()
            match = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", signal)
            if match:
                sx, sy, bx, by = map(int, match.groups())
                mapping[(sx, sy)] = (bx, by)
    return mapping


def calculate_distances(mapping):
    distances = {}
    for (sx, sy), (bx, by) in mapping.items():
        distances[(sx, sy)] = abs(sx - bx) + abs(sy - by)
    return distances


def apply_coverage(distances, beacons_map):
    min_i, min_j, max_i, max_j = 1000, 1000, -1000, -1000
    coverage_grid = defaultdict(lambda: defaultdict(lambda: "."))
    for (sj, si), distance in distances.items():
        for idx in range(-distance, distance + 1):
            for jdx in range(-distance, distance + 1):
                if abs(idx) + abs(jdx) > distance:
                    continue

                _i = si + idx
                _j = sj + jdx
                coverage_grid[_i][_j] = "#"

                min_i, min_j = min(min_i, _i), min(min_j, _j)
                max_i, max_j = max(max_i, _i), max(max_j, _j)

    for (sj, si), (bj, bi) in beacons_map.items():
        coverage_grid[si][sj] = "S"
        coverage_grid[bi][bj] = "B"

    return coverage_grid, min_i, min_j, max_i, max_j


def visualize(grid, coverage_grid, min_i, min_j, max_i, max_j):
    for idx in range(min_i, max_i + 1):
        print(f"{idx}:", end="")
        for jdx in range(min_j, max_j + 1):
            if (jdx, idx) in grid:
                print("S", end="")
            else:
                print(coverage_grid[idx][jdx], end="")
        print()


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    sensor_beacon_map = process_input(input_path)
    sensor_beacon_distance = calculate_distances(sensor_beacon_map)
    coverage_grid, min_i, min_j, max_i, max_j = apply_coverage(sensor_beacon_distance, sensor_beacon_map)

    query_row = 2000000
    count = 0
    row = coverage_grid[query_row]
    for value in row.values():
        if value == "#":
            count += 1
    # visualize(sensor_beacon_map, coverage_grid, min_i, min_j, max_i, max_j)
    print("1: ", count, min_j, max_j)
