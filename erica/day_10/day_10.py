CYCLE_TIME = {"noop": 1, "addx": 2}


def get_data_into_lines() -> list[str]:
    with open("erica/day_10/input_data.txt") as f:
        line_rows = f.readlines()
        return [line_rows.strip() for line_rows in line_rows]


def get_signal_value_for_each_signal(signals: list[str]) -> dict[str:int]:
    signal_indexes = []
    signal_val = {}
    x = 1
    for i, signal in enumerate(signals):
        if i == 0:
            start = 1
        else:
            start = signal_indexes[i - 1]

        end = start + CYCLE_TIME[signal.split()[0]]
        signal_indexes.append(end)

        for j in range(start, end):
            if j == 0:
                continue
            else:
                signal_val[j] = x

        if signal.split()[0] == "addx":
            x += int(signal.split()[1])
        signal_val[end] = x

    return signal_val


def ctr(signals):
    x = 1
    cycles = 0
    pixels = []

    def pixel_value():
        pos = (cycles - 1) % 40
        if pos in [x - 1, x, x + 1]:
            pixels.append("#")
        else:
            pixels.append(".")

    for signal in signals:
        cycles += 1
        pixel_value()
        if signal.startswith("addx"):
            cycles += 1
            pixel_value()
            x += int(signal.split()[1])
    return pixels


if __name__ == "__main__":
    signal_lines = get_data_into_lines()

    cycle_step_values = get_signal_value_for_each_signal(signals=signal_lines)

    sum_signal_strength = 0
    for r in range(20, max(sorted(cycle_step_values.keys())), 40):
        sum_signal_strength += cycle_step_values[r] * r
    print(f"part 1 {sum_signal_strength}")  # Part 1: 13440

    sprite_pixels = ctr(signals=signal_lines)
    for pixel in range(
        0, max(sorted(cycle_step_values.keys())), 40
    ):  # part 2: PBZGRAZA
        print(" ".join(sprite_pixels[pixel: pixel + 40]))
