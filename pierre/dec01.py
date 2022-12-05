with open('dec01.txt') as f:
    s = f.read()

print('max: {}, top3: {}'.format(*[sum(sorted(sum(int(x.strip()) for x in g.split('\n')) for g in s.strip('\n').split('\n\n'))[::-1][:k+1]) for k in range(3)][::2]))
