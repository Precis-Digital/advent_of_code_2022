import pathlib


def get_cleaning_schema(path: str) -> list[str]:
    return pathlib.Path(path).read_text().split("\n")


def ranges_are_sub_ranges(range_1: range, range_2) -> int:
    if range_1.start in range_2 and range_1[-1] in range_2:
        return 1
    elif range_2.start in range_1 and range_2[-1] in range_1:
        return 1
    else:
        return 0


def ranges_overlap(range_1: range, range_2) -> int:
    if set(range_1).intersection(range_2):
        return 1
    else:
        return 0


def generate_elf_pairs_task_range(cleaning_pair: str) -> dict:
    elfs_range = {}
    for i, tasks in enumerate(cleaning_pair.split(",")):
        tasks = tasks.split("-")
        elfs_range[f"elf{i + 1}"] = range(int(tasks[0]), int(tasks[1]) + 1)
    return elfs_range


if __name__ == "__main__":
    cleaning_schema = get_cleaning_schema("erica/day_4/input_data.txt")
    elf_pairs_tasks_range = [
        generate_elf_pairs_task_range(cleaning_pair=pair) for pair in cleaning_schema
    ]

    part_1 = 0
    part_2 = 0
    for elf_ranges in elf_pairs_tasks_range:
        part_1 += ranges_are_sub_ranges(
            range_1=elf_ranges["elf1"], range_2=elf_ranges["elf2"]
        )
        part_2 += ranges_overlap(range_1=elf_ranges["elf1"], range_2=elf_ranges["elf2"])

    print(part_1)  # part 1: 471
    print(part_2)  # part 2: 888
