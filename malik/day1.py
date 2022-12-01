PATH = "./day-1-input.txt"

from collections import defaultdict

elf_id = 0
calorie_dict = defaultdict(list)


with open(PATH, 'r') as f:
    for line in f.readlines():
        line = line.strip()
        if line == '':
            elf_id += 1
            continue
        calorie_dict[elf_id].append(int(line))

print('ans1', max([sum(cal_list) for cal_list in calorie_dict.values()]))
print('ans2', sum(sorted([sum(cal_list) for cal_list in calorie_dict.values()])[-3:]))