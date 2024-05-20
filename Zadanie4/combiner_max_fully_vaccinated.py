#!/usr/bin/python3

import sys

current_country = None
max_full_vac = 0
country = None

for line in sys.stdin:
    line = line.strip()
    country, full_vac = line.split('\t')
    try:
        full_vac = int(full_vac)
    except ValueError:
        continue
    if current_country == country:
        max_full_vac = max(max_full_vac, full_vac)
    else:
        if current_country:
            print('%s\t%s' % (current_country, max_full_vac))
        max_full_vac = full_vac
        current_country = country

print('%s\t%s' % (current_country, max_full_vac))
