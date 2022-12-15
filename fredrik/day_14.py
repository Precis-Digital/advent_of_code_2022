from __future__ import annotations

import collections
import dataclasses
import itertools
import sys
from typing import Iterable

from shared import utils


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def above(self) -> Point:
        return Point(x=self.x, y=self.y - 1)

    def below(self) -> Point:
        return Point(x=self.x, y=self.y + 1)

    def to_right(self) -> Point:
        return Point(x=self.x + 1, y=self.y)

    def to_left(self) -> Point:
        return Point(x=self.x - 1, y=self.y)


Path = list[Point]


class SandRunningOutError(Exception):
    pass


class SandSourceBlockedError(Exception):
    pass


class RockGrid:
    def __init__(self, sand_source: Point) -> None:
        self.sand_source = sand_source
        self.grid = collections.defaultdict(lambda: ".")
        self.lowest_point = 0
        self.grain_count = 0
        self.floor = sys.maxsize

    def fill_in_from_paths(self, paths: Iterable[Path]) -> None:
        for path in paths:
            self.fill_in_path(path=path)

    def fill_in_path(self, path: Path) -> None:
        for start, end in itertools.pairwise(path):
            self.fill_between_points(start=start, end=end)

    def fill_between_points(self, start: Point, end: Point) -> None:
        if start.x == end.x:
            min_y, max_y = min(start.y, end.y), max(start.y, end.y)
            for y in range(min_y, max_y + 1):
                self.grid[Point(start.x, y)] = "#"

            if max_y > self.lowest_point:
                self.lowest_point = max_y

        elif start.y == end.y:
            min_x, max_x = min(start.x, end.x), max(start.x, end.x)
            for x in range(min_x, max_x + 1):
                self.grid[Point(x, start.y)] = "#"

    def pour_sand(self) -> None:
        while True:
            try:
                self.drop_grain()
            except (SandRunningOutError, SandSourceBlockedError):
                break

    def point_is_free(self, point: Point) -> bool:
        return self.grid[point] == "." and point.y < self.floor

    def find_free_point(self, start: Point) -> Point:
        current = start
        while True:
            if (below := current.below()).y > self.lowest_point:
                raise SandRunningOutError

            if self.point_is_free(point=below):
                current = below
                continue

            below_left = current.below().to_left()
            if self.point_is_free(point=below_left):
                current = below_left
                continue

            below_right = current.below().to_right()
            if self.point_is_free(point=below_right):
                current = below_right
                continue

            return current

    def drop_grain(self) -> None:
        next_position = self.find_free_point(start=self.sand_source)
        self.grid[next_position] = "o"
        self.grain_count += 1
        if next_position == self.sand_source:
            raise SandSourceBlockedError

    def add_floor(self):
        self.floor = self.lowest_point + 2
        self.lowest_point = sys.maxsize


def parse_path(path_raw: str) -> Path:
    path = []
    for point in path_raw.split(" -> "):
        path.append(Point(*tuple(map(int, point.split(",")))))
    return path


def build_rock_formation(paths_raw: list[str], sand_source: Point) -> RockGrid:
    paths = (parse_path(path_raw=path_raw) for path_raw in paths_raw)
    grid = RockGrid(sand_source=sand_source)
    grid.fill_in_from_paths(paths=paths)
    return grid


def main() -> None:
    paths_raw = utils.read_input_to_string().splitlines()
    cave = build_rock_formation(paths_raw=paths_raw, sand_source=Point(500, 0))
    cave.pour_sand()
    grain_count1 = cave.grain_count

    cave.add_floor()
    cave.pour_sand()
    grain_count2 = cave.grain_count

    print(f"Part 1: {grain_count1}")
    print(f"Part 2: {grain_count2}")


if __name__ == "__main__":
    main()
