from trojan import Trojan, parasite
from cktnet import read_bench_file, partition_ckt
import argparse
try:
   import cPickle as pickle
except ImportError:
   import pickle


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='circuit to partition')

args = parser.parse_args()
print args.file

ckt, PIs, POs = read_bench_file(args.file)
ckt, partitions = partition_ckt(ckt, POs)
for i in range(0,500):
    t = Trojan()
    bad_ckt, POs = parasite(ckt, POs, t)
    test_ckt = [bad_ckt, PIs, POs, partitions, t]
    f = open("pyTrojan_"+str(i).zfill(3)+".pickle", 'w')
    pickle.dump(test_ckt, f)
    f.close()
