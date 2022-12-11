class MoveCommand:
    direction: str
    num_squares: int

    def __init__(self, direction: str, num_squares: int) -> "MoveCommand":
        self.direction = direction
        self.num_squares = num_squares

    def __repr__(self) -> str:
        return f"{self.direction} - {self.num_squares}"

    @classmethod
    def from_input_string(cls, string: str) -> "MoveCommand":
        direction = string.split(" ")[0]
        num_squares = int(string.split(" ")[1])
        return cls(direction, num_squares)

def get_moves(file_name: str) -> list[MoveCommand]:
    with open(file_name, "r") as f:
        return [MoveCommand.from_input_string(string.strip()) for string in f.readlines()]

def get_new_head_position(direction: str, current_position: tuple[int, int]) -> tuple[int, int]:
    match direction:
        case "R":
            return (current_position[0] + 1, current_position[1])
        case "L":
            return (current_position[0] - 1, current_position[1])
        case "U":
            return (current_position[0], current_position[1] + 1)
        case "D":
            return (current_position[0], current_position[1] - 1)

def get_allowed_tail_positions(head_position: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (head_position[0] - 1, head_position[1] - 1),
        (head_position[0], head_position[1] - 1),
        (head_position[0] + 1, head_position[1] - 1),
        (head_position[0] - 1, head_position[1]),
        (head_position[0], head_position[1]),
        (head_position[0] + 1, head_position[1]),
        (head_position[0] - 1, head_position[1] + 1),
        (head_position[0], head_position[1] + 1),
        (head_position[0] + 1, head_position[1] + 1),
    ]

def get_new_knot_position(new_head_position: tuple[int, int], current_tail_position: tuple[int, int]) -> tuple[int, int]:
    if current_tail_position in get_allowed_tail_positions(new_head_position):
        return current_tail_position
    new_x = current_tail_position[0]
    new_y = current_tail_position[1]
    # Check if in same column or row
    if new_head_position[0] == current_tail_position[0] or new_head_position[1] == current_tail_position[1]:
        # Move directly
        if new_head_position[0] > current_tail_position[0]:
            new_x = current_tail_position[0] + 1
        elif new_head_position[0] < current_tail_position[0]:
            new_x = current_tail_position[0] - 1
        elif new_head_position[1] < current_tail_position[1]:
            new_y = current_tail_position[1] - 1
        elif new_head_position[1] > current_tail_position[1]:
            new_y = current_tail_position[1] + 1
    else:
        # Move diagonally
        if new_head_position[0] < current_tail_position[0]:
            new_x = current_tail_position[0] - 1
        elif new_head_position[0] > current_tail_position[0]:
            new_x = current_tail_position[0] + 1
        
        if new_head_position[1] < current_tail_position[1]:
            new_y = current_tail_position[1] - 1
        elif new_head_position[1] > current_tail_position[1]:
            new_y = current_tail_position[1] + 1
    return (new_x, new_y)
    

def determine_unique_positions_of_tail(moves: list[MoveCommand], rope_length: int, visualise: bool = False) -> dict[tuple[int, int], bool]:
    coords: dict[tuple[int, int], bool] = {}
    current_head_position: tuple[int, int] = (0,0)
    current_rope_positions: dict[int, tuple[int, int]] = {rope_number: (0,0) for rope_number in range(1, rope_length + 1)}
    move_counter = 0
    for move in moves:
        for _ in range(move.num_squares):
            
            move_counter += 1
            current_head_position = get_new_head_position(move.direction, current_head_position)
            for rope_number in range(1, rope_length + 1):
                prev_rope = current_head_position if rope_number == 1 else current_rope_positions[rope_number-1]
                current_rope_positions[rope_number] = get_new_knot_position(prev_rope, current_rope_positions[rope_number])

            if visualise:
                visualise_output(rope_length, current_rope_positions, current_head_position, max_x = visualise[0], max_y = visualise[1])

            coords[current_rope_positions[rope_length]] = True
    return coords


### THIS VISUALISITION ONLY WORKS FOR THE SAMPLE INPUT ###
import os
import sys
import time


def visualise_output(rope_length: int, current_rope_positions: dict[int, tuple[int, int]], current_head_position: tuple[int, int], max_x: int, max_y: int) -> None:
    time.sleep(0.2)
    os.system("clear")
    sys.stdout.flush()
    coord_system = [["." for _ in range(max_x)] for _ in range(max_y)]
    for num in range(0, -(rope_length), -1):
        rope_number = num + rope_length
        coord_system[max_y - current_rope_positions[rope_number][1] - 1 ][current_rope_positions[rope_number][0]] = str(rope_number)
    coord_system[max_y - current_head_position[1] - 1][current_head_position[0]] = "H"
    sys.stdout.write("---"*20 + "\n")
    sys.stdout.write("\n".join(["|".join(coord) for coord in coord_system]))
### END VISUALISATION ###

# Sample 1 - 13
# Visualisation param = [6,5]
print(len(determine_unique_positions_of_tail(get_moves("sample_input.txt"), rope_length=1).keys()))

# Part 1 - 6314
print(len(determine_unique_positions_of_tail(get_moves("input.txt"), rope_length=1).keys()))

# Sample 2 - 1
# Visualisation param = [6, 5]
print(len(determine_unique_positions_of_tail(get_moves("sample_input.txt"), rope_length=9).keys()))

# Sample 2 Large - 36
print(len(determine_unique_positions_of_tail(get_moves("sample_input_large.txt"), rope_length=9).keys()))

# Part 2 - 2504
print(len(determine_unique_positions_of_tail(get_moves("input.txt"), rope_length=9).keys()))