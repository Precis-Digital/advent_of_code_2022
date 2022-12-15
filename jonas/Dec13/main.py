
# Day 13, Year 2022
# Link: https://adventofcode.com/2022/day/13
import time
from functools import cmp_to_key

DIVIDER_PACKETS = ['[[2]]', '[[6]]']

class DataPacketPair:
    left_str: str
    right_str: str
    
    def __init__(self, left_str: str, right_str: str) -> "DataPacketPair":
        self.left_str = left_str
        self.right_str = right_str

    def __repr__(self) -> str:
        return f"{self.left_str} | {self.right_str}"
    
    @property
    def is_in_the_right_order(self) -> bool:
        left_val = eval(self.left_str)
        right_val = eval(self.right_str) 

        comparison = compare_values(left_val, right_val)
        if comparison == 1:
            return True
        elif comparison == -1:
            return False
        else:
            raise Exception(f"Error! Could not determine if the order is correct.")


def compare_values(left_val, right_val):
    if isinstance(left_val, int) and isinstance(right_val, int):
        if left_val < right_val:
            return 1
        elif left_val > right_val:
            return -1
        else:
            return 0
    
    if isinstance(left_val, list) and isinstance(right_val, list):
        right_val_len = len(right_val)
        i = -1
        for val in left_val:
            i += 1 
            
            if i >= right_val_len:
                # If i is not in the right list, the items are in the right order
                return -1
            value_comp = compare_values(val, right_val[i])
            if value_comp == 0:
                # If the comparison of the values == 0, just continue to next item
                continue
            else:
                # If it's not zero we have an answer to if it's ordered correctly, so return that
                return value_comp
        else:
            if i+1 < right_val_len:
                # When the loop is done, if i is still lower than the right list length, the right list must be longer, so it's not in order
                return 1
            else:
                # Else just return 0 to continue to next iteration
                return 0
                
    if isinstance(left_val, list):
        return compare_values(left_val, [right_val])
    else:
        return compare_values([left_val], right_val)

def get_divider_packet_indexes(sorted_values:list[str]) -> list[int]:
    values = []
    for divider in DIVIDER_PACKETS:
        values.append(sorted_values.index(eval(divider)) + 1)
    return values

def get_input_values(file_name: str, as_pairs: bool = True) -> list[DataPacketPair]:
    with open(file_name, 'r') as f:
        if as_pairs:   
            parsed_values = []
            values = [val.strip() for val in f.readlines()]
            for i in range(0, len(values), 3):
                parsed_values.append(DataPacketPair(values[i], values[i+1]))
        else:
            parsed_values = [val.strip() for val in f.readlines() if val != "\n"]
        return parsed_values

def part_1_sample():
    start_time = time.time()
    ans = sum([i for i, data_packet in enumerate(get_input_values('Dec13/sample_input.txt'),1) if data_packet.is_in_the_right_order])
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_1_answer():
    start_time = time.time()
    ans = sum([i for i, data_packet in enumerate(get_input_values('Dec13/input.txt'),1) if data_packet.is_in_the_right_order])
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

def part_2_sample():
    start_time = time.time()
    sorted_vals = sorted([eval(val) for val in get_input_values('Dec13/sample_input.txt', as_pairs=False) + DIVIDER_PACKETS], key=cmp_to_key(compare_values))[::-1]
    values = get_divider_packet_indexes(sorted_vals)
    ans = values[0] * values[1]
    print(f'Ran in {time.time() - start_time} seconds')
    return ans


def part_2_answer():
    start_time = time.time()
    sorted_vals = sorted([eval(val) for val in get_input_values('Dec13/input.txt', as_pairs=False) + DIVIDER_PACKETS], key=cmp_to_key(compare_values))[::-1]
    values = get_divider_packet_indexes(sorted_vals)
    ans = values[0] * values[1]
    print(f'Ran in {time.time() - start_time} seconds')
    return ans

if __name__ == "__main__":
    part_1_answer()
    part_2_answer()