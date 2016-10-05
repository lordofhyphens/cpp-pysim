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
                   help='circuit to generate and add trojans to')
args = parser.parse_args()

for infile in args.file:
    ckt, PIs, POs = read_bench_file(infile)
    partial_fanin = partial(get_fanin_cone, ckt=ckt, stop_at = ['bsc', 'dff'])
    origins = [ x for x in ckt if ckt[x].function.lower() == "test_point"] + POs
    p = multiprocessing.Pool(10)
    partial_partitions = p.map(partial_fanin, origins)
    p.close()
    p.join()
    partitions = []
    while len(partial_partitions) > 0:
        overlap = False
        tgt = None
        s = partial_partitions.pop()
        for p in partitions:
            if not overlap:
                if len(s.intersection(set(p.members))) > 0:
                    print "Merging", s, "with", p.members
                    print len(s.intersection(set(p.members))), "in common"
                    overlap = True
                    p.members = list(set(p.members) | s)
        if not overlap:
            # new partition object
            print "new Partition from", s
            p = Partition(ckt=ckt)
            p.members = list(s)
            partitions.append(copy.deepcopy(p))
    partitions = map(lambda x: x.update(), partitions)
    f = open(infile+"_partitions.pickle", 'wb')
    pickle.dump(partitions, f)
    f.close()
