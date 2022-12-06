from string import ascii_letters as letters
from functools import reduce

letters = '_' + letters

with open('dec03.txt') as f:
    s1 = f.read()

sacks = s1.strip('\n').split('\n')

mids = map(lambda x: len(x) // 2 , sacks)

sum_prios = sum(
    map(letters.index, [max(set(el[:m]) & set(el[m:])) for el, m in zip(sacks, mids)]
    )
)

badge_prio_sum = sum(
    map(
        letters.index,
        [max(reduce(set.__and__, map(set, group))) for group in zip(*[sacks[k::3] for k in (0,1,2)])]
    )
)

print(sum_prios)
print(badge_prio_sum)
