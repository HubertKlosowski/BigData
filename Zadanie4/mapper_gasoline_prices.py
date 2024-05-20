#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    country, gasoline = line[4], line[1]
    print('%s\t%s' % (country, gasoline))
