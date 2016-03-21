# Code to insert trojan into circuit
from cktnet import Gate
import random
import copy

# random trojan ckt pattern: N(3-7) inputs, M (1-3) output
# randomly build hierarchy of gates corresponding to number of inputs
# output gates are XORs or XNORs with one fan-in unspecificed (for integration into system)

class Trojan(object):
    _gate_enum = ["AND", "OR", "NOR", "XOR", "XNOR", "NAND", "BUFF", "NOT"]
    _out_enum = [ "OR", "NOR", "XNOR", "XOR" ]
    def __init__(self, name = None, fin = None , fot = None, seed = None):
        random.seed(seed)
        self.gates = dict()
        self.inputs = fin
        self.outputs = fot
        self.name = name
        if self.name is None:
            self.name = "__TrojCkt" + str(random.randint(0,9000))
        if self.inputs is None:
            self.inputs = random.randint(2,7)
        if self.outputs is None:
            self.outputs = random.randint(1,3)
        if self.outputs < self.inputs:
            self.outputs = random.randint(1, self.inputs - 1)
        self.gates["DUMMY"] = Gate("DUMMY")

        self.generate()
    def __getitem__(self, index):
        return self.gates[index]

    def load(self, netlist):
        """ Copy a netlist and transform it into a Trojan circuit. """
        self.gates = copy.deepcopy(netlist)
        self.inputs = len([k for (k,v) in self.gates.iteritems() if v.function is "INPUT"])
        self.outputs = len([x for x in self.gates if len(self.gates[x].fots) == 0])
        temp = dict()
        for k,v in self.gates.iteritems():
            k = self.name+"_"+k
            v.fins = [self.name+"_"+x for x in v.fins]
            v.fots = [self.name+"_"+x for x in v.fots]
            print k
            if v.function.upper() == "INPUT":
                v.function = "buff"
                v.fins.append("DUMMY");
            v.name = self.name+"_"+v.name
            temp[k] = v
        self.gates = temp

    def generate(self):
        """ Randomly generate a circuit netlist from a choice of gates. 
            Rules: Each gate has a single fan-out.
        """
        frontier = []
        for i in range(0,self.inputs):
            frontier.append("DUMMY")
        gateId = 0
        while (len(frontier) > self.outputs or "DUMMY" in frontier):
            g =  Gate(self.name+"_"+str(gateId))
            g.function = random.choice(self._gate_enum)
            g.fins, frontier = self.get_fins(frontier, g)
            self.set_fots(g)
            self.gates[g.name] = g
            gateId = gateId + 1
            frontier.append(g.name)
        for g in frontier:
            outgate = Gate(self.name+"_"+str(gateId))
            outgate.function = random.choice(self._out_enum)
            outgate.fins.append(g)
            outgate.fins.append(None)
            outgate.fots.append(None)
            self.set_fots(outgate)
            self.gates[outgate.name] = outgate
            gateId = gateId + 1
        self.gates["DUMMY"].fots = list(set(self.gates["DUMMY"].fots))
        for g in self.gates:
            self.gates[g].fots = list(set(self.gates[g].fots))
    def get_fins(self, frontier, gate):
        if gate.function is "BUFF" or gate.function is "NOT":
            sample = 1
        else:
            sample = random.randint(2, len(frontier))
        result = random.sample(frontier, sample)
        dummy = [x for x in frontier if x is "DUMMY"]
        frontier = [x for x in frontier if x is not "DUMMY"]
        for i in result:
            frontier = [x for x in frontier if x is not i]
            if i is "DUMMY":
                dummy.pop()
            self.gates[i].fots.append(gate.name)
        frontier = frontier + dummy

        return result, frontier
    def set_fots(self, g):
        for i in g.fins:
            if i is not None:
                self.gates[i].fots.append(g.name)
    def __str__(self):
        return str([str(self.gates[x]) for x in (self.gates)])
def get_fanin_cone(ckt, gate):
    fin_cone = set()
    frontier = ckt[gate].fins
    while len(frontier) > 0:
        next_frontier = []
        for z in frontier:
            fin_cone = fin_cone | set(z)
            next_frontier = next_frontier + ckt[z].fins
        frontier = next_frontier
    return fin_cone

def parasite(ckt, pos, trojan, seed = None):
    """ modify a ckt to randomly insert another circuit into it. Returns the modified circuit. """ 
    for k,g in trojan.gates.iteritems():
        print str(g)
    attach_points = [x for x in trojan.gates if "DUMMY" in trojan.gates[x].fins]
    random.seed(seed)
    pickups = []
    print "Attach points", attach_points
    for g in attach_points:
        attachgates = []
        for i in [x for x in trojan.gates[g].fins if x is "DUMMY"]:
            z = random.choice([x for x in ckt if ckt[x].function.upper() not in Trojan._gate_enum and len(ckt[x].fots) > 0])
            attachgates.append(z)
            pickups = pickups + attachgates
            print "adding ", str(z), "to", str(g)
            ckt[z].fots.append(g)
        trojan.gates[g].fins = trojan.gates[g].fins + attachgates
        trojan.gates[g].fins = [x for x in trojan.gates[g].fins if x is not "DUMMY"]
    # get the fan-in cones of all of the attach points
    disallowed = set()
    for g in pickups:
        disallowed = disallowed | get_fanin_cone(ckt, g)
    allowed = list(set(ckt) | disallowed)
    for g in [x for x in trojan.gates if None in trojan.gates[x].fots]:
        victim = random.choice(allowed)
        allowed = [x for x in allowed if x is not victim]
        tmpfots = ckt[victim].fots
        ckt[victim].fots = g
        trojan.gates[g].fins.append(victim)
        trojan.gates[g].fins = [x for x in trojan.gates[g].fins if x is not None]
        trojan.gates[g].fots = [x for x in trojan.gates[g].fots + tmpfots if x is not None]

    for g in [x for x in trojan.gates if x is not "DUMMY"]:
        ckt[g] = trojan.gates[g]

    return ckt, pos

if __name__ == "__main__": 
    # do some self-tests.
    t = Trojan(seed=10, fin=10)
    for k in t.gates.iterkeys():
       print t[k]
