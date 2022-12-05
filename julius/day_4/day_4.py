def input_to_list(path: str) -> list:
    input = open(path).read()
    return input.splitlines()

pair_list = input_to_list("day_4_input.txt")
pair_list = pair_list
is_subset_count = 0
is_overlapping_count = 0

for pair in pair_list:
    elf1, elf2 = pair.split(",")
    elf_1_id1, elf_1_id2 = elf1.split("-")
    elf_2_id1, elf_2_id2 = elf2.split("-")
    elf_1_sections = []
    elf_2_sections = [] 
    for i in range(int(elf_1_id1),int(elf_1_id2)+1):
        elf_1_sections.append(i)
    for i in range(int(elf_2_id1),int(elf_2_id2)+1):
        elf_2_sections.append(i)

    # part 1:
    if set(elf_1_sections).issubset(elf_2_sections) or set(elf_2_sections).issubset(elf_1_sections):
        is_subset_count += 1

    # part 2:
    if not set(elf_1_sections).isdisjoint(elf_2_sections):
        is_overlapping_count += 1

print("PART 1:",is_subset_count) # 540
print(f"PART 2:", is_overlapping_count) # 872