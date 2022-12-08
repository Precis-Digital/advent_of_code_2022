def get_data_into_lines() -> list[str]:
    with open("erica/day_7/input_data.txt") as f:
        line_rows = f.readlines()
        return line_rows


def get_file_structure_from_terminal_lines(lines: list[str]) -> dict:
    path = []
    file_structure = {}
    for line in lines:
        if line == "$ cd ..\n":
            path.pop()
        elif line.startswith('$ cd'):
            path.append(line.split()[-1])
            if "/".join(path) not in file_structure:
                file_structure['/'.join(path)] = 0
        elif line[0].isdigit():
            size = int(line.split()[0])
            pwd = []
            for sub_dir in path:
                pwd.append(sub_dir)
                file_structure['/'.join(pwd)] = file_structure['/'.join(pwd)] + size
    return file_structure


def find_smallest_file_to_delete(file_structure: dict) -> str:
    max_size = max(file_structure.values())
    current_space = 70000000 - max_size
    list_of_files_large_enough = []
    for v in file_structure.values():
        if current_space + v >= 30000000:
            list_of_files_large_enough.append(v)
    return min(list_of_files_large_enough)


def total_size_of_files_smaller_than_10000(file_structure: dict) -> int:
    return sum([v for v in file_structure.values() if v < 100000])


if __name__ == "__main__":
    terminal_lines = get_data_into_lines()
    directory_tree = get_file_structure_from_terminal_lines(lines=terminal_lines)

    total_size = total_size_of_files_smaller_than_10000(file_structure=directory_tree)
    file_size = find_smallest_file_to_delete(file_structure=directory_tree)

    print(f"part 1 {total_size}")  # Part 1: 1783610
    print(f"part 2 {file_size}")  # Part 1: 4370655
