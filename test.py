from trojan import Trojan, parasite
from cktnet import read_bench_file, partition_ckt
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
parser.add_argument('--partitions', type=str, default=None, help='Override the test inputs (useful for reusing partitions).')
rand_group.add_argument('--fin', type=int, default=None, help='Fix the number of inputs for trojans.')
rand_group.add_argument('--fot', type=int, default=None, help='Fix the number of output for trojans.')
parser.add_argument('--seed', type=int, default=None, help='Pass a value to fix the seed for RNG for testing.')
rand_group.add_argument('--count', type=int, default=500, help='Number of trojans to generate and add. Defaults to 500')
parser.add_argument('--tests', type=int, default=7000, help='Number of test patterns to make. Defaults to 7000')
parser.add_argument('--nopart', action='store_true', help='Don\'t generate partitions.')
fixed_group.add_argument('-tc', type=str, default=None, help="Use a random file from these arguments as the trojan instead of generating")

parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='circuit to generate and add trojans to')

args = parser.parse_args()
print args.tc
for infile in args.file:
        if args.tc is not None:
            static_trojan = Trojan()
            tckt, tPIs, tPOs = read_bench_file(args.tc)
            static_trojan.load(tckt)
        ckt, PIs, POs = read_bench_file(infile)
        if not args.nopart:
            ckt, partitions = partition_ckt(ckt, POs)
        
        bits = randbits(seed=args.seed)
        INPUTS=["input"] if args.nopart else ["bsc","input"] 
        test_inputs = []
        if args.inputs is None:
            for g in range(0,args.tests):
                cur_inputs = []
                if not args.nopart:
                    for part in partitions:
                        input_list = list({x for x in part.members if ckt[x].function.lower() in INPUTS})
                        cur_inputs.append(list(itertools.islice(bits, len(input_list))))
                else:
                    input_list = list({x for x in ckt if ckt[x].function.lower() in INPUTS})
                    cur_inputs.append(list(itertools.islice(bits, len(input_list))))
                test_inputs.append(cur_inputs)
        else:
            f = open(args.inputs)
            packed = pickle.load(f)
            f.close()
            ckt = packed[0]
            PIs = packed[2]
            POs = packed[3]
            

        if args.inputs is None:
            f = open("pyTrojan_"+path.basename(infile)+"_inputs.pickle", 'w')
            pickle.dump(test_inputs, f)
            f.close()
        if args.partitions is None and not args.nopart:
            f = open("pyTrojan_"+path.basename(infile)+"_partitions.pickle", 'w')
            pickle.dump(partitions, f)
            f.close()
        for i in range(0,args.count):
            if args.tc is not None:
                t = copy.deepcopy(static_trojan)
            else:
                t = Trojan(fin = args.fin, fot = args.fot, seed = args.seed)
            bad_ckt, POs = parasite(copy.deepcopy(ckt), POs, t)
            test_ckt = [ckt, bad_ckt, PIs, POs, t]
            f = open("pyTrojan_"+path.basename(infile)+"_"+str(i).zfill(3)+".pickle", 'w')
            pickle.dump(test_ckt, f)
            f.close()
