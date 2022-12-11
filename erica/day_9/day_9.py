import math

MAX_DISTANCE = math.hypot(1 - 2, 1 - 2)


def get_data_into_lines() -> list[str]:
    with open("erica/day_9/input_data.txt") as f:
        line_rows = f.readlines()
        return [line_rows.strip() for line_rows in line_rows]


def generate_head_coordinates(instructions: list[str]) -> list[tuple[int, int]]:
    head_coordinates_ = [(1, 1)]
    for i, instruction in enumerate(instructions):
        step_coordinates = []
        last_position = head_coordinates_[-1]
        direction = instruction[0]
        steps = int(instruction[1:])
        for step in range(steps):
            if direction == "R":
                last_position = (last_position[0] + 1, last_position[1])
            if direction == "L":
                last_position = (last_position[0] - 1, last_position[1])
            if direction == "U":
                last_position = (last_position[0], last_position[1] + 1)
            if direction == "D":
                last_position = (last_position[0], last_position[1] - 1)
            step_coordinates.append(last_position)
        head_coordinates_.extend(step_coordinates)
    return head_coordinates_


def generate_tail_coordinates(head_coord: list[tuple[int, int]]) -> list[tuple[int, int]]:
    tail_coordinates_ = [(1, 1)]
    for i, head in enumerate(head_coord):
        last_position = tail_coordinates_[-1]
        if i == 0:
            continue

        if math.hypot(head[0] - last_position[0], head[1] - last_position[1]) > MAX_DISTANCE:
            if head[0] > last_position[0]:
                last_position = (last_position[0] + 1, last_position[1])
            if head[0] < last_position[0]:
                last_position = (last_position[0] - 1, last_position[1])
            if head[1] > last_position[1]:
                last_position = (last_position[0], last_position[1] + 1)
            if head[1] < last_position[1]:
                last_position = (last_position[0], last_position[1] - 1)
        tail_coordinates_.append(last_position)
    return tail_coordinates_


if __name__ == "__main__":

    head_instructions = get_data_into_lines()

    head_coordinates = generate_head_coordinates(instructions=head_instructions)
    tail_coordinates = generate_tail_coordinates(head_coord=head_coordinates)
    print(f"part 1 {len(set(tail_coordinates))}")  # Part 1: 5907

    tail_cords = []
    for _ in range(8):
        tail_coordinates = generate_tail_coordinates(head_coord=tail_coordinates)
    print(f"part 2 {len(set(tail_coordinates))}")  # Part 2: 2303
