import time
from collections import defaultdict

def main():
    file = open('input/input7.txt')
    path = []
    sizes = defaultdict(int)
    answerPart1 = 0
    answerPart2 = []
    with file:
        lines = file.readlines()
        for line in lines:
            items = line.strip().split()
            if items[0] == '$':
                if items[1] == 'cd':
                    if(items[2] == '..'):
                        path.pop()
                    else:
                        path.append(items[2])
            elif items[0] == 'dir':
                continue
            else:
                size = int(items[0])
                for index in range(len(path) + 1):
                    if '/'.join(path[:index]):
                        sizes['/'.join(path[:index])] += size
    file.close()

    for size in sizes.values():
        if size <= 100_000:
            answerPart1 += size
        if size >= 30_000_000 - (70_000_000 - sizes['/']):
            answerPart2.append(size)

    print(f"Part 1: {answerPart1}")
    print(f"Part 2: {min(answerPart2)}")

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")