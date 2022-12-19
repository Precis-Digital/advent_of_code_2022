import dataclasses
import itertools

from shared import utils

BLOW_X_CHANGE_MAP = {"<": -1, ">": 1}
X_MIN, X_MAX = 0, 6
Y_MIN = 0

Point = tuple[int, int]


@dataclasses.dataclass(slots=True)
class CycleCandidate:
    length: int
    delta_y: int
    next_max_y: int
    next_rocks_dropped: int


@dataclasses.dataclass(slots=True)
class SeenCombo:
    max_y: int
    rocks_dropped: int


class Chamber:
    def __init__(self, jet_pattern: str) -> None:
        self.jet_pattern = itertools.cycle(enumerate(jet_pattern))
        self.chamber = set()
        self.rock_pattern = None
        self.max_y = 0
        self.rocks_dropped = 0
        self.rock_id = 0
        self.jet_id = 0
        self.cycle_length = None
        self.cycle_delta_y = None
        self.cycle_candidates = {}
        self.seen_combos = {}
        self.cycle_detected = False
        self.skipped = False
        self.skipped_y = 0

    @property
    def combo_id(self):
        return self.rock_id, self.jet_id

    def horizontal_rock(self) -> set[Point]:
        return {
            (2, self.max_y + 4),
            (3, self.max_y + 4),
            (4, self.max_y + 4),
            (5, self.max_y + 4),
        }

    def plus_rock(self) -> set[Point]:
        return {
            (3, self.max_y + 6),
            (2, self.max_y + 5),
            (3, self.max_y + 5),
            (4, self.max_y + 5),
            (3, self.max_y + 4),
        }

    def l_rock(self) -> set[Point]:
        return {
            (4, self.max_y + 6),
            (4, self.max_y + 5),
            (2, self.max_y + 4),
            (3, self.max_y + 4),
            (4, self.max_y + 4),
        }

    def verital_rock(self) -> set[Point]:
        return {
            (2, self.max_y + 7),
            (2, self.max_y + 6),
            (2, self.max_y + 5),
            (2, self.max_y + 4),
        }

    def square_rock(self) -> set[Point]:
        return {
            (2, self.max_y + 5),
            (3, self.max_y + 5),
            (2, self.max_y + 4),
            (3, self.max_y + 4),
        }

    def initialize_rock_pattern(self) -> None:
        self.rock_pattern = itertools.cycle(
            enumerate(
                [
                    self.horizontal_rock,
                    self.plus_rock,
                    self.l_rock,
                    self.verital_rock,
                    self.square_rock,
                ]
            )
        )

    def get_next_rock(self) -> set[Point]:
        self.rock_id, next_rock = next(self.rock_pattern)
        return next_rock()

    def get_next_jet_direction(self) -> str:
        self.jet_id, next_jet_direction = next(self.jet_pattern)
        return next_jet_direction

    def blow(self, rock_coords: set[Point]) -> set[Point]:
        delta_x = BLOW_X_CHANGE_MAP[self.get_next_jet_direction()]
        next_position = {(x + delta_x, y) for x, y in rock_coords}

        if self.valid_position(coords=next_position):
            return next_position
        return rock_coords

    def fall(self, rock_coords: set[Point]) -> tuple[set[Point], bool]:
        next_position = {(x, y - 1) for x, y in rock_coords}

        if self.valid_position(coords=next_position):
            return next_position, False
        return rock_coords, True

    def valid_position(self, coords: set[Point]) -> bool:
        return all(X_MIN <= x <= X_MAX and y > Y_MIN for x, y in coords) and not (
            coords & self.chamber
        )

    def drop_rock(self, coords: set[Point]) -> None:
        next_coords = coords
        stopped = False
        while not stopped:
            next_coords = self.blow(rock_coords=next_coords)
            next_coords, stopped = self.fall(rock_coords=next_coords)

            if stopped:
                self.update_max_y(coords=next_coords)
                self.chamber.update(next_coords)
                self.increment_rock_count()

                if not self.cycle_detected:
                    self.run_cycle_detection()

    def run_cycle_detection(self) -> None:
        if self.combo_id in self.cycle_candidates:
            self.check_if_cycle()

        if self.combo_id in self.seen_combos and not self.cycle_detected:
            self.add_cycle_candidate()
        else:
            self.seen_combos[self.combo_id] = SeenCombo(
                max_y=self.max_y, rocks_dropped=self.rocks_dropped
            )

    def check_if_cycle(self) -> None:
        cycle_candidate = self.cycle_candidates[self.combo_id]
        if (
            self.max_y == cycle_candidate.next_max_y
            and self.rocks_dropped == cycle_candidate.next_rocks_dropped
        ):
            self.cycle_detected = True
            self.cycle_delta_y = cycle_candidate.delta_y
            self.cycle_length = cycle_candidate.length

    def add_cycle_candidate(self) -> None:
        seen_combo = self.seen_combos[self.combo_id]
        length = self.rocks_dropped - seen_combo.rocks_dropped
        delta_y = self.max_y - seen_combo.max_y
        self.cycle_candidates[self.combo_id] = CycleCandidate(
            length=length,
            delta_y=delta_y,
            next_max_y=delta_y + self.max_y,
            next_rocks_dropped=length + self.rocks_dropped,
        )

    def update_max_y(self, coords: set[Point]) -> None:
        if (rock_max_y := max(y for _, y in coords)) > self.max_y:
            self.max_y = rock_max_y

    def increment_rock_count(self) -> None:
        self.rocks_dropped += 1

    def skip_ahead(self, nr_of_rocks: int) -> None:
        nr_of_repeats = (nr_of_rocks - self.rocks_dropped) // self.cycle_length

        self.skipped_y = nr_of_repeats * self.cycle_delta_y
        self.rocks_dropped += nr_of_repeats * self.cycle_length
        self.skipped = True

    def simulate_rocks_falling(self, nr_of_rocks: int) -> None:
        while self.rocks_dropped < nr_of_rocks:
            if self.cycle_detected and not self.skipped:
                self.skip_ahead(nr_of_rocks=nr_of_rocks)

            self.drop_rock(coords=self.get_next_rock())

        self.max_y += self.skipped_y


def main() -> None:
    jet_pattern = utils.read_input_to_string()

    rock_chamber = Chamber(jet_pattern=jet_pattern)
    rock_chamber.initialize_rock_pattern()
    rock_chamber.simulate_rocks_falling(nr_of_rocks=2022)

    height_after_2022 = rock_chamber.max_y

    rock_chamber = Chamber(jet_pattern=jet_pattern)
    rock_chamber.initialize_rock_pattern()
    rock_chamber.simulate_rocks_falling(nr_of_rocks=1_000_000_000_000)

    height_after_1_000_000_000_000 = rock_chamber.max_y

    print(f"Part 1: {height_after_2022}")
    print(f"Part 2: {height_after_1_000_000_000_000}")


if __name__ == "__main__":
    main()
