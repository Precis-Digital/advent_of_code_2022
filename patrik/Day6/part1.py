stream = open('data.txt', 'r').read()

for i, char in enumerate(stream):
    if i > 2:
        if len([*set([stream[i-3], stream[i-2], stream[i-1], char])]) > 3:
            print(i+1)
            break
