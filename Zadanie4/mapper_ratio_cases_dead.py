#!/usr/bin/python3

import sys

for line in sys.stdin:
    line = line.strip()
    line = line.split(',')
    continent, daily_deceased, daily_confirmed = line[61], line[87], line[75]
    print('%s\t%s\t%s' % (continent, daily_deceased, daily_confirmed))
