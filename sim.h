/*
Copyright (c) 2016 Joseph Lenox

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
#ifndef __EVENTSIM__
#define __EVENTSIM__
// public interface for event-driven simulator, patterned on Python
#include <set>
#include <map>
#include <vector>
#include <utility>
#include <algorithm>
#include <exception>
#include <stdexcept>
#include <string>
#include <iostream>
#include <fstream>
using namespace std;

typedef map<unsigned int, bool> result_t;

enum class gate_t : unsigned int
{
  BSC = 0, TP = 1, 
  INPUT = 2, AND = 3, NAND = 4, OR = 5, NOR = 6,
  XOR = 7,
  XNOR = 8,
  BUFF = 9,
  NOT = 10,
  OUTPUT = 11,
  DFF_O = 12,
  DFF = 13,
  DUMMY = 255
};
// simple representation of gate in a netlist.
class Gate {
  public:

    gate_t function;
    const string name;
    string dff_link;
    const unsigned int delay;
    vector<string> fanin, fanout;
    bool output;
    bool primary_output;
    unsigned int verbosity;

    Gate() : verbosity(0), delay(1), function(gate_t::DUMMY), name(""), fanin(vector<string>()),
      fanout(vector<string>()), output(false), primary_output(false) {}
    Gate(gate_t func, string name, vector<string> fanin, vector<string> fanout, bool isoutput, bool ispo ) : 
      delay(1), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo), verbosity(0) {
        std::sort(this->fanin.begin(), this->fanin.end());
        std::sort(this->fanout.begin(), this->fanout.end());
      }
    Gate(gate_t func, string name, vector<string> fanin, vector<string> fanout, unsigned int delay, bool isoutput, bool ispo) : 
      delay(delay), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo), verbosity(0), dff_link(""){
        std::sort(this->fanin.begin(), this->fanin.end());
        std::sort(this->fanout.begin(), this->fanout.end());
      }

    Gate(gate_t func, string name, string link, vector<string> fanin, vector<string> fanout, unsigned int delay, bool isoutput, bool ispo) : 
      delay(delay), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo), verbosity(0), dff_link(link) {}

    Gate& operator=(const Gate& other) {
      *this = Gate(other);
    }
    Gate(const Gate& other) : delay(other.delay), function(other.function), name(other.name), fanin(other.fanin),
    fanout(other.fanout), output(other.output), primary_output(other.primary_output), dff_link(other.dff_link)
    { }
    void debug_print()
    {
      cerr << name << " " << delay << endl;

    }

    size_t nfin() { return fanin.size(); }    
    size_t nfot() { return fanout.size(); }    
};

class EventSim {
  private:
    size_t c, t; // cycle and time references
    void start_cycle();
    map<string, bool> next_inputs;
    bool get_value(string name);
    bool end_sim;
    void process_gate(const string &name);
    bool new_file;
    void process_events();
    bool run_cycle(string);
    bool uninitialized;
  protected:
    int verbosity;

  public:
 
    bool bist; // treat bscs as inputs if this is on
    // list of gates, indexed by string name
    map<string, Gate> ckt; 
    // the input vectors 
    map<size_t, map<string, bool> > inputs;
    map<string, result_t> results; // top for any name is the newest value and the time it was at.
    map<string, result_t> dffs; // top for any name is the newest value and the time it was at.
    vector<size_t> cycles;
    map<size_t, set<string> > events;
    map<size_t, set<string> > new_events;
    void add_to_inputs(size_t c, string name, bool value);
    void add_gate(const Gate& g);
    void run(string);
    void dump_results(string);
    void dump_result(string, const unsigned int);
    EventSim() : c(0), t(0), next_inputs(map<string, bool>()), end_sim(false), bist(false), ckt(map<string, Gate>()),
    inputs(map<size_t, map<string, bool> >()), cycles(vector<size_t>()), events(map<size_t, set<string> >()), verbosity(0) , uninitialized(false)
    { }
    EventSim(int log_level) : c(0), t(0), next_inputs(map<string, bool>()), end_sim(false), bist(false), ckt(map<string, Gate>()),
    inputs(map<size_t, map<string, bool> >()), cycles(vector<size_t>()), events(map<size_t, set<string> >()), verbosity(log_level) , uninitialized(false)
    { }
};
#endif
