import os
import re
from collections import defaultdict

COLUMN_WIDTH = 4


def pad_list(lst: list[str], n: int) -> list[str]:
    """pad a list with empty strings"""
    return lst + [""] * (n - len(lst))


def get_crate_array(line: str) -> list[str]:
    """get the crates from a line"""
    return [
        line[i : i + COLUMN_WIDTH].strip().strip("[]")
        for i in range(0, len(line), COLUMN_WIDTH)
    ]


def get_data(file_name: str) -> (defaultdict[list], list[list[int, int, int]]):
    with open(file_name) as f:

        moves = []
        stacks = defaultdict(list)
        num_stacks = 0
        lines = f.readlines()
        last_line = 0
        for i, line in enumerate(lines):
            last_line = i
            if line.startswith(" 1 "):
                break
            crate_array = get_crate_array(line=line)

            for i, crate in enumerate(crate_array):
                if crate != "":
                    stacks[i + 1].append(crate)
                    num_stacks = max(num_stacks, i + 1)

        # reverse the order of the crates so the top of the stack is the last element
        for k, v in stacks.items():
            stacks[k] = v[::-1]

        for line in lines[last_line:]:
            m = re.match(r"move (\d+) from (\d+) to (\d+)", line)
            if m:
                moves.append(list(map(int, m.groups())))

        return stacks, moves


def solution(
    stacks: defaultdict[list], moves: list[list[int, int, int]], reverse_order=True
) -> str:

    step = -1 if reverse_order else 1
    for qty, from_stack, to_stack in moves:
        print(qty, from_stack, to_stack, stacks[from_stack][-qty:])
        stacks[to_stack].extend(stacks[from_stack][-qty:][::step])
        stacks[from_stack] = stacks[from_stack][:-qty]
    print(stacks)
    return "".join(stacks[k][-1] for k in sorted(stacks.keys()))


if __name__ == "__main__":
    stacks, moves = get_data(file_name="inputs/day-5-input.txt")
    print("solution 1:", solution(stacks=stacks, moves=moves, reverse_order=True))

    stacks, moves = get_data(file_name="inputs/day-5-input.txt")
    print("solution 2:", solution(stacks=stacks, moves=moves, reverse_order=False))
