/*
Copyright (c) 2016 Joseph Lenox

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
#include "kl.hpp"
#include "sim.h"
#include <algorithm>
#include <iterator>
#include <tuple>
#include <string>
#include <iostream>
using namespace std;

const int KLPartition::gain(const string &a, const string &b) {
    const int c_ab = ( 
        find(begin(ckt[a].fanin), end(ckt[a].fanin), b) != end(ckt[a].fanin) ||
        find(begin(ckt[a].fanout), end(ckt[a].fanout), b) != end(ckt[a].fanout) ||
        find(begin(ckt[b].fanin), end(ckt[b].fanin), b) != end(ckt[b].fanin) ||
        find(begin(ckt[b].fanout), end(ckt[b].fanout), b) != end(ckt[b].fanout) ? 1 : 0);
    return Dv[a] + Dv[b] - 2*c_ab;
}

const int KLPartition::calc_dv(const string &v, set<string> a, set<string> b) {
    int ec = 0, enc = 0;
    ec += count_if(begin(ckt[v].fanin), end(ckt[v].fanin), [&](auto s){ return find(begin(b), end(b), s) != end(b);} );
    ec += count_if(begin(ckt[v].fanout), end(ckt[v].fanout), [&](auto s){ return find(begin(b), end(b), s) != end(b);} );

    enc += count_if(begin(ckt[v].fanin), end(ckt[v].fanin), [&](auto s){ return find(begin(a), end(a), s) != end(a);} );
    enc += count_if(begin(ckt[v].fanout), end(ckt[v].fanout), [&](auto s){ return find(begin(a), end(a), s) != end(a);} );

    return ec - enc;
}

pair<vector<string>, vector<string> > KLPartition::partition_once(vector<string> initial) {
    vector<string> a, b; // partitions
    int GMAX = 0;
    for (size_t i = 0; i < initial.size(); i++) {
        // distribute to initial partitions
        if (i % 2) {
            a.emplace_back(initial[i]);
        } else {
            b.emplace_back(initial[i]);
        }
    }

    do 
    {
        set<string> a_tmp, b_tmp;
        // reset 
        for_each(begin(a), end(a), [&](string s) {a_tmp.insert(s);});
        for_each(begin(b), end(b), [&](string s) {b_tmp.insert(s);});

        vector< tuple<string, string, int> > fixed;
        for_each(begin(a), end(a), [a_tmp,b_tmp,this](string s) { this->Dv[s] = calc_dv(s, a_tmp, b_tmp);});
        for_each(begin(b), end(b), [a_tmp,b_tmp,this](string s) { this->Dv[s] = calc_dv(s, a_tmp, b_tmp);});

        string a_max = *(a_tmp.begin());
        string b_max = *(b_tmp.begin());

        int g_max = gain(a_max, b_max);

        for (size_t n = 0; n < initial.size() / 2; n++) {
            for (auto a_i = begin(a); a_i != end(a); a_i++) {
                for (auto b_j = begin(b); b_j != end(b); b_j++) {
                    int tmp_g = gain(*a_i, *b_j);
                    if (tmp_g > g_max) {
                        g_max = tmp_g;
                        a_max = *a_i;
                        b_max = *b_j;
                    }
                    cerr << n << ": Comparing " << *a_i << ", " << *b_j << "; gain " << tmp_g << endl;
                }
            }
            fixed.push_back(tuple<string, string, int>(a_max, b_max, g_max));
            a_tmp.erase(a_max);
            b_tmp.erase(b_max);
            for_each(begin(a), end(a), [=](string s) { this->Dv[s] = calc_dv(s, a_tmp, b_tmp);});
            for_each(begin(b), end(b), [=](string s) { this->Dv[s] = calc_dv(s, a_tmp, b_tmp);});
        }
        // find k which maximizes sum of g values 
        int index = 0, sum = 0;
        GMAX = 0;
        for (int i = 0; i < fixed.size(); i++) {
            sum += get<2>(fixed[i]);
            if (sum > GMAX) {
                index = i+1;
                GMAX = sum;
            }
        }
        cerr << "GMAX: " << GMAX << endl;
        if (GMAX > 0) {
            // perform swaps up for our count
            for (int i = 0; i < index; i++) {
                replace(begin(a), end(a), get<0>(fixed[i]), get<1>(fixed[i]));
                replace(begin(b), end(b), get<1>(fixed[i]), get<0>(fixed[i]));
            }
        }
        // if this sum > 0, perform the swaps on the true array
    } while (GMAX > 0);
    vector<string> a_out, b_out;
    for_each(begin(a), end(a), [&](string s) { a_out.push_back(s);});
    for_each(begin(b), end(b), [&](string s) { b_out.push_back(s);});
    return pair<vector<string>, vector<string> >(a_out, b_out);
}

void KLPartition::add_gate(const Gate& g) {
  ckt.insert(pair<string, Gate>(g.name, g));
}
