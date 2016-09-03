import cktnet
import argparse
import re
import csv

parser = argparse.ArgumentParser(description='Filter non-outputs and non-testpoints from simulation output.')
parser.add_argument('--ckt', type=str, help="ckt benchmark netlist")
parser.add_argument('infiles', nargs="+", type=str, help="input file")
args=parser.parse_args()

ckt, PIs, POs = cktnet.read_bench_file(args.ckt)

for f in args.infiles:
    with open(f, 'rb') as results_file:
        with open('_'.join([f, "filtered"]), 'wb') as filtered_output:
            csvin = csv.reader(results_file, delimiter=',')
            csvout = csv.writer(filtered_output)
            for row in csvin:
                cycle = int(row[0])
                outlist = [x for x in row[2:] if x in POs]
                outlist.insert(0, str(cycle))
                csvout.writerow(outlist)
