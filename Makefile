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
