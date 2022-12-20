import os
from pathlib import Path


def overlaps(pair1, pair2, strict=False):
    [lmin, lmax], [rmin, rmax] = map(int, pair1.split("-")), map(int, pair2.split("-"))
    if strict:
        return (lmin <= rmin and lmax >= rmax) or (rmin <= lmin and rmax >= lmax)

    return (lmin <= rmax and lmax >= rmin) or (rmin <= lmax and rmax >= lmin)


def process_inputs(input_path, strict=False):
    count = 0
    with open(input_path, "r") as input_file:
        for line in input_file:
            pair = line.strip().split(",")
            if overlaps(pair[0], pair[1], strict=strict):
                count += 1
    return count


if __name__ == "__main__":
    input_path = os.path.join(Path(__file__).parent.absolute(), "tst.txt")
    print("1: ", process_inputs(input_path, strict=True))
    print("2: ", process_inputs(input_path, strict=False))
