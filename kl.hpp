#include <map>
#include <set>
#include <string>
#include <utility>
#include "sim.h"

using namespace std;
class KLPartition {
    private:
        map<string, int> Dv;
        const int gain(const string &a, const string &b);
        const int calc_dv(const string &v, set<string> a, set<string> b);
    public:
        KLPartition() : ckt(map<string, Gate>()) {}
        const map<string, Gate> ckt;
        pair<vector<string>, vector<string> > partition_once(vector<string> initial);
        void add_gate(const Gate& g);

};
