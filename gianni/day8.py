import time
import numpy as np
import pandas as pd

def pandas_rolling_max(data):
    return pd.Series(data).cummax().to_numpy()

def check_if_next_number_is_the_same(array):
    new_array = []
    for i in range(len(array)):
        if i == 0: new_array.append(1)
        elif i != 0 and array[i - 1] == array[i]: new_array.append(0)
        else: new_array.append(1)
    return np.array(new_array)

def check_trees(data, direction):
    array = []
    for i in range(len(data)):
        concatenated = []
        if direction == 1: data_split = data[i, ...]
        else: data_split = data[..., i]
        data_rolling_max = pandas_rolling_max(data_split)
        data_rolling_max_reversed = pandas_rolling_max(np.array(list(reversed(data_split))))
        data_check = check_if_next_number_is_the_same(data_rolling_max)
        data_reversed_check = check_if_next_number_is_the_same(data_rolling_max_reversed)
        data_check_back_reversal = np.array(list(reversed(data_reversed_check)))
        for ii in range(len(data_check)):
            if data_check[ii] == 0 and data_check_back_reversal[ii] == 0: concatenated.append(0)
            else: concatenated.append(1)
        array.append(concatenated)
    return array

def part1(data):
    concatenated = []
    horizontal = np.array(check_trees(data, 1)).flatten()
    vertical = np.swapaxes(np.array(check_trees(data, 0)), 0, 1).flatten()
    for i in range(len(horizontal)):
        if horizontal[i] == 0 and vertical[i] == 0: concatenated.append(0)
        else: concatenated.append(1)
    reshaped = np.reshape(concatenated, data.shape)
    return len(data[reshaped == 1])

def main():
    file = open('input/input8.txt')
    data = []
    with file:
        lines = file.readlines()
        for line in lines:
            part = [int(x) for x in list(line.strip())]
            data.append(part)
    file.close()

    print(f"Part 1: {part1(np.array(data))}")
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
