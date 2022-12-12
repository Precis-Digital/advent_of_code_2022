from __future__ import annotations

import collections
import copy
import dataclasses
import math
import operator
import re
from typing import Callable, Iterable

from shared import utils


@dataclasses.dataclass
class Item:
    worry_level: int


class KeepAway:
    def __init__(self, monkeys: list[Monkey], can_be_bored: bool) -> None:
        self.monkeys = monkeys
        self.can_be_bored = can_be_bored
        self.lcm = None

        if not self.can_be_bored:
            self.lcm = math.lcm(*[monkey.test_divisor for monkey in self.monkeys])

    def play_round(self) -> None:
        for monkey in self.monkeys:
            self.play_turn(monkey=monkey)

    def play_turn(self, monkey: Monkey) -> None:
        while monkey.items:
            item = monkey.inspect()
            item = monkey.do_operation(item=item, lcm=self.lcm)

            if self.can_be_bored:
                item = monkey.get_bored(item=item)

            receiver_index = monkey.find_receiver(item=item)
            receiver = self.monkeys[receiver_index]
            monkey.throw(item=item, receiver=receiver)

    def find_most_active_monkeys(self, n: int) -> list[Monkey]:
        sorted_monkeys = sorted(self.monkeys, key=operator.attrgetter("inspect_count"))
        return sorted_monkeys[-n:]

    @property
    def monkey_business(self):
        monkey1, monkey2 = self.find_most_active_monkeys(n=2)
        return monkey1.inspect_count * monkey2.inspect_count


class Monkey:
    def __init__(
        self,
        items: Iterable[Item],
        operation: Callable[[int], int],
        test_divisor: int,
        actions: dict[bool, int],
    ) -> None:
        self.items = collections.deque(items)
        self.operation = operation
        self.test_divisor = test_divisor
        self.actions = actions
        self.inspect_count = 0

    @staticmethod
    def throw(item: Item, receiver: Monkey) -> None:
        receiver.receive(item=item)

    def receive(self, item: Item) -> None:
        self.items.append(item)

    def inspect(self) -> Item:
        self.inspect_count += 1
        return self.items.popleft()

    def do_operation(self, item: Item, lcm: int | None = None) -> Item:
        item_ = copy.deepcopy(item)
        item_.worry_level = self.operation(item_.worry_level)

        if lcm:
            item_.worry_level = item_.worry_level % lcm

        return item_

    @staticmethod
    def get_bored(item: Item) -> Item:
        item.worry_level = item.worry_level // 3
        return item

    def test(self, item: Item) -> bool:
        return item.worry_level % self.test_divisor == 0

    def find_receiver(self, item: Item) -> int:
        return self.actions[self.test(item)]

    @classmethod
    def parse_monkey(cls, monkey: str) -> Monkey:
        monkey_lines = monkey.splitlines()
        starting_items = get_starting_items(staring_items_raw=monkey_lines[1])
        operation = get_operation(operation_raw=monkey_lines[2])
        test = get_test_divisor(test_raw=monkey_lines[3])
        true_action = get_action(action_raw=monkey_lines[4])
        false_action = get_action(action_raw=monkey_lines[5])

        return cls(
            items=starting_items,
            operation=operation,
            test_divisor=test,
            actions={True: true_action, False: false_action},
        )


def get_action(action_raw: str) -> int:
    return int(action_raw.split("monkey ")[-1])


def get_test_divisor(test_raw: str) -> int:
    return int(test_raw.split("by ")[-1])


def get_operation(operation_raw: str) -> Callable:
    operation_str = operation_raw.split("=")[-1].strip()
    if operation_str == "old * old":
        return lambda x: x**2
    if "+" in operation_str:
        return lambda x: x + int(operation_str.split()[-1])
    if "*" in operation_str:
        return lambda x: x * int(operation_str.split()[-1])


def get_starting_items(staring_items_raw: str) -> list[Item]:
    pattern = re.compile(r"^\s*Starting items:\s*(\d+(?:,\s*\d+)*)")
    match = pattern.search(string=staring_items_raw)
    return list(map(lambda x: Item(int(x)), match.group(1).split(",")))


def main() -> None:
    monkey_input = utils.read_input_to_string().split("\n\n")
    monkeys = [Monkey.parse_monkey(monkey=monkey) for monkey in monkey_input]

    game1 = KeepAway(monkeys=copy.deepcopy(monkeys), can_be_bored=True)
    for _ in range(20):
        game1.play_round()

    game2 = KeepAway(monkeys=copy.deepcopy(monkeys), can_be_bored=False)

    for _ in range(10_000):
        game2.play_round()

    print(f"Part 1: {game1.monkey_business}")
    print(f"Part 1: {game2.monkey_business}")


if __name__ == "__main__":
    main()
