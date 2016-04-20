.PHONY: all clean

all: _sim.so

clean:
	rm -f _sim.so sim_wrap.o sim_wrap.cxx
_sim.so: sim.o sim_wrap.o
	c++ -shared $^ -o $@
sim_wrap.o: sim_wrap.cxx
	c++ -std=c++14 -c $^ -fPIC -I/usr/include/python2.7
sim_wrap.cxx: sim.i sim.h
	swig -python -c++ $<

sim.o: sim.cpp sim.h
	c++ -std=c++14 -c $^ -fPIC
