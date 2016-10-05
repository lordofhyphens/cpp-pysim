from trojan import Trojan, parasite
from cktnet import read_bench_file, write_bench_file
from random_bsc_partition import repartition_ckt
import copy
import argparse
import random
import itertools
import os.path as path
try:
   import cPickle as pickle
except ImportError:
   import pickle

def randbits(seed=None):
    random.seed(seed)
    while True:
        yield random.randint(0,1)
parser = argparse.ArgumentParser(description='Implant random Trojans into benchmark circuits.')
rand_group = parser.add_argument_group(title="Random Trojan Options", description=None) 
fixed_group = parser.add_argument_group(title="Fixed Trojan Options", description=None) 
parser.add_argument('--inputs', type=str, default=None, help='Override the test inputs (useful for reusing partitions).')
parser.add_argument('--outdir', type=str, default=None, help='Specify an output dir.')
rand_group.add_argument('--fin', type=int, default=None, help='Fix the number of inputs for trojans.')
rand_group.add_argument('--fot', type=int, default=None, help='Fix the number of output for trojans.')
parser.add_argument('--seed', type=int, default=None, help='Pass a value to fix the seed for RNG for testing.')
rand_group.add_argument('--count', type=int, default=500, help='Number of trojans to generate and add. Defaults to 500')
parser.add_argument('--tests', type=int, default=7000, help='Number of test patterns to make. Defaults to 7000')
parser.add_argument('--nopart', action='store_true', help='Don\'t generate partitions.')
parser.add_argument('--noinput', action='store_true', help='Don\'t generate inputs.')
fixed_group.add_argument('-tc', type=str, default=None, help="Use a random file from these arguments as the trojan instead of generating")

parser.add_argument('partitions', type=str, help='Override the test inputs (useful for reusing partitions).')
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='circuit to generate and add trojans to')

args = parser.parse_args()
print args.tc
if args.outdir is None:
    outdir = ""
else:
    outdir = args.outdir + "/"
for infile in args.file:
        if args.tc is not None:
            static_trojan = Trojan()
            tckt, tPIs, tPOs = read_bench_file(args.tc)
            static_trojan.load(tckt)
        ckt, PIs, POs = read_bench_file(infile)
        partckt, PIs, POs = read_bench_file(args.partitions)

        bsc_count = len([x for x,y in partckt.iteritems() if y.function.upper() == "BSC"])
        tp_count = len([x for x,y in partckt.iteritems() if y.function.upper() == "TEST_POINT"])
        ckt = repartition_ckt(ckt, bsc_count, tp_count)

        write_bench_file(outdir+"bench/"+"pyTrojan_"+path.basename(infile)+"-ckt.bench",ckt)
        for i in range(0,args.count):
            try:
                if args.tc is not None:
                    t = copy.deepcopy(static_trojan)
                else:
                    t = Trojan(fin = args.fin, fot = args.fot, seed = args.seed)
                bad_ckt, POs = parasite(copy.deepcopy(ckt), POs, t)
                print "Dumping ckt to ", outdir+"/pyTrojan_"+path.basename(infile)+"_"+str(i).zfill(3)+"-badckt.bench"
                write_bench_file(outdir+"bench/"+"pyTrojan_"+path.basename(infile)+"_"+str(i).zfill(3)+"-badckt.bench",bad_ckt)
                test_ckt = [ckt, bad_ckt, PIs, POs, t]
            except Exception:
                pass
        
