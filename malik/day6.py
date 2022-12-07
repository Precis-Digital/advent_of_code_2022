def get_sequence_of_4_unique_characters(s: str, num_unique_characters=4) -> int:
    """get the number of sequences of 4 unique characters"""
    N = num_unique_characters
    for i in range(N - 1, len(s)):
        if len(set(s[i - (N - 1) : i + 1])) == N:
            return i + 1
    return -1


if __name__ == "__main__":
    with open("inputs/day-6-input.txt", "r") as f:
        s = f.read().strip()
        print(
            "solution 1:",
            get_sequence_of_4_unique_characters(s=s, num_unique_characters=4),
        )

        print(
            "solution 2:",
            get_sequence_of_4_unique_characters(s=s, num_unique_characters=14),
        )
