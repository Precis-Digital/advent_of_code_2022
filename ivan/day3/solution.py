# %%
import requests
import os
import string
# %%
cookies = {"session": os.environ.get('SESSION_COOKIE')}  # TODO: set your personal Advent of Code session cookie.
response = requests.get("https://adventofcode.com/2022/day/3/input", cookies=cookies)
# %%

rucksacks = response.text.splitlines()

priority = {frozenset(letter): rank for rank, letter in enumerate(string.ascii_letters, start=1)}

sum_of_priorities = 0
for r in rucksacks:
    cmp1, cmp2 = frozenset(r[:len(r)//2]), frozenset(r[len(r)//2:])
    in_both = cmp1 & cmp2
    sum_of_priorities += priority[in_both]


print(f"Sum of priorities for a common item: {sum_of_priorities}")

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

sum_of_priorities_groups = 0
for group in chunker(rucksacks, 3):
    a, b, c = frozenset(frozenset(r) for r in group)
    badge = a & b & c
    sum_of_priorities_groups += priority[badge]

print(f"Sum of priorities for a group's badge: {sum_of_priorities_groups}")