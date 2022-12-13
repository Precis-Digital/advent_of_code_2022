import collections
import sys

from shared import utils

Coordinate = tuple[int, int]
GridMap = dict[tuple, int]
Graph = dict[Coordinate, list[Coordinate]]


def parse_heightmap(heightmap_raw: str) -> tuple[GridMap, Coordinate, Coordinate]:
    heightmap = {}
    start = end = (None, None)
    for y, line in enumerate(heightmap_raw.splitlines()):
        for x, value in enumerate(line):
            if value == "S":
                start = (x, y)
                value = "a"

            if value == "E":
                end = (x, y)
                value = "z"

            heightmap[(x, y)] = ord(value)

    return heightmap, start, end


def get_reachable_neighbors(heightmap: GridMap, coord: Coordinate) -> list[Coordinate]:
    potential_neighbors = [
        (coord[0] + 1, coord[1]),
        (coord[0] - 1, coord[1]),
        (coord[0], coord[1] + 1),
        (coord[0], coord[1] - 1),
    ]
    reachable_neighbors = []
    for neighbor in potential_neighbors:
        if not heightmap.get(neighbor):
            continue

        if heightmap[coord] + 1 >= heightmap[neighbor]:
            reachable_neighbors.append(neighbor)

    return reachable_neighbors


def heightmap_to_graph(heightmap: GridMap):
    return {
        coord: get_reachable_neighbors(heightmap=heightmap, coord=coord)
        for coord in heightmap.copy()
    }


def shortest_path_length(
    graph: {Coordinate, list[Coordinate]},
    start: Coordinate,
    end: Coordinate,
) -> int:
    queue = collections.deque([start])
    visited = set()
    distances = {start: 0}
    while queue:
        node = queue.popleft()

        if node in visited:
            continue

        visited.add(node)

        if node == end:
            return distances[node]

        neighbors = graph[node]
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            queue.append(neighbor)
            distances[neighbor] = distances[node] + 1

    return sys.maxsize


def shortest_hiking_trail_length(
    graph: Graph,
    starting_points: list[Coordinate],
    end: Coordinate,
) -> int:
    return min(
        shortest_path_length(graph=graph, start=start, end=end)
        for start in starting_points
    )


def find_hiking_starts(heightmap: GridMap) -> list[Coordinate]:
    return [coord for coord, height in heightmap.items() if height == ord("a")]


def main() -> None:
    heightmap_raw = utils.read_input_to_string()
    heightmap, start, end = parse_heightmap(heightmap_raw=heightmap_raw)
    graph = heightmap_to_graph(heightmap=heightmap)
    steps1 = shortest_path_length(graph=graph, start=start, end=end)

    hiking_starts = find_hiking_starts(heightmap=heightmap)
    steps2 = shortest_hiking_trail_length(
        graph=graph, starting_points=hiking_starts, end=end
    )

    print(f"Part 1: {steps1}")
    print(f"Part 1: {steps2}")


if __name__ == "__main__":
    main()
