with open('dec06.txt') as f:
    s = f.read().strip('\n')

def answer_for_n(sequence, n):
    for k in range(n-1, len(sequence)):
        if len(set(list(sequence[k - n : k]))) == n:
            return k

print(f'answer for n = 4: {answer_for_n(s, 4)}')
print(f'answer for n = 14: {answer_for_n(s, 14)}')
