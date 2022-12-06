import time

def main():
    file = open('input/input3.txt')
    group = []
    countPart1 = 0
    countPart2 = 0
    with file:
        lines = file.readlines()
        for line in lines:
            firstCompartment = set(line[:len(line)//2].strip())
            secondCompartment = set(line[len(line)//2:].strip())
            match = ''.join(firstCompartment & secondCompartment)
            offset = 96 if match.islower() else 38
            number = ord(match) - offset
            countPart1 += number
            group.append(set(line.strip()))
            if len(group) == 3:
                match = ''.join(group[0] & group[1] & group[2])
                offset = 96 if match.islower() else 38
                number = ord(match) - offset
                countPart2 += number
                group = []
        print(f"Part 1: {countPart1}")
        print(f"Part 2: {countPart2}")
    file.close()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")