#!/usr/bin/env python

import numpy
import pandas


def probabilistic_rounding(number):
    fp, ip = numpy.modf(number)
    roll = numpy.random.sample()
    if (fp > roll):
        return int(ip + 1)
    return int(ip)


def stratified_random_sample(dataset, fields, proportion):
    grouping = dataset.groupby(fields)
    rows = []
    for partition in grouping.groups:
        row_numbers = grouping.groups[partition]
        size = len(row_numbers)
        n = probabilistic_rounding(proportion * size)
        if (n > 0):
            rows = rows + list(numpy.random.choice(row_numbers, n))
    return dataset.loc[rows]
