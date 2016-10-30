/*
Copyright (c) 2016 Joseph Lenox

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/ 
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
