from cktnet import Gate, Partition, write_bench_file
import re
import argparse
from itertools import izip

try:
    import cPickle as pickle
except ImportError:
    import pickle

def check_array(results_array, ff_array, mapping):
    for f,ff in izip(results_array, ff_array):
        for k in ff:
            if bool(ff[k]) != bool(f[mapping[k]]):
                return False
    return True

parser = argparse.ArgumentParser(description='Simulate partitions from pickled representations.')

parser.add_argument('-w', action='store_true', help='')
parser.add_argument('ckt', type=str, help='Circuit results file')
parser.add_argument('ff', type=str, help='Fault free results array')
parser.add_argument('tests', metavar='N', type=str, nargs='*',
                   help='results')

args=parser.parse_args()

ckt_file = open(args.ckt, 'r')
ckt_data = pickle.load(ckt_file)
if args.w:
    write_bench_file(args.ckt+"-ckt.bench", ckt_data[0])
    write_bench_file(args.ckt+"-badckt.bench", ckt_data[1])
    exit()

for k in args.tests:
    results_file = open(k, 'r')
    ff_file = open(args.ff, 'r')
    
    results_array = pickle.load(results_file)
    ff_array = pickle.load(ff_file)


    mapping = dict()

    ckt = ckt_data[0]
    bad_ckt = ckt_data[1]
    PIs = ckt_data[2]
    POs = ckt_data[3]
    t = ckt_data[4]

    for i in [x for x in bad_ckt if len(bad_ckt[x].fots) == 0]:
        mapping[i] = i
        if re.search(".*TrojCkt.*", i) is not None:
            for j in bad_ckt[x].fins:
                if re.search(".*TrojCkt.*", i) is not None:
                    mapping[j] = i

    if not check_array(results_array, ff_array, mapping):
        print args.ff, "!=", k


# ckt data - original ckt, trojaned ckt, etc

# results array data -> array of dict of Event objects.
