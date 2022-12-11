class Command:
    command: str
    def __init__(self, command: str) -> "Command":
        self.command = command
    
    def __repr__(self) -> str:
        return self.command
    
    @property
    def type(self) -> str:
        if self.command.startswith("noop"):
            return "noop"
        else:
            return "addx"
    
    @property
    def value(self) -> int:
        if self.type == "addx":
            return int(self.command.split(" ")[1])
    
    @property
    def cycles(self) -> int:
        if self.type == "noop":
            return 1
        return 2

class ProgramInterface:
    commands: list[Command]
    register_x: int = 1
    cycle_counter: int = 0
    during_cycle_values: dict[int, int]
    after_cycle_values: dict[int, int]
    CRT_rows: list[list[str]]
    def __init__(self, commands: list[Command]):
        self.commands = commands
        self.during_cycle_values = {}
        self.after_cycle_values = {}
        self.CRT_rows = [["" for _ in range(40)] for _ in range(6)]

    def run_program(self):
        for command in self.commands:
            if command.type == "noop":
                self.cycle_counter += 1
                self._update_cycle_values("during")
                self._update_cycle_values("after")
            
            if command.type == "addx":
                self.cycle_counter += 1
                self._update_cycle_values("during")
                self._update_cycle_values("after")
                self.cycle_counter += 1
                self._update_cycle_values("during")
                self.register_x += command.value
                self._update_cycle_values("after")
    
    def _update_cycle_values(self, cycle_section: str) -> None:
        if cycle_section == "during":
            self._add_crt_symbol()
            self.during_cycle_values[self.cycle_counter] = self.signal_strength
        else:
            self.after_cycle_values[self.cycle_counter] = self.signal_strength

    @property
    def signal_strength(self) -> int:
        return self.register_x * self.cycle_counter

    def _add_crt_symbol(self) -> None:
        target_row = int(str(self.cycle_counter/40)[0])
        target_col = (self.cycle_counter - 1) % 40
        if target_col == 39:
            target_row -= 1

        symbol = "."

        for num in range(self.register_x - 1,self.register_x + 2):
            if num == target_col:
                symbol = "#"
                break
        
        self.CRT_rows[target_row][target_col] = symbol


def get_commands(file_name: str) -> list[Command]:
    with open(file_name, "r") as f:
        return [Command(row.strip()) for row in f.readlines()]

def get_signal_strengths_at_increments(commands: list[Command], start_num: int, step_size: int):
    program_interface = ProgramInterface(commands=commands)
    program_interface.run_program()

    return sum([program_interface.during_cycle_values[step] for step in range(start_num, program_interface.cycle_counter, step_size)])

def draw_sprite_from_program(commands: list[Command]) -> None:
    program_interface = ProgramInterface(commands=commands)
    program_interface.run_program()

    for row in program_interface.CRT_rows: print("".join(row))


# Sample 1 - 13140
print(get_signal_strengths_at_increments(get_commands("sample_input.txt"), 20, 40))

# Part 1 - 17380
print(get_signal_strengths_at_increments(get_commands("input.txt"), 20, 40))

# Sample 2
draw_sprite_from_program(get_commands("sample_input.txt"))
"""
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""

# Part 2 - FGCUZREC
draw_sprite_from_program(get_commands("input.txt"))
"""
####..##...##..#..#.####.###..####..##..
#....#..#.#..#.#..#....#.#..#.#....#..#.
###..#....#....#..#...#..#..#.###..#....
#....#.##.#....#..#..#...###..#....#....
#....#..#.#..#.#..#.#....#.#..#....#..#.
#.....###..##...##..####.#..#.####..##..
"""
