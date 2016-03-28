from cktnet import Gate, Partition
import re
import cPickle as pickle
import argparse

parser = argparse.ArgumentParser(description='readpartitions from benchmark circuits.')
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='circuit to generate and add trojans to')
args = parser.parse_args()

for infile in args.file:
    with open(infile, 'r') as fi:
        packed = pickle.load(fi)

        ckt = packed[0]
        bad_ckt = packed[1]
        PIs = packed[2]
        POs = packed[3]
        t = packed[4]

    print bad_ckt
