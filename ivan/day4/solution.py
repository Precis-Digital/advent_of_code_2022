# %%
import requests
import os
import re
# %%
cookies = {"session": os.environ.get('SESSION_COOKIE')}  # TODO: set your personal Advent of Code session cookie.
response = requests.get("https://adventofcode.com/2022/day/4/input", cookies=cookies)
# %%

assignments = response.text.splitlines()

count_pairs = 0
count_overlaps = 0
for pair in assignments:
    s = re.split("-|,", pair)
    _1st = set(range(int(s[0]), int(s[1])+1))
    _2nd = set(range(int(s[2]), int(s[3])+1))
    if _1st.issubset(_2nd) or _1st.issuperset(_2nd):
        count_pairs += 1
    if not _1st.isdisjoint(_2nd):
        count_overlaps += 1

print(count_pairs)
print(count_overlaps)
# %%
