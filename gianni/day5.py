import time
from copy import deepcopy

cargo = [
    ['B','V','S','N','T','C','H','Q'],
    ['W','D','B','G'],
    ['F','W','R','T','S','Q','B'],
    ['L','G','W','S','Z','J','D','N'],
    ['M','P','D','V','F'],
    ['F','W','J'],
    ['L','N','Q','B','J','V'],
    ['G','T','R','C','J','Q','S','N'],
    ['J','S','Q','C','W','D','M']
]

def main():
    file = open('input/input5.txt')
    part1_cargo = deepcopy(cargo)
    part2_cargo = deepcopy(cargo)
    moves = []
    messagePart1 = ''
    messagePart2 = ''
    with file:
        lines = file.readlines()
        for line in lines:
            line = line
            moves.append([int(s) for s in line.split() if s.isdigit()])
    file.close()

    for move in moves:
        moveAmount = move[0]
        moveFrom = move[1] - 1
        moveTo = move[2] - 1
        for amount in range(moveAmount):
            if len(part1_cargo[moveFrom]) > 0:
                part1_cargo[moveTo].append(part1_cargo[moveFrom].pop())
        part2_cargo[moveTo].extend(part2_cargo[moveFrom][-moveAmount:])
        part2_cargo[moveFrom][-moveAmount:] = []
    for crates in part1_cargo:
        messagePart1 += crates[-1]
    for crates in part2_cargo:
        messagePart2 += crates[-1]
    print(f"Part 1: {messagePart1}")
    print(f"Part 2: {messagePart2}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")