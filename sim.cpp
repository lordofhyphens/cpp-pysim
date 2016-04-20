// event-driven simulator
#include <set>
#include <map>
#include <utility>
#include <exception>
#include <algorithm>

#include "sim.h"

using namespace std;
bool EventSim::get_value(string name) {
  const auto& gat = results[name];
  const auto& iter = gat.lower_bound(t);
  // check to make sure it's not end and it is not greater -- these are invalid
  // if invalid, throw an exception, to be handled at the using level. 
  // exception means that this data is not-usable.
  if (iter == results[name].end())
    return false;
  else if (iter->first > t)
    return false;
  return iter->second;
}
void EventSim::run() {
  end_sim = false;
  while (!end_sim) {
    if (t % (ckt.size() * 5) == 0) { // wait for 5x number of gates in case we run into unseen cycles.
      cycles.push_back(t);
      next_inputs = inputs[c];
      inputs.erase(c);
      // clear the processing queue and load the input vectors for the next cycle.
      for_each(next_inputs.cbegin(), next_inputs.cend(), 
        [this](const pair<string,bool> ob) { events[t].insert(ob.first); });
      c++; // update current cycle step
      if (inputs.size() == 0) end_sim = true;
    }
    for_each(events[t].cbegin(), events[t].cend(), [this](string ob) { this->process_gate(ob); });
    t++; // update current time step;
  }
}

void EventSim::process_gate(const string &name) {
  const auto& g = ckt[name];
  const auto& fins = g.fanin;
  auto result = false;
  switch (g.function) {
    case Gate::gate_t::BSC:
      if (!bist);
        // copy the fanins to this gate if not bist, otherwise treat as an input;
        result = any_of(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); });
        break;
    case Gate::gate_t::INPUT:
      result = next_inputs[g.name];
      break;
    case Gate::gate_t::AND:
    case Gate::gate_t::NAND:
      result = all_of(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); });
      break;
    case Gate::gate_t::XOR: 
    case Gate::gate_t::XNOR:
      result = (count_if(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); }) % 2) == 1;
    case Gate::gate_t::OR:
    case Gate::gate_t::NOR:
    case Gate::gate_t::BUFF:
    case Gate::gate_t::NOT:
    case Gate::gate_t::TP:
    case Gate::gate_t::OUTPUT:
      result = any_of(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); });
      break;
    default:
      ;
  }
  // set for inverting gates
  switch(g.function) {
    case Gate::gate_t::NAND:
    case Gate::gate_t::XNOR:
    case Gate::gate_t::NOT:
    case Gate::gate_t::NOR:
      result = !result;
      break;
    default: break;
  }
  // store result in the appropriate time slot for this gate.
  // if there is no change, do not add this gate's fanouts to the event list.
  // unless it's an input or a bsc
  if (result != get_value(name) or g.function == Gate::gate_t::INPUT or g.function == Gate::gate_t::BSC )
    for (auto i = g.fanout.cbegin(); i != g.fanout.cend(); i++)
      events[t+g.delay].insert(*i);
  results[name][t+g.delay] = result;
}

void EventSim::add_to_inputs(size_t c, string name, bool value) {
  // meant to be called iteratively for every cycle + gate
  inputs[c][name] = value;
}

void EventSim::add_gate(Gate g) {
  ckt[g.name] = g;
}
