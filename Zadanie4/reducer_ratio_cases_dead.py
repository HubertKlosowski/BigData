#!/usr/bin/python3

from operator import itemgetter
import sys

current_continent = None
total_dead = 0
total_cases = 0
count = 0
continent = None

for line in sys.stdin:
    line = line.strip()
    continent, part_total_dead, part_total_cases = line.split('\t')
    try:
        part_total_dead, part_total_cases = int(part_total_dead), int(part_total_cases)
    except ValueError:
        continue
    if current_continent == continent:
        total_dead += part_total_dead
        total_cases += part_total_cases
    else:
        if current_continent:
            ratio = total_cases / total_dead
            print('%s %s' % (current_continent, ratio))
        total_dead = part_total_dead
        total_cases = part_total_cases
        current_continent = continent

ratio = total_cases / total_dead
print('%s %s' % (current_continent, ratio))
