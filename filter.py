import cktnet
import argparse
import csv
import itertools

parser = argparse.ArgumentParser(description='Filter non-outputs and non-testpoints from simulation output.')
parser.add_argument('--ckt', type=str, help="ckt benchmark netlist")
parser.add_argument('infiles', nargs="+", type=str, help="input file")
parser.add_argument('--dff', action='store_true', help='include dffs')
args=parser.parse_args()

ckt, PIs, POs = cktnet.read_bench_file(args.ckt)
def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return itertools.izip(*[iter(iterable)]*n)

def is_test_point(ckt, g):
    try:
        return ckt[g].function == "test_point"
    except:
        return False
def is_output(ckt, g):
    try:
        return len(ckt[g].fots) == 0
    except:
        return False
def is_dff(ckt, g):
    try:
        return ckt[g].function == "dff"
    except:
        return False

for f in args.infiles:
    with open(f, 'rb') as results_file:
        with open('_'.join([f, "filtered"]), 'wb') as filtered_output:
            csvin = csv.reader(results_file, delimiter=',')
            csvout = csv.writer(filtered_output)
            for row in csvin:
                cycle = int(row[0])
                outlist = [x for x in grouped(row[1:],2) if x[0] in POs or is_test_point(ckt, x[0]) or is_output(ckt, x[0]) or (args.dff and is_dff(ckt,x[0]))]
                processed_list = []
                for x in outlist:
                    processed_list.append(x[0])
                    processed_list.append(x[1])
                processed_list.insert(0, str(cycle))
                csvout.writerow(processed_list)
