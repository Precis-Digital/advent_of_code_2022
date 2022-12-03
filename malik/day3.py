from typing import Optional


def get_input(fname: str) -> list[str]:
    with open(fname) as f:
        return [line.strip() for line in f.readlines()]


def get_compartments(rucksack: str) -> tuple[str, str]:
    n = len(rucksack)
    return rucksack[: n // 2], rucksack[n // 2 :]


def get_items_in_both_compartments(comp1: str, comp2: str) -> Optional[str]:
    intersecting_items = set(comp1).intersection(comp2)
    return intersecting_items


def character_to_int(char: str) -> int:
    # a-z is 1-26 and A-Z is 27-52
    return ord(char) - 96 if char.islower() else ord(char) - 38


def solution_1(data: list[str]) -> int:
    total_character_score = 0
    for row in data:
        comp1, comp2 = get_compartments(rucksack=row)
        intersecting_items = get_items_in_both_compartments(comp1=comp1, comp2=comp2)
        item = next(iter(intersecting_items), None)
        if item:
            total_character_score += character_to_int(char=item)
    return total_character_score


def solution_2(data: list[str]) -> int:
    total_character_score = 0
    for i in range(0, len(data), 3):
        elf1 = data[i]
        elf2 = data[i + 1]
        elf3 = data[i + 2]
        item = next(iter(set(elf1).intersection(elf2).intersection(elf3)), None)
        if item:
            # print(item, character_to_int(char=item))
            total_character_score += character_to_int(char=item)
    # print(total_character_score)
    return total_character_score


if __name__ == "__main__":
    data = get_input("inputs/day-3-input.txt")
    print("solution 1:", solution_1(data=data))
    print("solution 2:", solution_2(data=data))
