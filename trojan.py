# Code to insert trojan into circuit
from cktnet import Gate, get_fanin_cone
import random
import copy
import multiprocessing
from functools import partial

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
            outgate.fins.add(g)
            outgate.fins.add(None)
            outgate.fots.add(None)
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
            self.gates[i].fots.add(gate.name)
        frontier = frontier + dummy

        return result, frontier
    def set_fots(self, g):
        for i in g.fins:
            if i is not None:
                self.gates[i].fots.add(g.name)
    def __str__(self):
        return str([str(self.gates[x]) for x in (self.gates)])


def parasite(ckt, pos, trojan, part = None, seed = None):
    """ modify a ckt to randomly insert another circuit into it. Returns the modified circuit. """ 
    restart = True
    cycles = 0
    to_attach = {}
    while restart:
        attach_points = [x for x in trojan.gates if "DUMMY" in trojan.gates[x].fins]
        troj_out = [x for x,v in trojan.gates.iteritems() if len(v.fots) == 0 or "DUMMY" in v.fots]
        if part is not None:
            gates_to_use = random.choice([x for x in part if len(x.members) >= (len(attach_points) + len(troj_out))]).members
            gates_to_use = [x for x in gates_to_use if ckt[x].function.lower() is not "test_point"]
            partial_fanin = partial(get_fanin_cone, ckt=ckt, available=gates_to_use)
            print "Using partition", str(gates_to_use)
        else:
            gates_to_use = [x for x in ckt if ckt[x].function.upper() in Trojan._gate_enum and len(ckt[x].fots) > 0]
            partial_fanin = partial(get_fanin_cone, ckt=ckt)
        random.seed(seed)
        pickups = []
        print "Attach points", attach_points
        to_attach = {}
        all_attach = []
        for g in attach_points:
            attachgates = []
            for i in [x for x in trojan.gates[g].fins if x in "DUMMY"]:
                z = random.choice(gates_to_use)
                attachgates.append(z)
                all_attach.append(z)
                pickups = pickups + attachgates
                print "adding ", str(z), "to", str(g)
            to_attach[g] = attachgates
        print "going to pickups"
        # get the fan-in cones of all of the attach points
        disallowed = set()
        p = multiprocessing.Pool(5)
        disallowed_set = p.map(partial_fanin, pickups)
        p.close()
        p.join()
        print "Reducing"
        disallowed = reduce(lambda x,y:x | y, disallowed_set, set())
        print "Getting inputs"
        inputs = set([x for x,v in ckt.iteritems() if v.function.upper() in ["BSC", "INPUT", "TEST_POINT"]])
        print "Getting allowed"
        if part is not None:
            allowed = list(set(gates_to_use) - (disallowed | inputs | set (all_attach)))
        else:
            allowed = list(set(ckt) - (disallowed | inputs | set(all_attach)))
        print "Allowed length;", len(allowed), len(troj_out)
        if len(allowed) < len(troj_out):
            # try again with different random gates
            restart = True
            cycles = cycles + 1
            print "Attempts remaining:", str(20 - cycles)
        else:
            restart = False
        if cycles > 20:
            raise RuntimeError("Couldn't find an appropriate attachment for trojan after 20 attempts")
    print "Found enough allowed gates to insert trojan."
    for g, att in to_attach.iteritems():
        trojan.gates[g].fins = trojan.gates[g].fins + att
        trojan.gates[g].fins = [x for x in trojan.gates[g].fins if x != "DUMMY"]
        for z in att:
            ckt[z].fots.add(g)

    for g in troj_out:
        victim = random.choice(allowed)
        print "Target gate:", g , "->", victim
        allowed = [x for x in allowed if x is not victim]
        # get the fins of the victim, pick one at random
        tmp = ckt[victim].fins
        victim_fin = random.choice(tuple(tmp))
        insert_or = Gate(g+"_WIRED_OR", function="OR")
        insert_or.fins = [victim_fin, g]
        ckt[g+"_WIRED_OR"] = copy.deepcopy(insert_or)
        ckt[victim].fins = [x for x in ckt[victim].fins if x is not victim_fin]
        ckt[victim].fins.append(insert_or.name)
        trojan.gates[g].fots.append(victim)
    for g in [x for x in trojan.gates if x is not "DUMMY"]:
        ckt[g] = trojan.gates[g]

    return ckt, pos

if __name__ == "__main__": 
    # do some self-tests.
    t = Trojan(seed=10, fin=10)
    for k in t.gates.iterkeys():
       print t[k]
