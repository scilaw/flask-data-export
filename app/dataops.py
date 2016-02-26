#!/usr/bin/env python

import os
import pandas
import datasets
import blosc
try:
    import cPickle as pickle
except:
    import pickle


loaded_datasets = {}


# TODO: load to a temporary file, then move to actual name
def func_cache(func):
    def inner(*args, **kwargs):
        name = func.func_name
        for arg in args[0:len(args)]:
            name = name + '_' + str(arg)
        for arg in kwargs:
            name = name + '_' + str(arg)
        fname = 'cache/' + name + '.pkl-blosc'
        if os.path.isfile(fname):
            fh = open(fname, 'rb')
            ret = pickle.loads(blosc.decompress(fh.read()))
        else:
            ret = func(*args, **kwargs)
            fh = open(fname, 'wb')
            fh.write(blosc.compress(pickle.dumps(ret, protocol=2), typesize=8))
        fh.close()
        return ret
    return inner


@func_cache
def load_data(dataset_name):
    if dataset_name not in loaded_datasets:
        filename = datasets.datasets[dataset_name]['source']
        path = datasets.data_path + os.path.sep + filename
        data = pandas.read_csv(path)
        data.fillna('', inplace=True)
        loaded_datasets[dataset_name] = data
    return loaded_datasets[dataset_name]


@func_cache
def fields_unique_values(dataset_name, fields):
    ret = {}
    data = load_data(dataset_name)
    for field in fields:
        ret[field] = data[field].unique()
        ret[field].sort()
    return ret


@func_cache
def dataset_record_count(dataset):
    data = load_data(dataset)
    return len(data)


def dataset_record_counts():
    ret = {}
    for dataset_name in datasets.datasets:
        ret[dataset_name] = dataset_record_count(dataset_name)
    return ret


@func_cache
def dataset_fields(dataset_name):
    return load_data(dataset_name).keys()


def all_datasets_fields():
    ret = {}
    for dataset_name in datasets.datasets:
        ret[dataset_name] = dataset_fields(dataset_name)
    return ret


def all_datasets_key_fields_unique_values():
    ret = {}
    for dataset_name in datasets.datasets:
        fields = datasets.datasets[dataset_name]['fields_of_interest']
        ret[dataset_name] = fields_unique_values(dataset_name, fields)
    return ret
