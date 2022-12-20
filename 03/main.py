import os
from pathlib import Path


def calculate_score(intersect):
    return ord(intersect) - ((ord("A") - 26) if intersect.isupper() else ord("a")) + 1


def get_priority(*inputs):
    tmp_set = set(inputs[0])
    for item in inputs[1:]:
        tmp_set = tmp_set.intersection(set(item))
    return calculate_score(tmp_set.pop())


def process_for_item_prio(input_path):
    score = 0
    with open(input_path, "r") as input_file:
        for line in input_file:
            length = len(line)
            score += get_priority(line[: length // 2], line[length // 2 :])
    return score


def process_for_badge_prio(input_path):
    score = 0
    with open(input_path, "r") as input_file:
        group = []
        for line in input_file:
            group.append(line.strip())
            if len(group) == 3:
                score += get_priority(*group)
                group = []
    return score


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")

    print("1: ", process_for_item_prio(input_path))
    print("2: ", process_for_badge_prio(input_path))
