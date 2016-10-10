import cktnet
import argparse
import csv
import itertools
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='Filter non-outputs and non-testpoints from simulation output.')
parser.add_argument('--ckt', type=str, help="ckt benchmark netlist")
parser.add_argument('infiles', nargs="+", type=str, help="input file")
parser.add_argument('--dff', action='store_true', help='include dffs')
parser.add_argument('--threads', type=int, default=2, help="number of threads to use")
args=parser.parse_args()

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

def _start(f, dff):
    print "Starting", f
    with open(f, 'rb') as results_file:
        with open('_'.join([f, "filtered"]), 'wb') as filtered_output:
            csvin = csv.reader(results_file, delimiter=',')
            csvout = csv.writer(filtered_output)
            for row in csvin:
                cycle = int(row[0])
                outlist = [x for x in grouped(row[1:],2) if x[0] in POs or is_test_point(ckt, x[0]) or is_output(ckt, x[0]) or (dff and is_dff(ckt,x[0]))]
                processed_list = []
                for x in outlist:
                    processed_list.append(x[0])
                    processed_list.append(x[1])
                processed_list.insert(0, str(cycle))
                csvout.writerow(processed_list)
    print "Done with", f
def _start_dff(f):
    _start(f, True)

def _start_no_dff(f):
    _start(f, False)

if __name__ == '__main__':
    ckt, PIs, POs = cktnet.read_bench_file(args.ckt)
    p = Pool(args.threads)
    if (args.dff):
        p.map(_start_dff, args.infiles)
    else:
        p.map(_start_no_dff, args.infiles)
    p.close()
    p.join()
