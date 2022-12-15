def get_path_cords():
    with open('erica/day_14/input_data.txt') as f:
        rows = [line.strip().split(" -> ") for line in f.readlines()]
        cave_cords = []
        for row in rows:
            row_cords = []
            for cord in row:
                row_cords.append(tuple(map(int, cord.split(","))))
            cave_cords.append(row_cords)
        return cave_cords


def get_cave_dimensions(scans):
    min_x = 0
    max_x = max_y = 0

    for scan in scans:
        x_pos = [pos[0] for pos in scan]
        max_x = max(max(x_pos), max_x)

        y_pos = [pos[1] for pos in scan]
        max_y = max(max(y_pos), max_y)

    return min_x, max_x, max_y


def set_stone(rock1, rock2, cave_, min_x):
    for x_pos in range(rock1[0], rock2[0] + 1):
        for y_pos in range(rock1[1], rock2[1] + 1):
            x = x_pos - min_x
            y = y_pos
            cave_[y][x] = '#'
    return cave_


def map_rock_paths(scans, cave_,  min_x):

    for scan in scans:
        for i in range(len(scan) - 1):
            rock1 = scan[i]
            rock2 = scan[i + 1]

            if rock1[0] > rock2[0] or rock1[1] > rock2[1]:
                cave_ = set_stone(rock2, rock1, cave_, min_x)
            else:
                cave_ = set_stone(rock1, rock2, cave_, min_x)

    return cave_


def create_cave(max_x, min_x, max_y, part2=False):
    empty_cave = []
    for y in range(0, max_y + 1):
        row = ['.'] * (max_x - min_x + 1)
        empty_cave.append(row)

    if part2:
        empty_cave.append(['#'] * (max_x - min_x + 1))

    return empty_cave


def sand_corn_path(cave_, start_x, start_y):
    """Sand corns fall down until they are blocked.
    If they cannot move down it will try to move diagonally down to the left first and then to the right"""
    sand_x = start_x
    sand_y = start_y

    pos1 = cave_[sand_y + 1][sand_x - 1]
    pos2 = cave_[sand_y + 1][sand_x]
    pos3 = cave_[sand_y + 1][sand_x + 1]
    if pos1 == 'O' and pos2 == 'O' and pos3 == 'O':
        if cave_[sand_y][sand_x] == '.':
            cave_[sand_y][sand_x] = 'O'
            return True
        else:
            return False

    while True:
        if sand_x < 0 or sand_x >= len(cave_[0]) or sand_y >= len(cave_):
            return False

        if sand_y == len(cave_) - 1 or cave_[sand_y + 1][sand_x] == '.':
            sand_y += 1
            continue

        if sand_x == 0 or cave_[sand_y + 1][sand_x - 1] == '.':
            sand_x -= 1
            sand_y += 1
            continue

        if sand_x == len(cave_) - 1 or cave_[sand_y + 1][sand_x + 1] == '.':
            sand_x += 1
            sand_y += 1
            continue

        break

    cave_[sand_y][sand_x] = 'O'
    return True


def pour_sand(cave_, min_x):
    sand_x_start = 500 - min_x
    sand_y_start = 0

    sand = 0
    sand_is_pouring = True
    while sand_is_pouring:
        sand_is_pouring = sand_corn_path(cave_, sand_x_start, sand_y_start)
        if not sand_is_pouring:
            break
        sand += 1
    return sand


def print_cave(cave_):
    for r in cave_:
        print(" ".join(r))


if __name__ == '__main__':
    scan_output = get_path_cords()
    x_min, x_max, y_max = get_cave_dimensions(scan_output)

    cave_dim = create_cave(x_max, x_min, y_max)
    cave = map_rock_paths(scan_output, cave_dim, x_min)
    sand_corns = pour_sand(cave, x_min)
    print(f"Part 1: {sand_corns}")  # part 1: 755

    infinite_width = 2 * y_max
    cave_dim = create_cave(x_max + infinite_width, x_min - infinite_width, y_max + 1, part2=True)
    cave = map_rock_paths(scan_output, cave_dim, x_min-infinite_width)
    sand_corns = pour_sand(cave, x_min - infinite_width)
    print(f"Part 2: {sand_corns}")  # part 2: 29805
