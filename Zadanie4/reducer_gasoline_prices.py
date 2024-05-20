#!/usr/bin/python3

import sys
from math import sqrt

current_country = None
sum_prices = 0
sum_of_squares = 0
count = 0

for line in sys.stdin:
    line = line.strip()
    country, sum_price, sum_square, cnt = line.split('\t')
    try:
        sum_price, sum_square, cnt = float(sum_price), float(sum_square), int(cnt)
    except ValueError:
        continue

    if current_country == country:
        sum_prices += sum_price
        sum_of_squares += sum_square
        count += cnt
    else:
        if current_country:
            mean = sum_prices / count
            variance = (sum_of_squares / count) - (mean ** 2)
            stddev = sqrt(variance)
            print('%s\t%s' % (current_country, stddev))

        current_country = country
        sum_prices = sum_price
        sum_of_squares = sum_square
        count = cnt

if current_country:
    mean = sum_prices / count
    variance = (sum_of_squares / count) - (mean ** 2)
    stddev = sqrt(variance)
    print('%s\t%s' % (current_country, stddev))
