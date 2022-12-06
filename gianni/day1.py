import time

def main():
    count = 0
    elfs = []
    file = open('input/input1.txt')

    with file:
        lines = file.readlines()
        for line in lines:
            if (line[0] != '\n'):
                count+=int(line)
            else:
                elfs.append(count)
                count = 0
                continue
        elfs.sort()
        print(f"Part 1: {max(elfs)}")
        print(f"Part 2: {elfs[-1] + elfs[-2] + elfs[-3]}")
    file.close()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")