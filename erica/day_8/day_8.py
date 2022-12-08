import numpy as np


def get_data_into_list_of_lists() -> list[list[float]]:
    with open("erica/day_8/input_data.txt") as f:
        lines = f.readlines()
        return [[float(tree) for tree in line.strip()] for line in lines]


def compare_trees_in_forrest(forrest: np.array) -> int:
    trees = []
    for (x, y), value in np.ndenumerate(forrest):
        visible_vertically = tree_is_visible_vertically(forrest=forrest, index=(x, y), val=value)
        visible_horizontally = tree_is_visible_horizontally(forrest=forrest, index=(x, y), val=value)
        if visible_horizontally or visible_vertically:
            trees.append(1)

    return sum(trees)


def tree_is_visible_horizontally(forrest: np.array, index: tuple, val: float) -> bool:
    x, y = index
    if any(forrest[x, :y] >= val) and any(forrest[x, y + 1:] >= val):
        return False
    else:
        return True


def tree_is_visible_vertically(forrest: np.array, index: tuple[int, int], val: float) -> bool:
    x, y = index
    if any(forrest[:x, y] >= val) and any(forrest[x + 1:, y] >= val):
        return False
    else:
        return True


def on_boarder(forrest_shape, index):
    x, y = index
    if x == 0 or y == 0 or x == forrest_shape[0] - 1 or y == forrest_shape[1] - 1:
        return True


def view_steps(direction):
    if any(direction):
        max_left = np.where(direction)[0][0].tolist() + 1
    else:
        max_left = direction.size
    return max_left


def tree_views(forrest: np.array) -> int:
    trees = []
    for (x, y), value in np.ndenumerate(forrest):
        if not on_boarder(forrest_shape=forrest.shape, index=(x, y)):

            up = forrest[:x, y] >= value
            down = forrest[x + 1:, y] >= value
            left = forrest[x, :y] >= value
            right = forrest[x, y + 1:] >= value

            max_up = view_steps(direction=up[::-1])
            max_down = view_steps(direction=down)
            max_left = view_steps(direction=left[::-1])
            max_right = view_steps(direction=right)

            trees.append(max_down*max_up*max_left*max_right)

    return max(trees)


if __name__ == "__main__":
    tree_lines = get_data_into_list_of_lists()

    visible_trees = compare_trees_in_forrest(
        forrest=np.array(tree_lines)
    )
    print(f"part 1 {visible_trees}")  # Part 1: 1870
    highest_score = tree_views(forrest=np.array(tree_lines))
    print(f"part 2 {highest_score}")  # Part 2: 517440
