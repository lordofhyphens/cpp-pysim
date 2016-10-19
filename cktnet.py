#!/usr/bin/python
import re
import random
import copy
from random import choice
from operator import itemgetter
import argparse
import KLPart

import EventSim
import multiprocessing
from functools import partial
from itertools import izip, product

def convert_Gate(ckt, partfile):
    adapt = {
        "AND": EventSim.AND,
        "NAND": EventSim.NAND,
        "OR": EventSim.OR,
        "NOR": EventSim.NOR,
        "XOR": EventSim.XOR,
        "XNOR": EventSim.XNOR,
        "BUFF": EventSim.BUFF,
        "BUF": EventSim.BUFF,
        "NOT": EventSim.NOT,
        "OUTPUT": EventSim.OUTPUT,
        "DUMMY": EventSim.DUMMY,
        "BSC": EventSim.BSC,
        "TEST_POINT": EventSim.TP,
        "INPUT" : EventSim.INPUT,
        "DFF_O" : EventSim.DFF_O,
        "DFF" : EventSim.DFF
        }

    for k, v in ckt.iteritems():
        # convert to Gate objects
        f1 = KLPart.StringVector(list(set(v.fins)))
        f2 = KLPart.StringVector(list(set(v.fots)))
        if v.function.upper() is "DFF":
            # Add the DFF
            g = EventSim.Gate(adapt[v.function.upper()], v.name, f1, Eventsim.StringVector([]), v.delay, True, False)
            partfile.add_gate(g)
            # Add the DFF_O
            g = EventSim.Gate(adapt[v.function.upper()], v.name + "_O", v.name, KLPart.StringVector([]), f2, 0, False, False)
            partfile.add_gate(g)
        else:
            g = EventSim.Gate(adapt[v.function.upper()], v.name, f1, f2, v.delay, len(v.fots) == 0, (len(v.fots) == 0 and v.function.upper() != "TEST_POINT"))
            partfile.add_gate(g)

def mssl(x):
    max_ending_here = max_so_far = 0
    index = 0
    for c,b,a in x:
        max_ending_here = max(0, max_ending_here + a)
        max_so_far = max(max_so_far, max_ending_here)
        index = index + 1
    return (max_ending_here, index-1)

def find_bscs(ckt, a):
    """ Return all of the gates that are a fan-in to thortpartition. """
    return reduce(lambda x, y: x | y, [ckt[x].fins for x in a]).difference(set(a))

def get_inputs(ckt, a):
    """ Return all of the gates that are a fa, n-in to this partition or are a primary input"""
    return find_bscs(ckt, a) | set([x for x in a if ckt[x].function.lower() in ['input']])


def find_tps(ckt, a):
    """ Return all of the gates that are a have a fan-out not in this partition. """
    return set([x for x in a if ckt[x].fots.isdisjoint(set(a))])

def find_dv(v, ckt, a, b):
    I = len((ckt[v].fins.intersection(a) | ckt[v].fots.intersection(a)) - set(v))
    E = len((ckt[v].fins.intersection(b) | ckt[v].fots.intersection(b)) - set(v))
    return (v, E - I)

def gain(ckt, a, b, d):
    c_ab = 1 if a in ckt[b].fins or a in ckt[b].fots or b in ckt[a].fins or b in ckt[a].fots else 0
    return d[a] + d[b] - 2 * c_ab

def maxgain(g):
    return g[2]

def pack_gain(x, ckt, dv):
    return (x[0], x[1], gain(ckt, x[0], x[1], dv))
def getKey(x):
    return x[2]

def getD(x):
    return x[1]

def sorted_gain(a, b, ckt):
    c_ab = 1 if a[0] in ckt[b[0]].fins or a[0] in ckt[b[0]].fots or b[0] in ckt[a[0]].fins or b[0] in ckt[a[0]].fots else 0
    return a[1] + b[1] - 2 * c_ab

def partition(ckt, gates):
    c = 0
    if len(gates) % 2 > 0:
        print "Adding dummy node for balancing purposes."
        ckt["___PART_DUMMY___"] = Gate("___PART_DUMMY___")
        ckt["___PART_DUMMY___"].function="DUMMY"
        gates.append("___PART_DUMMY___")
    a = set(gates[0:int(round(len(gates)/2))])
    b = set(gates[int(round(len(gates)/2)):])
    a_fixed = set()
    b_fixed = set()
    g_sum = 99999999
    prev_gsum = None
    pool = multiprocessing.Pool(8)
    swap_count = dict()
    while g_sum > 0 and prev_gsum != g_sum:
        tmp_a = copy.deepcopy(a)
        tmp_b = copy.deepcopy(b)
        Gm = []
        a_fixed = set()
        b_fixed = set()
        
        print "GSUM:", g_sum
        while len(a_fixed) < len(a) and len(b_fixed) < len(b):
            print c, "Set lengths:", len(a_fixed), len(a), len(b_fixed), len(b)
            print "Update gain/dv queue:", len(tmp_a - a_fixed), len(tmp_b - b_fixed)
            dv_func_a = partial(find_dv, ckt=ckt, b = b, a = a)
            dv_func_b = partial(find_dv, ckt=ckt, b = a, a = b)
            print c, ": Computing Dv for a, b"
            a_dv = pool.map(dv_func_a, tmp_a - a_fixed)
            b_dv = pool.map(dv_func_b, tmp_b - b_fixed)
            a_dv = sorted(a_dv, key=getD, reverse=True)
            b_dv = sorted(b_dv, key=getD, reverse=True)
            print c, ": Computing max gain"
            max_gain = (None, None, -999999)
            for j,k in izip(a_dv, b_dv):
                tmp = sorted_gain(j,k, ckt)
                if tuple(sorted([j[0], k[0]])) in swap_count:
                    continue # don't use this
                if max_gain[2] > tmp:
                    break
                else:
                    max_gain = (j[0], k[0], tmp)
            if None in max_gain:
                a_fixed |= tmp_a
                b_fixed |= tmp_b
                continue 
            t = max_gain
            Gm.append(t)
            print "Trying swap of ", t[0], "<->", t[1], " gain ", t[2]
            
            tmp_a.remove(t[0])
            tmp_b.remove(t[1])
            tmp_a.add(t[1])
            tmp_b.add(t[0])
            a_fixed.add(t[1])
            b_fixed.add(t[0])
            c = c + 1
        pre_gsum = g_sum
        g_sum, idx = mssl(Gm)
        print "Finished swapping cycle ", c, " g_sum ", g_sum
        if g_sum > 0:
            print "Max Gm", g_sum
            for t in Gm[:idx]:
                a.remove(t[0])
                a.add(t[1])
                b.remove(t[1])
                b.add(t[0])
                swap_count[tuple(sorted([t[0],t[1]]))] = 1

    pool.close()
    pool.join()
    return (list(a), list(b))

def part_recur(ckt, initial, w):
    """ Recursive descent to subdivide partitions that violate w """
    partition_set = []
#    partition_mech = KLPart.KLPartition()
#    convert_Gate(ckt, partition_mech)
    print "Diving into C++"
#    (a, b) = partition_mech.partition_once(KLPart.StringVector(list(set(initial))))
    (a, b) = partition(ckt, list(set(initial)))
    print "Coming back up"
    if len(get_inputs(ckt, a)) > w:
        partition_set = partition_set + part_recur(ckt, a, w)
    else:
        partition_set.append(a)
    if len(get_inputs(ckt, b)) > w:
        partition_set = partition_set + part_recur(ckt, b, w)
    else:
        partition_set.append(b)
    return partition_set

class Gate(object):
    _delay = {"AND": 5, "OR": 5, "INPUT": 0}
    def __init__(self, name, function = None):
        self.function = function
        self.name = name
        self.fins = set()
        self.fots = set()
        self.bscs = []
        self.tps = [] # test points
        self.gateid = 0
        self.delay = 1
    def __str__(self):
        return self.name + ": " + str(self.function) + ", " + str(self.fins) + "," + str(self.fots)

def gen_bsc():
   i = 0
   while True:
      g = Gate("__BSC_%d" % (i)) 
      g.function = "bsc"
      yield g
      i = i + 1

def gen_test_points():
   i = 0
   while True:
      g = Gate("__TP_%d" % (i)) 
      g.function = "test_point"
      yield g
      i = i + 1

class Partition(object):
    INPUTS=["bsc","input"]
    def __init__(self, ckt, members=[], initial_frontier = [], max_w = 0, available = []):
        self.members = members
        self.ckt = ckt
        self.max_w = max_w
        self.available = available
        self.frontier = initial_frontier # the furthest-in input gates.
        self.w = len(set([y for sublist in [self.ckt[x].fins for x in self.frontier if len(self.ckt[x].fins) > 0] for y in sublist]))
        self.members = self.members + self.frontier
        self.output = self.frontier # initial gates are the output.
        if self.w > self.max_w:
            print self.w,"initial width"
    def add(self, x):
        self.members.append(x)
        self.update()

    def get_inputs(self):
        return list({x for x in self.members if self.ckt[x].function.lower() in self.INPUTS})

    def update(self):
        """
        Update internal parameters based on the member list, in case it was modified externally.
        """
        self.w = len(set([y for sublist in [self.ckt[x].fins for x in self.frontier if len(self.ckt[x].fins) > 0] for y in sublist]))
        self.output = [x for x in self.members if len(self.ckt[x].fots) == 0]
        self.max_w = self.w

    def grow(self):
        """Expand this partition out one stage, if possible"""
        if len(self.frontier) == 0:
            return None # nothing left in the frontier
        candidates = []
        for f in self.frontier:
            for g in [x for x in self.ckt[f].fins if x in self.available and not x in self.members]:
                candidates.append((g, len(self.ckt[g].fins)-1 if len(self.ckt[g].fins) > 0 else 0))
        candidates = list(reversed(sorted(candidates, key=itemgetter(1))))
        while len(candidates) > 0:
            victim = candidates.pop()
            if victim[0] in self.available:
                self.frontier.append(victim[0])
                self.members.append(victim[0])
                self.available.remove(victim[0])
                self.frontier = [x for x in self.frontier if len([y for y in self.ckt[x].fins if not y in self.members and y in self.available]) > 0] # remove frontier entries with nothing in them
                self.w = len(set([y for sublist in [self.ckt[x].fins for x in self.frontier if len(self.ckt[x].fins) > 0] for y in sublist])) # recalculate w
                if self.w >= self.max_w - 1:
                    self.members.remove(victim[0])
                    self.available.append(victim[0])
                    self.frontier.remove(victim[0])
                    return None
        self.frontier = [x for x in self.frontier if len([y for y in self.ckt[x].fins if not y in self.members and y in self.available]) > 0] # remove frontier entries with nothing in them
        return True

    def size(self):
        return len(self.members)
    def __str__(self):
       return str(self.members)

class random_set(object):
    """ iterator whose next() function gives a random set of inputs number until it is exhausted."""
    def __init__(self, n = 0):
        self.size = n
        self.available = list(range(0,pow(2,n)))
    def __next__():
        return self.next()
    def __iter__(self):
        return self
    def next(self):
        try:
            victim = choice(self.available)
        except IndexError:
            raise StopIteration
        self.available.remove(victim)
        return [int(x) for x in bin(victim)[2:]]

class sort_topological(object):
   """ iterator whose next() function spits out the next legal gate in the ckt list for a topological sort """
   def __init__(self, ckt = None):
      """ Initializes the object with a circuit description""" 
      self.unplaced = list(ckt)
      self.ckt = ckt
      self.ids = 0
   def __next__(self):
      return self.next()
   def __iter__(self):
      return self
   def next(self):
      """ return a gate if and only if none of its prerequisites are in self.unplaced, or if it's a DFF """
      i = 0
      while len(self.unplaced) > 0:
         g = self.unplaced[i]
         print "Considering", g, self.ckt[g].function
         result = map(lambda x: x not in self.unplaced, self.ckt[g].fins)
         if len(result) == 0 or all(result) or self.ckt[g].function.upper() == "DFF":
            self.unplaced.remove(g)
            print "Removing", g
            self.ckt[g].cktid = self.ids
            self.ids = self.ids + 1
            return g
         i = i + 1
         if i >= len(self.unplaced):
            i = 0
      raise StopIteration

def write_bench_file(f, ckt): 
    output_queue = dict()
    output_queue[0] = [] # inputs
    output_queue[1] = [] # outputs 
    output_queue[2] = [] # test points
    output_queue[9] = [] # other
    with open(f, 'w') as outfile:
        for k, g in ckt.iteritems():
            if g.name == "DUMMY":
                continue
            if g.function.upper() == "INPUT": 
                output_queue[0].append("INPUT(" + k + ")\n")
            else:
                output_queue[9].append(k + " = " + g.function.lower() + "(" + re.sub('[\[\'\]]', '', str(list(g.fins))) + ")\n")
            if len(g.fots) == 0 and g.function.upper() != "TEST_POINT":
                output_queue[1].append("OUTPUT("+ k + ")\n")
        for k, q in output_queue.iteritems():
            for i in q:
                outfile.write(i)
            outfile.write("\n")

def read_bench_file(f):
    in_form = re.compile("INPUT\((.*)\)")
    out_form = re.compile("OUTPUT\((.*)\)")
    comment_form = re.compile("^#")
    gate_form = re.compile("(.*)[ ]*=[ ]*(.*)\((.*)\)")
    split_form = re.compile(",")
    ckt = dict()
    placed = []
    POs = []
    PIs = []
    with open(f, 'r') as infile:
        for l in infile:
            if re.match(comment_form, l) is not None:
                pass
            elif re.match(in_form, l) is not None:
                r = re.findall(in_form, l)
                if r[0].strip() not in placed:
                    placed.append(r[0].strip())
                ckt[r[0].strip()] = Gate(r[0].strip())
                ckt[r[0].strip()].function = "input"
                PIs.append([r[0].strip()])
                
            elif re.match(out_form, l) is not None:
                r = re.findall(out_form, l)
                if r[0].strip() not in POs:
                    POs.append(r[0].strip())
            elif re.match(gate_form, l) is not None:
                r = re.findall(gate_form, l)[0]
                g = Gate(r[0].strip())
                g.function = r[1].strip()
                g.fins = set([ x.strip() for x in re.split(split_form, r[2].strip())])
                print "Gate", g.name ,"fan-ins:",  g.fins
                ckt[r[0].strip()] = g
                try:
                    for fins in g.fins:
                        ckt[fins].fots.add(g.name)
                except KeyError:
                    pass
            else:
                print l
    print "Checking that fanouts are present"
    for k, g in ckt.iteritems():
        for fin in g.fins:
            print k, fin
            
            if k not in ckt[fin].fots:
                ckt[fin].fots.add(k)

# add all gates that have this as a fanin to this gate's fanout list
    for k,z in ckt.items():
        fots =  [ f for f in ckt.values() if k in f.fins]
        if len(fots) > 0:
            for i in fots:
                print "Adding ", i.name, " to fanouts of", k
                z.fots.add(i.name)

    PIs = map(lambda x: x[0], PIs)

    print "Parsed ckt"
    return ckt, PIs, POs

def partition_ckt(ckt, POs, w = 5):
    print "Partitioning circuit"
    part_list = part_recur(ckt, list(set(ckt.iterkeys())), w)
    parts = map(lambda x: Partition(ckt=ckt, members=x, max_w=w),part_list)
    bscs = gen_bsc()
    tps = gen_test_points()
    print "Adding BSCs and Test Points to ckt"
    for p in parts:
        made = dict()
        for i in find_bscs(ckt, p.members):
            part_gates = [x for x in p.members if i in ckt[x].fins]
            for g in part_gates:
                ckt[i].fots.remove(g)
                if i not in made:
                    new_bsc = bscs.next()
                    new_bsc.fins.add(i)
                    new_bsc.fots.add(g)
                    ckt[new_bsc.name] = new_bsc
                    ckt[g].fins.add(new_bsc.name)
                    made[i] = new_bsc.name
                else:
                    ckt[made[i]].fots.add(g)
                    ckt[g].fins.add(made[i])
                ckt[g].fins.remove(i)
        for k in find_tps(ckt, p.members):
            new_tp = tps.next()
            new_tp.fins.add(k)
            ckt[new_tp.name] = new_tp
            p.add(new_tp.name)
            ckt[p.members[0]].tps.append(new_tp.name)

    return ckt, parts

def get_fanin_cone(gate, ckt, stop_at = [], available = None):
    fin_cone = set()
    frontier = set(ckt[gate].fins)
    while len(frontier) > 0:
        next_frontier = set()
        next_frontier_tmp = map(lambda x:set(ckt[x].fins), frontier)
        fin_cone = fin_cone | frontier
        next_frontier = reduce(lambda x,y: x|y, next_frontier_tmp, set())
        next_frontier = next_frontier - fin_cone
        frontier = next_frontier
        # remove 
        frontier = frontier - set([x for x in frontier if ckt[x].function.lower() in ["input", "dff"]])
        frontier = frontier - set([x for x in frontier if ckt[x].function.lower() in stop_at])
        if available is not None:
            frontier = frontier - set([x for x in frontier if x not in available])
    return fin_cone

def get_partitions(ckt, POs, threads=10):
    partial_fanin = partial(get_fanin_cone, ckt=ckt, stop_at = ['bsc', 'dff'])
    origins = [ x for x in ckt if ckt[x].function.lower() == "test_point"] + POs
    p = multiprocessing.Pool(threads)
    partial_partitions = p.map(partial_fanin, origins)
    p.close()
    p.join()
    partitions = []
    while len(partial_partitions) > 0:
        overlap = False
        s = partial_partitions.pop()
        for p in partitions:
            if not overlap:
                if len(s.intersection(set(p.members))) > 0:
                    print "Merging", s, "with", p.members
                    print len(s.intersection(set(p.members))), "in common"
                    overlap = True
                    p.members = list(set(p.members) | s)
        if not overlap:
            # new partition object
            print "new Partition from", s
            p = Partition(ckt=ckt)
            p.members = list(s)
            partitions.append(copy.deepcopy(p))
    partitions = map(lambda x: x.update(), partitions)
    return partitions

if __name__ == "__main__": 
    pass
