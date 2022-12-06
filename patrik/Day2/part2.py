def convert(h):
    return {'A': 1, 'B': 2, 'C': 3}[h]


score = 0

for round in open('strategy.txt', 'r').read().split('\n'):
    foe, result = round.split(' ')
    foe = convert(foe)
    me = 0

    if (result == 'Y'):
        score += 3
        me = foe

    elif (result == 'Z'):
        score += 6
        if (foe == 1):
            me = 2
        elif (foe == 2):
            me = 3
        elif (foe == 3):
            me = 1

    else:
        if (foe == 1):
            me = 3
        elif (foe == 2):
            me = 1
        elif (foe == 3):
            me = 2

    score += me


print(score)
