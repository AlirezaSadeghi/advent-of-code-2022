import re
import json
from os.path import join

from pathlib import Path


def get_nested_item(dic, index, default=None):
    try:
        if len(index) == 1:
            return dic[index[0]]
        level_elem = get_nested_item(dic[index[0]], index[1:], default=default)
    except KeyError:
        return default
    return level_elem


class FileSystem:
    def __init__(self, root):
        self.cwd = [root]
        self.tree = {root: {}}

    def cd(self, path):
        if path == "..":
            del self.cwd[-1]
        else:
            self.cwd.append(path)
            if not get_nested_item(self.tree, self.cwd):
                get_nested_item(self.tree, self.cwd[:-1])[path] = {}

    def ls(self, results):
        dir_size = 0
        fs_node = get_nested_item(self.tree, self.cwd)
        for output in results:
            if output.startswith("dir"):
                continue
            fsize, fname = output.split()
            dir_size += int(fsize)
            fs_node[fname] = fsize

        if "sum_size" not in fs_node:
            fs_node["sum_size"] = dir_size
            for idx in range(1, len(self.cwd)):
                get_nested_item(self.tree, self.cwd[:idx])["sum_size"] += dir_size


def process_inputs(input_path):
    commands = []
    with open(input_path, "r") as input_file:
        for command in input_file:
            commands.append(command.strip())
    return commands


def find_small_directories(tree, size_limit=100000):
    layer_sum = 0
    if tree["sum_size"] <= size_limit:
        layer_sum += tree["sum_size"]

    for value in tree.values():
        if isinstance(value, dict):
            layer_sum += find_small_directories(value, size_limit)

    return layer_sum


def find_min_directory_to_free_up(tree, to_free, min_so_far):
    if tree["sum_size"] <= to_free:
        return min_so_far

    for value in tree.values():
        if isinstance(value, dict):
            min_so_far = min(
                min_so_far, find_min_directory_to_free_up(value, to_free, min_so_far)
            )

    return min(min_so_far, tree["sum_size"])


if __name__ == "__main__":
    input_path = join(Path(__file__).parent.absolute(), "input.txt")

    fs = FileSystem("/")

    history = process_inputs(input_path)[1:]

    idx = 0
    while idx < len(history):
        if history[idx] == "$ ls":
            idx += 1
            ls_results = []
            while idx < len(history) and not history[idx].startswith("$"):
                ls_results.append(history[idx])
                idx += 1
            fs.ls(ls_results)
        else:
            fs.cd(re.match("\$ cd (.+)", history[idx]).groups()[0])
            idx += 1

    print("1: ", find_small_directories(fs.tree["/"]))
    print(
        "2: ",
        find_min_directory_to_free_up(
            fs.tree["/"], fs.tree["/"]["sum_size"] - 40000000, 70000000
        ),
    )
