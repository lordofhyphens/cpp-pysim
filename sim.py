from cktnet import Gate, Partition
import argparse
import itertools
try:
   import cPickle as pickle
except ImportError:
   import pickle

_enum_gates = {"AND", "NAND", "OR", "NOR", "BUFF", "XOR", "XNOR", "DFF_OUT", "DFF", "NOT"}

class PySim(object):
    def init(self, ckt, partition, inputs):
        self.ckt = ckt
        self.partitions = partition
        self.inputs = inputs
        self.result = dict()

    def sim_cycle():
        """ clear result queue and pull the next input set off of the main array."""

    def sim_next():
        pass

parser = argparse.ArgumentParser(description='Simulate partitions from pickled representations.')
parser.add_argument('partitions', type=str, nargs=1, help='Partition pickle')
parser.add_argument('tests', type=str, nargs=1, help='Test input pickle')
parser.add_argument('pickled_file', metavar='N', type=str, nargs='+',
                   help='pickled files')

args=parser.parse_args()

f = open(args.tests, 'r')
test_inputs = pickle.load(f)
f.close()
f = open(args.partitions, 'r')
partitions = pickle.load(f)
f.close()
for f in args.pickled_file:
    f = open(f, 'r')
    packed = pickle.load(f)
    f.close()

    ckt = packed[0]
    bad_ckt = packed[1]
    PIs = packed[2]
    POs = packed[3]
    t = packed[4]
    partint = map(lambda x: x.get_inputs(), partitions)
    
    for z in test_inputs:
        assignments = itertools.izip(partint, z)
        for k,v in assignments:
            print list(zip(k,v))
        



