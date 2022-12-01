def get_elves(filepath: str):
    with open(filepath, "r") as f:
        contents = f.read()

    unique_elves = contents.split("\n\n")

    totals = []
    
    for e in unique_elves:
        calories = [int(x) for x in e.split("\n")]
        totals.append(sum(calories))

    totals.sort()
    return totals

if __name__ == "__main__":
    resp = get_elves("hungry.txt")
    p1 = resp[-1]
    p2 = sum(resp[-3:])

    print(p1)
    print(p2)
