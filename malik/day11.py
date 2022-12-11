import re
import math

MONKEY_REGEX = r"Monkey (\d+):$"


class Monkey:
    def __init__(
        self,
        monkey_id,
        starting_items,
        operation,
        divisible_by: int,
        if_true: int,
        if_false: int,
        feels_relief: False,
    ):
        self.monkey_id = monkey_id
        self.items = starting_items
        self.operation = operation
        self.divisible_by = divisible_by
        self.if_true = if_true
        self.if_false = if_false
        self.inspection_counter = 0
        self.feels_relief = feels_relief

    def calculate_worry(self, item: int) -> int:
        old = item
        return eval(self.operation)

    def catch_item(self, item: int):
        self.items.append(item)

    def throw_to_monkey(
        self, item, monkey_id: int, monkey_hashmap: dict[int, "Monkey"]
    ):

        monkey = monkey_hashmap[monkey_id]
        monkey.catch_item(item)

        # print(f"Monkey {self.monkey_id} threw {item} to Monkey {monkey_id}")

    def run(self, monkey_hashmap: dict[int, "Monkey"], mod_prod: int):
        while self.items:
            item = self.items.pop(0)
            item = item % mod_prod
            self.inspection_counter += 1
            # calculate worry
            value = self.calculate_worry(item)

            # process relief
            if self.feels_relief:
                value = value // 3

            # throw item

            if value % self.divisible_by == 0:
                self.throw_to_monkey(value, self.if_true, monkey_hashmap)
            else:
                self.throw_to_monkey(value, self.if_false, monkey_hashmap)

    def __repr__(self):
        return f"Monkey {self.monkey_id}: {self.items} {self.inspection_counter}"


def get_data(fname: str, feel_relief: bool) -> dict[int, Monkey]:
    """
    Sample input:
    Monkey 0:
      Starting items: 79, 98
      Operation: new = old * 19
      Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3

    :param fname:
    :return:
    """
    output = {}
    with open(fname, "r") as fname:
        monkey_id: int
        starting_items: list[int]
        operation: str
        divisible_by: int
        if_true: int
        if_false: int
        end_of_block: bool = False

        for row in fname.readlines():

            row = row.strip()

            if row.startswith("Monkey"):
                monkey_id = int(re.findall(MONKEY_REGEX, row)[0])
                output[monkey_id] = {
                    "starting_items": [],
                    "operation": "",
                    "test": {
                        "divisible_by": None,
                        "if_true": None,
                        "if_false": None,
                    },
                }
            elif row.startswith("Starting items"):
                starting_items = [int(x) for x in row.split(": ")[1].split(", ")]
            elif row.startswith("Operation"):
                operation = row.split(": ")[1].replace("new = ", "")
            elif row.startswith("Test"):
                divisible_by = int(row.split(": ")[1].split(" ")[2])
            elif row.startswith("If true"):
                if_true = int(row.split(": ")[1].split(" ")[3])
            elif row.startswith("If false"):
                if_false = int(row.split(": ")[1].split(" ")[3])

                # create a new monkey
                output[monkey_id] = Monkey(
                    monkey_id,
                    starting_items,
                    operation,
                    divisible_by,
                    if_true,
                    if_false,
                    feels_relief=feel_relief,
                )

    return output


def compute_product_of_mods(monkey_lookup: dict[int, Monkey]) -> int:
    """
    Takes advantage of 3 properties of mod arithmetic:
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem ( a subtle hint is that all values are prime...)
    https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-multiplication
    https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-addition-and-subtraction
    :param monkey_lookup:
    :return:
    """
    product = 1
    for monkey in monkey_lookup.values():
        product *= monkey.divisible_by
    return product


def solution_1(fname: str) -> int:
    monkey_lookup = get_data(fname=fname, feel_relief=True)
    for _ in range(20):
        for _, monkey in monkey_lookup.items():
            monkey.run(monkey_lookup, mod_prod=compute_product_of_mods(monkey_lookup))
    counters = [monkey.inspection_counter for monkey in monkey_lookup.values()]
    return math.prod(sorted(counters)[-2:])


def solution_2(fname: str) -> int:
    monkey_lookup = get_data(fname=fname, feel_relief=False)
    for _ in range(10000):
        for _, monkey in monkey_lookup.items():
            monkey.run(monkey_lookup, mod_prod=compute_product_of_mods(monkey_lookup))
    counters = [monkey.inspection_counter for monkey in monkey_lookup.values()]
    return math.prod(sorted(counters)[-2:])


if __name__ == "__main__":
    FNAME = "inputs/day-11-input.txt"
    print(solution_1(fname=FNAME))

    print(solution_2(fname=FNAME))
