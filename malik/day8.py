import copy
import timeit
import time
import sys

sys.setrecursionlimit(1500)


def get_data(fname):
    grid_dict = {}
    R, C = 0, 0
    with open(fname) as f:
        lines = f.readlines()
        for r, line in enumerate(lines):
            line = line.strip()
            R = r
            for c, v in enumerate(list(map(int, line))):
                C = c
                grid_dict[(r, c)] = {
                    "value": v,
                    "left": None,
                    "right": None,
                    "top": None,
                    "down": None,
                }
    return grid_dict, R, C


COUNTER = 0
COUNTER_CACHE_MISS = 0

DIRECTIONS = {
    "top": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


def get_max_direction(
    grid_dict, r, c, max_r, max_c, direction, max_value=None, solution=2
):
    global COUNTER, COUNTER_CACHE_MISS
    COUNTER += 1
    cell_max = grid_dict[(r, c)][direction]
    if cell_max:
        return cell_max

    edge_tuple = (-1, r, c)

    COUNTER_CACHE_MISS += 1

    if direction == "left" and c == 0:
        grid_dict[(r, c)][direction] = edge_tuple
        return edge_tuple
    elif direction == "right" and c == max_c:
        grid_dict[(r, c)][direction] = edge_tuple
        return edge_tuple
    elif direction == "top" and r == 0:
        grid_dict[(r, c)][direction] = edge_tuple
        return edge_tuple
    elif direction == "down" and r == max_r:
        grid_dict[(r, c)][direction] = edge_tuple
        return edge_tuple

    if cell_max is None:
        # print("missed cache", direction, r, c)
        direction_r, direction_c = DIRECTIONS[direction]
        new_r = r + direction_r
        new_c = c + direction_c
        # md =

        # if the cell values are equal then should pick the nearest one
        # solves solution 1
        if solution == 1:
            grid_dict[(r, c)][direction] = max(
                (grid_dict[(new_r, new_c)]["value"], new_r, new_c),
                get_max_direction(
                    grid_dict, new_r, new_c, max_r, max_c, direction, solution=1
                ),
            )
            return grid_dict[(r, c)][direction]

        elif solution == 2:
            if grid_dict[(new_r, new_c)]["value"] >= max_value:
                # print(grid_dict[(new_r, new_c)], grid_dict[(r, c)]["value"])
                return (
                    grid_dict[(new_r, new_c)]["value"],
                    new_r,
                    new_c,
                )
            else:
                return get_max_direction(
                    grid_dict,
                    new_r,
                    new_c,
                    max_r,
                    max_c,
                    direction,
                    max_value=max_value,
                    solution=2,
                )

        return grid_dict[(r, c)][direction]
    return cell_max


def compute_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def solution1(grid_dict, R, C):
    counter = 0
    t = time.time()
    for r in range(R + 1):
        for c in range(C + 1):
            v = grid_dict[(r, c)]["value"]
            if r == 0 or r == R or c == 0 or c == C:
                counter += 1
            elif v > get_max_direction(grid_dict, r, c, R, C, "left", solution=1)[0]:
                counter += 1
            elif v > get_max_direction(grid_dict, r, c, R, C, "right", solution=1)[0]:
                counter += 1
            elif v > get_max_direction(grid_dict, r, c, R, C, "top", solution=1)[0]:
                counter += 1
            elif v > get_max_direction(grid_dict, r, c, R, C, "down", solution=1)[0]:
                counter += 1

    print(counter, time.time() - t)


def solution2(grid_dict, R, C):
    score = 0
    for r in range(R + 1):
        for c in range(C + 1):
            if r == 0 or r == R or c == 0 or c == C:
                continue
            v = grid_dict[(r, c)]["value"]
            mdl = get_max_direction(
                grid_dict, r, c, R, C, "left", max_value=v, solution=2
            )
            mdr = get_max_direction(
                grid_dict, r, c, R, C, "right", max_value=v, solution=2
            )
            mdt = get_max_direction(
                grid_dict, r, c, R, C, "top", max_value=v, solution=2
            )
            mdd = get_max_direction(
                grid_dict, r, c, R, C, "down", max_value=v, solution=2
            )
            new_score = (
                compute_distance(r, c, mdl[1], mdl[2])
                * compute_distance(r, c, mdr[1], mdr[2])
                * compute_distance(r, c, mdt[1], mdt[2])
                * compute_distance(r, c, mdd[1], mdd[2])
            )
            # print(r, c, mdl, mdr, mdt, mdd, new_score)
            score = max(score, new_score)
    return score


def run_large():

    grid_dict, R, C = get_data(fname="inputs/day-8-large.txt")
    print(solution1(grid_dict, R, C))
    # print(COUNTER, COUNTER_CACHE_MISS)
    # grid_dict, R, C = get_data(fname="inputs/day-8-large.txt")
    # print(solution2(grid_dict, R, C))


if __name__ == "__main__":
    import timeit

    print("MW timeit 10 runs: ", timeit.timeit(run_large, number=10) / 10)
