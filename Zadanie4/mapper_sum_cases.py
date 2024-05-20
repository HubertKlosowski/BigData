#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    country, cases = line[0], line[75]
    print('%s\t%s' % (country, cases))
