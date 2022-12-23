import pathlib
from itertools import groupby
import heapq


text = pathlib.Path("erica/day_01/input_data.txt").read_text().split('\n')


def split_condition(value):
    return value in {""}


elfs_kcal = [list(v) for k, v in groupby(text, key=split_condition) if not k]
elf_dict = {elf+1: sum(list(map(int, kcal))) for elf, kcal in enumerate(elfs_kcal)}

print(elf_dict[max(elf_dict, key=elf_dict.get)])  # part 1

top_elfs = heapq.nlargest(3, elf_dict, key=elf_dict.get)
print(sum([elf_dict[top_elf] for top_elf in top_elfs]))  # part 2
