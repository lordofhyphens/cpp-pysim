#!/usr/bin/python
import re
import argparse

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
        # see if the contents of part are themselves containers?
        pass

def partition(ckt, w, po):
    assigned = []
    partitions = []
    p = []
    # pick a PO at random

def add_to_partition(ckt, s, w, partitions):
    inputs = 0

    # if s is in a partition already we don't want to touch it
    if any([in_partition(s, k) for k in partitions]):
        return None
    # number of inputs needed is the sum of the fanins of the furthest range.
    for fin in ckt[s].fins:
        add_to_partition(ckt, fin, w, partitions)

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
                g.fins = [ x for x in re.split(split_form, r[2].strip())]
                ckt[r[0].strip()] = g
            else:
                print l

# add all gates that have this as a fanin to this gate's fanout list
for k,z in ckt.items():
    fots =  [ f for f in ckt.values() if k in f.fins] 
    if len(fots) > 0:
        for i in fots:
            z.fots.append(i.name)

for k,z in ckt.items():
    print z.fots
