

def get_program(fname: str) -> list[tuple[str, int]]:
    """Reads a program from a file and returns a list of tuples (instruction, value)"""
    program = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if line == "noop":
                program.append(("noop", 0))
            else:
                instruction, value = line.split()
                program.append((instruction, int(value)))
    return program

def run_program(program: list[tuple[str, int]]) -> list[tuple[int, int]]:
    output = []
    cycle_time = 0
    X = 1
    output.append((cycle_time, X))
    for instruction, value in program:
        if instruction == "noop":
            cycle_time += 1
            output.append((cycle_time, X))
        elif instruction == "addx":
            cycle_time += 2
            X += value

            output.append((cycle_time, X))

    return output

def solution1(program_output: list[tuple[int, int]]) -> int:
    "just brute force it :) "

    total = 0
    for cycle_time in range(20, 221, 40):
        nearest = sorted(list(filter(lambda x: x[0] < cycle_time, program_output)), reverse=True)[0]
        # print(f"cycle_time: {cycle_time}", nearest)
        total += cycle_time * nearest[1]
    return total

def solution2(program: list[tuple[str, int]]):
    i = 1
    sprite_position = 1
    crt = ""
    crt_pointer = 0
    while program:
        instruction, value = program.pop(0)
        print(instruction, value)
        ts = 2 if instruction == "addx" else 1

        for _ in range(ts):
            if crt_pointer in (sprite_position - 1, sprite_position, sprite_position + 1):
                crt += "#"
            else:
                crt += "."
            crt_pointer += 1
            crt_pointer = crt_pointer % 40
        sprite_position += value

    for i in range(0, 240, 40):
        print(crt[i : i + 40])

    


if __name__ == "__main__":
    program = get_program("inputs/day-10-sample.txt")
    po = run_program(program=program)
    assert solution1(program_output=po) == 13140
    solution2(program=program)

    ########################################

    program = get_program("inputs/day-10-input.txt")
    po = run_program(program=program)
    assert solution1(program_output=po) == 12880
    solution2(program=program)