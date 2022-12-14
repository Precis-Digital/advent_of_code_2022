import timeit


def parse_data():
    with open('erica/day_13/input_data.txt') as f:
        lines = [lines.strip() for lines in f.readlines() if lines.strip()]
        return lines


def compare_pairs(a, b):

    if isinstance(a, int) and isinstance(b, int):
        return 1 if a < b else -1 if b < a else 0
    elif isinstance(a, int) and isinstance(b, list):
        return compare_pairs([a], b)
    elif isinstance(a, list) and isinstance(b, int):
        return compare_pairs(a, [b])
    else:
        len_a = len(a)
        for i, val in enumerate(b):
            if i + 1 > len_a:
                return 1
            compared = compare_pairs(a[i], val)
            if compared != 0:
                return compared
        if len(b) < len_a:
            return -1
        else:
            return 0


def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if compare_pairs(arr[j], arr[j + 1]) != 1:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def part1():
    data_lines = parse_data()
    packet_pairs = [(eval(data_lines[i]), eval(data_lines[i+1])) for i in range(0, len(data_lines), 2)]
    right_packages = [i + 1 for i, pair in enumerate(packet_pairs) if compare_pairs(pair[0], pair[1]) == 1]
    return sum(right_packages)


def part2():
    data_lines = parse_data()
    part_2_data = [eval(line) for line in data_lines] + [[[2]]] + [[[6]]]
    sorted_packages = bubble_sort(part_2_data)
    return (sorted_packages.index([[2]]) + 1) * (sorted_packages.index([[6]]) + 1)


if __name__ == '__main__':
    print(f"part 1: {part1()}")  # part 1: 6072
    print(f"part 2: {part2()}")  # part 2: 22184

    print(f"part1: {timeit.timeit(part1, number=100)/100}")
    print(f"part2: {timeit.timeit(part2, number=100)/100}")
