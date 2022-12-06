rucksacks = open('data.txt', 'r').read().split('\n')
grouped = [rucksacks[n:n+3] for n in range(0, len(rucksacks), 3)]

t = 0
for group in grouped:
    prio = ord(list(set(group[0]) & set(group[1]) & set(group[2]))[0])
    t += prio - 96 if prio > 96 else prio - 38

print(t)
