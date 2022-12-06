import re

# Stole parser from Jonas. Please don't be mad Santa :(
def get_stacks_and_strategies_from_file(file_name: str) -> tuple[list[str, list], list[str]]:
    with open(file_name, "r") as f:
        strategy_file = f.readlines()

    parsed_lines = [line for line in strategy_file]

    raw_stacks = parsed_lines[:parsed_lines.index("\n")]
    strategies = [line.strip() for line in parsed_lines[parsed_lines.index("\n")+1:]]
    
    boxes_array = [get_boxes_array_from_raw_row(row) for row in raw_stacks[:-1]]

    stacks = {val: [boxes[int(val)-1] for boxes in boxes_array if boxes[int(val)-1] != " "] for val in raw_stacks[-1].strip().split(" ") if val != ""}
    return stacks, strategies


def get_boxes_array_from_raw_row(row: str) -> list[str]:
    cleaned_row = row.replace("\n", "")
    stacks = []
    for i, character in enumerate(cleaned_row):
        if i % 4 == 1:
            stacks.append(character)

    return stacks

stacks_and_moves = get_stacks_and_strategies_from_file("day_5_input.txt")

# ---- Non stolen below:

for i in stacks_and_moves[1]:
    instruction_list = re.split(r'\D+',i) # grab only numbers
    amount_to_move, move_from, move_to = [number for number in instruction_list if number != ""]

    for i in range(int(amount_to_move)):
        stacks_and_moves[0][move_to].insert(0, stacks_and_moves[0][move_from].pop(0))

top_crates = ""
for v in stacks_and_moves[0].values():
    top_crates += v[0]

print("PART 1:", top_crates) # HNSNMTLHQ

### Part 2 ###

stacks_and_moves = get_stacks_and_strategies_from_file("day_5_input.txt")

for i in stacks_and_moves[1]:
    instruction_list = re.split(r'\D+',i) # grab only numbers
    amount_to_move, move_from, move_to = [number for number in instruction_list if number != ""]
    
    stacks_and_moves[0][move_to] = stacks_and_moves[0][move_from][:int(amount_to_move)] + stacks_and_moves[0][move_to]
    for i in range(int(amount_to_move)):
        stacks_and_moves[0][move_from].pop(0)

top_crates = ""
for v in stacks_and_moves[0].values():
    top_crates += v[0]

print("PART 2:", top_crates) # RNLFDJMCT