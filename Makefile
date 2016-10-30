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

.PHONY: all clean
SWIG=swig3.0
all: _EventSim.so _KLPart.so

clean:
	rm -f _EventSim.so sim_wrap.o sim_wrap.cxx kl_wrap.o kl_wrap.o _KLPart.so
_EventSim.so: sim.o sim_wrap.o
	c++ -g -shared $^ -o $@

_KLPart.so: kl.o kl_wrap.o
	c++ -g -shared $^ -o $@

sim_wrap.o: sim_wrap.cxx
	c++ -std=c++14 -c $^ -fPIC -I/usr/include/python2.7
sim_wrap.cxx: sim.i sim.h
	$(SWIG) -python -c++ $<

kl_wrap.o: kl_wrap.cxx
	c++ -std=c++14 -c $^ -fPIC -I/usr/include/python2.7
kl_wrap.cxx: kl.i kl.hpp
	$(SWIG) -python -c++ $<
	
kl.o: kl.cpp sim.h kl.hpp
	c++ -std=c++14 -O2 -fpermissive -c $^ -fPIC

sim.o: sim.cpp sim.h
	c++ -std=c++14 -O2 -fpermissive -c $^ -fPIC
