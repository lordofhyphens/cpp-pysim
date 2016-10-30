/*
Copyright (c) 2016 Joseph Lenox

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
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
    uninitialized = true;
    return false;
  }
  else if (exact->first <= t) {
    return exact->second;
  }
  else if (iter->first > t) {
    uninitialized = true;
    return false;
  }
  return iter->second;
}

bool EventSim::run_cycle(string filename) {
  if (verbosity > 5) cout << "Start cycle: " << c << "\n";
  
  // load next set of inputs
  next_inputs = inputs[c];
  inputs.erase(c);
  for_each(next_inputs.cbegin(), next_inputs.cend(), 
      [this](const pair<string,bool> ob) { events[t].insert(ob.first); });
  // preload any DFFs
  for_each(dffs.cbegin(), dffs.cend(), 
      [this](const pair<string, result_t> ob) { events[t].insert(ob.first); });

  // run all time steps for this cycle.
  process_events();
  dffs.clear(); // clear out dff list to save memory.
  for_each(ckt.cbegin(), ckt.cend(), 
      [this](const pair<string,Gate> ob) { bool temp_result = get_value(ob.first); results[ob.first][t-1] = temp_result; if (ob.second.function == gate_t::DFF) dffs[ob.first][t-1] = temp_result; });
  cycles.push_back(t-1);

  // dump output
  //for_each(results.begin(), results.end(), [this](pair<string, result_t> ob) { if (this->ckt[ob.first].fanout.size() != 0) this->results.erase(ob.first);}); // clean up non-outputs
  dump_result(filename, c);
  // Save results to dff list.
  results.clear();
  c++;

  return inputs.size() > 0;
}

void EventSim::process_events() {
  size_t local_time = 0;
  // run through all active events.
  while (events.size() > 0 && (local_time < (ckt.size() *2))) { 
    if (events[t].size() == 0) {t++; local_time++; continue;}
    if (verbosity > 15) cout << "start t: " << t << endl;
    if (verbosity > 12) cout << "event list size: " << events.size() <<" "<< events[t].size() << endl;
    for_each(events[t].begin(), events[t].end(), [this](string ob) { this->process_gate(ob); });
    events[t].clear(); // empty current queue
    // copy next round's queue into this round.
    for (auto i = new_events.cbegin(); i != new_events.cend(); i++) {
      if (events.find(i->first) == events.end()) {
        events[i->first] = i->second;
      } else {
        for_each(i->second.cbegin(), i->second.cend(), [this,i](string ob) { events[i->first].insert(ob);} );
      }
    }
    new_events.clear();
    events.erase(t);
    local_time++;
    t++;
    if (verbosity > 5 && t % 1000 == 0) cout << "Time step: " << t << ", this cycle " << local_time << "\n";
  }    
  if (events.size() > 0) 
    cout << events.size() << " Events left in queue after local_time " << local_time << endl;
}

void EventSim::run(string filename) {
  while (run_cycle(filename)); 
  if (verbosity > 5) cout << "End simulation.\n";
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
    case gate_t::DFF_O:
        result = get_value(g.dff_link); // get the newest value, if any
        break;
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
    case gate_t::DFF: // treat DFF inputs like buffers
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
  if (!uninitialized and (result != get_value(name) or g.function == gate_t::INPUT or g.function == gate_t::BSC ))
  {
    for (auto i = g.fanout.cbegin(); i != g.fanout.cend(); i++)
    {
      new_events[t+g.delay].insert(*i);
    }
  } else {
    uninitialized = false; // reset uninitialized to hold back propagation of gates
  }

  if (verbosity > 6) cout << "Pushing " << name << ", " << result << " at time " << t+g.delay << endl;
  results[name][t+g.delay] = result;
}

void EventSim::add_to_inputs(size_t c, string name, bool value) {
  // meant to be called iteratively for every cycle + gate
  inputs[c][name] = value;
}

void EventSim::add_gate(const Gate& g) {
  ckt.insert(pair<string, Gate>(g.name, g));
}
void EventSim::dump_result(string filename, const unsigned int cycle) {
  ofstream outfile;
  if (cycle == 0)
    outfile.open(filename, ofstream::out);
  else 
    outfile.open(filename, ofstream::out | ofstream::app);

  outfile << cycle << ",";
  size_t t = cycles.at(cycle);
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
  outfile.close();
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
