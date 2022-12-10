import string
from typing import TypeVar

from shared import utils

T = TypeVar("T")

PRIORITY = {
    item_type: priority + 1
    for priority, item_type in enumerate(
        [*string.ascii_lowercase, *string.ascii_uppercase]
    )
}


def find_common_type(*args: str) -> str:
    (common_type,) = set.intersection(*map(set, args))
    return common_type


def find_common_type_in_rucksack(rucksack: str) -> str:
    split_index = int(len(rucksack) / 2)
    compartment_1, compartment_2 = rucksack[:split_index], rucksack[split_index:]
    return find_common_type(compartment_1, compartment_2)


def main() -> None:
    rucksacks = utils.read_input_to_string().splitlines()

    priority_sum_1 = 0
    for rucksack in rucksacks:
        common_type = find_common_type_in_rucksack(rucksack=rucksack)
        priority_sum_1 += PRIORITY[common_type]

    priority_sum_2 = 0
    for elf_group in utils.chunks(lst=rucksacks, n=3):
        common_type = find_common_type(*elf_group)
        priority_sum_2 += PRIORITY[common_type]

    print(f"Part 1: {priority_sum_1}")
    print(f"Part 2: {priority_sum_2}")


if __name__ == "__main__":
    main()
