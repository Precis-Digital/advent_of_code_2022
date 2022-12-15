from __future__ import annotations

import dataclasses
import functools
import itertools
import re
from typing import Iterable

from shared import utils

Y = 2_000_000
LOWER_BOUND = 0
UPPER_BOUND = 4_000_000
PATTERN = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)

Number = int | float
Point = tuple[Number, Number]


class ParallellLinesError(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class Line:
    """Line on standard form ax + by + c = 0"""

    a: Number
    b: Number
    c: Number

    def intersection(self, other: Line, /) -> Point:
        if (denominator := self.a * other.b - other.a * self.b) == 0:
            raise ParallellLinesError

        x = (self.b * other.c - other.b * self.c) / denominator
        y = (self.c * other.a - other.c * self.a) / denominator

        return x, y


@dataclasses.dataclass(frozen=True)
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int

    @functools.cached_property
    def beacon_distance(self):
        return manhattan_distance(
            x1=self.x, x2=self.beacon_x, y1=self.y, y2=self.beacon_y
        )

    @functools.cached_property
    def barely_unreachable_lines(self) -> tuple[Line, ...]:
        outside_beacon_range = self.beacon_distance + 1
        l1 = Line(a=1, b=-1, c=self.y - self.x + outside_beacon_range)
        l2 = Line(a=1, b=-1, c=self.y - self.x - outside_beacon_range)
        l3 = Line(a=-1, b=-1, c=self.y + self.x + outside_beacon_range)
        l4 = Line(a=-1, b=-1, c=self.y + self.x - outside_beacon_range)
        return l1, l2, l3, l4


def parse_sensors_and_beacons(
    sensors_raw: list[str],
) -> tuple[set[Sensor], set[Point]]:
    sensors, beacons = set(), set()
    for sensor_raw in sensors_raw:
        sensor = parse_sensor(sensor_raw=sensor_raw)
        sensors.add(sensor)
        beacons.add((sensor.beacon_x, sensor.beacon_y))

    return sensors, beacons


def parse_sensor(sensor_raw: str) -> Sensor:
    matches = tuple(map(int, PATTERN.match(sensor_raw).groups()))
    return Sensor(*matches)


def manhattan_distance(x1: Number, y1: Number, x2: Number, y2: Number) -> Number:
    return abs(x1 - x2) + abs(y1 - y2)


def out_of_sensor_reach(sensor: Sensor, point: Point) -> bool:
    dist = manhattan_distance(x1=sensor.x, y1=sensor.y, x2=point[0], y2=point[1])
    return dist > sensor.beacon_distance


def integer_point(point: Point) -> bool:
    return point[0].is_integer() and point[1].is_integer()


def within_boundary(point: Point) -> bool:
    return all(LOWER_BOUND < coord < UPPER_BOUND for coord in point)


def undetectable(point: Point, sensors: Iterable[Sensor]) -> bool:
    return all(out_of_sensor_reach(sensor=sensor, point=point) for sensor in sensors)


def only_possible_location(point: Point, sensors: Iterable[Sensor]) -> bool:
    if not integer_point(point=point):
        return False
    if not within_boundary(point=point):
        return False
    if not undetectable(point=point, sensors=sensors):
        return False
    return True


def find_only_possible_location(sensors: Iterable[Sensor]) -> Point:
    for sensor1, sensor2 in itertools.product(sensors, repeat=2):
        if sensor1 is sensor2:
            continue

        lines1 = sensor1.barely_unreachable_lines
        lines2 = sensor2.barely_unreachable_lines

        for line1, line2 in itertools.product(lines1, lines2):
            if line1 is line2:
                continue

            try:
                interection = line1.intersection(line2)
            except ParallellLinesError:
                continue

            if only_possible_location(point=interection, sensors=sensors):
                return interection


def calculate_tuning_frequency(point: Point) -> int:
    return int(UPPER_BOUND * point[0] + point[1])


def sensor_reach_x(sensor: Sensor) -> tuple[int, int]:
    return sensor.x - sensor.beacon_distance, sensor.x + sensor.beacon_distance + 1


def in_sensor_reach(sensor: Sensor, point: Point) -> bool:
    return not out_of_sensor_reach(sensor=sensor, point=point)


def count_impossible_beacon_positions(sensors: set[Sensor], beacons: set[Point]) -> int:
    no_beacon_possible = set()
    for sensor in sensors:
        for x in range(*sensor_reach_x(sensor=sensor)):
            if in_sensor_reach(sensor=sensor, point=(x, Y)) and (x, Y) not in beacons:
                no_beacon_possible.add((x, Y))

    return len(no_beacon_possible)


def main() -> None:
    sensors_raw = utils.read_input_to_string().splitlines()
    sensors, beacons = parse_sensors_and_beacons(sensors_raw=sensors_raw)

    non_beacon_locations = count_impossible_beacon_positions(
        sensors=sensors, beacons=beacons
    )

    tuning_frequency = calculate_tuning_frequency(
        point=find_only_possible_location(sensors=sensors)
    )

    print(f"Part 1: {non_beacon_locations}")
    print(f"Part 2: {tuning_frequency}")


if __name__ == "__main__":
    main()
