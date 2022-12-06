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
    return [char for i, char in enumerate(row.replace("\n", "")) if i % 4 == 1]

def get_move_string_actions(command: str) -> tuple[int, str, str]:
    command_split = command.split(" ")
    return int(command_split[1]), command_split[3], command_split[5]

def execute_move_command(stacks: dict[str, list], command: str) -> dict[str, list]:
    move_num, move_from, move_to = get_move_string_actions(command)
    for _ in range(move_num):
        stacks[move_to].insert(0,stacks[move_from].pop(0))
    
    return stacks

def execute_move_command_9001(stacks: dict[str, list], command: str) -> dict[str, list]:
    move_num, move_from, move_to = get_move_string_actions(command)

    stacks[move_to] = stacks[move_from][:move_num] + stacks[move_to]
    for _ in range(move_num):
        stacks[move_from].pop(0)
    
    return stacks

def move_boxes(stacks: dict[str, list], command_list: list[str], crane_type: str = "9000") -> dict[str, list]:
    for command in command_list:
        if crane_type == "9000":
            stacks = execute_move_command(stacks, command)
        elif crane_type == "9001":
            stacks = execute_move_command_9001(stacks, command)
        else:
            raise ModuleNotFoundError(f"Unknown Crane Type '{crane_type}'")
    
    return stacks

def get_top_box_string(stacks: dict[str, list]) -> str:
    top_box_string = ""
    for _,v in stacks.items():
        top_box_string += v[0]
    
    return top_box_string

# Sample 1 - CMZ
print(get_top_box_string(move_boxes(*get_stacks_and_strategies_from_file("sample_input.txt"))))

# Part 1 - WCZTHTMPS
print(get_top_box_string(move_boxes(*get_stacks_and_strategies_from_file("input.txt"))))

# Sample 2 - MCD
print(get_top_box_string(move_boxes(*get_stacks_and_strategies_from_file("sample_input.txt"), "9001")))

# Part 2 - BLSGJSDTS
print(get_top_box_string(move_boxes(*get_stacks_and_strategies_from_file("input.txt"), "9001")))
