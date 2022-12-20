import os

from pathlib import Path

def process_input(input_path):
    grid = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            grid.append(list(map(int, line.strip())))
    return grid


def find_visible_trees(grid):
    edge_nodes = 4 * (len(grid) - 1)

    internal_nodes = 0
    for idx in range(1, len(grid) - 1):
        for jdx in range(1, len(grid[0]) - 1):
            cur_tree = grid[idx][jdx]
            row, col = grid[idx], [item[jdx] for item in grid]

            lv = max(row[:jdx]) < cur_tree
            rv = max(row[jdx+1:]) < cur_tree
            tv = max(col[:idx]) < cur_tree
            bv = max(col[idx+1:]) < cur_tree

            if any([lv, rv, tv, bv]):
                internal_nodes += 1

    return edge_nodes + internal_nodes

def find_scenic_score(grid):
    cur_ss = 0
    for idx in range(1, len(grid) - 1):
        for jdx in range(1, len(grid[0]) - 1):
            cur_tree = grid[idx][jdx]
            row, col = grid[idx], [item[jdx] for item in grid]

            lss, rss, tss, bss = 0, 0, 0, 0

            for kdx in range(1, jdx + 1):
                lss += 1
                if row[jdx - kdx] >= cur_tree:
                    break
            
            for kdx in range(1, idx + 1):
                tss += 1
                if col[idx - kdx] >= cur_tree:
                    break
            
            for kdx in range(1, len(row) - jdx):
                rss += 1
                if row[jdx + kdx] >= cur_tree:
                    break
            
            for kdx in range(1, len(col) - idx):
                bss += 1
                if col[idx + kdx] >= cur_tree:
                    break
            
            cur_ss = max(cur_ss, lss * rss * tss * bss)
    
    return cur_ss
            

if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    grid = process_input(input_path)
    print("1: ", find_visible_trees(grid))
    print("2: ", find_scenic_score(grid))