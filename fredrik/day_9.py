from __future__ import annotations

import enum
import math
from typing import Generator

from shared import utils

NR_OF_TAILS = 9


class Direction(str, enum.Enum):
    RIGHT = "R"
    LEFT = "L"
    UP = "U"
    DOWN = "D"


class Knot:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = {(self.x, self.y)}

    def __repr__(self) -> str:
        return f"{type(self).__name__}(x={self.x}, y={self.y})"

    def move(self, direction: Direction) -> None:
        if direction == Direction.RIGHT:
            self.x += 1
        elif direction == Direction.LEFT:
            self.x -= 1
        elif direction == Direction.UP:
            self.y += 1
        elif direction == Direction.DOWN:
            self.y -= 1

    def distance(self, other: Knot, /) -> float:
        return math.dist((self.x, self.y), (other.x, other.y))

    def add_current_position_to_visited(self) -> None:
        self.visited.add((self.x, self.y))

    def follow(self, head: Knot, /) -> None:
        def _close_gap(diagonal: bool) -> None:
            if self.x > head.x:
                self.move(direction=Direction.LEFT)
                if not diagonal:
                    return

            if self.x < head.x:
                self.move(direction=Direction.RIGHT)
                if not diagonal:
                    return

            if self.y > head.y:
                self.move(direction=Direction.DOWN)
                if not diagonal:
                    return

            if self.y < head.y:
                self.move(direction=Direction.UP)

        if self.distance(head) <= math.sqrt(2):
            return

        if self.x != head.x and self.y != head.y:
            _close_gap(diagonal=True)
        else:
            _close_gap(diagonal=False)

        self.add_current_position_to_visited()


def head_path(moves: list[str]) -> Generator[Knot, None, None]:
    head = Knot(x=0, y=0)
    for move in moves:
        direction, steps = move.split()
        for _ in range(int(steps)):
            head.move(direction=direction)
            yield head


def main() -> None:
    moves = utils.read_input_to_string().splitlines()
    tails = [Knot(x=0, y=0) for _ in range(NR_OF_TAILS)]

    for head in head_path(moves=moves):
        tails[0].follow(head)
        for i in range(1, NR_OF_TAILS):
            tails[i].follow(tails[i - 1])

    print(f"Part 1: {len(tails[0].visited)}")
    print(f"Part 2: {len(tails[-1].visited)}")


if __name__ == "__main__":
    main()
