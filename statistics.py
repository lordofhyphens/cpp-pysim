from cktnet import Gate, Partition, read_bench_file
import get_partitions
import re
import cPickle as pickle
import argparse

parser = argparse.ArgumentParser(description='read partitions from benchmark circuits.')

parser.add_argument('-b, --bench', dest='b', action='store_true', help='Use bench netlists')
parser.add_argument('-p, --partition', dest='partition', default=None, type=str, help='Partition pickle')
parser.set_defaults(b=False)
parser.set_defaults(b=False)
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='circuit to generate and add trojans to')
args = parser.parse_args()

for infile in args.file:
    part = None
    if args.b:
        bad_ckt, PIs, POs = read_bench_file(infile)
    else:
        with open(infile, 'r') as fi:
            packed = pickle.load(fi)

            ckt = packed[0]
            bad_ckt = packed[1]
            PIs = packed[2]
            POs = packed[3]
            t = packed[4]
    if args.partition is None:
        part = get_partitions.get_partition_set(bad_ckt, POs)
    else:
        with open(args.partition, 'r') as pt:
            part = pickle.load(pt)
    print len(part) 
    for p in part:
        if len(p.get_inputs()) < 1:
            all_inputs = [bad_ckt[x].fins for x in p.members]
            all_inputs = reduce(lambda x,y: x+y, all_inputs)
            #print set(all_inputs).difference(set(p.members))
            [x for x in bad_ckt.iterkeys()]
        print p.get_inputs()
    #print bad_ckt

