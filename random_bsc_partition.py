# Copyright (c) 2016 Joseph Lenox
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE. 

from cktnet import Partition, sort_topological, Gate
import random
import copy


def Bsc_Tp_Generator():
    num = 0
    while 1:
        tmp_bsc = Gate("__BSC_" + str(num), function = "bsc")
        tmp_tp  = Gate("__TP_" + str(num), function = "test_point")
        tmp_tp.fots = set([tmp_bsc.name])
        tmp_bsc.fins = set([tmp_tp.name])
        num = num + 1
        yield [copy.deepcopy(tmp_tp), copy.deepcopy(tmp_bsc)]

def add_to_ckt(ckt, victim, pair_gen):
    """ insert a gate pair from a generator into the ckt """
    tp, bsc = next(pair_gen)
    victim_input = random.choice([x for x in ckt[victim].fins if ckt[x].function.lower() is not "bsc"])
    try:
        ckt[victim_input].fots.remove(victim_input)
    except KeyError:
        pass

    ckt[victim].fins.remove(victim_input)
    ckt[victim].fins.add(bsc.name)
    ckt[victim_input].fots.add(tp.name)
    ckt[victim_input].fots.add(bsc.name)
    bsc.fots.add(victim)
    tp.fins.add(victim_input)
    bsc.fins.add(victim_input)

    ckt[tp.name] = copy.deepcopy(tp)
    ckt[bsc.name] = copy.deepcopy(bsc)


def repartition_ckt(ckt, bsc_count, tp_count):
    """ Randomly place N BSC + TPs in the circuit, before some 
    gate in the circuit that is not an input or a test point."""
    pair_gen = Bsc_Tp_Generator()

    used = []
    for i in range(0,bsc_count):
        """ pick a gate at random that isn't used and also isn't a bsc, input, or testpoint 
        and put our gate in front of one of its inputs. """
        gates = [x for x,y in ckt.iteritems() if y.function.upper() != "INPUT" and y.function.upper() != "BSC" and y.function.upper() != "TEST_POINT" and x not in used]
        try: 
            victim = random.choice(gates)
        except IndexError:
            continue
        if len([x for x in ckt[victim].fins if ckt[x].function.lower() != "bsc"]) > 0:
            add_to_ckt(ckt, victim, pair_gen)
        # if this gate has all of its inputs taken up by bscs then 
        # remove it from consideration
        if len([x for x in ckt[victim].fins if ckt[x].function.lower() != "bsc"]) == 0:
            used.append(victim)
    print bsc_count, tp_count
    return ckt
