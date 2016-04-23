.PHONY: all clean

all: _EventSim.so

clean:
	rm -f _EventSim.so sim_wrap.o sim_wrap.cxx
_EventSim.so: sim.o sim_wrap.o
	c++ -g -shared $^ -o $@
sim_wrap.o: sim_wrap.cxx
	c++ -std=c++14 -c $^ -fPIC -I/usr/include/python2.7
sim_wrap.cxx: sim.i sim.h
	swig -python -c++ $<

sim.o: sim.cpp sim.h
	c++ -std=c++14 -O2 -fpermissive -c $^ -fPIC
