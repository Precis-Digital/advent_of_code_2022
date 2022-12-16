import collections
import inspect
import sys
from typing import Iterable, TypeVar

T = TypeVar("T")


def read_input_to_string() -> str:
    day = inspect.stack()[1].filename.split("/")[-1].split(".")[0]
    with open(f"inputs/{day}.txt", "r") as file:
        return file.read()


def chunks(lst: list[T], n: int) -> list[T]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def drop_empty_rows(rows: Iterable[str], /) -> list[str]:
    return [row for row in rows if row != ""]


def shortest_path_length(graph: dict[T, list[T]], start: T, end: T) -> int:
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
