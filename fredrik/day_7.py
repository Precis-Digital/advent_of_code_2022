import functools
import operator
from typing import Any, Mapping

from shared import utils

TOTAL_SPACE = 70_000_000
NEEDED_SPACE = 30_000_000

TypeSafeMapping = Mapping | dict


class TerminalReader:
    def __init__(self):
        self.cwd = []
        self.directory_tree = {}
        self.directory_sizes = []

    def update_cwd(self, command: str) -> None:
        if command.endswith(".."):
            self.cwd.pop()
        else:
            directory = self.get_directory(line=command)
            self.cwd.append(directory)

    def add_dir_to_directory_tree(self, line: str) -> None:
        directory = self.get_directory(line=line)
        self.directory_tree[str(self.cwd)][directory] = {}

    @staticmethod
    def get_directory(line: str) -> str:
        return line.split(" ")[-1]

    def get_value_from_path(self, path: list[str]) -> TypeSafeMapping:
        return functools.reduce(operator.getitem, path, self.directory_tree)

    def upsert_value_from_cwd(self, value: dict[str, Any]) -> None:
        try:
            self.get_value_from_path(path=self.cwd[:-1])[self.cwd[-1]].update(value)
        except KeyError:
            self.get_value_from_path(path=self.cwd[:-1])[self.cwd[-1]] = value

    def ensure_cwd_in_directory_tree(self) -> None:
        try:
            self.get_value_from_path(path=self.cwd)
        except KeyError:
            self.upsert_value_from_cwd(value={})

    def add_file_to_cwd(self, line: str) -> None:
        file_size, file_name = line.split(" ")
        self.upsert_value_from_cwd(value={file_name: file_size})

    def get_size(self, directory: dict[str, Any]) -> int:
        total_size = 0
        for value in directory.values():
            if isinstance(value, dict):
                total_size += self.get_size(directory=value)
            else:
                total_size += int(value)
        return total_size

    def evaluate_line(self, line: str) -> None:
        if line.startswith("$ cd"):
            self.update_cwd(command=line)
            self.ensure_cwd_in_directory_tree()
        elif line.split(" ")[0].isdigit():
            self.add_file_to_cwd(line=line)

    def get_directory_sizes(self, directory: dict[str, Any] | None = None):
        if directory is None:
            directory = self.directory_tree

        for sub_directory, contents in directory.items():
            if isinstance(contents, dict):
                self.directory_sizes.append(self.get_size(contents))
                self.get_directory_sizes(directory=contents)

    def parse(self, terminal_output: str) -> None:
        for line in terminal_output.splitlines():
            self.evaluate_line(line=line)


def part1(terminal_reader: TerminalReader) -> int:
    return sum(size for size in terminal_reader.directory_sizes if size <= 100_000)


def part2(terminal_reader: TerminalReader) -> int:
    used_space = terminal_reader.directory_sizes[0]
    available_space = TOTAL_SPACE - used_space
    min_delete_size = NEEDED_SPACE - available_space
    return min(
        size for size in terminal_reader.directory_sizes if size > min_delete_size
    )


def main() -> None:
    terminal_output = utils.read_input_to_string()
    terminal_reader = TerminalReader()
    terminal_reader.parse(terminal_output=terminal_output)
    terminal_reader.get_directory_sizes()

    total_size = part1(terminal_reader=terminal_reader)
    min_deletable_file_size = part2(terminal_reader=terminal_reader)

    print(f"Part 1: {total_size}")
    print(f"Part 2: {min_deletable_file_size}")


if __name__ == "__main__":
    main()
