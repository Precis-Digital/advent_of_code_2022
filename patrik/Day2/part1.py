def convert(h):
    return {'A': 1, 'X': 1, 'B': 2, 'Y': 2, 'C': 3, 'Z': 3}[h]


score = 0

for round in open('strategy.txt', 'r').read().split('\n'):
    foe, me = convert(round.split(' ')[0]), convert(round.split(' ')[1])
    score += me

    if (foe == me):
        score += 3

    elif ((foe == 1 and me == 2) or (foe == 2 and me == 3) or (foe == 3 and me == 1)):
        score += 6

print(score)
