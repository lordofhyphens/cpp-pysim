// public interface for event-driven simulator, patterned on Python
#include <set>
#include <map>
#include <vector>
#include <utility>
#include <exception>
#include <stdexcept>

using namespace std;

typedef map<size_t, bool> result_t;

// simple representation of gate in a netlist.
class Gate {
  public:
    enum class gate_t : unsigned int 
    {
      BSC, TP, INPUT, AND, NAND, OR, NOR, XOR, XNOR, BUFF, NOT, OUTPUT, DUMMY
    };
    const gate_t function;
    const string name;
    const unsigned int delay;
    set<string> fanin, fanout;
    bool output;
    bool primary_output;

    Gate() : delay(1), function(gate_t::DUMMY), name(""), fanin(set<string>()),
      fanout(set<string>()), output(false), primary_output(false) {}
    Gate(gate_t func, string name, set<string> fanin, set<string> fanout, bool isoutput, bool ispo ) : 
      delay(1), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo) {}
    Gate(gate_t func, string name, set<string> fanin, set<string> fanout, unsigned int delay, bool isoutput, bool ispo) : 
      delay(delay), function(func), name(name), fanin(fanin),
      fanout(fanout), output(isoutput), primary_output(ispo) {}
    Gate& operator=(const Gate& other) {
      *this = Gate(other);
    }
    Gate(const Gate& other) : delay(other.delay), function(other.function), name(other.name), fanin(other.fanin),
    fanout(other.fanout), output(other.output), primary_output(other.primary_output)
    { }

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

  public:

    bool bist; // treat bscs as inputs if this is on
    // list of gates, indexed by string name
    map<string, Gate> ckt; 
    // the input vectors 
    map<size_t, map<string, bool> > inputs;
    map<string, result_t> results; // top for any name is the newest value and the time it was at.
    vector<size_t> cycles;
    map<size_t, set<string> > events;
    void add_to_inputs(size_t c, string name, bool value);
    void add_gate(Gate g);
    void run();
};

