 %module EventSim
 %{
 /* Includes the header in the wrapper code */
 #include "sim.h"
 
 %}
 
 /* Parse the header file to generate wrappers */
 %include "std_string.i"
 %include "std_vector.i"
 %include "std_map.i"
 %include "std_set.i"
// Instantiate templates used by example
namespace std {
   %template(StringVector) vector<string>;
   %template(UintVector) vector<size_t>;
   %template(ResultMap) map<unsigned int, bool>;
   %template(ResultQueue) map<string, map<unsigned int, bool> >;
}
%include "sim.h"
