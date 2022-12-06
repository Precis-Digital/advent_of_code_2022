import abc
import copy
import dataclasses
import re

from shared import utils

Stacks = list[list[str]]


@dataclasses.dataclass
class Move:
    quantity: int
    from_: int
    to: int

    def __post_init__(self) -> None:
        self.from_ = self.from_ - 1
        self.to = self.to - 1


class CrateMover(abc.ABC):
    def __init__(self, stacks: Stacks) -> None:
        self.stacks = copy.deepcopy(stacks)

    @abc.abstractmethod
    def rearrange_crates(self, moves: list[Move]) -> None:
        pass

    @abc.abstractmethod
    def execute_single_move(self, move: Move) -> None:
        pass

    def get_top_crates_message(self) -> str:
        crates = []
        for stack in self.stacks:
            crates.append(stack[-1])

        return "".join(crates)


class CrateMover9000(CrateMover):
    def __init__(self, stacks: Stacks) -> None:
        super().__init__(stacks=stacks)

    def execute_single_move(self, move: Move) -> None:
        crate = self.stacks[move.from_].pop()
        self.stacks[move.to].append(crate)

    def rearrange_crates(self, moves: list[Move]) -> None:
        for move in moves:
            for _ in range(move.quantity):
                self.execute_single_move(move=move)


class CrateMover9001(CrateMover):
    def __init__(self, stacks: Stacks) -> None:
        super().__init__(stacks=stacks)

    def rearrange_crates(self, moves: list[Move]) -> None:
        for move in moves:
            self.execute_single_move(move=move)

    def execute_single_move(self, move: Move) -> None:
        crates = self.stacks[move.from_][-move.quantity :]
        self.stacks[move.from_] = self.stacks[move.from_][: -move.quantity]
        self.stacks[move.to].extend(crates)


def parse_stacks(stacks: str) -> Stacks:
    stack_lines = stacks.splitlines()
    nr_of_stacks = int(stack_lines[-1].strip()[-1])

    stacks_ = [[] for _ in range(nr_of_stacks)]
    for line in reversed(stack_lines[:-1]):
        for i, crate in enumerate(line[1::2][::2]):
            if crate == " ":
                continue

            stacks_[i].append(crate)

    return stacks_


def parse_moves(moves: str) -> list[Move]:
    moves_lines = moves.splitlines()
    moves_ = []
    for line in moves_lines:
        moves_.append(Move(*[int(move) for move in re.findall(r"\d+", line)]))

    return moves_


def main() -> None:
    data = utils.read_input_to_string()
    stacks, moves = data.split("\n\n")
    stacks = parse_stacks(stacks=stacks)
    moves = parse_moves(moves=moves)

    crate_mover_9000 = CrateMover9000(stacks=stacks)
    crate_mover_9000.rearrange_crates(moves=moves)
    message_part1 = crate_mover_9000.get_top_crates_message()

    crate_mover_9001 = CrateMover9001(stacks=stacks)
    crate_mover_9001.rearrange_crates(moves=moves)
    message_part2 = crate_mover_9001.get_top_crates_message()

    print(f"Part 1: {message_part1}")
    print(f"Part 2: {message_part2}")


if __name__ == "__main__":
    main()
