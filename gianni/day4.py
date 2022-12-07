import time

def main():
    file = open('input/input4.txt')
    countPart1 = 0
    countPart2 = 0
    with file:
        lines = file.readlines()
        for line in lines:
            elves = line.strip().split(',')
            pair1 = elves[0].split('-')
            pair2 = elves[1].split('-')
            range1 = [str(item).zfill(3) for item in list(range(int(pair1[0]), int(pair1[1]) + 1))]
            range2 = [str(item).zfill(3) for item in list(range(int(pair2[0]), int(pair2[1]) + 1))]
            if ('-'.join(range1) in '-'.join(range2) or '-'.join(range2) in '-'.join(range1) ):
                countPart1 += 1
            if any(item in range1 for item in range2):
                countPart2 += 1
    print(f"Part 1: {countPart1}")
    print(f"Part 2: {countPart2}")
    file.close()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")