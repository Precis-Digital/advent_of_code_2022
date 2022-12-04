import os


def get_data(file_name: str) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    with open(file_name) as f:
        output = []
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            e1, e2 = line.split(",")
            range1 = tuple(map(int, e1.split("-")))
            range2 = tuple(map(int, e2.split("-")))
            output.append((range1, range2))
        return output


def solution1(data: list[tuple[tuple[int, ...], tuple[int, ...]]]) -> int:
    # the idea is that if one range is fully contained inside another range than the range
    # of the container must be <= to the lower bound and >= to the upper bound of the inner range

    overlap_counter = 0
    for e1, e2 in data:
        x1, y1 = e1
        x2, y2 = e2
        x_min = min(x1, x2)
        y_max = max(y1, y2)
        if e1 == (x_min, y_max) or e2 == (x_min, y_max):
            overlap_counter += 1
    return overlap_counter


def solution2(data: list[tuple[tuple[int, ...], tuple[int, ...]]]) -> int:
    # first sort the ranges by the lower bound
    # an overlap occurs if the lower bound of the next range is <= to the upper bound of the previous range
    overlap_counter = 0
    for e1, e2 in data:
        sorted_ranges = sorted([e1, e2])
        largest_lower_bound = sorted_ranges[1][0]
        upper_bound_of_range_with_smallest_lower_bound = sorted_ranges[0][1]
        if largest_lower_bound <= upper_bound_of_range_with_smallest_lower_bound:
            overlap_counter += 1
    return overlap_counter


if __name__ == "__main__":
    file_name = os.path.join("inputs", "day-4-input.txt")
    data = get_data(file_name=file_name)
    print("solution 1:", solution1(data=data))
    print("solution 2:", solution2(data=data))
