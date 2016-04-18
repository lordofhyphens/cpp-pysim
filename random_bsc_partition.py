from cktnet import Partition, sort_topological, Gate
import random
import copy


def Bsc_Tp_Generator():
    num = 0
    while 1:
        tmp_bsc = Gate("__BSC_" + str(num), function = "bsc")
        tmp_tp  = Gate("__TP_" + str(num), function = "test_point")
        tmp_tp.fots = [tmp_bsc.name]
        tmp_bsc.fins = [tmp_tp.name]
        num = num + 1
        yield [copy.deepcopy(tmp_tp), copy.deepcopy(tmp_bsc)]

def add_to_ckt(ckt, victim, pair_gen):
    """ insert a gate pair from a generator into the ckt """
    tp, bsc = next(pair_gen)
    victim_input = random.choice([x for x in ckt[victim].fins if ckt[x].function.lower() is not "bsc"])
    ckt[victim_input].fots = [x for x in ckt[victim_input].fots if x is not victim_input]
    ckt[victim].fins = [x for x in ckt[victim].fins if x is not victim_input]
    ckt[victim].fins.append(bsc.name)
    ckt[victim_input].fots.append(tp.name)
    ckt[victim_input].fots.append(bsc.name)
    bsc.fots.append(victim)
    tp.fins.append(victim_input)
    bsc.fins.append(victim_input)

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
