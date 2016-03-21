#!/usr/bin/python
import re
import random


class Gate(object):
    _delay = {"AND": 5, "OR": 5, "INPUT": 0}
    def __init__(self, name):
        self.function = None
        self.name = name
        self.fins = []
        self.fots = []
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
    def __init__(self, ckt, initial_frontier = [], max_w = 0, available = []):
        self.members = []
        self.ckt = ckt
        self.max_w = max_w
        self.available = available
        self.frontier = initial_frontier # the furthest-in input gates.
        self.w = len(set([y for sublist in [self.ckt[x].fins for x in self.frontier if self.ckt[x].fins != []] for y in sublist]))
        self.members = self.members + self.frontier
        self.output = self.frontier # initial gates are the output.
    def get_inputs(self):
        return list({x for x in self.members if self.ckt[x].function.lower() in self.INPUTS})

    def grow(self, initial = None):
        """Expand this partition out one stage, if possible"""
        print "Attempting to grow partition from frontier of", p.frontier
        frontier_old = self.frontier
        old_w = self.w
        self.frontier = list(set([y for sublist in [self.ckt[x].fins for x in self.frontier if self.ckt[x].fins != []] for y in sublist]))
        self.w = len(set([y for sublist in [self.ckt[x].fins for x in self.frontier if self.ckt[x].fins != []] for y in sublist]))
        if self.w > self.max_w:
            """ randomly choose a subset of the old frontier """
            temp_frontier = random.sample(self.frontier, len(self.frontier)-1)
            attempt = len(set([y for sublist in [self.ckt[x].fins for x in temp_frontier if self.ckt[x].fins != []] for y in sublist]))
            tries = 0
            while attempt <= self.max_w and tries < 50:
                print "Attempt", tries
                temp_frontier = random.sample(self.frontier, len(self.frontier)-1)
                attempt = len(set([y for sublist in [self.ckt[x].fins for x in temp_frontier if self.ckt[x].fins != []] for y in sublist]))
                tries = tries + 1
            if tries >= 50:
                self.frontier = frontier_old
                self.w = len(self.frontier)
                raise StopIteration("can't grow any more!")
            else:
                self.frontier = temp_frontier
                self.members = self.members + self.frontier
        else:
            self.members = self.members + self.frontier
        # restrict to available gates
        self.frontier = [x for x in self.frontier if x in self.available]
        self.members = [x for x in self.members if x in self.available]
        self.frontier = self.frontier + [x for x in self.members if ckt[x].function is "input" ]
        self.w = len(self.frontier)
    def size(self):
        return len(self.members)
    def __str__(self):
       return str(self.members)

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
      """ return a gate if and only if none of its prerequisites are in self.unplaced """
      i = 0
      while len(self.unplaced) > 0:
         g = self.unplaced[i]
         result = map(lambda x: x not in self.unplaced, self.ckt[g].fins)
         if len(result) == 0 or all(result):
            self.unplaced.remove(g)
            self.ckt[g].cktid = self.ids
            self.ids = self.ids + 1
            return g
         i = i + 1
         if i >= len(self.unplaced):
            i = 0
      raise StopIteration

def grow_partition(ckt, g, size, w):
    gate = ckt[g]

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
                output_queue[9].append(k + " = " + g.function.lower() + "(" + re.sub('[\[\'\]]', '', str(g.fins)) + ")\n")
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
                g.fins = [ x.strip() for x in re.split(split_form, r[2].strip())]
                print "Gate", g.name ,"fan-ins:",  g.fins
                ckt[r[0].strip()] = g
                try:
                    for fins in g.fins:
                        ckt[fins].fots.append(g.name)
                except KeyError:
                    pass
            else:
                print l
    print "Checking that fanouts are present"
    for k, g in ckt.iteritems():
        for fin in g.fins:
            print fin
            if k not in ckt[fin].fots:
                ckt[fin].fots.append(k)

# add all gates that have this as a fanin to this gate's fanout list
    for k,z in ckt.items():
        fots =  [ f for f in ckt.values() if k in f.fins] 
        if len(fots) > 0:
            for i in fots:
                print "Adding ", i.name, " to fanouts of", k
                z.fots.append(i.name)

    PIs = map(lambda x: x[0], PIs)

    print "Parsed ckt"
    return ckt, PIs, POs

def partition_ckt(ckt, POs):
    sorted_ckt = [x for x in sort_topological(ckt)]
    unplaced = [x for x in sorted_ckt if x not in POs]

    parts = []
    max_w = 5
    for po in POs:
       p = Partition(ckt=ckt, initial_frontier=[po], available=unplaced, max_w = max_w)   
       l = [po]
       try:
          while len(p.frontier) < max_w:
             p.grow()
             if l == p.frontier:
                raise StopIteration
             l = p.frontier

       except Exception, e:
          print "Error occurred", e
       parts.append(p)
       unplaced = [x for x in unplaced if x not in p.members]

    while len(unplaced) > 0:
       start = random.sample(unplaced, 1)
       p = Partition(ckt=ckt, initial_frontier=start, available=unplaced, max_w = max_w)
       l = start
       try: 
          while len(p.frontier) < max_w:
             p.grow()
             if l == p.frontier:
                raise StopIteration
             l = p.frontier
       except Exception:
          print "Error occurred", e
       parts.append(p)
       unplaced = [x for x in unplaced if x not in p.members]

    bscs = gen_bsc()
    tps = gen_test_points()
    for p in parts:
       for g in p.frontier:
          new_finset = ckt[g].fins
          for fin in ckt[g].fins:
             new_bsc = bscs.next()
             new_bsc.fots.append(g)
             ckt[new_bsc.name] = new_bsc
             ckt[new_bsc.name].fins.append(fin)
             ckt[new_bsc.name].fots.append(g)
             ckt[g].bscs.append(new_bsc.name)
             p.members.append(new_bsc.name)
             new_finset = [x for x in new_finset if x is not fin]
             new_finset.append(new_bsc.name)
          ckt[g].fins = new_finset
          
       new_tp = tps.next()
       new_tp.fins.append(p.members[0])
       ckt[new_tp.name] = new_tp
       p.members.append(new_tp.name)
       ckt[p.members[0]].tps.append(new_tp.name)

    return ckt, parts

if __name__ == "__main__": 
    pass
