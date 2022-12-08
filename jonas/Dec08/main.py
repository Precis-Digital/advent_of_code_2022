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
    num_rows = 0
    num_cols = 0
    tree_map = {}
    with open(file_name, "r") as f:
        trees = f.readlines()
        num_cols = len(trees)
        for i, row in enumerate(trees):
            num_rows = len(row)
            for j, tree_height in enumerate(row.strip()):
                tree_map[(j,i)] = Tree(int(tree_height), j, i)
    
    tree_map = add_height_to_trees(tree_map, num_rows, num_cols)
    return tree_map

def calc_direction_visibility_and_score(direction: str, tree: Tree, tree_map: dict[tuple[int, int], Tree], num_rows: int, num_cols: int) -> tuple[bool, int]:
    i = 1
    is_visible = True
    scenic_score = 0

    def test_while_condition(direction: str, x: int, y: int, i: int, num_rows: int, num_cols: int) -> bool:
        match direction:
            case "north":
                return y - i >= 0
            case "west":
                return x - i >= 0
            case "south":
                return y + i < num_rows
            case "east":
                return x + i < num_cols
    
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

    while test_while_condition(direction, tree.x, tree.y, i, num_rows, num_cols):
        next_tree = tree_map.get(get_next_cords(direction, tree.x, tree.y, i))
        if next_tree.height >= tree.height:
            is_visible = False
            scenic_score = i
            break
        i += 1
    else:
        scenic_score = i - 1

    return is_visible, scenic_score


def add_height_to_trees(tree_map: dict[tuple[int, int], Tree], num_rows: int, num_cols: int) -> dict[tuple[int, int], Tree]:
    for tree in tree_map.values():

        north_visible, north_scenic_score = calc_direction_visibility_and_score("north", tree, tree_map, num_rows, num_cols)
        east_visible, east_scenic_score = calc_direction_visibility_and_score("east", tree, tree_map, num_rows, num_cols)
        south_visible, south_scenic_score = calc_direction_visibility_and_score("south", tree, tree_map, num_rows, num_cols)
        west_visible, west_scenic_score = calc_direction_visibility_and_score("west", tree, tree_map, num_rows, num_cols)

        tree.is_visible = north_visible or east_visible or south_visible or west_visible
        tree.scenic_score = north_scenic_score * east_scenic_score * south_scenic_score * west_scenic_score

    return tree_map


# Sample 1 - 21
print(len([tree for tree in get_trees("sample_input.txt").values() if tree.is_visible]))

# Part 1 - 1700
print(len([tree for tree in get_trees("input.txt").values() if tree.is_visible]))

# Sample 2 - 8
print(max([tree.scenic_score for tree in get_trees("sample_input.txt").values()]))

# Part 2 - 470596
print(max([tree.scenic_score for tree in get_trees("input.txt").values()]))