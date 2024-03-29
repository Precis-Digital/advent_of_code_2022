from shared import utils

CYCLES_TO_SAVE = [20 + 40 * i for i in range(6)]
CRT_WIDTH = 40

Program = list[str]


class CPU:
    def __init__(self) -> None:
        self.x_register = 1
        self.cycle = 0
        self.signal_stengths = []
        self.pixels = []

    def addx(self, v: int) -> None:
        for _ in range(2):
            self.increment_cycle()
        self.x_register += v

    def noop(self) -> None:
        self.increment_cycle()

    def save_signal_strength(self) -> None:
        self.signal_stengths.append(self.cycle * self.x_register)

    def crt_draws_on_sprite(self) -> bool:
        return abs(self.x_register - self.cycle % CRT_WIDTH) <= 1

    def draw(self) -> None:
        if self.crt_draws_on_sprite():
            self.pixels.append("#")
        else:
            self.pixels.append(".")

    def increment_cycle(self) -> None:
        self.draw()
        self.cycle += 1
        if self.cycle in CYCLES_TO_SAVE:
            self.save_signal_strength()

    def run(self, program: Program) -> None:
        for instruction in program:
            if instruction == "noop":
                self.noop()
            else:
                v = int(instruction.split()[-1])
                self.addx(v=v)

    def render_graphical_output(self) -> None:
        for row in utils.chunks(lst=self.pixels, n=CRT_WIDTH):
            print("".join(row))


def main() -> None:
    program = utils.read_input_to_string().splitlines()
    cpu = CPU()
    cpu.run(program=program)

    print(f"Part 1: {sum(cpu.signal_stengths)}")
    print("Part 2:")
    cpu.render_graphical_output()


if __name__ == "__main__":
    main()
