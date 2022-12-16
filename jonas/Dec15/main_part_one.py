
# Day 15, Year 2022
# Link: https://adventofcode.com/2022/day/15
import time


def get_input_values(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return [Sensor(line.strip()) for line in f.readlines()]

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
    
    @property
    def scanned_coords(self) -> list[tuple[int, int]]:
        scanned_coords = []
        num_to_walk = abs(self.position[0] - self.closest_beacon_position[0]) + abs(self.position[1] - self.closest_beacon_position[1])

        for i in range(num_to_walk + 1):
            for j in range(num_to_walk + 1):
                os.system("clear")
                scanned_coords.append((min(self.position[0] - j + i, self.position[0]), self.position[1] + i)) # bottom-left
                scanned_coords.append((max(self.position[0] + j - i, self.position[0]), self.position[1] + i)) # bottom-right
                scanned_coords.append((min(self.position[0] - j + i, self.position[0]), self.position[1] - i)) # top-left
                scanned_coords.append((max(self.position[0] + j - i, self.position[0]), self.position[1] - i)) # top-right

        return scanned_coords

    def scanned_boundary(self, y_target: int) -> tuple[int, int]:
        num_to_walk = abs(self.position[0] - self.closest_beacon_position[0]) + abs(self.position[1] - self.closest_beacon_position[1])
        
        if (self.position[1] - num_to_walk) > y_target:
            return None
        if y_target > (self.position[1] + num_to_walk):
            return None

        steps_left = (num_to_walk - abs(self.position[1] - y_target))
        return self.position[0] - steps_left, self.position[0] + steps_left

import os


def draw_map(map_dict: dict):
    min_x = map_dict["min_x"]
    min_y = map_dict["min_y"]
    max_x = map_dict["max_x"]
    max_y = map_dict["max_y"]
    map_list = [[f"{i:05d}"] + ["." for _ in range(min_x - 2, max_x - 1)] for i in range(min_y, max_y+ 1)]
    
    for coord, val in map_dict["coords"].items():
        if coord[1] < min_y or coord[1] > max_y or coord[0] < min_x or coord[0] > max_x:
            continue
        map_list[coord[1] - min_y][coord[0] - min_x + 1] = val
    map_list.insert(0, ["-----"] + [str(num) for num in range(min_x, max_x + 1)])
    os.system("clear")
    for row in map_list: print("|".join(row))
    time.sleep(0.005)

def generate_coords_at_target_y(sensors: list[Sensor], target_y: int) -> dict:
    coords_at_target = {}
    for sensor in sensors:
        if sensor.position[1] == target_y:
            coords_at_target[(sensor.position[0], target_y)] = "S"
        
        if sensor.closest_beacon_position[1] == target_y:
            coords_at_target[(sensor.closest_beacon_position[0], target_y)] = "B"
        
        scanned_boundary_at_target = sensor.scanned_boundary(target_y)
       
        if scanned_boundary_at_target is None:
            continue
        
        for i in range(scanned_boundary_at_target[1] - scanned_boundary_at_target[0]):
            if (i + scanned_boundary_at_target[0], target_y) not in coords_at_target:
                coords_at_target[(i + scanned_boundary_at_target[0], target_y)] = "#"
    return coords_at_target


def generate_map_brute_force(sensors: list[Sensor], print_map: bool) -> dict:

    map_dict = {
        "max_x": 0,
        "min_x": int(1e9),
        "max_y": 0,
        "min_y": int(1e9),
        "coords": {}
    }

    for sensor in sensors:
        map_dict["coords"][sensor.position] = "S"
        map_dict["coords"][sensor.closest_beacon_position] = "B"
        map_dict["max_x"] = max(map_dict["max_x"], sensor.closest_beacon_position[0], sensor.position[0])
        map_dict["min_x"] = min(map_dict["min_x"], sensor.closest_beacon_position[0], sensor.position[0])
        map_dict["max_y"] = max(map_dict["max_y"], sensor.closest_beacon_position[1], sensor.position[1])
        map_dict["min_y"] = min(map_dict["min_y"], sensor.closest_beacon_position[1], sensor.position[1])
        if print_map: draw_map(map_dict)
        for coord in sensor.scanned_coords:
            map_dict["max_x"] = max(coord[0],map_dict["max_x"])
            map_dict["min_x"] = min(coord[0],map_dict["min_x"])
            map_dict["max_y"] = max(coord[1],map_dict["max_y"])
            map_dict["min_y"] = min(coord[1],map_dict["min_y"])
            if coord not in map_dict["coords"]:
                if print_map: draw_map(map_dict)
                map_dict["coords"][coord] = "#"
    
    return map_dict
    
    

def part_1_sample():
    start_time = time.time()
    map_dict = generate_map_brute_force(get_input_values('Dec15/sample_input.txt'), True)
    ans = len([v for k, v in map_dict["coords"].items() if k[1] == 10 and v == "#"])
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_1_answer():
    start_time = time.time()
    ans = len(generate_coords_at_target_y(get_input_values("Dec15/input.txt"), 2000000))
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

if __name__ == "__main__":
    print(part_1_sample())
    #print(part_1_answer())