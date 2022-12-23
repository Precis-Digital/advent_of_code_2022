def get_jet_stream():
    with open("erica/day_17/input_data.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        lines = "".join(lines)
        streams = [stream for stream in lines]
        return streams


class RockTetris:
    def __init__(self, jet_streams):
        self.jet_streams = jet_streams
        self.jet_index = 0
        self.rock_index = 0
        self.chamber = set()
        self.height = 0
        self.rocks = self.get_rocks()
        self.y_min = 0
        self.x_min = 0
        self.x_max = 6

    @staticmethod
    def get_rocks():
        return {
            0: {
                (2, 4),
                (3, 4),
                (4, 4),
                (5, 4),
            },
            1: {
                (3, 6),
                (2, 5),
                (3, 5),
                (4, 5),
                (3, 4),
            },
            2: {
                (4, 6),
                (4, 5),
                (2, 4),
                (3, 4),
                (4, 4),
            },
            3: {
                (2, 7),
                (2, 6),
                (2, 5),
                (2, 4),
            },
            4: {
                (2, 5),
                (3, 5),
                (2, 4),
                (3, 4),
            },
        }

    def pos_is_ok(self, coords) -> bool:
        return all(self.x_min <= x <= self.x_max and y > self.y_min for x, y in coords) and not (
            coords & self.chamber
        )

    def jet_push(self, cords):
        """check if the jet stream can blow the rock"""
        if self.jet_index >= len(self.jet_streams):
            self.jet_index = 0
        jet_direction = self.jet_streams[self.jet_index]
        push = 1 if jet_direction == ">" else -1
        next_pos = {(x + push, y) for x, y in cords}
        self.jet_index += 1

        # check that next pos is in the board and not already in the chamber
        if self.pos_is_ok(next_pos):
            return next_pos
        else:
            return cords

    def fall(self, cords):
        next_pos = {(x, y - 1) for x, y in cords}
        if self.pos_is_ok(next_pos):
            return next_pos, False
        else:
            return cords, True

    def move_rock(self):
        """move the rock down the board until it hits the bottom or another rock"""
        rock = self.rocks[self.rock_index % 5]
        new_pos = {(x, y + self.height) for x, y in rock}
        stuck = False
        while not stuck:
            new_pos = self.jet_push(new_pos)
            new_pos, stuck = self.fall(new_pos)

            if stuck:
                self.chamber.update(new_pos)
                self.rock_index += 1
                max_y_in_round = max(y for _, y in new_pos)
                if max_y_in_round > self.height:
                    self.height = max_y_in_round


def part_1():
    tetris_game = RockTetris(get_jet_stream())

    for i in range(2022):
        tetris_game.move_rock()

    print(f"Part 1: {tetris_game.height}")  # 3197


if __name__ == "__main__":
    part_1()
