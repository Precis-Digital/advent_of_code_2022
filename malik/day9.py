from dataclasses import dataclass

@dataclass
class Rope:
    """ assumes position is (row, column)"""
    num_knots: int
    knot_positions: list[tuple[int, int]] = None
    prior_positions: list[tuple[int, int]] = None
    tail_positions: set[tuple[int, int]] = None

    def init_positions(self):
        self.knot_positions = [(0,0) for _ in range(self.num_knots)]
        self.prior_positions = [(0, 0) for _ in range(self.num_knots)]

    def update_head(self,action: str, value: int):
        if action == "R":
            self.knot_positions[0] = (self.knot_positions[0][0] + value, self.knot_positions[0][1])
        elif action == "L":
            self.knot_positions[0] = (self.knot_positions[0][0] - value, self.knot_positions[0][1])
        elif action == "U":
            self.knot_positions[0] = (self.knot_positions[0][0], self.knot_positions[0][1] + value)
        elif action == "D":
            self.knot_positions[0] = (self.knot_positions[0][0], self.knot_positions[0][1] - value)

    def update_positions(self):
        # print(self.knot_positions, self.prior_positions)
        for i in range(1, self.num_knots):
            hr, hc = self.knot_positions[(i-1)]
            tr, tc = self.knot_positions[i]
            delta_r = hr - tr
            delta_c = hc - tc
            # print(hr, hc, tr, tc, delta_r, delta_c)
            # if the distance is sufficient update the position
            if abs(delta_r) > 1 or abs(delta_c) > 1:
                move_r = delta_r // abs(delta_r) if delta_r != 0 else 0
                move_c = delta_c // abs(delta_c) if delta_c != 0 else 0
                self.knot_positions[i] = (tr + move_r, tc + move_c)



        if self.tail_positions is None:
            self.tail_positions = set()
        self.tail_positions.add(self.knot_positions[-1])


def get_movements(fname: str) -> list[tuple[str, int]]:
    """Read movements from file"""
    with open(fname, "r") as f:
        output = []
        for line in f.readlines():
            action, value = line.strip().split(" ")
            value = int(value)
            output.append((action, value))
        return output


def solution1(movements: list[tuple[str, int]]) -> int:

    rope = Rope(num_knots=2)
    rope.init_positions()
    for movement in movements:
        action, value = movement
        for _ in range(value):
            rope.update_head(action, 1)
            rope.update_positions()
            # print(rope.knot_positions[0], rope.knot_positions[-1])
    return len(rope.tail_positions)


def solution2(movements: list[tuple[str, int]]) -> int:

    rope = Rope(num_knots=10)
    rope.init_positions()
    for movement in movements:
        action, value = movement
        for _ in range(value):
            rope.update_head(action, 1)
            rope.update_positions()
            # print("HT", rope.knot_positions[0], rope.knot_positions[1])
        # print(rope.knot_positions)
    # print(rope.tail_positions)
    return len(rope.tail_positions)

if __name__ == "__main__":
    mvmts = get_movements("inputs/day-9-sample.txt")
    assert solution1(mvmts) == 13
    assert solution2(mvmts) == 1

    mvmts = get_movements("inputs/day-9-sample-2.txt")
    assert solution2(mvmts) == 36

    mvmts = get_movements("inputs/day-9-input.txt")
    assert solution1(mvmts) == 6470
    assert solution2(mvmts) == 2658

