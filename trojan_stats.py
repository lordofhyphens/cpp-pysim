#!/usr/bin/python
import argparse
import re
from cktnet import Partition, read_bench_file
try:
    import cPickle as pickle
except ImportError:
    import pickle


def hasTrojanFanin(x):
    s = 0
    for i in x.fins:
        if (re.search("__TrojCkt", i) is not None):
            s = s + 1
    return s

def hasTrojanFanout(x):
    s = 0
    for i in x.fots:
        if (re.search("__TrojCkt", i) is not None):
            s = s + 1
    return s

def getBSCs(ckt, p):
    a = []
    all_members = [ckt[x].fins for x in p.members]
    if len(all_members) > 0:
        for l in all_members:
            if type(l) is list:
                a.extend(l)
            else:
                a.append(l)
    else:
        a = all_members
    return filter(lambda x: ckt[x].function == "bsc", a)
parser = argparse.ArgumentParser(description="Generate some statistics about trojans in a partition")

parser.add_argument('--csv', type=str, default=None, help="output to a csv file, default is to print to stdout")
parser.add_argument('--append', action='store_true', default=False, help="append to csv file instead of overwriting.")
parser.add_argument('partition', type=str, help="partition file")
parser.add_argument('files', metavar='F', type=str, nargs='+', help="Trojan-infectect circuits")
args = parser.parse_args()

"""

Iterate over all infected circuits.  In each infected circuit, count the
inputs/outputs of the Trojan in the partition. Check each partition in the 
infected circuit.

"""

partition_file = open(args.partition, 'rb')
partitions = pickle.load(partition_file)

for f in args.files:
    ckt, PIs, POs = read_bench_file(f)
    for p in partitions:
        # If this gate is a test point, only check the fan-ins
        # else, check all fanins and fanouts in the ckt for a 
        # gate with the name of "Troj"
        bscs = getBSCs(ckt, p)
        troj_fots = reduce(lambda x,y: x+y, map(hasTrojanFanout, [ckt[x] for x in p.members if ckt[x].function is not "test_point"]), 0)
        if troj_fots > 0:
            lot = zip(p.members, map(hasTrojanFanout, [ckt[x] for x in p.members if ckt[x].function is not "test_point"]))
        #troj_fots = troj_fots + reduce(lambda x,y: x+y, map(hasTrojanFanout, [ckt[x] for x in bscs]), 0)
        troj_fins = reduce(lambda x,y: x+y, map(hasTrojanFanin, [ckt[x] for x in p.members]), 0) 
        if troj_fins > 0:
            lin = zip(p.members, map(hasTrojanFanin, [ckt[x] for x in p.members]))
        if troj_fins > 0:
            print "Fins in partition", p.members, ": ", troj_fins
            print lin
        if troj_fots > 0:
            print "Fots in partition", p.members, ": ", troj_fots
            print lot

if args.csv is not None:
    if args.append:
        temp_csv = open(args.csv, 'ab')
    else:
        temp_csv = open(args.csv, 'wb')
    csv_out = csv.DictWriter(temp_csv, fieldnames=fieldnames)
    if not args.append:
        csv_out.writeheader()
if args.csv is not None:
    temp_csv.close()
