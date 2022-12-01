import pathlib
from itertools import groupby

text = pathlib.Path("erica/day_1/input_data.txt").read_text().split('\n')


def split_condition(value):
    return value in {""}


elfs_kcal = [list(v) for k, v in groupby(text, key=split_condition) if not k]
elf_dict = {elf+1: sum(list(map(int, kcal))) for elf, kcal in enumerate(elfs_kcal)}

print(elf_dict[max(elf_dict, key=elf_dict.get)])
