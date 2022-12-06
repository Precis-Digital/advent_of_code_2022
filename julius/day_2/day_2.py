def input_to_list(path: str) -> list:
    input = open(path).read()
    return input.splitlines()

def replace_all(text: str, dic: dict) -> str:
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

game_moves_list  = input_to_list("day_2_input.txt")

replace_dict = {
    "A": "1", # rock / lose
    "X": "1",
    "B": "2", # paper / draw
    "Y": "2",
    "C": "3", # scissors / win
    "Z": "3"
}

cleaned_list = []
for i in game_moves_list:
    cleaned_list.append(replace_all(i, replace_dict))


winning_elf_move_dict = {
    "1": "2",
    "2": "3",
    "3": "1"
}

win_score = 6
draw_score = 3
score = 0

def generalised_if(elf_move, my_move, winning_elf_move):
    global score
    if elf_move == winning_elf_move:
        score += int(my_move)
    elif elf_move == my_move:
        score += int(my_move) + draw_score
    else:
        score += win_score + int(my_move)

for round in cleaned_list:
    elf_move,my_move = round.split()
    generalised_if(elf_move,my_move, winning_elf_move_dict[my_move])

print("PART 1: Total score is", score) # 13675

strategy_move_dict = {
    "1": "2",
    "2": "3",
    "3": "1"
}

print("PART 2:", score) # 14184
