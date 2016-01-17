#!/usr/bin/python
import re
import argparse
import dag

class Gate(object):
    def __init__(self, name):
        self.function = None
        self.name = name
        self.fins = []
    def __str__(self):
        return self.name + ": " + self.function + ", " + str(self.fins)

def topological_sort(gatelist):
    pass


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
ckt = dag.Composite()
free = []
placed = []
pos = []
for f in args.file:
    with open(f, 'r') as infile:
        for l in infile:
            if re.match(comment_form, l) is not None:
                pass
            elif re.match(in_form, l) is not None:
                r = re.findall(in_form, l)
                if r[0] not in placed:
                    placed.append(r[0])
                
            elif re.match(out_form, l) is not None:
                r = re.findall(out_form, l)
                if r[0] not in pos:
                    pos.append(r[0])
            elif re.match(gate_form, l) is not None:
                r = re.findall(gate_form, l)[0]
                g = dag.Node()
                g.name=r[0]
                g.func = r[1]
                g.fins = [ x for x in re.split(split_form, r[2])]
                
                
            else:
                print l
            
