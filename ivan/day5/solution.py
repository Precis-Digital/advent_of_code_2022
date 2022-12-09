# %%
import requests
import os
import re
from collections import deque
# %%
cookies = {"session": os.environ.get('SESSION_COOKIE')}  # TODO: set your personal Advent of Code session cookie.
response = requests.get("https://adventofcode.com/2022/day/5/input", cookies=cookies)
# %%

input = response.text.splitlines()

input_drawing = input[:8:]
input_rules = input[10::]

# 'move 1 from 3 to 5'

input_drawing.reverse()
boxes = []
for row in input_drawing:
    r = re.findall('.{3}(.)?', "  " + row)
    boxes.append(r)


rules = []
for row in input_rules:
    r = tuple(map(int, re.findall('\d+', row)))
    rules.append(r)

def make_stacks():
    a_list = list(map(list, zip(*boxes)))
    stacks = [deque(i for i in line if i != ' ') for line in a_list]
    return stacks
# %% Part 1

stacks = make_stacks()

def move(boxes: int, _from: int, _to: int):
    for _ in range(boxes):
        stacks[_to-1].append(stacks[_from-1].pop())

def solve(func):
    for rule in rules:
        func(*rule)

    for stack in stacks:
        print(stack[-1], end='')

solve(move)
# %% Part 2

stacks = make_stacks()

def move_multiple_boxes(boxes: int, _from: int, _to: int):
    reverser = deque()
    for _ in range(boxes):
        reverser.append(stacks[_from-1].pop())
    reverser.reverse()
    stacks[_to-1].extend(reverser)

solve(move_multiple_boxes)