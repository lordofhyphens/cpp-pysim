// public interface for event-driven simulator, patterned on Python
#include <set>
#include <map>
#include <vector>
#include <utility>
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
  DUMMY = 255
};
// simple representation of gate in a netlist.
class Gate {
  public:

    gate_t function;
    const string name;
    const unsigned int delay;
    vector<string> fanin, fanout;
    bool output;
    bool primary_output;
    unsigned int verbosity;

    Gate() : verbosity(0), delay(1), function(gate_t::DUMMY), name(""), fanin(vector<string>()),
      fanout(vector<string>()), output(false), primary_output(false) {}
    Gate(gate_t func, string name, vector<string> fanin, vector<string> fanout, bool isoutput, bool ispo ) : 
      delay(1), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo), verbosity(0) {}
    Gate(gate_t func, string name, vector<string> fanin, vector<string> fanout, unsigned int delay, bool isoutput, bool ispo) : 
      delay(delay), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo), verbosity(0) {}

    Gate& operator=(const Gate& other) {
      *this = Gate(other);
    }
    Gate(const Gate& other) : delay(other.delay), function(other.function), name(other.name), fanin(other.fanin),
    fanout(other.fanout), output(other.output), primary_output(other.primary_output)
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
  protected:
    int verbosity;

  public:
 
    bool bist; // treat bscs as inputs if this is on
    // list of gates, indexed by string name
    map<string, Gate> ckt; 
    // the input vectors 
    map<size_t, map<string, bool> > inputs;
    map<string, result_t> results; // top for any name is the newest value and the time it was at.
    vector<size_t> cycles;
    map<size_t, set<string> > events;
    map<size_t, set<string> > new_events;
    void add_to_inputs(size_t c, string name, bool value);
    void add_gate(const Gate& g);
    void run(string);
    void dump_results(string);
    void dump_result(string, const unsigned int);
    EventSim() : c(0), t(0), next_inputs(map<string, bool>()), end_sim(false), bist(false), ckt(map<string, Gate>()),
    inputs(map<size_t, map<string, bool> >()), cycles(vector<size_t>()), events(map<size_t, set<string> >()), verbosity(0)
    { }
    EventSim(int log_level) : c(0), t(0), next_inputs(map<string, bool>()), end_sim(false), bist(false), ckt(map<string, Gate>()),
    inputs(map<size_t, map<string, bool> >()), cycles(vector<size_t>()), events(map<size_t, set<string> >()), verbosity(log_level)
    { }
};

