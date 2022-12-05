import time


def get_results_from_file(file_name: str) -> list[int]:
    with open(file_name, "r") as f:
        lines = f.readlines()

    rounds = []

    for line in lines:
        splitlines = line.strip().split(" ")
        rounds.append((splitlines[0], splitlines[1]))

    return rounds

RULES_DICT = {
    "A":{"Y": "win", "B": "win", "X": "draw", "A": "draw", "Z": "lose", "C": "lose"},
    "B":{"Y": "draw", "B": "draw", "X": "lose", "A": "lose", "Z": "win", "C": "win"},
    "C":{"Y": "lose", "B": "lose", "X": "win", "A": "win", "Z": "draw", "C": "draw"}
}
STRATEGY_DICT = {
    "X": "lose",
    "Y": "draw",
    "Z": "win"
}
RESULT_SCORE_DICT = {"win": 6, "draw": 3, "lose": 0}
SHAPE_SCORE_DICT = {"X": 1, "Y": 2, "Z": 3, "A": 1, "B": 2, "C": 3}

def calc_score_from_strategy(rnd: tuple, determine_action_from_opponent = False) -> int:
    opponent_action = rnd[0]
    player_action = rnd[1]

    if determine_action_from_opponent:
        player_action = determine_action(opponent_action, player_action)
    
    return SHAPE_SCORE_DICT[player_action] + RESULT_SCORE_DICT[RULES_DICT[opponent_action][player_action]]

def determine_action(oppo_action: str, expected_output: str):
    exp_result = STRATEGY_DICT[expected_output]
    for k,v in RULES_DICT[oppo_action].items():
        if v == exp_result:
            return k


start = time.time()
# Sample 1 - expected 15
print(sum([calc_score_from_strategy(rnd) for rnd in get_results_from_file("sample_input.txt")]))

# Part 1
print(sum([calc_score_from_strategy(rnd) for rnd in get_results_from_file("input.txt")]))

# Sample part 2 - expected 12
print(sum([calc_score_from_strategy(rnd, True) for rnd in get_results_from_file("sample_input.txt")]))

# Part 2
print(sum([calc_score_from_strategy(rnd, True) for rnd in get_results_from_file("input.txt")]))

print(f"Finished in {time.time() - start} seconds") # Finished in 0.005616188049316406 seconds