import functools

def get_packets(fname: str):
    output = []
    with open(fname) as f:
        cache = []
        for line in f.readlines():
            line = line.strip()
            if not line:
                output.append(cache)
                cache = []
                continue
            packet = eval(line)
            cache.append(packet)
    output.append(cache)
    return output

def check_packets_are_in_right_order(left: list, right: list) -> bool:

    run = True
    for l, r in zip(left, right):
        # print(l, r)
        if type(l) == int and type(r) == int:
            if l < r:
                return True
            elif l > r:
                return False

        else:
            l = [l] if type(l) == int else l
            r = [r] if type(r) == int else r
            resp = check_packets_are_in_right_order(l, r)
            if resp is not None:
                return resp
    else:
        if len(left) < len(right):
            return True
        elif len(left) > len(right):
            return False


def solution1(packet_pairs: list[list]) -> int:
    ans = 0
    for i, (left, right) in enumerate(packet_pairs):
        ro = check_packets_are_in_right_order(left=left, right=right)
        if ro:
            ans += (i + 1)
    return ans

def solution2(packet_pairs: list[list]) -> int:
    # https://www.geeksforgeeks.org/how-does-the-functools-cmp_to_key-function-works-in-python/

    def packet_cmp(packet_a, packet_b):
        in_order = check_packets_are_in_right_order(left=packet_a, right=packet_b)
        if in_order:
            return -1
        else:
            return 1
        return 0

    divider1 = [[2]]
    divider2 = [[6]]
    packets = [divider1, divider2]
    for left, right in packet_pairs:
        packets.append(left)
        packets.append(right)
    packets_sorted = sorted(packets, key=functools.cmp_to_key(packet_cmp))

    ans = 1
    for idx, packet in enumerate(packets_sorted):
        if packet in (divider1, divider2):
           ans *= (idx + 1)
    return ans


if __name__ == "__main__":
    import time

    pairs = get_packets("inputs/day-13-sample.txt")
    assert solution1(packet_pairs=pairs) == 13

    pairs = get_packets("inputs/day-13-sample.txt")
    assert solution2(packet_pairs=pairs) == 140

    s = time.time()
    pairs = get_packets("inputs/day-13-input.txt")
    print("time taken to read input", time.time() - s)
    assert solution1(packet_pairs=pairs) == 5350
    print("Solution 1 took", time.time() - s, "seconds")

    s = time.time()
    pairs = get_packets("inputs/day-13-input.txt")
    assert solution2(packet_pairs=pairs) == 19570
    print("Solution 2 took", time.time() - s, "seconds")