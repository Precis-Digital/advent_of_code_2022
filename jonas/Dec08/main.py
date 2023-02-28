import time
import timeit


class Tree:
    height: int
    x: int
    y: int
    is_visible: bool = True
    scenic_score: int = 0

    def __init__(self, height: int, x: int, y: int) -> "Tree":
        self.height = height
        self.x = x
        self.y = y
    
    def __repr__(self):
        return str(self.__dict__)

def get_trees(file_name: str) -> dict[tuple[int, int], Tree]:
    tree_map = {}
    with open(file_name, "r") as f:
        trees = f.readlines()
        for i, row in enumerate(trees):
            for j, tree_height in enumerate(row.strip()):
                tree_map[(j,i)] = Tree(int(tree_height), j, i)
    
    tree_map = parse_trees(tree_map)
    return tree_map

def parse_trees(tree_map: dict[tuple[int, int], Tree]) -> dict[tuple[int, int], Tree]:
    for tree in tree_map.values():

        north_visible, north_scenic_score = calc_direction_visibility_and_score("north", tree, tree_map)
        east_visible, east_scenic_score = calc_direction_visibility_and_score("east", tree, tree_map)
        south_visible, south_scenic_score = calc_direction_visibility_and_score("south", tree, tree_map)
        west_visible, west_scenic_score = calc_direction_visibility_and_score("west", tree, tree_map)

        tree.is_visible = north_visible or east_visible or south_visible or west_visible
        tree.scenic_score = north_scenic_score * east_scenic_score * south_scenic_score * west_scenic_score

    return tree_map

COUNTER = 0

def calc_direction_visibility_and_score(direction: str, tree: Tree, tree_map: dict[tuple[int, int], Tree]) -> tuple[bool, int]:
    # global COUNTER


    i = 1
    is_visible = True
    scenic_score = 0
    
    def get_next_cords(direction: str, x: int, y:int, i: int) -> tuple[int, int]:
        match direction:
            case "north":
                return (x, y - i)
            case "west":
                return (x - i, y)
            case "south":
                return (x, y + i)
            case "east":
                return (x+i, y)

    while tree_map.get(get_next_cords(direction, tree.x, tree.y, i)):
        next_tree = tree_map.get(get_next_cords(direction, tree.x, tree.y, i))
        # COUNTER += 1
        if next_tree.height >= tree.height:
            is_visible = False
            scenic_score = i
            break
        i += 1
    else:
        scenic_score = i - 1

    return is_visible, scenic_score

# Sample 1 - 21
# print(len([tree for tree in get_trees("sample_input.txt").values() if tree.is_visible]))

# Part 1 - 1700
def large_input():
    print(len([tree for tree in get_trees("/Users/malikwoods/Developer/advent_of_code_2022/malik/inputs/day-8-large.txt").values() if tree.is_visible]))
    # print(max([tree.scenic_score for tree in get_trees("/Users/malikwoods/Developer/advent_of_code_2022/malik/inputs/day-8-large.txt").values()]))

print('JB: timeit', timeit.timeit(large_input, number=10)/10)

# # Sample 2 - 8
# print(max([tree.scenic_score for tree in get_trees("sample_input.txt").values()]))
#
# # Part 2 - 470596
# print(max([tree.scenic_score for tree in get_trees("input.txt").values()]))

