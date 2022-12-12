
# Day 12, Year 2022
# Link: https://adventofcode.com/2022/day/12
def get_input_values(file_name: str) -> str:
    starting_point = None
    finishing_point = None
    with open(file_name, 'r') as f:
        graph = [list(line.strip()) for line in f.readlines()]
        for y, row in enumerate(graph):
            for x, height in enumerate(row):
                if height == "S":
                    starting_point = (x, y)
                    graph[y][x] = "a"
                elif height == "E":
                    finishing_point = (x, y)
                    graph[y][x] = "z"
    
    return graph, starting_point, finishing_point

def grid_neighbors(graph, x, y):
    potential_options = [
        (x, y - 1), #UP
        (x - 1, y), #LEFT
        (x + 1, y), #RIGHT
        (x, y + 1), #DOWN
    ]
    return [c for c in potential_options if 0 <= c[0] < len(graph[0]) and 0 <= c[1] < len(graph)]

def find_neighbors(x, y, graph):
    return [node for node in grid_neighbors(graph, x, y) if ord(graph[node[1]][node[0]]) - ord(graph[y][x])  <= 1]

import collections


def walk_mountain(graph, starting_point, finishing_point):
    active = collections.deque([(0, starting_point)])
    seen = set()
    while active:
        steps, current = active.popleft()
        if current == finishing_point:
            return steps
        if current in seen:
            continue
        seen.add(current)
        for neighbor in find_neighbors(current[0], current[1], graph):
            active.append((steps + 1, neighbor))
    return float("inf")

def get_all_positions_with_elevation_a(graph):
    all_positions = []
    for y, row in enumerate(graph):
        for x, height in enumerate(row):
            if height == "a":
                all_positions.append((x, y))
    return all_positions

def part_1_sample():
    return walk_mountain(*get_input_values('Dec12/sample_input.txt'))

def part_1_answer():
    return walk_mountain(*get_input_values('Dec12/input.txt'))

def part_2_sample():
    graph, _, finishing_point = get_input_values('Dec12/sample_input.txt')

    shortest_path = 1e9
    for potential_starting_points in get_all_positions_with_elevation_a(graph):
        path_length = walk_mountain(graph, potential_starting_points, finishing_point)
        if path_length < shortest_path:
            shortest_path = path_length
    
    return shortest_path

def part_2_answer():
    graph, _, finishing_point = get_input_values('Dec12/input.txt')

    shortest_path = 1e9
    for potential_starting_points in get_all_positions_with_elevation_a(graph):
        path_length = walk_mountain(graph, potential_starting_points, finishing_point)
        if path_length < shortest_path:
            shortest_path = path_length
    
    return shortest_path

if __name__ == "__main__":
    part_1_sample()
    part_1_answer()
    part_2_sample()
    part_2_answer()