import time

scorePart1 = 0
scorePart2 = 0

def decidePart1(user, opponent):
    global scorePart1
    if opponent == 'A': opponent = 'R'
    if opponent == 'B': opponent = 'P'
    if opponent == 'C': opponent = 'S'
    if user == 'X': user = 'R'
    if user == 'Y': user = 'P'
    if user == 'Z': user = 'S'
    if user == opponent:
        if user == 'R': scorePart1 += 4
        elif user == 'P': scorePart1 += 5
        elif user == 'S': scorePart1 += 6
    elif user == 'R':
        if opponent == 'S': scorePart1 += 7
        else: scorePart1 += 1
    elif user == 'P':
        if opponent == 'R': scorePart1 += 8
        else: scorePart1 += 2
    elif user == 'S':
        if opponent == 'P': scorePart1 += 9
        else: scorePart1 += 3

def decidePart2(user, opponent):
    global scorePart2
    if user == 'X':
        if opponent == 'B': scorePart2 += 1
        elif opponent == 'C': scorePart2 += 2
        elif opponent == 'A': scorePart2 += 3
    elif user == 'Y':
        if opponent == 'A': scorePart2 += 4
        elif opponent == 'B': scorePart2 += 5
        elif opponent == 'C': scorePart2 += 6
    elif user == 'Z':
        if opponent == 'C': scorePart2 += 7
        elif opponent == 'A': scorePart2 += 8
        elif opponent == 'B': scorePart2 += 9

def main():
    global scorePart1, scorePart2
    file = open('input/input2.txt')
    with file:
        lines = file.readlines()
        for line in lines:
            split = line.split(' ')
            opponent = split[0].strip()
            user = split[1].strip()
            decidePart1(user, opponent)
            decidePart2(user, opponent)
    print(f"Part 1: {scorePart1}")
    print(f"Part 2: {scorePart2}")
    file.close()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")