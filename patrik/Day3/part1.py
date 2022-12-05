t = 0
for rucksack in open('data.txt', 'r').read().split('\n'):
    i = int(len(rucksack)/2)
    for l in [*rucksack[0:i]]:
        if l in [*rucksack[i:]]:
            prio = ord(l)
            t += prio - 96 if prio > 96 else prio - 38
            break
print(t)
