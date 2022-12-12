
# Day 12, Year 2022
# Link: https://adventofcode.com/2022/day/12
def get_input_values(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return [line.strip() for line in f.readlines()]

CHARS = list(map(chr, range(97, 123)))

class Coordinate:
    x: int
    y: int
    height: int
    visited: bool = False
    is_target: bool = False
    is_starting_point: bool = False

    def __init__(self, x: int, y: int, height: str) -> "Coordinate":
        self.x = x
        self.y = y
        if height == "E":
            self.is_target = True
            self.height = CHARS.index("z")
        elif height == "S":
            self.is_starting_point = True
            self.height = CHARS.index("a")
        else:
            self.height = CHARS.index(height)
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) - {self.height}"

def grid_to_coordinates(grid: list[str]) -> str:
    coords: dict[tuple[int, int], Coordinate] = {}
    starting_point: Coordinate = None
    for i, row in enumerate(grid[::-1]):
        for j, cell in enumerate(row):
            coord = Coordinate(x=j,y=i,height=cell)
            coords[j,i] = coord
            if coord.is_starting_point:
                starting_point = coord
    return coords, starting_point

def get_available_options(coordinates: dict[tuple[int, int], Coordinate], current_position: Coordinate) -> list[tuple[int, int]]:
    available_options: list[tuple[int, int]] = []

    def is_height_within_reach(current_height, target_height) -> bool:
        return -1 <= (current_height - target_height) <= 1

    potential_options = [
        (current_position.x, current_position.y - 1), #UP
        (current_position.x - 1, current_position.y), #LEFT
        (current_position.x + 1, current_position.y), #RIGHT
        (current_position.x, current_position.y + 1), #DOWN
    ]
   
    for option_coords in potential_options:
        if option_coords in coordinates:
            coord = coordinates[option_coords]
            if is_height_within_reach(current_position.height, coord.height) and not coord.visited:
                available_options.append(coordinates[option_coords])
    
    return available_options

from random import randint


def pick_best_option(available_options: list[Coordinate]) -> Coordinate:
    highest_height = max([opt.height for opt in available_options])
    options_with_highest_height = list(filter(lambda x: x.height == highest_height, available_options))

    return options_with_highest_height[randint(0, len(options_with_highest_height)-1)]

import os
import time


def add_leading_zero(num: str) -> str:
    """Returns a non-leading zero number as a leading zero number"""
    if int(num) < 10:
        return "0" + str(int(num))
    return str(num)

def print_mountain(coordinates, climbing_path) -> None:
    columns = []
    visited_columns = []
    for y in range(5):
        row = []
        visited_row = []
        for x in range(8):
            row.append(add_leading_zero(coordinates[x, y].height))
            if coordinates[x, y].visited:
                visited_row.append("x")
            else:
                visited_row.append(".")
        columns.append(row)
        visited_columns.append(visited_row)
    
    for coord in climbing_path:
        visited_columns[coord[1]][coord[0]] = "X"
    
    os.system("clear")
    for row in columns: print("|".join(row))
    print("-" * 20)
    for row in visited_columns: print("|".join(row))
    time.sleep(0.02)
            

climbing_path: list[tuple[int, int]] = []
def climb_mountain(coordinates: dict[tuple[int, int], Coordinate], climbing_path: list[Coordinate], print_solution: bool) -> int:
    if print_solution: print_mountain(coordinates, climbing_path)
    current_position = coordinates[climbing_path[-1]]
    if current_position.is_target:
        # Found the top
        return coordinates, climbing_path
    
    potential_options = get_available_options(coordinates, current_position)
    
    if len(potential_options) == 0:
        climbing_path.pop()
    else:
        new_position = pick_best_option(potential_options)
        climbing_path.append((new_position.x, new_position.y))
        new_position.visited = True
    
    if len(climbing_path) == 1:
        # Went all the way back so retrying
        for k in coordinates:
            coordinates[k].visited = False

    return climb_mountain(coordinates, climbing_path, print_solution)    

import copy
import sys
import threading


def climb_mountain_n_times(coordinates, starting_point: int, n: int, print_output: bool) -> int:
    best_path = None
    for _ in range(n):
        climbing_path = [(starting_point.x, starting_point.y)]
        _, climbing_path = climb_mountain(copy.deepcopy(coordinates), climbing_path, print_output)
        if best_path == None:
            best_path = climbing_path
        elif len(climbing_path) < len(best_path):
            best_path = climbing_path
    return best_path

def part_1_sample():
    coordinates, starting_point = grid_to_coordinates(get_input_values('Dec12/sample_input.txt'))
    best_path = climb_mountain_n_times(coordinates, starting_point, 10, True)
    print("The optimal path is length: ",len(best_path) - 1)
    return len(best_path) - 1

def part_1_answer():
    coordinates, starting_point = grid_to_coordinates(get_input_values('Dec12/input.txt'))
    best_path = climb_mountain_n_times(coordinates, starting_point, 1, False)
    print(len(best_path) - 1)
    return len(best_path) - 1

def part_2_sample():
    ...

def part_2_answer():
    ...

if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    threading.stack_size(2**27)
    
    part_1_sample()
    #part_1_answer()
    #part_2_sample()
    #part_2_answer()
        