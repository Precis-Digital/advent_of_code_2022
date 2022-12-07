import pathlib


def get_stream(path: str) -> str:
    return pathlib.Path(path).read_text()


def find_marker(stream: str, unique_char: int) -> int:
    for i, letter in enumerate(stream[unique_char - 1:]):
        if len(set(stream[i:i+unique_char])) == unique_char:
            return i + unique_char


if __name__ == "__main__":

    elf_stream = get_stream("erica/day_6/input_data.txt")
    part_1 = find_marker(stream=elf_stream, unique_char=4)
    print(f"part 1: {part_1}")  # Part1 : 1598
    part_2 = find_marker(stream=elf_stream, unique_char=14)
    print(f"part 2: {part_2}")  # Part 2: 2414
