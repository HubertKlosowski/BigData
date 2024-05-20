#!/usr/bin/python3

import sys

current_continent = None
total_case, total_dead = 0, 0
continent = None

for line in sys.stdin:
    line = line.strip()
    continent, cases, dead = line.split('\t')

    try:
        cases, dead = int(cases), int(dead)
    except ValueError:
        continue

    if current_continent == continent:
        total_cases += cases
        total_dead += dead
    else:
        if current_continent:
            print('%s\t%s\t%s' % (current_continent, total_cases, total_dead))
        current_continent = continent
        total_cases = cases
        total_dead = dead

print('%s\t%s\t%s' % (current_continent, total_cases, total_dead))
