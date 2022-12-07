import collections

from shared import utils


def find_start_of_packet_marker(datastream: str, unique_len: int) -> int:
    sliding_window = collections.deque(maxlen=unique_len)
    for i, char in enumerate(datastream):
        sliding_window.append(char)

        if len(sliding_window) == len(set(sliding_window)) == unique_len:
            return i + 1


def main() -> None:
    datastream = utils.read_input_to_string()
    index1 = find_start_of_packet_marker(datastream=datastream, unique_len=4)
    index2 = find_start_of_packet_marker(datastream=datastream, unique_len=14)

    print(f"Part 1: {index1}")
    print(f"Part 2: {index2}")


if __name__ == "__main__":
    main()
