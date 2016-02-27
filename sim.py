from cktnet import Gate, Partition
import argparse
import itertools
import re
import copy
try:
   import cPickle as pickle
except ImportError:
   import pickle

class LOG(object):
    DEBUG = 4
    INFO = 3
    ERROR = -1
    WARN = 0


def get_regular_po(gate, ckt):
    if args.verbose > LOG.DEBUG:
        print gate
    a = re.search("__TrojCkt", gate)
    if a is not None:
        for k in ckt[gate].fins:
            a = re.search("__TrojCkt", k)
            if k is None:
                return k
    return gate


_enum_gates = {"AND", "NAND", "OR", "NOR", "BUFF", "XOR", "XNOR", "DFF_OUT", "DFF", "NOT"}
class Event(object):
    """ Encapsulates set of times for a single gate """
    def __init__(self):
        self.data = dict()
    def max(self, t = None):
        if t is None:
            try:
                return self.data[max(self.data)]
            except ValueError:
                return 0
        else:
            try:
                return self.data[max(x for x in self.data if x <= t)]
            except ValueError:
                return 0
            except KeyError:
                return 0
    def __add__(self, x):
        """ Combine two Event objects together """
        self.data.update(x.data)
        return self
    def filter_unused(self, t):
        self.data = {x:self.data[x] for x in self.data if x in t}
    def __getitem__(self, key, **args):
        if key in self.data:
            return self.data[key]
        return 0

    def __setitem__(self, key,value, **args):
        self.data[key] = value
    def now(self, t):
        return t in self.data

class PySim(object):
    def __init__(self, ckt, inputs, partition = None):
        self.ckt = ckt
        self.partitions = partition
        self.inputs = inputs
        self.result = dict() # key: gate names from ckt; value: Event object
        self.outputs = []
        for g in ckt:
            self.result[g] = Event()
        self.cycle = 0
        self.cycles = []
        self.bist = partition is not None
        self.t = 0
        self.current_queue = dict()
        self.next_queue = []
        self.partitions = map(lambda x: x.get_inputs(), self.partitions) if self.bist else [[x for x in self.ckt if self.ckt[x].function.lower() == "input"]]
        self.total_cycles = len(self.inputs)
        self.sim_cycle()

    def sim_cycle(self):
        if args.verbose > LOG.INFO:
            print "Getting next set of PIs"
        self.current_queue = dict()
        if self.t not in self.current_queue:
            self.current_queue[self.t] = set()
        self.cycles.append(self.t)
        z = self.inputs.pop(0)
        self.outputs.append({x:self.result[x].max() for x in self.result if self.ckt[x].function.upper() in ["TP"] or len(self.ckt[x].fots) == 0})
        self.result = dict()
        for g in ckt:
            self.result[g] = Event()
        assignments = itertools.izip(self.partitions, z)
        if args.verbose > LOG.INFO:
            print self.partitions
        for k,v in assignments:
            for inp in zip(k,v):
                self.result[inp[0]][self.t] = inp[1]
                self.current_queue[self.t].add(inp[0])
        if args.verbose > LOG.INFO:
            output = {x:self.result[x].max(self.t) for x in self.result if self.ckt[x].function in "TP" or len(self.ckt[x].fots) == 0}
            output = {get_regular_po(x, self.ckt):y for x, y in output.iteritems()}
            print "Outputs at time ", self.t, output
        self.cycle = self.cycle + 1
        

    def sim_next(self):
        if self.t in self.current_queue:
            for g in self.current_queue[self.t]:
                if args.verbose > LOG.DEBUG:
                    print "Simming", g
                try:
                    next_t = self.ckt[g].delay + self.t
                except TypeError:
                    next_t = self.t + 1
                if next_t not in self.current_queue:
                    if args.verbose > LOG.INFO:
                        print "making new queue", next_t
                    self.current_queue[next_t] = set()
                for fot in self.ckt[g].fots:
                    self.current_queue[next_t].add(fot)
                self.result[g][self.t] = self.gates(g)
        self.t = self.t + 1
    def run(self):
        while(self.cycle < self.total_cycles+1):
            if self.cycle % 100 == 0:
                print "cycle: ", self.cycle
            while(self.t <= max(self.current_queue.iterkeys())):
                if args.verbose > LOG.INFO:
                    print "t: ", self.t
                self.sim_next()
            try:
                self.sim_cycle()
            except IndexError:
                self.cycle = self.cycle+1
    def gates(self, g):
        gate = self.ckt[g]
        result = 0 # default value
        if gate.function.upper() in {"INPUT", "BSC"}:
            result = self.result[g].max(self.t)
        if args.verbose > LOG.DEBUG:
            print "Inputs:", gate.fins
        if gate.function.upper() in {"NAND", "AND"}:
            result = all([self.result[x].max(self.t) for x in gate.fins]) 
        if gate.function.upper() in {"NOR", "OR", "NOT", "BUFF"}:
            result = any([self.result[x].max(self.t) for x in gate.fins])
        if gate.function.upper() in {"XNOR", "XOR"}:
            result = (([self.result[x].max(self.t) for x in gate.fins].count(1) % 2) == 1)
        if gate.function.upper() in {"NOR", "NAND", "NOT", "XNOR"}:
            result = 0 if result else 1
        if args.verbose > LOG.DEBUG:
            print "Gate:", gate.function.upper(), [self.result[x].max(self.t) for x in gate.fins], result
        return result

parser = argparse.ArgumentParser(description='Simulate partitions from pickled representations.')

parser.add_argument('--ff', action='store_true', help='Output fault-free response')
parser.add_argument('--parts', type=str, default=None, help='Partition pickle')
parser.add_argument('--verbose', type=str, default=0, help='Verbosity level, defaults to 0')
parser.add_argument('tests', type=str, help='Test input pickle')
parser.add_argument('pickled_file', metavar='N', type=str, nargs='+',
                   help='pickled files')

args=parser.parse_args()
f = open(args.tests, 'r')
test_inputs = pickle.load(f)
f.close()
print args.ff

if args.parts is not None:
    f = open(args.parts, 'r')
    partitions = pickle.load(f)
    f.close()

for f in args.pickled_file:
    with open(f, 'r') as fi:
        packed = pickle.load(fi)

        ckt = packed[0]
        bad_ckt = packed[1]
        PIs = packed[2]
        POs = packed[3]
        t = packed[4]

        to_sim = ckt if args.ff else bad_ckt
        sim_element = PySim(to_sim, copy.deepcopy(test_inputs), None) if (args.parts is None) else PySim(to_sim, copy.deepcopy(test_inputs), copy.deepcopy(partitions))
        sim_element.run()
        if args.ff:
            outfile = open("results_"+f+"_ff",'w')
        else:
            outfile = open("results_"+f,'w')
        pickle.dump(sim_element.outputs, outfile)
        outfile.close()
