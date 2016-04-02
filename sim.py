from cktnet import Gate, Partition, read_bench_file
import argparse
import itertools
import re
import copy
from multiprocessing import Pool, TimeoutError
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
    def __init__(self, ckt, inputs, partition = None, cycles = None, bist = None):
        self.ckt = ckt
        self.partitions = partition
        self.inputs = inputs
        self.result = dict() # key: gate names from ckt; value: Event object
        self.outputs = []
        print "Initializing result dict;"
        for g in ckt:
            self.result[g] = Event()
        self.cycle = 0
        self.cycles = []
        if bist is not None:
            self.bist = bist
        else:
            self.bist = partition is not None

        self.t = 0
        self.current_queue = dict()
        self.next_queue = []
        self.partitions = map(lambda x: x.get_inputs(), self.partitions) if (partition is not None) else [[x for x in self.ckt if self.ckt[x].function.lower() == "input"]]
        if cycles is not None:
            self.total_cycles = min(cycles, len(self.inputs))
        else:
            self.total_cycles = len(self.inputs)
        self.sim_cycle()

    def __reinit_results(self):
        self.result = dict()
        for g in self.ckt:
            self.result[g] = Event()

    def sim_cycle(self):
        if args.verbose > LOG.INFO:
            print "Getting next set of PIs"
        self.current_queue = dict()
        if self.t not in self.current_queue:
            self.current_queue[self.t] = set()
        self.cycles.append(self.t)
        z = self.inputs.pop(0)
        self.outputs.append({x:self.result[x].max() for x in self.result if self.ckt[x].function.upper() in ["TEST_POINT"] or len(self.ckt[x].fots) == 0})
        if args.verbose > LOG.INFO:
            output = {x:self.result[x].max(self.t) for x in self.result if self.ckt[x].function in "TEST_POINT" or len(self.ckt[x].fots) == 0}
            output = {get_regular_po(x, self.ckt):y for x, y in output.iteritems()}
            print "Outputs at time ", self.t, output
        self.__reinit_results()
        if args.verbose > LOG.INFO:
            print self.partitions
        for k, v in z.iteritems():
            try:
                self.result[k][self.t] = v
                self.current_queue[self.t].add(k)
            except KeyError:
                if args.verbose >= LOG.WARN:
                    print "ID not in ckt"
        self.cycle = self.cycle + 1
        self.timeout = len(self.ckt)
        

    def sim_next(self):
        if self.t in self.current_queue:
            for g in self.current_queue[self.t]:
                if args.verbose > LOG.DEBUG:
                    print "Simming", g
                    print "Gate:", str(g)
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
                assert(g in self.result)
                self.result[g][self.t] = self.gates(g)

        self.t = self.t + 1
    def run(self):
        self.timeout = len(self.ckt)
        while(self.cycle < self.total_cycles+1):
            if self.cycle % 100 == 0:
                print "cycle: ", self.cycle
            while(self.t <= max(self.current_queue.iterkeys()) and self.timeout > 0):
                if args.verbose > LOG.INFO:
                    print "t: ", self.t
                self.sim_next()
                self.timeout = self.timeout - 1
            if self.timeout <= 0:
                if args.verbose >= LOG.WARN:
                    print "Timeout reached, cycles present"

            if args.verbose > LOG.INFO:
                print "cycle: ", self.cycle
            try:
                self.sim_cycle()
            except IndexError:
                self.cycle = self.cycle+1
    def gates(self, g):
        gate = self.ckt[g]
        print "Processing", g, gate.function
        result = 0 # default value
        if gate.function.upper() in {"INPUT", "BSC"}:
            if self.bist or gate.function.upper() in {"INPUT"}:
                result = self.result[g].max(self.t)
            else:
                result = self.result[gate.fins[0]].max(self.t)
        if gate.function.upper() in {"NAND", "AND"}:
            result = int(all([self.result[x].max(self.t) for x in gate.fins])) 
        if gate.function.upper() in {"NOR", "OR", "NOT", "BUFF", "TEST_POINT"}:
            result = int(any([self.result[x].max(self.t) for x in gate.fins]))
        if gate.function.upper() in {"XNOR", "XOR"}:
            result = (([self.result[x].max(self.t) for x in gate.fins].count(1) % 2) == 1)
        if gate.function.upper() in {"NOR", "NAND", "NOT", "XNOR"}:
            result = 0 if result else 1
        if args.verbose > LOG.DEBUG:
            print "Gate:", gate.function.upper(), [self.result[x].max(self.t) for x in gate.fins], result
        return result

def start_(f, args, test_inputs, partitions):
    print "Testing ckt", f
    with open(f, 'r') as fi:
        if args.b:
            ckt, PIs, POs = read_bench_file(args.ckt)
            bad_ckt, bad_PIs, bad_POs = read_bench_file(f)
        else:
            packed = pickle.load(fi)

            ckt = packed[0]
            bad_ckt = packed[1]
            PIs = packed[2]
            POs = packed[3]

        to_sim = ckt if args.ff else bad_ckt
        if args.verbose > LOG.DEBUG:
            for k,g in to_sim.iteritems():
                print k,str(g)
        sim_element = PySim(to_sim, copy.deepcopy(test_inputs), None, cycles=args.cycles, bist=args.bist) if (args.parts is None) else PySim(to_sim, copy.deepcopy(test_inputs), copy.deepcopy(partitions), cycles=args.cycles, bist=args.bist)
        sim_element.run()
        if args.cycles is not None:
            for k in test_inputs[0:args.cycles]:
                print k
        else:
            print test_inputs
        f = re.sub("bench/","", f)
        if args.ff:
            outfile = open("results_"+f+"_ff",'w')
        else:
            outfile = open("results_"+f,'w')
        if args.verbose > LOG.DEBUG:
            for k in sim_element.outputs[1:len(sim_element.outputs)]:
                print k
        pickle.dump(sim_element.outputs, outfile)
        outfile.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simulate partitions from pickled representations.')

    parser.add_argument('--ff', action='store_true', help='Output fault-free response')
    parser.add_argument('--parts', type=str, default=None, help='Partition pickle')
    parser.add_argument('--verbose', type=str, default=0, help='Verbosity level, defaults to 0')
    parser.add_argument('-b', action='store_true', help="Treat as benchmark netlists, not pickled")
    parser.add_argument('--ckt', type=str, help="ckt benchmark netlist")
    parser.add_argument('--bist', action='store_true', help="Simulate with partition support")
    parser.add_argument('--cycles', type=int, default=None, help="ckt benchmark netlist")
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
    else:
        partitions = None
    pool = Pool(processes=8)  
    for f in args.pickled_file:
        pool.apply_async(start_, (f,args,test_inputs, partitions))


