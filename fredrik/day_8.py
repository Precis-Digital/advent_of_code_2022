import itertools
from typing import Generator, Iterable

from shared import utils

Grid = list[list[int]]


def generate_grid(map_: str) -> Grid:
    return [list(map(int, row)) for row in map_.splitlines()]


def is_outer(grid: Grid, x: int, y: int) -> bool:
    return x == 0 or y == 0 or x == len(grid) - 1 or y == len(grid) - 1


def left_visible(grid: Grid, x: int, y: int) -> bool:
    return grid[y][x] > max(grid[y][:x])


def right_visible(grid: Grid, x: int, y: int) -> bool:
    return grid[y][x] > max(grid[y][x + 1 :])


def top_visible(grid: Grid, x: int, y: int) -> bool:
    for row in grid[:y]:
        if row[x] >= grid[y][x]:
            return False
    return True


def bottom_visible(grid: Grid, x: int, y: int) -> bool:
    for row in grid[y + 1 :]:
        if row[x] >= grid[y][x]:
            return False
    return True


def is_visible(grid: Grid, x: int, y: int) -> bool:
    kwargs = locals()
    return (
        is_outer(**kwargs)
        or left_visible(**kwargs)
        or right_visible(**kwargs)
        or top_visible(**kwargs)
        or bottom_visible(**kwargs)
    )


def viewing_distance(height: int, tree_line: Iterable[int]) -> int:
    viewing_distance_ = 0
    for tree in tree_line:
        viewing_distance_ += 1
        if tree >= height:
            return viewing_distance_

    return viewing_distance_


def viewing_distance_left(grid: Grid, x: int, y: int) -> int:
    return viewing_distance(height=grid[y][x], tree_line=reversed(grid[y][:x]))


def viewing_distance_right(grid: Grid, x: int, y: int) -> int:
    return viewing_distance(height=grid[y][x], tree_line=grid[y][x + 1 :])


def viewing_distance_up(grid: Grid, x: int, y: int) -> int:
    return viewing_distance(
        height=grid[y][x], tree_line=reversed([grid[i][x] for i in range(y)])
    )


def viewing_distance_down(grid: Grid, x: int, y: int) -> int:
    return viewing_distance(
        height=grid[y][x], tree_line=[grid[i][x] for i in range(y + 1, len(grid))]
    )


def calculate_scenic_score(grid: Grid, x: int, y: int) -> int:
    kwargs = locals()
    return (
        viewing_distance_left(**kwargs)
        * viewing_distance_right(**kwargs)
        * viewing_distance_up(**kwargs)
        * viewing_distance_down(**kwargs)
    )


def all_indices(grid: Grid) -> Generator[tuple[int, int], None, None]:
    grid_size_range = range(len(grid))
    for x, y in itertools.product(grid_size_range, grid_size_range):
        yield x, y


def count_visible(grid: Grid) -> int:
    count = 0
    for x, y in all_indices(grid=grid):
        if is_visible(grid=grid, x=x, y=y):
            count += 1

    return count


def highest_scenic_score(grid: Grid) -> int:
    max_ = 0
    for x, y in all_indices(grid=grid):
        score = calculate_scenic_score(grid=grid, x=x, y=y)
        if score > max_:
            max_ = score

    return max_


def main() -> None:
    height_map = utils.read_input_to_string()
    grid = generate_grid(map_=height_map)
    visible_trees = count_visible(grid=grid)
    max_scenic_score = highest_scenic_score(grid=grid)

    print(f"Part 1: {visible_trees}")
    print(f"Part 2: {max_scenic_score}")


if __name__ == "__main__":
    main()
