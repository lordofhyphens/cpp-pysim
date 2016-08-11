from cktnet import Gate, Partition, read_bench_file
import EventSim
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
        self.current_queue = dict()
        if self.t not in self.current_queue:
            self.current_queue[self.t] = set()
        self.cycles.append(self.t)
        z = self.inputs.pop(0)
        self.outputs.append({x:self.result[x].max() for x in self.result if self.ckt[x].function.upper() in ["TEST_POINT"] or len(self.ckt[x].fots) == 0})
        self.__reinit_results()
        for k, v in z.iteritems():
            try:
                self.result[k][self.t] = v
                self.current_queue[self.t].add(k)
            except KeyError:
                print "ID not in ckt"
        self.cycle = self.cycle + 1
        self.timeout = len(self.ckt)
        

    def sim_next(self):
        if self.t in self.current_queue:
            for g in self.current_queue[self.t]:
                try:
                    next_t = self.ckt[g].delay + self.t
                except TypeError:
                    next_t = self.t + 1
                if next_t not in self.current_queue:
                    self.current_queue[next_t] = set()
                for fot in self.ckt[g].fots:
                    self.current_queue[next_t].add(fot)
                assert(g in self.result)
                self.result[g][self.t] = self.gates(g)

        self.t = self.t + 1
    def run(self):
        self.timeout = len(self.ckt)
        while(self.cycle < self.total_cycles+1):
            while(self.t <= max(self.current_queue.iterkeys()) and self.timeout > 0):
                self.sim_next()
                self.timeout = self.timeout - 1
            if self.timeout <= 0:
                print "Timeout reached, cycles present"

            try:
                self.sim_cycle()
            except IndexError:
                self.cycle = self.cycle+1
    def gates(self, g):
        gate = self.ckt[g]
        gate.function = gate.function.upper()
        result = 0 # default value
        if gate.function == "INPUT":
            result = self.result[g].max(self.t)
        elif gate.function == "BSC":
            if self.bist:
                result = self.result[g].max(self.t)
            else:
                result = self.result[gate.fins[0]].max(self.t)
        elif gate.function == "NAND":
            result = int(all([self.result[x].max(self.t) for x in gate.fins])) 
            result = 0 if result else 1
        elif gate.function == "AND":
            result = int(all([self.result[x].max(self.t) for x in gate.fins])) 
        elif gate.function == "NOR" or gate.function == "NOT":
            result = int(any([self.result[x].max(self.t) for x in gate.fins]))
            result = 0 if result else 1
        elif gate.function == "OR" or gate.function == "BUFF" or gate.function == "BUF" or gate.function == "TEST_POINT":
            result = int(any([self.result[x].max(self.t) for x in gate.fins]))
        elif gate.function == "XNOR":
            result = (([self.result[x].max(self.t) for x in gate.fins].count(1) % 2) == 1)
            result = 0 if result else 1
        elif gate.function == "XOR":
            result = (([self.result[x].max(self.t) for x in gate.fins].count(1) % 2) == 1)
        return result
    def dump(self, filename):
        with open(filename, 'w') as outfile:
            for c in self.cycles:
                pass


class CppPySim(PySim):
    adapt = {
        "AND": EventSim.gate_t_AND,
        "NAND": EventSim.gate_t_NAND,
        "OR": EventSim.gate_t_OR,
        "NOR": EventSim.gate_t_NOR,
        "XOR": EventSim.gate_t_XOR,
        "XNOR": EventSim.gate_t_XNOR,
        "BUFF": EventSim.gate_t_BUFF,
        "BUF": EventSim.gate_t_BUFF,
        "NOT": EventSim.gate_t_NOT,
        "OUTPUT": EventSim.gate_t_OUTPUT,
        "DUMMY": EventSim.gate_t_DUMMY,
        "BSC": EventSim.gate_t_BSC,
        "TEST_POINT": EventSim.gate_t_TP,
        "INPUT" : EventSim.gate_t_INPUT,
        "DFF_O" : EventSim.gate_t_DFF_O,
        "DFF" : EventSim.gate_t_DFF
        }
    def __init__(self, ckt, inputs, partition = None, cycles = None, bist = None):
        """ instantiate the EventSim """
        bist = True if bist is not None else False
        self.ckt = ckt
        self.sim = EventSim.EventSim(int(args.verbose))
        self.sim.bist = bist
        self.outputs = []
        self.inputs = inputs 
        for k, v in ckt.iteritems():
            # convert to Gate objects
            f1 = EventSim.StringVector(list(set(v.fins)))
            f2 = EventSim.StringVector(list(set(v.fots)))
            if v.function.upper() is "DFF":
                # Add the DFF
                g = EventSim.Gate(CppPySim.adapt[v.function.upper()], v.name, f1, Eventsim.StringVector([]), v.delay, True, False)
                self.sim.add_gate(g)
                # Add the DFF_O
                g = EventSim.Gate(CppPySim.adapt[v.function.upper()], v.name + "_O", v.name, EventSim.StringVector([]), f2, 0, False, False)
                self.sim.add_gate(g)
            else:
                g = EventSim.Gate(CppPySim.adapt[v.function.upper()], v.name, f1, f2, v.delay, len(v.fots) == 0, (len(v.fots) == 0 and v.function.upper() != "TEST_POINT"))
                self.sim.add_gate(g)
        k = 0
        for v in inputs:
            for g, i in v.iteritems():
                self.sim.add_to_inputs(k,g,bool(i))
            k = k + 1
    def run(self, filename):
        self.sim.run(filename)
    def dump(self, filename):
        self.sim.dump_results(str(filename))



def start_(f, args, test_inputs, partitions):
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
        print args.verbose, LOG.DEBUG
        if args.verbose > LOG.DEBUG:
            for k,g in to_sim.iteritems():
                print k,str(g)
        sim_element = CppPySim(to_sim, copy.deepcopy(test_inputs), None, cycles=args.cycles, bist=args.bist) if (args.parts is None) else PySim(to_sim, copy.deepcopy(test_inputs), copy.deepcopy(partitions), cycles=args.cycles, bist=args.bist)
        f = re.sub("bench/","", f)
        output_name = ""
        if args.ff:
            output_name = "results_"+f+"_ff"
        else:
            output_name = "results_"+f
        sim_element.run(output_name)
        print "Finished ", f


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
    if args.cycles is not None:
        test_inputs = test_inputs[:args.cycles]
    f.close()
    print args.ff

    if args.parts is not None:
        f = open(args.parts, 'r')
        partitions = pickle.load(f)
        f.close()
    else:
        partitions = None
#    pool = Pool(processes=4)  
    for f in args.pickled_file:
        start_(f, args, test_inputs, partitions)
#        pool.apply_async(start_, (f,args,test_inputs, partitions))
#    pool.close()
#    pool.join()


