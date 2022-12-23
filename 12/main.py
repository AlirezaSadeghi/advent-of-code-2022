import os

from pathlib import Path


def neighbors(grid, start, visited):
    candidates = []
    for idx in range(-1, 2):
        for jdx in range(-1, 2):
            if abs(idx ^ jdx) != 1:
                continue

            i, j = start[0] + idx, start[1] + jdx
            if i>=0 and j>=0 and i < len(grid) and j < len(grid[0]):
                if (i,j) != start:
                    if grid[i][j] - grid[start[0]][start[1]] <= 1:
                        if (i, j) not in visited or visited[start] - 1 >= visited[(i, j)]:
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
    visited = {start: 0}
    queue = [start]

    while queue:
        node = queue.pop(0)
        if node == end:
            return visited[node]
        _n = neighbors(grid, node, visited)
        for neighbor in _n:
            visited[neighbor] = visited[node] + 1
            queue.append(neighbor)


def process_input(input_path, count_a=False):
    grid = []
    start, end = [0,0], [0, 0]
    a_positions = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.split()[0]
            
            _res = []
            for idx, char in enumerate(line):
                if char == "S":
                    char = "a"
                    start = [len(grid), idx]
                if char == "E":
                    char = "z"
                    end = [len(grid), idx]

                if count_a and char == "a":
                    a_positions.append((len(grid), idx))

                _res.append(ord(char) - ord("a"))
            
            grid.append(_res)

    return grid, start, end, a_positions

if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    grid, start, end, a_positions = process_input(input_path, count_a=True)
    print("1: ", bfs_non_rec(grid, tuple(start), tuple(end)))
    print("2: ", min([bfs_non_rec(grid, tuple(node), tuple(end)) for node in a_positions]))
