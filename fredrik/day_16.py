import functools
import itertools
import re
from typing import Any, Iterable

from shared import utils

PATTERN = r"Valve (\w+) has flow rate=(\d+); (tunnel|tunnels) (lead|leads) to (valve|valves) (.*)"
TIME_LIMIT = 30
ORIGIN = "AA"

Graph = dict[str, list[str]]
DistDict = dict[tuple[str, str], int]


class ValveSystem:
    def __init__(self, flow_rates: dict[str, int], travel_times: DistDict) -> None:
        self.flow_rates = flow_rates
        self.travel_times = travel_times

    def open_optimally(self, nonzero_valves: Iterable[str]) -> int:
        return self.find_best_option(
            current_position=ORIGIN,
            time_remaining=TIME_LIMIT,
            nonzero_valves=tuple(nonzero_valves),
        )

    @functools.cache
    def find_best_option(
        self,
        current_position: str,
        time_remaining: int,
        nonzero_valves: tuple[str],
    ) -> int:

        max_pressure_released = 0
        for valve in nonzero_valves:
            if valve == current_position:
                continue

            next_nonzero_valves = tuple_remove(tuple_=nonzero_valves, element=valve)
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


def tuple_remove(tuple_: tuple[Any], element: Any) -> tuple[Any]:
    return tuple(x for x in tuple_ if x != element)


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


def main() -> None:
    valves_raw = utils.read_input_to_string().splitlines()
    graph, nonzero_valves, flow_rates = parse_valves(valves_raw=valves_raw)
    travel_times = get_travel_times(graph=graph, valves=[*nonzero_valves, ORIGIN])

    valve_system = ValveSystem(flow_rates=flow_rates, travel_times=travel_times)
    pressured_released = valve_system.open_optimally(nonzero_valves=nonzero_valves)

    assert pressured_released == 1724

    print(f"Part 1: {pressured_released}")


if __name__ == "__main__":
    main()
