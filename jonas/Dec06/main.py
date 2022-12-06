MARKER_TYPE_CHARACTERS = {
    "packet": 4,
    "message": 14
}

def get_datastream_input(filename: str) -> str:
    with open(filename, "r") as f:
        return [char for char in f.readline()]

def determine_marker_index(datastream: list[str], marker_type: str) -> int:
    char_nums = MARKER_TYPE_CHARACTERS[marker_type]

    prev_stack = datastream[:char_nums]
    for i, char in enumerate(datastream[char_nums:], char_nums):
        if len(unique_values(prev_stack)) == char_nums:
            return i
        
        prev_stack.pop(0)
        prev_stack.append(char)

def unique_values(input_list: list[str]) -> list[str]:
    return list(set(input_list))

# Sample 1 - 7
print(determine_marker_index(get_datastream_input("sample_input.txt"), "packet"))

# Part 1
print(determine_marker_index(get_datastream_input("input.txt"), "packet"))

# Sample 2 - 7
print(determine_marker_index(get_datastream_input("sample_input.txt"), "message"))

# Part 2
print(determine_marker_index(get_datastream_input("input.txt"), "message"))