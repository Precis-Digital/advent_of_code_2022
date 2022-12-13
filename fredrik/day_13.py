import ast
import functools
import itertools
import math
from typing import Any, Iterable

from shared import utils

BOOL_CMP = {True: 1, False: -1}

PacketList = list[int | list["PacketList"]]
PacketEntry = int | PacketList


class ListExhaustedError(Exception):
    pass


def extract_packets(packets: Iterable[str]) -> list[PacketList]:
    return list(map(ast.literal_eval, packets))


def normalize(x: PacketEntry, /) -> PacketList:
    if isinstance(x, int):
        return [x]
    return x


def both_int(a: Any, b: Any, /) -> bool:
    return isinstance(a, int) and isinstance(b, int)


def normalized_check_packet_order(left: PacketEntry, right: PacketEntry) -> bool:
    return check_packet_order(left=normalize(left), right=normalize(right))


def check_packet_order(left: PacketList, right: PacketList) -> bool:
    for left_item, right_item in itertools.zip_longest(left, right):
        if left_item is None:
            return True
        if right_item is None:
            return False
        if right_item == left_item:
            continue
        if both_int(left_item, right_item):
            return right_item > left_item

        try:
            return normalized_check_packet_order(left=left_item, right=right_item)
        except ListExhaustedError:
            continue

    raise ListExhaustedError


def evaluate_packet_pair(packet_pair: list[str]) -> bool:
    left, right = extract_packets(packets=packet_pair)
    return check_packet_order(left=left, right=right)


def get_index_sum(packet_pairs: list[str]) -> int:
    index_sum = 0
    for i, packet_pair in enumerate(packet_pairs):
        if evaluate_packet_pair(packet_pair=packet_pair.splitlines()):
            index_sum += i + 1

    return index_sum


def packet_sort(left: PacketList, right: PacketList) -> int:
    return BOOL_CMP[check_packet_order(left=left, right=right)]


def get_decoder_key(packets_raw: str, divider_packets: list[PacketList]) -> int:
    packets = extract_packets(utils.drop_empty_rows(packets_raw.splitlines()))
    packets.extend(divider_packets)
    sorted_packets = sorted(
        packets, key=functools.cmp_to_key(packet_sort), reverse=True
    )
    indices = (sorted_packets.index(packet) for packet in divider_packets)
    return math.prod(index_ + 1 for index_ in indices)


def main() -> None:
    packets_raw = utils.read_input_to_string()
    index_sum = get_index_sum(packet_pairs=packets_raw.split("\n\n"))

    divider_packets = [[[2]], [[6]]]
    key = get_decoder_key(packets_raw=packets_raw, divider_packets=divider_packets)

    print(f"Part 1: {index_sum}")
    print(f"Part 1: {key}")


if __name__ == "__main__":
    main()
