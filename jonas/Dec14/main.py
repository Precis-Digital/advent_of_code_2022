
# Day 14, Year 2022
# Link: https://adventofcode.com/2022/day/14
import time


class RockPath:
    coords: list[tuple[int,int]]
    coord_string: str

    def __init__(self, coord_string: str) -> "RockPath":
        self.coords = []
        self.coord_string = coord_string
        for coord in coord_string.split(" -> "):
            self.coords.append(tuple([int(c) for c in coord.split(",")]))

    def __repr__(self) -> str:
        return self.coord_string
    
    @property
    def path_coordinates(self) -> list[tuple[int,int]]:
        all_coords = []
        for i, coord in enumerate(self.coords):
            all_coords.append(coord)
            if i + 1 >= len(self.coords):
                break
            all_coords.extend(self._get_points_between_coords(coord, self.coords[i+1]))
        
        return all_coords
    
    @staticmethod
    def _get_points_between_coords(coord_a: tuple[int, int], coord_b: tuple[int, int]) -> list[tuple[int,int]]:
        all_points = []
        if coord_a[0] == coord_b[0]:
            # Must be Y movement
            for i in range(1, abs(coord_b[1] - coord_a[1])):
                all_points.append((coord_a[0], coord_b[1] - i if coord_b[1] > coord_a[1] else coord_a[1] - i))
        else:
            for i in range(1, abs(coord_b[0] - coord_a[0])):
                all_points.append((coord_b[0] - i if coord_b[0] > coord_a[0] else coord_a[0] - i, coord_a[1]))
        return all_points


def get_input_values(file_name: str) -> tuple[list[RockPath], int, int, int, int]:
    rock_paths = []
    min_x = 500
    max_x = 500
    min_y = 0
    max_y = 0
    with open(file_name, 'r') as f:
        for line in f.readlines():
            rock_path = RockPath(line.strip())
            for coord in rock_path.coords:
                if coord[0] > max_x:
                    max_x = coord[0]
                elif coord[0] < min_x:
                    min_x = coord[0]
                if coord[1] > max_y:
                    max_y = coord[1]
                elif coord[1] < min_y:
                    min_y = coord[1]
            rock_paths.append(rock_path)

    return rock_paths, min_x, max_x, min_y, max_y

import os


def print_coord_system(coord_system: list[list[str]]):
    os.system("clear")
    for row in coord_system: print("|".join(row))
    time.sleep(0.02)

def determine_next_sand_position(coord_system: list[list[str]], current_sand_position: tuple[int, int]) -> tuple[int, int]:
        if current_sand_position[1] + 1 >= len(coord_system):
            return None
        if coord_system[current_sand_position[1] + 1][current_sand_position[0]] not in ["🪨", "o"]:
            if current_sand_position[1] + 1 >= len(coord_system):
                return None
            return (current_sand_position[0], current_sand_position[1] + 1)
        
        if coord_system[current_sand_position[1] + 1][current_sand_position[0] - 1] not in ["🪨", "o"]:
            if current_sand_position[0] - 1 < 0:
                return None
            return (current_sand_position[0] - 1, current_sand_position[1] + 1)

        if coord_system[current_sand_position[1] + 1][current_sand_position[0] + 1] not in ["🪨", "o"]:
            if current_sand_position[0] + 1 >= len(coord_system[0]):
                return None
            return (current_sand_position[0] + 1, current_sand_position[1] + 1)
        
        return current_sand_position

def drop_sand_grain(coord_system: list[list[str]], min_x: int) -> tuple[list[list[str]], bool]:
    current_sand_position = (500 - min_x, 0)
    coord_system[0][500-min_x] = "+"
    while True:
        next_sand_position = determine_next_sand_position(coord_system, current_sand_position)
        if next_sand_position == (500 - min_x, 0):
            coord_system[next_sand_position[1]][next_sand_position[0]] = "o" 
            return coord_system, False
        if next_sand_position == None:
            coord_system[current_sand_position[1]][current_sand_position[0]] = "."
            return coord_system, False
        if next_sand_position == current_sand_position:
            break
        if current_sand_position != (500 - min_x, 0):
            coord_system[current_sand_position[1]][current_sand_position[0]] = "."
        coord_system[next_sand_position[1]][next_sand_position[0]] = "o" 
        current_sand_position = next_sand_position
        #print_coord_system(coord_system)
        
    coord_system[current_sand_position[1]][current_sand_position[0]] = "o"
    return coord_system, True
    

def draw_rock_map(rock_paths: list[RockPath], min_x: int, max_x: int, min_y: int, max_y: int, part: int = 1) -> int:
    coord_system = [["." for x in range(max_x - min_x + 1)] for y in range(max_y-min_y + 1)]
    if part == 2:
        coord_system[-1] = ["🪨" for _ in coord_system[-1]]
    for rock_path in rock_paths:
        for coord in rock_path.path_coordinates:
            coord_system[coord[1] - min_y][coord[0] - min_x] = "🪨"
            #print_coord_system(coord_system)

    sand_counter = 0
    while True:
        coord_system, continue_dropping = drop_sand_grain(coord_system, min_x)
        #print_coord_system(coord_system)
        if not continue_dropping:
            break
        
        sand_counter += 1

    return sand_counter

def part_1_sample():
    start_time = time.time()
    ans = draw_rock_map(*get_input_values('Dec14/sample_input.txt'))
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_1_answer():
    start_time = time.time()
    ans = draw_rock_map(*get_input_values('Dec14/input.txt'))
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_2_sample():
    start_time = time.time()
    rock_paths, min_x, max_x, min_y, max_y = get_input_values('Dec14/sample_input.txt')
    ans = draw_rock_map(rock_paths, min_x - 20, max_x + 20, min_y, max_y +2, part=2) + 1
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_2_answer():
    start_time = time.time()
    rock_paths, min_x, max_x, min_y, max_y = get_input_values('Dec14/input.txt')
    ans = draw_rock_map(rock_paths, min_x - 50000, max_x + 50000, min_y, max_y +2, part=2) + 1
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

if __name__ == "__main__":
    print(part_1_sample())
    print(part_1_answer())
    print(part_2_sample())
    print(part_2_answer())