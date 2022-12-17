import functools
import itertools
import re
from typing import Any, Iterable, TypeVar

from shared import utils

PATTERN = r"Valve (\w+) has flow rate=(\d+); (tunnel|tunnels) (lead|leads) to (valve|valves) (.*)"
TIME_LIMIT = 30
TIME_LIMIT_ELEPHANT = 26
ORIGIN = "AA"

T = TypeVar("T")
Graph = dict[str, list[str]]
DistDict = dict[tuple[str, str], int]


class ValveSystem:
    def __init__(self, flow_rates: dict[str, int], travel_times: DistDict) -> None:
        self.flow_rates = flow_rates
        self.travel_times = travel_times
        self.paths = set()

    def open_optimally(self, nonzero_valves: Iterable[str]) -> int:
        return self.find_best_option(
            current_position=ORIGIN,
            time_remaining=TIME_LIMIT,
            nonzero_valves=frozenset(nonzero_valves),
        )

    @functools.cache
    def find_best_option(
        self,
        current_position: str,
        time_remaining: int,
        nonzero_valves: frozenset[str],
    ) -> int:

        max_pressure_released = 0
        for valve in nonzero_valves:
            if valve == current_position:
                continue

            next_nonzero_valves = frozenset_remove(
                frozenset_=nonzero_valves, element=valve
            )
            time_remaining_if_valve = (
                time_remaining - self.travel_times[(current_position, valve)] - 1
            )

            if time_remaining_if_valve <= 0:
                continue

            future_pressure_released = self.find_best_option(
                nonzero_valves=next_nonzero_valves,
                current_position=valve,
                time_remaining=time_remaining_if_valve,
            )

            next_valve_release = self.flow_rates[valve] * time_remaining_if_valve

            pressure_released = next_valve_release + future_pressure_released

            if pressure_released > max_pressure_released:
                max_pressure_released = pressure_released

        return max_pressure_released

    def get_path_score(
        self,
        path: Iterable[str],
        time_limit: int = TIME_LIMIT_ELEPHANT,
    ) -> int:
        score = 0
        time_remaining = time_limit
        for start, end in itertools.pairwise((ORIGIN, *path)):
            time_remaining -= self.travel_times[(start, end)] + 1

            if time_remaining < 0:
                return 0

            score += self.flow_rates[end] * time_remaining

        return score

    def open_optimally_elephant(self, nonzero_valves: Iterable[str]) -> int:
        path_scores = {}
        for path in get_permutations(iterable=nonzero_valves, min_len=6, max_len=7):
            if (score := self.get_path_score(path)) > 0:
                path_scores[path] = score

        max_score = 0
        for combo1, combo2 in itertools.product(path_scores.keys(), repeat=2):
            if not set(combo1) & set(combo2):
                if (score := path_scores[combo1] + path_scores[combo2]) > max_score:
                    max_score = score

        return max_score


def frozenset_remove(frozenset_: frozenset[Any], element: Any) -> frozenset[Any]:
    return frozenset(x for x in frozenset_ if x != element)


def parse_valves(valves_raw: list[str]) -> tuple[Graph, list[str], dict[str, int]]:
    graph, flow_rates = {}, {}
    nonzero_valves = []
    for valve_raw in valves_raw:
        match = re.search(PATTERN, valve_raw)
        valve = match.group(1)
        flow_rate = int(match.group(2))
        leads_to = match.group(6).split(", ")
        graph[valve] = leads_to
        flow_rates[valve] = flow_rate

        if flow_rate > 0:
            nonzero_valves.append(valve)

    return graph, nonzero_valves, flow_rates


def get_travel_times(graph: Graph, valves: list[str]) -> DistDict:
    travel_times = {}
    for start, end in itertools.product(valves, repeat=2):
        if start == end or travel_times.get((start, end)):
            continue

        dist = utils.shortest_path_length(graph=graph, start=start, end=end)
        travel_times[(start, end)] = travel_times[(end, start)] = dist

    return travel_times


def get_permutations(
    iterable: Iterable[T],
    min_len: int,
    max_len: int,
) -> list[tuple[T]]:
    permutations = []
    for i in range(min_len, max_len + 1):
        permutations.extend(list(itertools.permutations(iterable, i)))

    return permutations


def main() -> None:
    valves_raw = utils.read_input_to_string().splitlines()
    graph, nonzero_valves, flow_rates = parse_valves(valves_raw=valves_raw)
    travel_times = get_travel_times(graph=graph, valves=[*nonzero_valves, ORIGIN])

    valve_system = ValveSystem(flow_rates=flow_rates, travel_times=travel_times)
    pressured_released = valve_system.open_optimally(nonzero_valves=nonzero_valves)

    pressure_released_elephant = valve_system.open_optimally_elephant(
        nonzero_valves=nonzero_valves
    )

    print(f"Part 1: {pressured_released}")
    print(f"Part 2: {pressure_released_elephant}")


if __name__ == "__main__":
    main()
