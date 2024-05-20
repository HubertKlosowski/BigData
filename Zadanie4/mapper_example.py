#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    id, country, cases = line.split(',')
    if id:
        print('%s\t%s' % (country, cases))
