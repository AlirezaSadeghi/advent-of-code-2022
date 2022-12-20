import os

from pathlib import Path

def process_input(input_path):
    moves = []
    with open(input_path, "r") as input_file:
        for line in input_file:
            direction, steps = line.strip().split()
            steps = int(steps)
            moves.append((direction, steps))
    return moves

def adapt_tail_position(knots_ij, head_idx, tail_idx):
    head_i, head_j, tail_i, tail_j = *knots_ij[head_idx], *knots_ij[tail_idx]
    if abs(head_i - tail_i) <= 1 and abs(head_j - tail_j) <= 1:
        return tail_i, tail_j, False
    
    diff = abs(head_i - tail_i) + abs(head_j - tail_j)
    # hori/vert move
    if diff == 2:
        # vertical move
        if head_i != tail_i:
            knots_ij[tail_idx][0] += 1 if head_i > tail_i else -1
        else:
            knots_ij[tail_idx][1] += 1 if head_j > tail_j else -1
    
    # diagonal move
    if diff > 2:
        knots_ij[tail_idx][0] += 1 if head_i > tail_i else -1
        knots_ij[tail_idx][1] += 1 if head_j > tail_j else -1

    return *knots_ij[tail_idx], True


def unique_tail_positions(moves, knots=2):
    tail_positions = set([(0, 0)])
    knots_ij = [[0, 0] for _ in range(knots)]
    
    for direction, steps in moves:
        for _ in range(steps):
            if direction == "D":
                knots_ij[0][0] -= 1
            elif direction == "U":
                knots_ij[0][0] += 1
            elif direction == "L":
                knots_ij[0][1] -= 1
            elif direction == "R":
                knots_ij[0][1] += 1

            for idx in range(1, len(knots_ij)):
                tail_i, tail_j, did_move = adapt_tail_position(knots_ij, idx - 1, idx)
                if not did_move:
                    break
                if idx == knots - 1:
                    tail_positions.add((tail_i, tail_j))

    
    return tail_positions

if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    moves = process_input(input_path)
    print("1: ", len(unique_tail_positions(moves)))
    print("2: ", len(unique_tail_positions(moves, knots=10)))
