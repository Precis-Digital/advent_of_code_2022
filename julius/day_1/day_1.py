def input_to_list(path: str) -> list:
    input = open(path).read()
    return input.splitlines()

elf_list  = input_to_list("julius/day_01/day_1_input.txt")

elf_dict = {"elf_1": []}
counter = 1
for i in elf_list:
    if i != "":
        i = int(i)
        elf_dict[f"elf_{counter}"].append(i)
    else:
        counter += 1
        elf_dict[f"elf_{counter}"] = []

elf_totals = {}
for key, value in elf_dict.items():
    elf_totals[f"{key}"] = sum(value)


max_value = max(elf_totals.values())
print(f"maximum calories elf carries {max_value} calories")

sum_of_calories_desc = sorted(elf_totals.values(), reverse=True)
print(f"The sum of calories for top 3 food carrying elfs is: {sum(sum_of_calories_desc[0:3])}")