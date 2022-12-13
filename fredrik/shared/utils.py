import inspect
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
