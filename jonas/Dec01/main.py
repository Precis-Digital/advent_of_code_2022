
def get_all_elfs_from_file(file_name: str) -> list[int]:
    with open(file_name, "r") as f:
        lines = f.readlines()

    all_elfs = []
    curr_elf = []

    for line in lines:
        if len(line) == 1:
            all_elfs.append(curr_elf)
            curr_elf = []
            continue
        curr_elf.append(int(line))

    return all_elfs

def get_max_n_sum_array(list_of_lists: list[list[int]], n) -> list[int]:
    max_array = [sum(row) for row in list_of_lists]

    sorted_array = sorted(max_array, reverse=True)

    return sorted_array[:n]

# Part 1
all_elfs = get_all_elfs_from_file("input01.txt")
max_1_array = get_max_n_sum_array(all_elfs, 1)
max_1_values_sum = sum(max_1_array)
print(f"Solution to Part1 = {max_1_values_sum}")

# Part 2
max_3_array = get_max_n_sum_array(all_elfs, 3)
max_3_values_sum = sum(max_3_array)
print(f"Solution to Part2 = {max_3_values_sum}")

