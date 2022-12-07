with open('dec05.txt') as f:
    sin = f.read()

stack_chart, proc = sin.strip('\n').split('\n\n')

slines = (stack_chart.strip('\n') + ' ').split('\n')

print(stack_chart)
print('==================')

parsed_lines = [
    [el[1] for el in zip(*[line[k::4] for k in range(3)])]
    for line in slines[:-1]
]

stacks = [[] for k in range(9)]

for line in parsed_lines:
    for l, let in enumerate(line):
        if let == ' ':
            continue
        stacks[l].append(let)

rev_stacks = [el[::-1] for el in stacks]

def parse_proc(line):
    m = list(map(int, line.split(' ')[1::2]))
    return m

proc_ints = list(map(parse_proc, proc.split('\n')))


def move_from_to(pp, count, fro, to, single_crate):
    crates = pp[fro-1][-count:]
    pp[fro-1] = pp[fro-1][:-count]
    if single_crate:
        crates = crates[::-1]
    pp[to-1].extend(crates)



for count, fro, to in proc_ints:
    move_from_to(rev_stacks, count, fro, to, single_crate=True)

tops = [el[-1] for el in rev_stacks]
print(''.join(tops))

rev_stacks = [el[::-1] for el in stacks]

for count, fro, to in proc_ints:
    move_from_to(rev_stacks, count, fro, to, single_crate=False)

tops = [el[-1] for el in rev_stacks]
print(''.join(tops))
