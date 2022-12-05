# %%
import requests
import os
# %%
cookies = {"session": os.environ.get('SESSION_COOKIE')}  # TODO: set your personal Advent of Code session cookie.
response = requests.get("https://adventofcode.com/2022/day/2/input", cookies=cookies)
# %%
games = response.text
# %%
# Part 1
shape_score = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

outcome_score = {
    ('A', 'X'): 3, 
    ('A', 'Y'): 6, 
    ('A', 'Z'): 0, 
    ('B', 'X'): 0, 
    ('B', 'Y'): 3, 
    ('B', 'Z'): 6, 
    ('C', 'X'): 6, 
    ('C', 'Y'): 0, 
    ('C', 'Z'): 3, 
}


total_score_1 = 0
total_score_2 = 0

for game in games.splitlines():
    game_t = tuple(game.split())
    total_score_1 += outcome_score[game_t] + shape_score[game_t[1]]

    # Part 2
    true_meaning = {
        'X': 0,
        'Y': 3,
        'Z': 6
    }

    result = tuple(key for key, value in outcome_score.items() if game_t[0] in key and value == true_meaning[game_t[1]])
    total_score_2 += outcome_score[result[0]] + shape_score[result[0][1]]


print(f'If I follow the ambiguous strategy guide, my total score will be: {total_score_1}')
print(f'If I follow the true ultra top secret strategy guide, my total score will be: {total_score_2}')

