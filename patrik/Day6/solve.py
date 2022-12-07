stream = open('data.txt', 'r').read()
marker = int(input())

for i, char in enumerate(stream):
    if i > marker-1:
        arr = [stream[i-j] for j in range(marker)]
        if len([*set(arr)]) > marker-1:
            print('For marker length', marker, 'the answer is', i+1)
            break
