
# Day 15, Year 2022
# Link: https://adventofcode.com/2022/day/15
import functools
import time


def get_input_values(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return [Sensor(line.strip()) for line in f.readlines()]

import dataclasses
import itertools

import matplotlib.pyplot as plt
from skspatial.objects import Line


class ParallellLinesError(Exception):
    pass

@dataclasses.dataclass(frozen=True)
class Line:
    """Line on standard form ax + by + c = 0"""

    a: int
    b: int
    c: int

    def intersection(self, other: Line, /) -> tuple[int, int]:
        if (denominator := self.a * other.b - other.a * self.b) == 0:
            raise ParallellLinesError

        x = (self.b * other.c - other.b * self.c) / denominator
        y = (self.c * other.a - other.c * self.a) / denominator

        return x, y

class Sensor:
    input_string: str
    position: tuple[int, int]
    closest_beacon_position: tuple[int, int]

    def __init__(self, input_string: str) -> "Sensor":
        self.input_string = input_string
        # Stupid parser - regex sucks
        splits = input_string.split(":")
        
        sensor_pos_string = splits[0].replace("Sensor at ", "").split(",")
        self.position = (int(sensor_pos_string[0].replace("x=", "")),int(sensor_pos_string[1].replace("y=", "")))
        
        closest_beacon_pos_string = splits[1].replace(" closest beacon is at ", "").split(",")
        self.closest_beacon_position = (int(closest_beacon_pos_string[0].replace("x=", "")), int(closest_beacon_pos_string[1].replace("y=", "")))

    def __repr__(self) -> str:
        return self.input_string

    @functools.cached_property
    def distance_to_beacon(self) -> str:
        return manhattan_distance(self.position[0], self.position[1], self.closest_beacon_position[0], self.closest_beacon_position[1])

    @functools.cached_property
    def barely_unreachable_lines(self) -> tuple[Line, ...]:
        outside_beacon_range = self.distance_to_beacon + 1
        l1 = Line(a=1, b=-1, c=self.position[1] - self.position[0] + outside_beacon_range)
        l2 = Line(a=1, b=-1, c=self.position[1] - self.position[0] - outside_beacon_range)
        l3 = Line(a=-1, b=-1, c=self.position[1] + self.position[0] + outside_beacon_range)
        l4 = Line(a=-1, b=-1, c=self.position[1] + self.position[0] - outside_beacon_range)
        return l1, l2, l3, l4
    

def within_boundary(point: tuple[int, int], upper_bound: int) -> bool:
    return all(0 < coord < upper_bound for coord in point)

def undetectable(point: tuple[int, int], sensors: list[Sensor]) -> bool:
    return all(out_of_sensor_reach(sensor=sensor, point=point) for sensor in sensors)

def only_possible_location(point: tuple[int, int], sensors: list[Sensor], upper_bound: int) -> bool:
    if not within_boundary(point=point, upper_bound=upper_bound):
        return False
    if not undetectable(point=point, sensors=sensors):
        return False
    return True

def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

def out_of_sensor_reach(sensor: Sensor, point: tuple[int, int]) -> bool:
    dist = manhattan_distance(x1=sensor.position[0], y1=sensor.position[1], x2=point[0], y2=point[1])
    return dist > sensor.distance_to_beacon

def get_point_with_no_overlap(sensors: list[Sensor], upper_bound: int) -> tuple[int,int]:
    _, ax = plt.subplots()
    for sens_1, sens_2 in itertools.product(sensors, repeat=2):
        lines1 = sens_1.barely_unreachable_lines
        lines2 = sens_2.barely_unreachable_lines
        for line1, line2 in itertools.product(lines1, lines2):
            if line1 == line2:
                continue
            
            try:
                intersection = line1.intersection(line2)
            except ParallellLinesError as e:
                continue

            intersection_x = int(intersection[0])
            intersection_y = int(intersection[1])

            if only_possible_location(point=(intersection_x, intersection_y), sensors=sensors, upper_bound=upper_bound):
                return (intersection_x, intersection_y)

    #ax.grid()

    #plt.show()

def part_2_sample():
    start_time = time.time()
    point = get_point_with_no_overlap(get_input_values('Dec15/sample_input.txt'), 20)
    ans = point[0]*4000000 + point[1]
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_2_answer():
    start_time = time.time()
    point = get_point_with_no_overlap(get_input_values('Dec15/input.txt'), 4000000)
    ans = point[0]*4000000 + point[1]
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

if __name__ == "__main__":
    print(part_2_sample())
    print(part_2_answer())