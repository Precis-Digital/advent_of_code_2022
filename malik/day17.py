from dataclasses import dataclass

# defines the relative shape of each rock
# line of 4 boxes
ROCK1 = [(0, 0), (1, 0), (2, 0), (3, 0)]

# plus sign
ROCK2 = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]

# revers L
ROCK3 = [(2, 0), (2, 1), (0,2), (1, 2), (2, 2)]

# staigh line down
ROCK4 = [(0, 0), (0, 1), (0, 2), (0, 3)]

# Square
ROCK5 = [(0, 0), (1, 0), (0, 1), (1, 1)]


@dataclass
class Rock:
    x: int
    y: int
    shape: list[tuple[int, int]]
    occupied_spaces: set[tuple[int, int]] # representation of height map of floor
    stopped: bool = False
    min_x: int = 0
    max_x: int = 6

    def get_shape(self) -> list[tuple[int, int]]:
        return self.shape

    def move(self, x: int, y: int):
        self.x += x
        self.y += y

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def move_down(self):
        self.move(0, 1)

    def get_current_position_shape(self) -> list[tuple[int, int]]:
        return [(x + self.x, y + self.y) for x, y in self.shape]



def simulation():

    rock_templates = [ROCK1, ROCK2, ROCK3, ROCK4, ROCK5]
    occupied_spaces = set((x, 0) for x in range(7))
    print(occupied_spaces)
    for i in range(20):
        pass