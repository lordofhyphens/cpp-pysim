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
 %include "sim.h"
