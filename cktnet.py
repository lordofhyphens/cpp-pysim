#!/usr/bin/python
import re
import argparse
import random

class Gate(object):
    def __init__(self, name):
        self.function = None
        self.name = name
        self.fins = []
        self.fots = []
    def __str__(self):
        return self.name + ": " + self.function + ", " + str(self.fins)

def topological_sort(gatelist):
    pass

def in_partition(g, part):
    result = g in part
    if result:
        return result
    else:
        try:
            result = False
            for r in g:
                result = result | in_partition(g, r)
        except TypeError:
            return False
        # see if the contents of part are themselves containers?
        pass

def partition(ckt, w, po):
    start_list = po
    gate_pool = set(ckt)
    assigned = set()
    partitions = []
    p = []
    # pick a PO at random
    start_list = POs
    while len(start_list)>0:
        
        z = random.choice(list(start_list))
        start_list.remove(z)
        print "Making partition from " + z
        i = set()
        i.add(z)
        part = make_partition(ckt, i, i , w, assigned)
        if part is None:
            print "returned none"
        else:
            gate_pool = gate_pool - part
            assigned = assigned & part
            partitions = partitions + [part]
    while len(gate_pool) > 0:
        # pick a gate at random
        z = random.choice(list(gate_pool))
        print "Making partition from " + z
        i = set()
        i.add(z)
        gate_pool = gate_pool - i
        part = make_partition(ckt, i, i , w, assigned)
        if part is None:
            print "returned none"
            partitions = partitions + [i]
            assigned = assigned & i
        else:
            gate_pool = gate_pool - part
            assigned = assigned & part
            partitions = partitions + [part]
    print "All Partitions:", partitions


def make_partition(ckt, frontier, current_partition, w, partitions):
    """ s is the current frontier """
    inputs = len(frontier)
    if inputs > w:
        print "Input count ", len(frontier), " exceeds ", w
        return None
    new_frontier = set()
    current_partition = set(current_partition | frontier)
    for s in current_partition:
        # create a new frontier from the fan-in of the current frontier. 
        if s in partitions or s in current_partition:
            print s, "already in a partition"
            continue
        if len(ckt[s].fins) == 0:
            print s, "has no inputs"
            continue
        for fin in ckt[s].fins:
            new_frontier.add(fin)
    if new_frontier == frontier:
        print "Frontier isn't changing..."
        return None
    print new_frontier
    p = make_partition(ckt, new_frontier, current_partition, w, partitions)
    if p is not None:
        p = current_partition | p
    else:
        p = current_partition
    return p

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('file', metavar='N', type=str, nargs='+',
                   help='an integer for the accumulator')

args = parser.parse_args()
print args.file

in_form = re.compile("INPUT\((.*)\)")
out_form = re.compile("OUTPUT\((.*)\)")
comment_form = re.compile("^#")
gate_form = re.compile("(.*)[ ]*=[ ]*(.*)\((.*)\)")
split_form = re.compile(",")
fins = dict()
ckt = dict()
free = []
placed = []
POs = []
PIs = []
BSCs = []
partitions = []
for f in args.file:
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
                g.func = r[1].strip()
                g.fins = [ x.strip() for x in re.split(split_form, r[2].strip())]
                ckt[r[0].strip()] = g
            else:
                print l

# add all gates that have this as a fanin to this gate's fanout list
for k,z in ckt.items():
    fots =  [ f for f in ckt.values() if k in f.fins] 
    if len(fots) > 0:
        for i in fots:
            z.fots.append(i.name)


partition(ckt, 15, POs)
