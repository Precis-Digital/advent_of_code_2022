import time

def findMarker(buffer, amount):
    for index in range(len(buffer)):
        marker = buffer[index:index + amount]
        if(len(marker) == amount):
            if (len(set(marker)) == len(marker)):
                return buffer.find(marker) + amount

def main():
    file = open('input/input6.txt')

    with file:
        lines = file.readlines()
        for line in lines:
            print(f"Part 1: {findMarker(line.strip(), 4)}")
            print(f"Part 2: {findMarker(line.strip(), 14)}")
    file.close()

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")