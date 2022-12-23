import re


REGEX_PATTERN = (
    r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)"
)
SHORTEST_PATHS = {}
VALVES = {}
MAX_MINUTES_ALONE = 30
MAX_MINUTES_WITH_ELEPHANT = 26


def get_valve_data():
    with open("erica/day_16/input_data.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    for line in lines:
        g = re.match(REGEX_PATTERN, line).groups()
        VALVES[g[0]] = {
            "name": g[0],
            "rate": int(g[1]),
            "destinations": g[2].split(", "),
        }


def path_key(dest_1, dest_2) -> tuple:
    return tuple(sorted([dest_1, dest_2]))


def map_shortest_path_between_tunnels():
    # Get all possible paths between valves and the time to travel between them
    for valve in VALVES:
        for destination in VALVES[valve]["destinations"]:
            SHORTEST_PATHS[path_key(destination, valve)] = 1
            new_paths = {}
            for path, length in SHORTEST_PATHS.items():
                if destination == path[0] and valve != path[1]:
                    k = path_key(path[1], valve)
                elif destination == path[1] and valve != path[0]:
                    k = path_key(path[0], valve)
                else:
                    continue
                if k not in SHORTEST_PATHS or SHORTEST_PATHS[k] > length + 1:
                    new_paths[k] = length + 1
            SHORTEST_PATHS.update(new_paths)


def test_path(
    start,
    unvisited,
    minutes=0,
    rate=0,
    flow=0,
    path=None,
    paths=None,
    max_minutes=MAX_MINUTES_ALONE,
):
    """Test the path from the start valve to all other valves"""
    if len(unvisited) == 0:
        flow += (max_minutes - minutes) * rate
        paths.append((path, flow))
        return flow
    for valve in unvisited:
        new_minutes = SHORTEST_PATHS.get(path_key(start, valve), 0) + 1
        if new_minutes == 1 or minutes + new_minutes >= max_minutes:
            new_flow = (max_minutes - minutes) * rate
            paths.append((path, flow + new_flow))
            continue
        new_flow = rate * new_minutes
        # recursive to test all possible paths
        test_path(
            start=valve,
            unvisited=unvisited - {valve},
            minutes=minutes + new_minutes,
            rate=rate + VALVES[valve]["rate"],
            flow=flow + new_flow,
            path=path + [valve],
            paths=paths,
            max_minutes=max_minutes,
        )


def part_1():
    get_valve_data()
    map_shortest_path_between_tunnels()

    # only valves with flow rate > 0 are worth visiting
    unvisited_valves = {v["name"] for v in VALVES.values() if v["rate"]}

    paths = []
    test_path(
        start=VALVES["AA"]["name"],
        unvisited=unvisited_valves,
        path=[],
        paths=paths,
    )

    released_pressure = max([path[1] for path in paths])

    print(f"Part 1: {released_pressure}")  # Part 1 2080


if __name__ == "__main__":
    part_1()
