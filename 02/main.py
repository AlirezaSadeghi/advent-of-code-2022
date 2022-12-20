import os
from pathlib import Path

losing_strat = ["C", "A", "B"]
winning_strat = ["B", "C", "A"]


def shape_score(shape):
    return ord(shape) - ord("A") + 1


def best_play(op, strat):
    _shape_score = shape_score(strat)

    if strat == op:
        return 3 + _shape_score
    if op == losing_strat[ord(strat) - ord("A")]:
        return 6 + _shape_score

    return _shape_score


def round_result(op, strat):
    shape, score = op, 3
    index = ord(op) - ord("A")
    if strat == "C":
        shape, score = winning_strat[index], 6
    elif strat == "A":
        shape, score = losing_strat[index], 0

    return shape_score(shape) + score


def process_input(input_path, strategy=best_play):
    score = 0
    with open(input_path, "r") as input_file:
        for line in input_file:
            op, strat = line.split()
            score += strategy(op, chr(ord(strat) - 23))
    return score


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")
    print("1: ", process_input(input_path, strategy=best_play))
    print("2: ", process_input(input_path, strategy=round_result))
