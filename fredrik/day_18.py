import collections
import functools
import itertools
import operator
from typing import Generator

from shared import utils

Point = tuple[int, int, int]


def parse_cubes_raw(cubes_raw: list[str]) -> set[Point]:
    return {tuple(map(int, cube.split(","))) for cube in cubes_raw}


def exposed_surface_area(cube: Point, cubes: set[Point]) -> int:
    return len(
        [neighbor for neighbor in neighbors(point=cube) if neighbor not in cubes]
    )


def exposed_inner_surface_area(cube: Point, trapped_air: set[Point]) -> int:
    return len(
        [neighbor for neighbor in neighbors(point=cube) if neighbor in trapped_air]
    )


def get_total_surface_area(cubes: set[Point]) -> int:
    return sum(exposed_surface_area(cube=cube, cubes=cubes) for cube in cubes)


def get_inner_surface_area(cubes: set[Point], air: set[Point]) -> int:
    return sum(exposed_inner_surface_area(cube=cube, trapped_air=air) for cube in cubes)


def get_min_max_points(cubes: set[Point]) -> list[int, ...]:
    min_max_coords = []
    for i in range(3):
        min_max_coords.append(min(cubes, key=operator.itemgetter(i))[i])
        min_max_coords.append(max(cubes, key=operator.itemgetter(i))[i])
    return min_max_coords


def get_all_possible_cubes(cubes: set[Point]) -> frozenset[Point]:
    x_min, x_max, y_min, y_max, z_min, z_max = get_min_max_points(cubes=cubes)

    x_boundaries = range(x_min, x_max + 1)
    y_boundaries = range(y_min, y_max + 1)
    z_boundaries = range(z_min, z_max + 1)

    return frozenset(
        (x, y, z)
        for x, y, z in itertools.product(x_boundaries, y_boundaries, z_boundaries)
    )


def neighbors(point: Point) -> Generator[Point, None, None]:
    yield point[0] + 1, point[1], point[2]
    yield point[0] - 1, point[1], point[2]
    yield point[0], point[1] + 1, point[2]
    yield point[0], point[1] - 1, point[2]
    yield point[0], point[1], point[2] + 1
    yield point[0], point[1], point[2] - 1


@functools.lru_cache
def out_of_bounds(search_space: frozenset[Point], point: Point) -> bool:
    return point not in search_space


def is_trapped(coord: Point, cubes: set[Point], search_space: frozenset[Point]):
    to_check = collections.deque([coord])
    checked = set()
    while to_check:
        point = to_check.popleft()
        for neighbor in neighbors(point=point):
            if neighbor in checked:
                continue

            checked.add(neighbor)

            if out_of_bounds(search_space=search_space, point=neighbor):
                return False

            if neighbor in cubes:
                continue

            to_check.append(neighbor)

    return True


def find_air_pockets(cubes: set[Point]) -> set[Point]:
    all_possible_cubes = get_all_possible_cubes(cubes=cubes)
    candidates = all_possible_cubes - cubes

    trapped = set()
    for candidate in candidates:
        if is_trapped(coord=candidate, cubes=cubes, search_space=all_possible_cubes):

            trapped.add(candidate)

    return trapped


def main() -> None:
    cubes_raw = utils.read_input_to_string().split()
    cubes = parse_cubes_raw(cubes_raw=cubes_raw)
    total_surface_area = get_total_surface_area(cubes=cubes)

    air = find_air_pockets(cubes=cubes)
    inner_surface_area = get_inner_surface_area(cubes=cubes, air=air)
    outer_surface_area = total_surface_area - inner_surface_area

    print(f"Part 1: {total_surface_area}")
    print(f"Part 2: {outer_surface_area}")


if __name__ == "__main__":
    main()
