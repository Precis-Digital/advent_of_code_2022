from typing import Tuple

STACK_ROW_POSITIONS = range(1, 500, 4)
STACK_COLUMNS = range(1, 10)

STACK_DICT = {col: STACK_ROW_POSITIONS[col - 1] for col in STACK_COLUMNS}


def get_input(file_name: str) -> Tuple[list[dict], list[dict]]:
    with open(file_name) as f:
        stacks = []
        procedures = []
        for line in f.readlines():
            if line == "\n":
                continue
            elif "[" in line:
                line_pos = {}
                for col, pos in STACK_DICT.items():
                    if pos < len(line):
                        line_pos[col] = line[pos]
                stacks.append(line_pos)
            elif line.startswith("move"):
                procedure = line.split()
                procedure_dict = {}
                for i, l in enumerate(procedure):
                    if i % 2 == 0:
                        procedure_dict[l] = procedure[i + 1]
                procedures.append(procedure_dict)
        return stacks, procedures


def stacks_from_row_to_columns(stacks: list[dict]) -> dict:
    columnar_store = {}
    for col in STACK_COLUMNS:
        columnar_store[col] = []
        for row in stacks:
            columnar_store[col].append(row.get(col, " "))
    for k, v in columnar_store.items():
        columnar_store[k] = [val for val in v if val != " "]
    return columnar_store


def rearrange(
    columnar_stacks: dict, procedures: list[dict], crate_mover="CrateMover9000"
) -> dict:
    for procedure in procedures:
        move_from = columnar_stacks[int(procedure["from"])]
        move_to = columnar_stacks[int(procedure["to"])]
        max_steps = int(procedure["move"])
        if crate_mover == "CrateMover9000":
            step = 0
            while step < max_steps:
                move_to.insert(0, move_from.pop(0))
                columnar_stacks[int(procedure["from"])] = move_from
                columnar_stacks[int(procedure["to"])] = move_to
                step += 1
        else:
            columnar_stacks[int(procedure["from"])] = move_from[max_steps:]
            columnar_stacks[int(procedure["to"])] = (
                move_from[0:max_steps] + columnar_stacks[int(procedure["to"])]
            )
    return columnar_stacks


def main():
    stacks, procedures = get_input("erica/day_05/input_data.txt")
    columnar_stacks = stacks_from_row_to_columns(stacks=stacks)
    rearranged_stacks = rearrange(
        columnar_stacks=columnar_stacks, procedures=procedures
    )
    part_1 = "".join([crate[0] for crate in rearranged_stacks.values() if crate])
    print(f"part 1: {part_1}")  # part 1: FRDSQRRCD

    rearranged_stacks = rearrange(
        columnar_stacks=columnar_stacks,
        procedures=procedures,
        crate_mover="CrateMover9001",
    )
    part_2 = "".join([crate[0] for crate in rearranged_stacks.values() if crate])
    print(f"part 2: {part_2}")  # part 2: HRFTQVWNN


if __name__ == "__main__":
    main()
