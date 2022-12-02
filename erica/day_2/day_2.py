import pathlib
game_rules = {
    "X": [{"C": "win", "B": "loss", "A": "draw", "points": 1}, {"A": "Z", "B": "X", "C": "Y"}],
    "Y": [{"A": "win", "C": "loss", "B": "draw", "points": 2}, {"A": "X", "B": "Y", "C": "Z"}],
    "Z": [{"B": "win", "A": "loss", "C": "draw", "points": 3}, {"A": "Y", "B": "Z", "C": "X"}]
}
game_points = {"win": 6, "loss": 0, "draw": 3}
game = [tuple(line.replace(" ", "")) for line in pathlib.Path("erica/day_2/input_data.txt").read_text().split('\n')]
total_points = sum([game_points[game_rules[r[1]][0][r[0]]] + game_rules[r[1]][0]["points"] for r in game])
print(f"total sum: {total_points}")  # part 1: 9241
new_total_points = sum([game_points[game_rules[game_rules[r[1]][1][r[0]]][0][r[0]]] + game_rules[game_rules[r[1]][1][r[0]]][0]["points"] for r in game])
print(f"total sum: {new_total_points}")  # part 2: 14610
# Don't take this seriously
