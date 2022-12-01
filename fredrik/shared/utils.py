def read_input_to_string() -> str | list[str]:
    with open("input.txt", "r") as file:
        return file.read()
