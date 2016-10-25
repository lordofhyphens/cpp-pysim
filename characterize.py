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
parser.add_argument('--out', type=str, default=None, help="Output file to write results to.")
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='pickled partition file')
args = parser.parse_args()

for infile in args.file:
    with open(infile, 'rb') as f:
        parts = pickle.load(f)
        ckt = parts[0].ckt
        bsc_count = len(set([x[0] for x in ckt.iteritems() if x[1].function.lower() == "bsc"]))
        part_count = len(parts)
        mems = [len(x.members) for x in parts]

        avg_part_size = sum(mems) / len(parts)
        min_part_size = min(mems)
        max_part_size = max(mems)
        median_part_size = sorted(mems)[len(mems)/2]

        avg_w = sum([len(x.get_inputs()) for x in parts]) / len(parts)

        stats = [ infile, bsc_count, part_count, avg_part_size, min_part_size, max_part_size, median_part_size, avg_w]
        stats = map(lambda x:str(x), stats)

        if args.out is not None:
            with open(args.out, 'ab') as f:
                ",".join(stats)
        else:
            print ",".join(stats)

