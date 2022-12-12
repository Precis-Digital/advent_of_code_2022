import copy
import math


class Monkey:
    def __init__(
        self, items: list, operation: str, test: int, if_true: int, if_false: int
    ):
        self.items = items
        self.operation = operation
        self.test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspected_items = 0

    def run_operation(self, value):
        operation = self.operation.split(" ")[1]
        factor = (
            value
            if self.operation.split(" ")[2] == "old"
            else int(self.operation.split(" ")[2])
        )
        if operation == "+":
            return value + factor
        elif operation == "*":
            return value * factor

    def inspect_item(self, item, divisor=None):
        level = self.run_operation(item)
        if divisor:
            level = level % divisor
        return level

    @staticmethod
    def get_bored(stress_level: int):
        return stress_level // 3

    def run_test(self, stress_level: int):
        return stress_level % self.test == 0

    def receive_item(self, item):
        self.items.append(item)


def parse_monkey(monkey_rows: list[str]) -> Monkey:
    monkey_input = [monkey_row.split(":")[1] for monkey_row in monkey_rows]
    m = Monkey(
        items=[int(item) for item in monkey_input[1].split(",")],
        operation=monkey_input[2].split("=")[1].strip(),
        test=int(monkey_input[3].split(" ")[-1]),
        if_true=int(monkey_input[4].split(" ")[-1]),
        if_false=int(monkey_input[5].split(" ")[-1]),
    )
    return m


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for j in range(0, len(lst), n):
        yield lst[j : j + n]


def get_monkeys() -> list[Monkey]:
    with open("erica/day_11/input_data.txt") as f:
        line_rows = f.readlines()
        rows = [line_rows.strip() for line_rows in line_rows if line_rows != "\n"]
        monkeys_rows = chunks(rows, 6)
        return [parse_monkey(monkey_rows) for monkey_rows in monkeys_rows]


def play_monkey_round(monkey: Monkey, monkey_list: list[Monkey], divisor=None):
    for item in monkey.items:
        stress_level = monkey.inspect_item(item, divisor)

        if divisor:
            stress_level_after_inspection = stress_level
        else:
            stress_level_after_inspection = monkey.get_bored(stress_level)

        test_outcome = monkey.run_test(stress_level_after_inspection)
        if test_outcome:
            receiver_monkey = monkey.if_true
        else:
            receiver_monkey = monkey.if_false
        monkey_list[receiver_monkey].receive_item(stress_level_after_inspection)

        monkey.inspected_items += 1
        monkey.items = monkey.items[1:]


def find_top_2_monkey_business(monkeys_: list[Monkey]):
    top_2_monkeys = sorted(monkeys_, key=lambda monkey: monkey.inspected_items)[-2:]
    return top_2_monkeys[0].inspected_items * top_2_monkeys[1].inspected_items


if __name__ == "__main__":
    monkeys = get_monkeys()

    monkeys_part_1 = copy.deepcopy(monkeys)
    for i in range(20):
        for monkey_part_1 in monkeys_part_1:
            play_monkey_round(monkey_part_1, monkeys_part_1)

    print(f"part 1 {find_top_2_monkey_business(monkeys_part_1)}")  # part 1: 111210

    monkeys_part_2 = copy.deepcopy(monkeys)
    monkey_divisor = math.prod([monkey.test for monkey in monkeys_part_2])
    for i in range(10000):
        for monkey_part_2 in monkeys_part_2:
            play_monkey_round(monkey_part_2, monkeys_part_2, monkey_divisor)

    print(f"part 2 {find_top_2_monkey_business(monkeys_part_2)}")  # part 2: 15447387620
