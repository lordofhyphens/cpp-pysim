// event-driven simulator
#include <vector>
#include <map>
#include <utility>
#include <exception>
#include <algorithm>
#include <string>
#include <iostream>

#include "sim.h"

using namespace std;
bool EventSim::get_value(string name) {
  const auto& gat = results[name];
  const auto& iter = gat.lower_bound(t);
  const auto& exact = gat.find(t);
  const auto& last = gat.crbegin();
  
  if (gat.size() > 0 and last->first <= t) {
    return last->second;
  } else if (iter == gat.end() and exact == gat.end()) {
    return false;
  }
  else if (exact->first <= t) {
    return exact->second;
  }
  else if (iter->first > t) {
    return false;
  }
  return iter->second;
}
void EventSim::run() {
  end_sim = false;
  bool last_cycle = false;
  while (!end_sim) {
    if (t % (ckt.size() * 2) == 0) { // wait for 2x number of gates in case we run into unseen cycles.
      if (verbosity > 5) cout << "Start cycle: " << c << "\n";
      if (last_cycle) end_sim = true;
      next_inputs = inputs[c];
      inputs.erase(c);
      // clear the processing queue and load the input vectors for the next cycle.
      for_each(next_inputs.cbegin(), next_inputs.cend(), 
        [this](const pair<string,bool> ob) { events[t].insert(ob.first); });
      // load the last 
      if (t > 0)
      for_each(ckt.cbegin(), ckt.cend(), 
        [this](const pair<string,Gate> ob) { bool temp_result = get_value(ob.first); results[ob.first][t-1] = temp_result; });

      c++; // update current cycle step
      if (inputs.size() == 0) last_cycle = true;
      if (t > 0) cycles.push_back(t-1);
      }
    if (!end_sim) {
      for_each(events[t].begin(), events[t].end(), [this](string ob) { this->process_gate(ob); });
      for (auto i = new_events.cbegin(); i != new_events.cend(); i++) {
        if (events.find(i->first) == events.end()) {
          events[i->first] = i->second;
        } else {
          for_each(i->second.cbegin(), i->second.cend(), [this,i](string ob) { events[i->first].insert(ob);} );
        }
        new_events = map<size_t, set<string>>();
        
      }
      t++; // update current time step;
      if (verbosity > 5 && t % 1000 == 0) cout << "Time step: " << t << "\n";
    }
  }
  for_each(ckt.cbegin(), ckt.cend(), 
      [this](const pair<string,Gate> ob) { results[ob.first][t] = get_value(ob.first); });
  if (verbosity > 5) cout << "End simulation.\n";
  if (verbosity > 5) cout << "Removing non-outputs from results.\n";
  size_t orig_size = results.size();
  for_each(results.begin(), results.end(), [this](pair<string, result_t> ob) { if (this->ckt[ob.first].fanout.size() != 0) this->results.erase(ob.first);});
  if (verbosity > 5) cout << "Removed " << orig_size - results.size() << " non-outputs from result size of " << orig_size << ".\n";
}

void EventSim::process_gate(const string &name) {
  // short circuit in the case that we have "extra" inputs 
  // or somehow have gates in the event list that are not in
  // the circuit
  if (ckt.find(name) == ckt.cend()) return; 

  const auto& g = ckt[name];
  const auto& fins = g.fanin;
  auto result = false;
  switch (g.function) {
    case gate_t::BSC:
      if (!bist);
        // copy the fanins to this gate if not bist, otherwise treat as an input;
        result = any_of(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); });
        break;
    case gate_t::INPUT:
      result = next_inputs[g.name];
      results[name][t] = result;
      break;
    case gate_t::AND:
    case gate_t::NAND:
      result = all_of(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); });
      break;
    case gate_t::XOR: 
    case gate_t::XNOR:
      result = (count_if(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); }) % 2) == 1;
    case gate_t::OR:
    case gate_t::NOR:
    case gate_t::BUFF:
    case gate_t::NOT:
    case gate_t::TP:
    case gate_t::OUTPUT:
      result = any_of(fins.begin(), fins.end(), [this](string ob) { return get_value(ob); });
      break;
    default:
      ;
  }
  // set for inverting gates
  switch(g.function) {
    case gate_t::NAND:
    case gate_t::XNOR:
    case gate_t::NOT:
    case gate_t::NOR:
      result = !result;
      break;
    default: break;
  }
  // store result in the appropriate time slot for this gate.
  // if there is no change, do not add this gate's fanouts to the event list.
  // unless it's an input or a bsc
  if (result != get_value(name) or g.function == gate_t::INPUT or g.function == gate_t::BSC )
  {
    for (auto i = g.fanout.cbegin(); i != g.fanout.cend(); i++)
    {
      new_events[t+g.delay].insert(*i);
    }
  }
  results[name][t+g.delay] = result;
}

void EventSim::add_to_inputs(size_t c, string name, bool value) {
  // meant to be called iteratively for every cycle + gate
  inputs[c][name] = value;
}

void EventSim::add_gate(const Gate& g) {
  ckt.insert(pair<string, Gate>(g.name, g));
}
void EventSim::dump_results(string filename) {
  ofstream outfile(filename);
  for (auto i = cycles.begin(); i != cycles.end(); i++) {
    const auto cycle = distance(cycles.begin(), i);
    unsigned int t = *i;
    outfile << cycle << ",";
    for (auto g = ckt.cbegin(); g != ckt.cend(); g++) {
      try {
        auto& temp = results.at(g->first);
        outfile << g->first << "," << temp[t] << ",";
      } catch (const out_of_range& oor) {
        if (verbosity > 4)
          cerr << g->first << " not in results array.\n";
      }
    }
    outfile << "\n";
  }
  outfile.close();
}
