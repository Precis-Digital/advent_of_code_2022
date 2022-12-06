def parse_line(line):
    pair = line.split(',')
    a = list(map(int, pair[0].split('-')))
    b = list(map(int, pair[1].split('-')))
    return a, b


def one_subsets_other(a_b):
    a, b = a_b
    return (b[0] <= a[0] <= a[1] <= b[1]) or (a[0] <= b[0] <= b[1] <= a[1])


def nonempty_intersection(a_b):
    a, b = a_b
    return (a[0] <= b[0] <= a[1]) or (b[0] <= a[0] <= b[1])

with open('dec04.txt') as f:
    s1 = f.read()

pairs = s1.strip('\n').split('\n')

print(sum(map(one_subsets_other, map(parse_line, pairs))))
print(sum(map(nonempty_intersection, map(parse_line, pairs))))
