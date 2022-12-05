# %%
import requests
import os
# %%
cookies = {"session": os.environ.get('SESSION_COOKIE')}  # TODO: set your personal Advent of Code session cookie.
response = requests.get("https://adventofcode.com/2022/day/1/input", cookies=cookies)
# %%
elves = response.text.split("\n\n")

elves_carrying_total = []
for elf in elves:
    elf_carrying = 0
    for food in elf.splitlines():
        elf_carrying += int(food)
    elves_carrying_total.append(elf_carrying)

print(f"""
🧝‍♂️ The mightiest elf is carrying {max(elves_carrying_total)} calories.

That's approx. {max(elves_carrying_total) / 250} Snickers bars.
""")

elves_carrying_total.sort(reverse=True)

print(f"""
🧝‍♂️🧝‍♂️🧝‍♂️ Top 3 mightiest elves are carrying {sum(elves_carrying_total[0:3])} calories in total.

That's approx. {sum(elves_carrying_total[0:3]) / 250} Snickers bars.
""")

