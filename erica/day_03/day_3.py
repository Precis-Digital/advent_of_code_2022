import pathlib
from typing import List


def read_input_data(path: str):
    return pathlib.Path(path).read_text().split("\n")


def find_duplicates_in_backpacks(backpacks: List[str]) -> List[set]:
    duplicates_in_backpacks = []
    for backpack in backpacks:
        compartments = split_backpack_into_compartments(backpack=backpack)
        duplicates_in_backpacks.append(find_common_letter(backpacks=compartments))
    return duplicates_in_backpacks


def split_backpack_into_compartments(backpack: str) -> List[str]:
    length = int(len(backpack) / 2)
    return [backpack[:length],  backpack[length:]]


def find_common_letter(backpacks: List[str]) -> set[str]:
    return set.intersection(*map(set, backpacks))


def map_letters_to_values(duplicates: List[set]) -> List[int]:
    backpack_values = []
    for duplicate_items in duplicates:
        item = next(iter(duplicate_items))
        value = ord(item.lower()) - 70 if item.isupper() else ord(item.lower()) - 96
        backpack_values.append(value)
    return backpack_values


def divide_backpacks_into_chunks_of_three(backpacks: List[str]) -> List[List[str]]:
    for i in range(0, len(backpacks), 3):
        yield backpacks[i: i + 3]


def find_badges_in_backpacks(backpacks: List[str]) -> List[set]:
    backpacks_groups = divide_backpacks_into_chunks_of_three(backpacks=backpacks)
    badges = []
    for backpacks_of_three in backpacks_groups:
        badges.append(find_common_letter(backpacks_of_three))
    return badges


def main():
    backpacks = read_input_data("erica/day_03/input_data.txt")
    list_of_duplicates = find_duplicates_in_backpacks(backpacks=backpacks)
    backpack_values = sum(map_letters_to_values(duplicates=list_of_duplicates))
    print(backpack_values)  # part 1: 7826

    badges = find_badges_in_backpacks(backpacks=backpacks)
    print(sum(map_letters_to_values(badges)))  # part 2: 2577


if __name__ == "__main__":
    main()
