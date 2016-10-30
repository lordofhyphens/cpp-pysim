# Copyright (c) 2016 Joseph Lenox
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE. 

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
z = [ "infile", "bsc_count", "ckt size","sum of part members", "part_count", "avg_part_size", "min_part_size", "max_part_size", "median_part_size", "avg_w"]
if args.out is not None:
    with open(args.out, 'ab') as f:
        f.write(",".join(z))
else:
    print ",".join(z)

for infile in args.file:
    with open(infile, 'rb') as f:
        parts = pickle.load(f)
        for p in parts:
            print p.members
        ckt = parts[0].ckt
        bsc_count = len(set([x[0] for x in ckt.iteritems() if x[1].function.lower() == "bsc"]))
        len(ckt) 
        part_count = len(parts)
        mems = [len(x.members) for x in parts]

        avg_part_size = sum(mems) / len(parts)
        min_part_size = min(mems)
        max_part_size = max(mems)
        median_part_size = sorted(mems)[len(mems)/2]

        avg_w = sum([len(x.get_inputs()) for x in parts]) / len(parts)

        stats = [ infile, bsc_count, len(ckt),sum(mems), part_count, avg_part_size, min_part_size, max_part_size, median_part_size, avg_w]
        stats = map(lambda x:str(x), stats)

        if args.out is not None:
            with open(args.out, 'ab') as f:
                f.write(",".join(stats))
        else:
            print ",".join(stats)
