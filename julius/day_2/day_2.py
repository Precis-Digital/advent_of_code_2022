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

win_score = 6
equal_score = 3
score_list = []
for round in cleaned_list:
    elf_move,my_move = round.split()
    if my_move == elf_move:
        score_list.extend([equal_score, int(my_move)])
    elif my_move == "1":
        if elf_move == "3":
            score_list.extend([win_score, int(my_move)])
        else:
            score_list.append(int(my_move))
    elif my_move == "2":
        if  elf_move == "1":
            score_list.extend([win_score, int(my_move)])
        else:
            score_list.append(int(my_move))
    elif my_move == "3":
        if elf_move == "1":
            score_list.extend([win_score, int(my_move)])
        elif elf_move == "2":
            score_list.append(int(my_move))

print("PART 1: Total score is", sum(score_list))

win_score = 6
equal_score = 3
score_list = []
# Part 2:
for round in cleaned_list:
    elf_move,my_move = round.split()
    if my_move == "2":
        score_list.extend([equal_score,int(elf_move)])
    elif my_move == "1":
        if elf_move == "1":
            score_list.append(3)
        elif elf_move == "2":
            score_list.append(1)
        else:
            score_list.append(2)
    elif my_move == "3":
        score_list.append(win_score)
        if elf_move == "1":
            score_list.append(2)
        elif elf_move == "2":
            score_list.append(3)
        else:
            score_list.append(1)


print("PART 2: Total score is", sum(score_list))
