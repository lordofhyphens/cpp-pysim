from cktnet import read_bench_file, get_fanin_cone, Partition
import copy
import argparse
import random
import itertools
from functools import partial
import os.path as path
import multiprocessing
try:
   import cPickle as pickle
except ImportError:
   import pickle

parser = argparse.ArgumentParser(description='Define partitions from a file with test points and bscs in it')
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='pickled partition file')
args = parser.parse_args()

for infile in args.file:
    with open(infile, 'rb') as f:
        parts = pickle.load(f)
        print infile
        ckt = parts[0].ckt
        print "BSCs:", len([x[0] for x in ckt.iteritems() if x[1].function.lower() == "bsc"])
        print "Partitions:", len(parts)
