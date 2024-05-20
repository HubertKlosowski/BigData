#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    country, full_vac = line[0], line[100]
    print('%s\t%s' % (country, full_vac))
