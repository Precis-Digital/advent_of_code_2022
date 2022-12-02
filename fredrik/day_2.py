from shared import utils

SHAPE_SCORES = {"Rock": 1, "Paper": 2, "Scissors": 3}
RPS_MAP = {
    "A": "Rock",
    "X": "Rock",
    "B": "Paper",
    "Y": "Paper",
    "C": "Scissors",
    "Z": "Scissors",
}
BEATS = {"Rock": "Scissors", "Scissors": "Paper", "Paper": "Rock"}
LOSES_TO = {value: key for key, value in BEATS.items()}
DRAWS = {value: value for _, value in BEATS.items()}
OUTCOME_MAP = {"X": "Lose", "Y": "Draw", "Z": "Win"}
OUTCOME_OPPONENT_MAP = {"Win": LOSES_TO, "Lose": BEATS, "Draw": DRAWS}
GAME_SCORES = {"Win": 6, "Draw": 3, "Lose": 0}


def rock_paper_scissors(opponent: str, you: str) -> str:
    if BEATS[opponent] == you:
        return "Lose"
    if BEATS[you] == opponent:
        return "Win"
    return "Draw"


def translate_game(
    map_1: dict[str, str],
    map_2: dict[str, str],
    game: str,
) -> tuple[str, str]:
    entry_1, entry_2 = game.split()
    return map_1[entry_1], map_2[entry_2]


def part_1(game: str) -> int:
    opponent, you = translate_game(map_1=RPS_MAP, map_2=RPS_MAP, game=game)
    outcome = rock_paper_scissors(opponent=opponent, you=you)
    return SHAPE_SCORES[you] + GAME_SCORES[outcome]


def part_2(game: str) -> int:
    opponent, outcome = translate_game(map_1=RPS_MAP, map_2=OUTCOME_MAP, game=game)
    you = OUTCOME_OPPONENT_MAP[outcome][opponent]
    return SHAPE_SCORES[you] + GAME_SCORES[outcome]


def main() -> None:
    games = utils.read_input_to_string().splitlines()
    score_1, score_2 = 0, 0
    for game in games:
        score_1 += part_1(game=game)
        score_2 += part_2(game=game)

    print(f"Part 1: {score_1}")
    print(f"Part 2: {score_2}")


if __name__ == "__main__":
    main()
