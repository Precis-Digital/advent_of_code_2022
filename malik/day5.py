import os
import copy
import re
from collections import defaultdict

COLUMN_WIDTH = 4


def pad_list(lst: list[str], n: int) -> list[str]:
    """pad a list with empty strings"""
    return lst + [""] * (n - len(lst))


def get_crate_array(line: str) -> list[str]:
    """get the crates from a line"""
    return [m[1] for m in re.findall(r"(\[([A-Z])\]\s)|((\s){3}\s)", line)]


def extract_stacks(lines: list[str]) -> defaultdict[list]:
    stacks = defaultdict(list)
    for line in lines:
        crate_array = get_crate_array(line=line)
        for i, crate in enumerate(crate_array):
            if crate != "":
                stacks[i + 1].append(crate)

    # reverse the order of the crates so the top of the stack is the last element
    # this all treats the stacks as stacks, not queues!!
    for k, v in stacks.items():
        stacks[k] = v[::-1]
    return stacks


def extract_moves(lines: list[str]) -> list[list[int, int, int]]:
    moves = []
    for line in lines:
        m = re.match(r"move (\d+) from (\d+) to (\d+)", line)
        if m:
            moves.append(list(map(int, m.groups())))
    return moves


def get_data(file_name: str) -> (defaultdict[list], list[list[int, int, int]]):
    with open(file_name) as f:
        lines = f.readlines()
        lines_with_crates = [line for line in lines if "[" in line]
        stacks = extract_stacks(lines=lines_with_crates)
        moves = extract_moves(lines=lines)

        return stacks, moves


def solution(
    stacks: defaultdict[list],
    moves: list[list[int, int, int]],
    reverse_order_when_moving=True,
) -> str:
    # done so it doesnt mutate the original
    stacks = copy.deepcopy(stacks)
    step = -1 if reverse_order_when_moving else 1
    for qty, from_stack, to_stack in moves:
        # print(qty, from_stack, to_stack, stacks[from_stack][-qty:])
        stacks[to_stack].extend(stacks[from_stack][-qty:][::step])
        stacks[from_stack] = stacks[from_stack][:-qty]
    # print(stacks)
    return "".join(stacks[k][-1] for k in sorted(stacks.keys()))


if __name__ == "__main__":
    stacks, moves = get_data(file_name="inputs/day-5-input.txt")
    print(
        "solution 1:",
        solution(stacks=stacks, moves=moves, reverse_order_when_moving=True),
    )
    print(
        "solution 2:",
        solution(stacks=stacks, moves=moves, reverse_order_when_moving=False),
    )
