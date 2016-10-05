from trojan import Trojan, parasite
from cktnet import read_bench_file, partition_ckt, write_bench_file, random_set
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
parser.add_argument('--partitions', type=str, default=None, help='Use these partitions.')
rand_group.add_argument('--fin', type=int, default=None, help='Fix the number of inputs for trojans.')
rand_group.add_argument('--fot', type=int, default=None, help='Fix the number of output for trojans.')
parser.add_argument('--seed', type=int, default=None, help='Pass a value to fix the seed for RNG for testing.')
rand_group.add_argument('--count', type=int, default=500, help='Number of trojans to generate and add. Defaults to 500')
parser.add_argument('--tests', type=int, default=7000, help='Number of test patterns to make. Defaults to 7000')
parser.add_argument('--w', type=int, default=10, help='Partitions depend on no more than these many inputs.')
parser.add_argument('--pe', dest='pe', action='store_true', help='Generate as many test patterns that are required to bring all inputs to the partition')
parser.set_defaults(feature=False, trojan=True)
parser.add_argument('--notrojan', dest='trojan', action='store_false', help="Don't add Trojans.")
parser.add_argument('--nopart', action='store_true', help='Don\'t generate partitions.')
parser.add_argument('--noinput', action='store_true', help='Don\'t generate inputs.')
parser.add_argument('--fullcapture', action='store_true', help="Only put Trojans inputs/outputs into the same partition")
fixed_group.add_argument('-tc', type=str, default=None, help="Use a random file from these arguments as the trojan instead of generating")

parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='circuit to generate and add trojans to')
partitions = None
args = parser.parse_args()
print args.tc
for infile in args.file:
        if args.tc is not None:
            static_trojan = Trojan()
            tckt, tPIs, tPOs = read_bench_file(args.tc)
            static_trojan.load(tckt)
        ckt, PIs, POs = read_bench_file(infile)
        if not args.nopart:
            ckt, partitions = partition_ckt(ckt, POs, args.w)
            print "Size of widest partition:", max([len(x.get_inputs()) for x in partitions])
        if not args.noinput:
            INPUTS=["bsc","input"] 
            test_inputs = []
            if args.inputs is None:
                if args.pe:                
                    for part in partitions:
                        input_list = list(part.get_inputs())
                        count = 0
                        for r in random_set(len(input_list)):
                            if count >= len(test_inputs):
                                test_inputs.append(dict(zip(input_list, r)))
                            else:
                                test_inputs[count].update(dict(zip(input_list, r)))
                            count = count + 1
                    # fill in holes
                    input_list = list({x for x in ckt if ckt[x].function.lower() in INPUTS})
                    for k in input_list:
                        for t in test_inputs:
                            t.update([{k, int(random.random() > 0.5)} for k in t if not k in t])
                    print "Number of cycles:", len(test_inputs), "partitions: ", len(partitions), len(list({x for x in ckt if ckt[x].function.lower() in INPUTS})
                )
                else:
                    for g in range(0,args.tests):
                        cur_inputs = []
                        input_list = list({x for x in ckt if ckt[x].function.lower() in INPUTS})
                        cur_inputs = ({k: int(random.random() > 0.5) for k in input_list})
                        print "INPUT LIST", input_list
                        test_inputs.append(cur_inputs)
            else:
                f = open(args.inputs)
                packed = pickle.load(f)
                f.close()
                ckt = packed[0]
                PIs = packed[2]
                POs = packed[3]
        if args.outdir is None:
            outdir = ""
        else:
            outdir = args.outdir + "/"
        if args.inputs is None and not args.noinput:
            f = open(outdir+"input/"+"pyTrojan_"+path.basename(infile)+"_inputs.pickle", 'w')
            pickle.dump(test_inputs, f)
            f.close()
        if args.partitions is None and not args.nopart:
            f = open(outdir+"part/"+"pyTrojan_"+path.basename(infile)+"_partitions.pickle", 'w')
            pickle.dump(partitions, f)
            f.close()
        write_bench_file(outdir+"bench/"+"pyTrojan_"+path.basename(infile)+"-ckt.bench",ckt)
        if args.trojan:
            for i in range(0,args.count):
                if args.tc is not None:
                    t = copy.deepcopy(static_trojan)
                else:
                    t = Trojan(fin = args.fin, fot = args.fot, seed = args.seed)
                try: 
                    if args.fullcapture:
                        if partitions is None:
                            f = open(args.partitions, 'rb')
                            partitions = pickle.load(f)
                            f.close()
                        bad_ckt, POs = parasite(copy.deepcopy(ckt), POs, t, part = partitions)
                    else:
                        bad_ckt, POs = parasite(copy.deepcopy(ckt), POs, t)
                    print "Writing ", outdir+"bench/"+"pyTrojan_"+path.basename(infile)+"_"+str(i).zfill(3)+"-badckt.bench"
                    write_bench_file(outdir+"bench/"+"pyTrojan_"+path.basename(infile)+"_"+str(i).zfill(3)+"-badckt.bench",bad_ckt)
                    test_ckt = [ckt, bad_ckt, PIs, POs, t]
                    f = open(outdir+"pyTrojan_"+path.basename(infile)+"_"+str(i).zfill(3)+".pickle", 'w')
                    pickle.dump(test_ckt, f)
                    f.close()
                except Exception:
                    pass
