import sys
from typing import Optional
from dataclasses import dataclass
import heapq

@dataclass
class Cell:
    char: str
    elevation: int
    coordinates: tuple[int, int]

    def get_neighbors(self, height_map: "HeightMap") -> list["Cell"]:
        x, y = self.coordinates
        output = []
        for coord in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            cell = height_map.get_cell(coord)
            if cell and cell.elevation <= (self.elevation + 1):
                output.append(cell)
        return output

    def reverse_get_neighbors(self, height_map: "HeightMap") -> list["Cell"]:
        """Get neighbors that can reach the target cell"""
        x, y = self.coordinates
        output = []
        for coord in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            cell = height_map.get_cell(coord)
            if cell and self.elevation <= (cell.elevation + 1):
                output.append(cell)
        return output


@dataclass
class HeightMap:
    start_coords: tuple[int, int]
    end_coords: tuple[int, int]
    map: dict[tuple[int, int], Cell]

    def get_cell(self, coordinates: tuple[int, int]) -> Optional[Cell]:
        return self.map.get(coordinates)


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


def find_shortest_path(height_map: HeightMap, start_coords: Optional[tuple[int, int]] = None, end_coords_set: set[tuple[int, int]] = None, reverse_search=False) -> int:
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
    i = 0
    if start_coords is None:
        start_coords = height_map.start_coords
    if end_coords_set is None:
        end_coords_set = set([height_map.end_coords])

    distances = {cell.coordinates: sys.maxsize for cell in height_map.map.values()}
    distances[start_coords] = 0
    unvisited = set(height_map.map.keys())
    visited = set()

    while unvisited:
        current_coords = min(unvisited, key=lambda x: distances[x])
        # print(current_coords)
        if current_coords in end_coords_set:
            return distances[current_coords]

        if reverse_search:
            neighbors = height_map.map[current_coords].reverse_get_neighbors(height_map)
        else:
            neighbors = height_map.map[current_coords].get_neighbors(height_map)

        for neighbor in neighbors:
            # print(neighbor)
            if neighbor.coordinates in visited:
                continue
            new_distance = distances[current_coords] + 1
            if new_distance < distances[neighbor.coordinates]:
                distances[neighbor.coordinates] = new_distance

        unvisited.remove(current_coords)
        visited.add(current_coords)



def solution1(height_map: HeightMap) -> int:
    return find_shortest_path(height_map)

def solution2(height_map: HeightMap) -> int:
    coordinates_with_zero_elevation = set([cell.coordinates for cell in height_map.map.values() if cell.elevation == 0])

    result = find_shortest_path(height_map=height_map, start_coords=height_map.end_coords, end_coords_set=coordinates_with_zero_elevation, reverse_search=True)
    return result
    # return min(find_shortest_path(height_map, cell.coordinates) for cell in coordinates_with_zero_elevation)
    # return find_shortest_path(height_map, start_coords=(0, 0))




if __name__ == "__main__":
    import time
    s = time.time()
    hm = build_height_map(fname="inputs/day-12-sample.txt")
    assert solution1(hm) == 31

    hm = build_height_map(fname="inputs/day-12-sample.txt")
    assert solution2(hm) == 29


    hm = build_height_map(fname="inputs/day-12-input.txt")
    assert solution1(hm) == 408
    # print(solution2(hm))
    hm = build_height_map(fname="inputs/day-12-input.txt")
    assert solution2(hm) == 399




    print('elapsed tiem', time.time() - s)