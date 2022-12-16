# regex to parse the integers from the input: "Sensor at x=20, y=1: closest beacon is at x=15, y=3"
import re
REGEX = r'x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'

def compute_manhattan_distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def compute_x_range_from_y_and_manhattan_distance(y, sensor_x, sensor_y,  manhattan_distance):
    # the distance to y is too far
    if abs(sensor_y - y) > manhattan_distance:
        return None

    net_distance = manhattan_distance - abs(y - sensor_y)

    return sensor_x - net_distance, sensor_x + net_distance

def get_data(fname: str) -> list[tuple[int, int, int, int, int]]:
    output = []
    with open(fname) as f:
        for line in f.readlines():
            line = line.strip()
            sensor_x, sensor_y, beacon_x, beacon_y = list(map(int, re.findall(REGEX, line)[0]))
            output.append((sensor_x, sensor_y, beacon_x, beacon_y, compute_manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)))
    return output

def get_merged_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges.sort(key=lambda x: x[0])
    merged_ranges = []

    for start, end in ranges:
        if not merged_ranges:
            merged_ranges.append((start, end))
        else:
            last_start, last_end = merged_ranges[-1]
            if start <= (last_end + 1):
                merged_ranges[-1] = (last_start, max(last_end, end))
            else:
                merged_ranges.append((start, end))
    return merged_ranges

def solution1(data: list[tuple[int, int, int, int, int]], y: int) -> int:
    ranges = []
    for sensor_x, sensor_y, beacon_x, beacon_y, distance in data:
        x: tuple[int, int] = compute_x_range_from_y_and_manhattan_distance(y, sensor_x, sensor_y, distance)
        # print(f'sensor_x={sensor_x}, sensor_y={sensor_y}: closest beacon is at x={beacon_x}, y={beacon_y}; distance={distance}')
        if x:
            ranges.append(x)

    merged_ranges = get_merged_ranges(ranges=ranges)
    ans = sum([end-start for start, end in merged_ranges])
    # print(merged_ranges, ans)
    return ans

def solution2(data, range_min = 0, range_max = 4000000):
    """ take about 1 second per 100K iterations"""
    for y in range(range_min, range_max):
        if y % 100000 == 0:
            print(f'processing y={y}')
        ranges = []
        for sensor_x, sensor_y, beacon_x, beacon_y, distance in data:
            x: tuple[int, int] = compute_x_range_from_y_and_manhattan_distance(y, sensor_x, sensor_y, distance)
            if x:
                ranges.append(x)
        # print(ranges)
        mr = get_merged_ranges(ranges=ranges)
        if len(mr) > 1:
            print((mr[0][1] + 1) * 4000000 + y)
            return (mr[0][1] + 1) * 4000000 + y


if __name__ == '__main__':
    data = get_data('inputs/day-15-sample.txt')
    assert solution1(data, y=10) == 26
    assert solution2(data, range_min=0, range_max=20) == 56000011

    data = get_data('inputs/day-15-input.txt')
    #assert solution1(data) == 26
    assert solution1(data, y=2000000) == 4748135
    assert solution2(data, range_min=0, range_max=4000000) == 13743542639657 # takes 30 seconds or so
