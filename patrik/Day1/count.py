#!/usr/bin/env python3
c = []
for elf in open('calories.txt', 'r').read().split('\n\n'):
    c.append(sum(map(int, elf.split('\n'))))

c.sort(reverse=True)
print(sum(c[0:3]))
