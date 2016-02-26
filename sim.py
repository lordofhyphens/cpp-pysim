from cktnet import Gate, Partition
import argparse
import itertools
import re
try:
   import cPickle as pickle
except ImportError:
   import pickle

def get_regular_po(gate, ckt):
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
        for g in ckt:
            self.result[g] = Event()
        self.cycle = 0
        self.bist = partition is not None
        self.t = 0
        self.current_queue = dict()
        self.current_queue[0] = set()
        self.next_queue = []
        self.partitions = map(lambda x: x.get_inputs(), self.partitions) if self.bist else [[x for x in self.ckt if self.ckt[x].function.lower() == "input"]]
        self.total_cycles = len(self.inputs)
        self.sim_cycle()

    def sim_cycle(self):
        print "Getting next set of PIs"
        if self.t not in self.current_queue:
            self.current_queue[self.t] = set()

        z = self.inputs.pop(0)
        assignments = itertools.izip(self.partitions, z)
        print self.partitions
        for k,v in assignments:
            for inp in zip(k,v):
                print inp
                self.result[inp[0]][self.t] = inp[1]
                self.current_queue[self.t].add(inp[0])
                print k
        output = {x:self.result[x].max(self.t) for x in self.result if self.ckt[x].function in "TP" or len(self.ckt[x].fots) == 0}
        output = {get_regular_po(x, ckt):y for x, y in output.iteritems()}
        print "Outputs at time ", self.t, output
        self.cycle = self.cycle + 1

    def sim_next(self):
        if self.t in self.current_queue:
            for g in self.current_queue[self.t]:
                print "Simming", g

                try:
                    next_t = self.ckt[g].delay + self.t
                except TypeError:
                    next_t = self.t + 1
                if next_t not in self.current_queue:
                    print "making new queue", next_t
                    self.current_queue[next_t] = set()
                for fot in self.ckt[g].fots:
                    self.current_queue[next_t].add(fot)
                self.result[g][self.t] = self.gates(g)
        self.t = self.t + 1
    def run(self):
        while(self.cycle < self.total_cycles+1):
            print "t: ", self.t
            while(self.t <= max(self.current_queue.iterkeys())):
                print "t: ", self.t
                self.sim_next()
            output = {x:self.result[x].max() for x in self.result if self.ckt[x].function in "TP" or len(self.ckt[x].fots) == 0}
            output = {get_regular_po(x, ckt):y for x, y in output.iteritems()}
            try:
                self.sim_cycle()
            except IndexError:
                self.cycle = self.cycle+1
    def gates(self, g):
        gate = self.ckt[g]
        result = 0 # default value
        if gate.function.upper() in {"INPUT", "BSC"}:
            result = self.result[g].max(self.t)
        print "Inputs:", gate.fins
        if gate.function.upper() in {"NAND", "AND"}:
            result = all([self.result[x].max(self.t) for x in gate.fins]) 
        if gate.function.upper() in {"NOR", "OR", "NOT", "BUFF"}:
            result = any([self.result[x].max(self.t) for x in gate.fins])
        if gate.function.upper() in {"XNOR", "XOR"}:
            result = (([self.result[x].max(self.t) for x in gate.fins].count(1) % 2) == 1)
        if gate.function.upper() in {"NOR", "NAND", "NOT", "XNOR"}:
            result = 0 if result else 1
        print "Gate:", gate.function.upper(), [self.result[x].max(self.t) for x in gate.fins], result
        return result

parser = argparse.ArgumentParser(description='Simulate partitions from pickled representations.')

parser.add_argument('--ff', action='store_true', help='Output fault-free response')
parser.add_argument('--parts', type=str, default=None, help='Partition pickle')
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
    f = open(f, 'r')
    packed = pickle.load(f)
    f.close()

    ckt = packed[0]
    bad_ckt = packed[1]
    PIs = packed[2]
    POs = packed[3]
    t = packed[4]

    to_sim = ckt if args.ff else bad_ckt
    sim_element = PySim(to_sim, test_inputs, None) if (args.parts is None) else PySim(to_sim, test_inputs, partitions)
    sim_element.run()
    output = {x:sim_element.result[x].max() for x in sim_element.result if sim_element.ckt[x].function in "TP" or len(sim_element.ckt[x].fots) == 0}
    output = {get_regular_po(x, ckt):y for x, y in output.iteritems()}
    print output
    print [ckt[x].function for x in ckt]

