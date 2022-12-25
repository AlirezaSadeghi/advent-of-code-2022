import os

from pathlib import Path
from collections import defaultdict


def neighbors(grid, start, visited):
    candidates = []
    for idx in range(-1, 2):
        for jdx in range(-1, 2):
            if abs(idx ^ jdx) != 1:
                continue

            i, j = start[0] + idx, start[1] + jdx
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                if grid[i][j] - grid[start[0]][start[1]] <= 1:
                    if (i, j) not in visited:
                        candidates.append((i, j))
    return candidates


def bfs(grid, start, end, visited):
    if start == end:
        return 0

    if start not in visited:
        visited[start] = 1000000

    for neighbor in neighbors(grid, start, visited):
        visited[start] = min(visited[start], bfs(grid, neighbor, end, visited) + 1)

    return visited[start]


def bfs_non_rec(grid, start, end):
    visited = defaultdict(int)
    queue = [start]

    while queue:
        node = queue.pop(0)
        if node == end:
            return visited[node]

        for neighbor in neighbors(grid, node, visited):
            visited[neighbor] += visited[node] + 1

            queue.append(neighbor)


def process_input(input_path, count_a=False):
    grid = []
    start, end = [0, 0], [0, 0]
    a_positions = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.split()[0]

            _res = []
            for idx, char in enumerate(line):
                if count_a and char == "a":
                    a_positions.append((len(grid), idx))

                if char == "S":
                    char = "a"
                    start = [len(grid), idx]
                if char == "E":
                    char = "z"
                    end = [len(grid), idx]

                _res.append(ord(char) - ord("a"))

            grid.append(_res)

    return grid, start, end, a_positions


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    grid, start, end, a_positions = process_input(input_path, count_a=True)
    print("1: ", bfs_non_rec(grid, tuple(start), tuple(end)))

    nums = []
    for start in a_positions:
        _result = bfs_non_rec(grid, tuple(start), tuple(end))
        if _result:
            nums.append(_result)

    print("2: ", min(nums))
