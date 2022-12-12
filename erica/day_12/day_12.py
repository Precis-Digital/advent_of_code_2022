from collections import deque


def get_height_map():
    """Return a height map of the terrain. From input file"""
    with open('erica/day_12/input_data.txt') as f:
        rows = [list(line.strip()) for line in f.readlines()]
        heatmap = {}
        start, end = (0, 0), (0, 0)
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                if col == "S":
                    start = (i, j)
                    col = "a"
                if col == "E":
                    end = (i, j)
                    col = "z"
                heatmap[(i, j)] = ord(col) - 97
        return heatmap, start, end


def get_neighbors(point, height_map__):
    """return valid neighbors of point"""
    x, y = point
    neighbors = []
    for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if (i, j) in height_map__ and height_map__[(i, j)] <= height_map__[point] + 1:
            neighbors.append((i, j))
    return neighbors


def get_shortest_path(start, end, height_map_):
    """Return the shortest path from start to end, using height_map and allow for revisiting steps.
     Breadth First Search Algorithm https://www.techwithtim.net/tutorials/breadth-first-search/"""

    queue = deque([(start, 0)])
    visited = set()
    while queue:
        point, steps = queue.popleft()
        if point == end:
            return steps
        if point in visited:
            continue
        visited.add(point)
        for neighbor in get_neighbors(point, height_map_):
            queue.append((neighbor, steps + 1))
    return queue


def get_all_possible_starting_points(terrain):
    """Return all possible starting points"""
    start_points = []
    for pos in terrain:
        if terrain[pos] == 0:
            start_points.append(pos)
    return start_points


if __name__ == '__main__':
    height_map, start_pos, end_pos = get_height_map()
    nr_steps = get_shortest_path(start_pos, end_pos, height_map)
    print(f"part 1: {nr_steps}")  # part 1: 391

    potential_starting_points = get_all_possible_starting_points(terrain=height_map)
    nr_steps = []
    for point in potential_starting_points:
        nr_s = get_shortest_path(point, end_pos, height_map)
        if nr_s:
            nr_steps.append(nr_s)
    print(f"part 2: {min(nr_steps)}")  # part 2: 386
