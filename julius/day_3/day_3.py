import string

def input_to_list(path: str) -> list:
    input = open(path).read()
    return input.splitlines()

def middle_split_string_and_return_common_character(items:str) -> str:
    first_half  = items[:len(items)//2]
    second_half = items[len(items)//2:]
    return "".join(set(first_half).intersection(second_half))

alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
priority_lookup = {}
priority = 1
for i in alphabet:
    priority_lookup[f"{i}"] = priority
    priority += 1

items_list = input_to_list("day_3_input.txt")
priorities_list = []
for item in items_list:
    priorities_list.append(priority_lookup[f"{middle_split_string_and_return_common_character(item)}"])

print("PART 1:", sum(priorities_list)) # 7795

### PART 2 ###

def return_common_character(strings: list[str]) -> str:
    return "".join(set.intersection(*map(set,strings)))

items = input_to_list("day_3_input.txt")
priorities_list = []
for i in [items[x:x+3] for x in range(0, len(items), 3)]: # group by 3
    priorities_list.append(priority_lookup[f"{return_common_character(i)}"])

print("PART 2:", sum(priorities_list)) # 2703
