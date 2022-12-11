class Monkey:
    params: list[str]
    num: int
    items: list[int]
    operation: str
    divisible_by: int
    operation_operator: str
    operation_value: str
    if_true_monkey: int
    if_false_monkey: int
    test_results: tuple[str, str]
    inspection_counter: int = 0

    def __init__(self, monkey_params: str) -> "Monkey":
        self.params = monkey_params

        self.num = monkey_params[0].replace(":","").split(" ")[1]
        self.items = [int(item) for item in monkey_params[1].replace("Starting items: ", "").split(", ")]
        self.operation_operator = monkey_params[2].replace("Operation: new = old ", "").split(" ")[0]
        self.operation_value = monkey_params[2].replace("Operation: new = old ", "").split(" ")[1]
        self.divisible_by = int(monkey_params[3].replace("Test: divisible by ", ""))
        self.if_true_monkey = monkey_params[4].replace("If true: throw to monkey ", "")
        self.if_false_monkey = monkey_params[5].replace("If false: throw to monkey ", "")
    
    def get_target_monkey_and_new_value(self, item: int, worry_level_divisor: int, lcm: int):
        self.inspection_counter += 1
        if worry_level_divisor > 1:
            new_worry_level = rounddown(self._calculate_worry_level(item) / worry_level_divisor)
        else:
            new_worry_level = self._calculate_worry_level(item) % lcm
            
        if self.test_passes(new_worry_level):
            return self.if_true_monkey, new_worry_level
        else:
            return self.if_false_monkey, new_worry_level

    def _calculate_worry_level(self, prev_worry_level: int) -> int:
        if self.operation_value == "old":
            operation_value = prev_worry_level
        else:
            operation_value = int(self.operation_value)

        if self.operation_operator == "+":
            return operation_value + int(prev_worry_level)
        elif self.operation_operator == "*":
            return operation_value * int(prev_worry_level)
        else:
            raise Exception(f"Unknown operation operator '{self.operation_operator}'")

    def test_passes(self, item_worry_level: int) -> bool:
        return item_worry_level % self.divisible_by == 0

    def __repr__(self) -> str:
        return f"#{self.num} | Total inspections {self.inspection_counter} | Items: [{', '.join([str(item) for item in self.items])}] | Operation operator {self.operation_operator} | Operation value {self.operation_value} | Test Divisble by {self.divisible_by} | If true monkey {self.if_true_monkey} | If false monkey {self.if_false_monkey}"

def rounddown(num: int) -> int:
    """Simple rounddown of integers"""
    return int(str(num).split(".")[0])

def product(numbers: list[int]) -> int:
    """Simple product functions of list of integers"""
    val = 1
    for num in numbers:
        val *= num
    return val

def lcm(a: int, b: int) -> int:
    if a > b:
        greater = a
    else:
        greater = b
    while(True):
        if((greater % a == 0) and (greater % b == 0)):
            lcm = greater
            break
        greater += 1
    return lcm

def get_monkeys(file_name: str) -> list[Monkey]:
    with open(file_name, "r") as f:
        monkeys = []
        curr_monkey = []
        for row in f.readlines():
            if row.strip() != "":
                curr_monkey.append(row.strip())
            else:
                monkeys.append(Monkey(curr_monkey))
                curr_monkey = []
        else:
            monkeys.append(Monkey(curr_monkey))
    
    return monkeys

def play_monkey_game(monkeys: list[Monkey], rounds: int, worry_level_divisor: int):
    # Calculate the Least Common Multiple of the divisibles in the monkeys
    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    lcm_num = 1
    for monkey in monkeys:
        lcm_num = lcm(lcm_num, monkey.divisible_by)

    monkey_map = {monkey.num: monkey for monkey in monkeys}
    for _ in range(1, rounds+1):
        for monkey in monkeys:
            for item in monkey.items:
                target_monkey, new_value = monkey.get_target_monkey_and_new_value(item, worry_level_divisor, lcm_num)
                monkey_map[target_monkey].items.append(new_value)
            monkey.items=[]

    return monkeys

def get_n_most_active_monkeys(monkeys: list[Monkey], rounds: int, n: int, worry_level_divisor: int):
    monkeys_after_game = play_monkey_game(monkeys, rounds, worry_level_divisor)

    #for monkey in monkeys_after_game: print(f"#{monkey.num}: {monkey.inspection_counter}")

    sorted_monkeys = sorted(monkeys_after_game, key=lambda x: x.inspection_counter, reverse=True)
    return sorted_monkeys[:n]

# Sample 1 - 10605
print(product([monkey.inspection_counter for monkey in get_n_most_active_monkeys(get_monkeys("sample_input.txt"), rounds=20, n=2, worry_level_divisor=3)]))

# Part 1 - 57838
print(product([monkey.inspection_counter for monkey in get_n_most_active_monkeys(get_monkeys("input.txt"), rounds=20, n=2, worry_level_divisor=3)]))
    
# Sample 2 - 2713310158
print(product([monkey.inspection_counter for monkey in get_n_most_active_monkeys(get_monkeys("sample_input.txt"), rounds=10000, n=2, worry_level_divisor=1)]))

# Part 2 - 14399639972
print(product([monkey.inspection_counter for monkey in get_n_most_active_monkeys(get_monkeys("input.txt"), rounds=10000, n=2, worry_level_divisor=1)]))


