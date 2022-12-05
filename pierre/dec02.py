import numpy as np

with open('dec02.txt') as f:
    s1 = f.read()

elf, x = np.array([[ord(t[0]) - 65, ord(t[1]) - 88] for t in s1.replace(' ', '').strip('\n').split('\n')]).T

wins_when_x_is_my_move = (x - elf + 1) % 3
score_when_x_is_my_move = (wins_when_x_is_my_move * 3 + x + 1).sum()

my_move_when_x_is_wins = (x + elf - 1) % 3
score_when_x_is_wins = (x * 3 + my_move_when_x_is_wins + 1).sum()

print('score_when_x_is_my_move:', score_when_x_is_my_move)
print('score_when_x_is_wins:', score_when_x_is_wins)
