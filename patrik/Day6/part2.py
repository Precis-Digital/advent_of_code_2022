stream = open('data.txt', 'r').read()

for i, char in enumerate(stream):
    if i > 13:
        arr = [stream[i-j] for j in range(14)]
        if len([*set(arr)]) > 13:
            print(i+1)
            break
