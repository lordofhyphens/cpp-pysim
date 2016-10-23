#!/usr/bin/python

import sys
import cPickle as pickle
import cktnet

cfile = sys.argv[1]
pfile = sys.argv[2]

print cfile, pfile

ckt, PIs, POs = cktnet.read_bench_file(cfile)

a = open(pfile, 'rb')
parts = pickle.load(a)

a.close()

for p in parts:
    newp = set()
    for g in p.members:
        newp.add(g)
        newp |= ckt[g].fins
    p.members = newp

for p in parts:
    print p.get_inputs()

a = open(pfile, 'wb')
pickle.dump(parts, a)
a.close()
