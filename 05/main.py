import os
import re
from pathlib import Path


def process_inputs(input_path):
    stacks = []
    commands = []
    caught_stack_identifiers = False
    with open(input_path, "r") as input_file:
        for line in input_file:
            line = line.strip("\n")
            if not line:
                continue
            if line[1].isdigit():
                caught_stack_identifiers = True
                continue

            if not caught_stack_identifiers:
                for idx, character in enumerate(line):
                    if idx % 4 == 1:
                        stack_index = idx // 4
                        if stack_index + 1 > len(stacks):
                            stacks.append([])
                        if character.strip():
                            stacks[stack_index].insert(0, character)

            if caught_stack_identifiers:
                match = re.match("move (\d+) from (\d+) to (\d+)", line)

                commands.append(list(map(int, match.groups())))

    return stacks, commands


def process_commands(stacks, commands, new_model=False):
    for command in commands:
        count = command[0]
        f_idx, t_idx = command[1] - 1, command[2] - 1
        if new_model:
            stacks[t_idx] += stacks[f_idx][-count:]
            del stacks[f_idx][-count:]
        else:
            for _ in range(count):
                elem = stacks[f_idx].pop()
                stacks[t_idx].append(elem)

    return stacks


def read_heads(stacks):
    result = ""
    for stack in stacks:
        result += stack[-1]
    return result


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "input.txt")
    stacks, commands = process_inputs(input_path)

    print("1: ", read_heads(process_commands([item[:] for item in stacks], commands)))
    print(
        "2: ",
        read_heads(process_commands([item[:] for item in stacks], commands, True)),
    )
