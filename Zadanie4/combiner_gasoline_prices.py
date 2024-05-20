#!/usr/bin/python3

import sys
from collections import defaultdict

current_country = None
country_sums = defaultdict(lambda: [0, 0, 0])
for line in sys.stdin:
    line = line.strip()
    country, price = line.split('\t')
    try:
        price = float(price)
    except ValueError:
        continue

    country_sums[country][0] += price
    country_sums[country][1] += price ** 2
    country_sums[country][2] += 1

for country, values in country_sums.items():
    print('%s\t%s\t%s\t%s' % (country, values[0], values[1], values[2]))
