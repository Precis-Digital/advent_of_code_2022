def get_rucksacks_from_file(file_name: str) -> list[list]:
    with open(file_name, "r") as f:
        rucksacks = f.readlines()

    return [parse_rucksack(rucksack.strip()) for rucksack in rucksacks]

LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def parse_rucksack(rucksack: str) -> list:
    comp1 = rucksack[:len(rucksack)//2]
    comp2 = rucksack[len(rucksack)//2:]
    shared_items = set(comp1) & set(comp2)
    shared_items_value = LETTERS.index(shared_items.pop())+1
    return [rucksack, comp1, comp2, shared_items, shared_items_value]

def calc_sum_of_shared_items(rucksacks: list[list], value_index: int = 4) -> int:
    return sum([rucksack[value_index] for rucksack in rucksacks])

def add_badges_to_rucksacks(rucksacks: list[list]) -> list[list]:
    parsed_rucksacks = []
    group_rucksacks = []
    for i, rucksack in enumerate(rucksacks):
        group_rucksacks.append(rucksack)
        if i % 3 == 2:
            group_badge = (set(group_rucksacks[0][0]) & set(group_rucksacks[1][0]) & set(group_rucksacks[2][0])).pop()
            group_badge_value = LETTERS.index(group_badge)+1
            
            for rucksack2 in group_rucksacks: 
                rucksack2.extend([group_badge, group_badge_value])
                parsed_rucksacks.append(rucksack2)
            group_rucksacks = []

    return parsed_rucksacks

# Part 1 Sample
print(calc_sum_of_shared_items(get_rucksacks_from_file("sample_input.txt"))) # 157

# Part 1
print(calc_sum_of_shared_items(get_rucksacks_from_file("input.txt"))) # 8233

# Part 2 Sample
print(int(calc_sum_of_shared_items(add_badges_to_rucksacks(get_rucksacks_from_file("sample_input.txt")), 6)/3))

# Part 2
print(int(calc_sum_of_shared_items(add_badges_to_rucksacks(get_rucksacks_from_file("input.txt")), 6)/3))