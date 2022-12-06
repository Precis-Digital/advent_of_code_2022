def detect_start_of_packet_marker(input: str, part:str,  distinct_characters: int) -> str:
    four_characters = []
    position_in_list_counter = 0
    for character in input:
        position_in_list_counter += 1
        four_characters.extend(character)
        if len(set(four_characters)) == distinct_characters:
            return print(part, position_in_list_counter)
        elif len(four_characters) == distinct_characters:
            four_characters.pop(0)
            
detect_start_of_packet_marker(open("day_6_input.txt").read(), "PART 1", 4) # 1987
detect_start_of_packet_marker(open("day_6_input.txt").read(), "PART 2", 14) # 3059


    