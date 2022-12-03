from typing import Optional


def get_input(file_name: str) -> list[str]:
    with open(file_name) as f:
        return [line.strip() for line in f.readlines()]


def get_compartments(rucksack: str) -> tuple[str, str]:
    n = len(rucksack)
    return rucksack[: n // 2], rucksack[n // 2 :]


def character_to_int(char: Optional[str]) -> int:
    # a-z is 1-26 and A-Z is 27-52
    if char is None:
        return 0
    return ord(char) - 96 if char.islower() else ord(char) - 38


def solution_1(data: list[str]) -> int:
    total_character_score = 0
    for row in data:
        comp1, comp2 = get_compartments(rucksack=row)
        intersecting_items = set(comp1).intersection(comp2)
        item = next(iter(intersecting_items), None)
        total_character_score += character_to_int(char=item)
    return total_character_score


def solution_2(data: list[str]) -> int:
    total_character_score = 0
    for i in range(0, len(data), 3):
        elf1, elf2, elf3 = data[i], data[i + 1], data[i + 2]
        shared_items = set(elf1).intersection(elf2).intersection(elf3)
        item = next(iter(shared_items), None)
        total_character_score += character_to_int(char=item)
    return total_character_score


if __name__ == "__main__":
    rucksacks = get_input("inputs/day-3-input.txt")
    print("solution 1:", solution_1(data=rucksacks))
    print("solution 2:", solution_2(data=rucksacks))
