#!/usr/bin/python
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

""" Utility script to add missing BSCs to a circuit, based on a set of partitions """
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
