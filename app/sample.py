#!/usr/bin/env python

import numpy
import pandas


def find_partitions(dataset, fields):
    ret = []
    if (len(fields) == 1):
        for value in dataset[fields[0]].unique():
            ret.append([value])
        return ret
    else:
        first = find_partitions(dataset, [fields[0]])
        rest = find_partitions(dataset, fields[1:])
        for ritem in rest:
            for litem in first:
                ret.append(litem + ritem)
        return ret


def partition_rows(dataset, fields, partition):
    criteria = pandas.Series([True] * len(dataset))
    for i in range(len(fields)):
        field = fields[i]
        value = partition[i]
        selection = dataset[field] == value
        criteria = criteria & selection
    return criteria


def partition_sizes(dataset, fields, partitions):
    sizes = []
    for partition in partitions:
        criteria = partition_rows(dataset, fields, partition)
        size = numpy.sum(criteria)
        sizes.append(size)
        print("partition size: " + str(size))
    return sizes


def probabilistic_rounding(number):
    fp, ip = numpy.modf(number)
    roll = numpy.random.sample()
    if (fp > roll):
        return int(ip + 1)
    return int(ip)


def stratified_random_sample(dataset, fields, proportion):
    partitions = find_partitions(dataset, fields)
    sizes = partition_sizes(dataset, fields, partitions)
    sample = pandas.DataFrame()
    for i in range(len(partitions)):
        n = probabilistic_rounding(proportion * sizes[i])
        rows = partition_rows(dataset, fields, partitions[i])
        append = dataset[rows].sample(n)
        sample = pandas.concat([sample, append])
    return sample
