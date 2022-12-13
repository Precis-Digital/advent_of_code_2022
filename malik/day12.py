import sys
from typing import Optional
from dataclasses import dataclass
import heapq

@dataclass
class Cell:
    char: str
    elevation: int
    coordinates: tuple[int, int]
    distance: int = sys.maxsize

    def get_neighbors(self, height_map: "HeightMap") -> list["Cell"]:
        x, y = self.coordinates
        output = []
        for coord in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            cell = height_map.get_cell(coord)
            if cell and cell.elevation <= (self.elevation + 1):
                output.append(cell)
        return output

    def get_distance(self) -> int:
        return self.distance

    def set_distance(self, distance: int) -> None:
        self.distance = distance

    def __post_init__(self):
        self.sort_index = self.distance

@dataclass
class HeightMap:
    start_coords: tuple[int, int]
    end_coords: tuple[int, int]
    map: dict[tuple[int, int], Cell]

    def get_cell(self, coordinates: tuple[int, int]) -> Optional[Cell]:
        return self.map.get(coordinates)

def compute_distance(from_coords: tuple[int, int], to_coords: tuple[int, int]) -> int:
    x1, y1 = from_coords
    x2, y2 = to_coords
    return abs(x1 - x2) + abs(y1 - y2)

def build_height_map(fname: str) -> HeightMap:
    with open(fname) as f:
        lines = f.readlines()
    map = {}
    start = None
    end = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line.strip()):
            elevation = ord(char) - ord('a')
            if char == "S":
                start = (x, y)
                elevation = 0
            elif char == "E":
                end = (x, y)
                elevation = ord('z') - ord('a')
            map[(x, y)] = Cell(char, elevation, (x, y))
    return HeightMap(start_coords=start, end_coords=end, map=map)


def find_shortest_path(height_map: HeightMap) -> int:
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
    i = 0
    start_coords = height_map.start_coords
    end_coords = height_map.end_coords

    start_cell = height_map.get_cell(start_coords)
    start_cell.set_distance(0)
    unvisited = set(height_map.map.keys())
    visited = set()

    while unvisited:
        current_cell = min(unvisited, key=lambda x: height_map.get_cell(x).get_distance())
        if current_cell == end_coords:
            return height_map.get_cell(current_cell).get_distance()
        unvisited.remove(current_cell)
        visited.add(current_cell)
        neighbors = height_map.get_cell(current_cell).get_neighbors(height_map)
        for neighbor in neighbors:
            if neighbor.coordinates in visited:
                continue
            new_distance = height_map.get_cell(current_cell).get_distance() + 1
            if new_distance < neighbor.get_distance():
                neighbor.set_distance(new_distance)











if __name__ == "__main__":
    hm = build_height_map(fname="inputs/day-12-sample.txt")
    # print(hm.get_cell((2, 0)).get_neighbors(hm))
    print(find_shortest_path(hm))
    assert find_shortest_path(hm) == 31

    hm = build_height_map(fname="inputs/day-12-input.txt")

    assert find_shortest_path(hm) == 408