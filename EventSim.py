# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_EventSim', [dirname(__file__)])
        except ImportError:
            import _EventSim
            return _EventSim
        if fp is not None:
            try:
                _mod = imp.load_module('_EventSim', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _EventSim = swig_import_helper()
    del swig_import_helper
else:
    import _EventSim
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _EventSim.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _EventSim.SwigPyIterator_value(self)
    def incr(self, n=1): return _EventSim.SwigPyIterator_incr(self, n)
    def decr(self, n=1): return _EventSim.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _EventSim.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _EventSim.SwigPyIterator_equal(self, *args)
    def copy(self): return _EventSim.SwigPyIterator_copy(self)
    def next(self): return _EventSim.SwigPyIterator_next(self)
    def __next__(self): return _EventSim.SwigPyIterator___next__(self)
    def previous(self): return _EventSim.SwigPyIterator_previous(self)
    def advance(self, *args): return _EventSim.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _EventSim.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _EventSim.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _EventSim.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _EventSim.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _EventSim.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _EventSim.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _EventSim.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class StringVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, StringVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, StringVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _EventSim.StringVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _EventSim.StringVector___nonzero__(self)
    def __bool__(self): return _EventSim.StringVector___bool__(self)
    def __len__(self): return _EventSim.StringVector___len__(self)
    def pop(self): return _EventSim.StringVector_pop(self)
    def __getslice__(self, *args): return _EventSim.StringVector___getslice__(self, *args)
    def __setslice__(self, *args): return _EventSim.StringVector___setslice__(self, *args)
    def __delslice__(self, *args): return _EventSim.StringVector___delslice__(self, *args)
    def __delitem__(self, *args): return _EventSim.StringVector___delitem__(self, *args)
    def __getitem__(self, *args): return _EventSim.StringVector___getitem__(self, *args)
    def __setitem__(self, *args): return _EventSim.StringVector___setitem__(self, *args)
    def append(self, *args): return _EventSim.StringVector_append(self, *args)
    def empty(self): return _EventSim.StringVector_empty(self)
    def size(self): return _EventSim.StringVector_size(self)
    def clear(self): return _EventSim.StringVector_clear(self)
    def swap(self, *args): return _EventSim.StringVector_swap(self, *args)
    def get_allocator(self): return _EventSim.StringVector_get_allocator(self)
    def begin(self): return _EventSim.StringVector_begin(self)
    def end(self): return _EventSim.StringVector_end(self)
    def rbegin(self): return _EventSim.StringVector_rbegin(self)
    def rend(self): return _EventSim.StringVector_rend(self)
    def pop_back(self): return _EventSim.StringVector_pop_back(self)
    def erase(self, *args): return _EventSim.StringVector_erase(self, *args)
    def __init__(self, *args): 
        this = _EventSim.new_StringVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _EventSim.StringVector_push_back(self, *args)
    def front(self): return _EventSim.StringVector_front(self)
    def back(self): return _EventSim.StringVector_back(self)
    def assign(self, *args): return _EventSim.StringVector_assign(self, *args)
    def resize(self, *args): return _EventSim.StringVector_resize(self, *args)
    def insert(self, *args): return _EventSim.StringVector_insert(self, *args)
    def reserve(self, *args): return _EventSim.StringVector_reserve(self, *args)
    def capacity(self): return _EventSim.StringVector_capacity(self)
    __swig_destroy__ = _EventSim.delete_StringVector
    __del__ = lambda self : None;
StringVector_swigregister = _EventSim.StringVector_swigregister
StringVector_swigregister(StringVector)

class UintVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, UintVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, UintVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _EventSim.UintVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _EventSim.UintVector___nonzero__(self)
    def __bool__(self): return _EventSim.UintVector___bool__(self)
    def __len__(self): return _EventSim.UintVector___len__(self)
    def pop(self): return _EventSim.UintVector_pop(self)
    def __getslice__(self, *args): return _EventSim.UintVector___getslice__(self, *args)
    def __setslice__(self, *args): return _EventSim.UintVector___setslice__(self, *args)
    def __delslice__(self, *args): return _EventSim.UintVector___delslice__(self, *args)
    def __delitem__(self, *args): return _EventSim.UintVector___delitem__(self, *args)
    def __getitem__(self, *args): return _EventSim.UintVector___getitem__(self, *args)
    def __setitem__(self, *args): return _EventSim.UintVector___setitem__(self, *args)
    def append(self, *args): return _EventSim.UintVector_append(self, *args)
    def empty(self): return _EventSim.UintVector_empty(self)
    def size(self): return _EventSim.UintVector_size(self)
    def clear(self): return _EventSim.UintVector_clear(self)
    def swap(self, *args): return _EventSim.UintVector_swap(self, *args)
    def get_allocator(self): return _EventSim.UintVector_get_allocator(self)
    def begin(self): return _EventSim.UintVector_begin(self)
    def end(self): return _EventSim.UintVector_end(self)
    def rbegin(self): return _EventSim.UintVector_rbegin(self)
    def rend(self): return _EventSim.UintVector_rend(self)
    def pop_back(self): return _EventSim.UintVector_pop_back(self)
    def erase(self, *args): return _EventSim.UintVector_erase(self, *args)
    def __init__(self, *args): 
        this = _EventSim.new_UintVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _EventSim.UintVector_push_back(self, *args)
    def front(self): return _EventSim.UintVector_front(self)
    def back(self): return _EventSim.UintVector_back(self)
    def assign(self, *args): return _EventSim.UintVector_assign(self, *args)
    def resize(self, *args): return _EventSim.UintVector_resize(self, *args)
    def insert(self, *args): return _EventSim.UintVector_insert(self, *args)
    def reserve(self, *args): return _EventSim.UintVector_reserve(self, *args)
    def capacity(self): return _EventSim.UintVector_capacity(self)
    __swig_destroy__ = _EventSim.delete_UintVector
    __del__ = lambda self : None;
UintVector_swigregister = _EventSim.UintVector_swigregister
UintVector_swigregister(UintVector)

class ResultMap(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultMap, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ResultMap, name)
    __repr__ = _swig_repr
    def iterator(self): return _EventSim.ResultMap_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _EventSim.ResultMap___nonzero__(self)
    def __bool__(self): return _EventSim.ResultMap___bool__(self)
    def __len__(self): return _EventSim.ResultMap___len__(self)
    def __iter__(self): return self.key_iterator()
    def iterkeys(self): return self.key_iterator()
    def itervalues(self): return self.value_iterator()
    def iteritems(self): return self.iterator()
    def __getitem__(self, *args): return _EventSim.ResultMap___getitem__(self, *args)
    def __delitem__(self, *args): return _EventSim.ResultMap___delitem__(self, *args)
    def has_key(self, *args): return _EventSim.ResultMap_has_key(self, *args)
    def keys(self): return _EventSim.ResultMap_keys(self)
    def values(self): return _EventSim.ResultMap_values(self)
    def items(self): return _EventSim.ResultMap_items(self)
    def __contains__(self, *args): return _EventSim.ResultMap___contains__(self, *args)
    def key_iterator(self): return _EventSim.ResultMap_key_iterator(self)
    def value_iterator(self): return _EventSim.ResultMap_value_iterator(self)
    def __setitem__(self, *args): return _EventSim.ResultMap___setitem__(self, *args)
    def asdict(self): return _EventSim.ResultMap_asdict(self)
    def __init__(self, *args): 
        this = _EventSim.new_ResultMap(*args)
        try: self.this.append(this)
        except: self.this = this
    def empty(self): return _EventSim.ResultMap_empty(self)
    def size(self): return _EventSim.ResultMap_size(self)
    def clear(self): return _EventSim.ResultMap_clear(self)
    def swap(self, *args): return _EventSim.ResultMap_swap(self, *args)
    def get_allocator(self): return _EventSim.ResultMap_get_allocator(self)
    def begin(self): return _EventSim.ResultMap_begin(self)
    def end(self): return _EventSim.ResultMap_end(self)
    def rbegin(self): return _EventSim.ResultMap_rbegin(self)
    def rend(self): return _EventSim.ResultMap_rend(self)
    def count(self, *args): return _EventSim.ResultMap_count(self, *args)
    def erase(self, *args): return _EventSim.ResultMap_erase(self, *args)
    def find(self, *args): return _EventSim.ResultMap_find(self, *args)
    def lower_bound(self, *args): return _EventSim.ResultMap_lower_bound(self, *args)
    def upper_bound(self, *args): return _EventSim.ResultMap_upper_bound(self, *args)
    __swig_destroy__ = _EventSim.delete_ResultMap
    __del__ = lambda self : None;
ResultMap_swigregister = _EventSim.ResultMap_swigregister
ResultMap_swigregister(ResultMap)

class ResultQueue(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultQueue, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ResultQueue, name)
    __repr__ = _swig_repr
    def iterator(self): return _EventSim.ResultQueue_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _EventSim.ResultQueue___nonzero__(self)
    def __bool__(self): return _EventSim.ResultQueue___bool__(self)
    def __len__(self): return _EventSim.ResultQueue___len__(self)
    def __iter__(self): return self.key_iterator()
    def iterkeys(self): return self.key_iterator()
    def itervalues(self): return self.value_iterator()
    def iteritems(self): return self.iterator()
    def __getitem__(self, *args): return _EventSim.ResultQueue___getitem__(self, *args)
    def __delitem__(self, *args): return _EventSim.ResultQueue___delitem__(self, *args)
    def has_key(self, *args): return _EventSim.ResultQueue_has_key(self, *args)
    def keys(self): return _EventSim.ResultQueue_keys(self)
    def values(self): return _EventSim.ResultQueue_values(self)
    def items(self): return _EventSim.ResultQueue_items(self)
    def __contains__(self, *args): return _EventSim.ResultQueue___contains__(self, *args)
    def key_iterator(self): return _EventSim.ResultQueue_key_iterator(self)
    def value_iterator(self): return _EventSim.ResultQueue_value_iterator(self)
    def __setitem__(self, *args): return _EventSim.ResultQueue___setitem__(self, *args)
    def asdict(self): return _EventSim.ResultQueue_asdict(self)
    def __init__(self, *args): 
        this = _EventSim.new_ResultQueue(*args)
        try: self.this.append(this)
        except: self.this = this
    def empty(self): return _EventSim.ResultQueue_empty(self)
    def size(self): return _EventSim.ResultQueue_size(self)
    def clear(self): return _EventSim.ResultQueue_clear(self)
    def swap(self, *args): return _EventSim.ResultQueue_swap(self, *args)
    def get_allocator(self): return _EventSim.ResultQueue_get_allocator(self)
    def begin(self): return _EventSim.ResultQueue_begin(self)
    def end(self): return _EventSim.ResultQueue_end(self)
    def rbegin(self): return _EventSim.ResultQueue_rbegin(self)
    def rend(self): return _EventSim.ResultQueue_rend(self)
    def count(self, *args): return _EventSim.ResultQueue_count(self, *args)
    def erase(self, *args): return _EventSim.ResultQueue_erase(self, *args)
    def find(self, *args): return _EventSim.ResultQueue_find(self, *args)
    def lower_bound(self, *args): return _EventSim.ResultQueue_lower_bound(self, *args)
    def upper_bound(self, *args): return _EventSim.ResultQueue_upper_bound(self, *args)
    __swig_destroy__ = _EventSim.delete_ResultQueue
    __del__ = lambda self : None;
ResultQueue_swigregister = _EventSim.ResultQueue_swigregister
ResultQueue_swigregister(ResultQueue)

BSC = _EventSim.BSC
TP = _EventSim.TP
INPUT = _EventSim.INPUT
AND = _EventSim.AND
NAND = _EventSim.NAND
OR = _EventSim.OR
NOR = _EventSim.NOR
XOR = _EventSim.XOR
XNOR = _EventSim.XNOR
BUFF = _EventSim.BUFF
NOT = _EventSim.NOT
OUTPUT = _EventSim.OUTPUT
DFF_O = _EventSim.DFF_O
DFF = _EventSim.DFF
DUMMY = _EventSim.DUMMY
class Gate(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Gate, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Gate, name)
    __repr__ = _swig_repr
    __swig_setmethods__["function"] = _EventSim.Gate_function_set
    __swig_getmethods__["function"] = _EventSim.Gate_function_get
    if _newclass:function = _swig_property(_EventSim.Gate_function_get, _EventSim.Gate_function_set)
    __swig_getmethods__["name"] = _EventSim.Gate_name_get
    if _newclass:name = _swig_property(_EventSim.Gate_name_get)
    __swig_setmethods__["dff_link"] = _EventSim.Gate_dff_link_set
    __swig_getmethods__["dff_link"] = _EventSim.Gate_dff_link_get
    if _newclass:dff_link = _swig_property(_EventSim.Gate_dff_link_get, _EventSim.Gate_dff_link_set)
    __swig_getmethods__["delay"] = _EventSim.Gate_delay_get
    if _newclass:delay = _swig_property(_EventSim.Gate_delay_get)
    __swig_setmethods__["fanin"] = _EventSim.Gate_fanin_set
    __swig_getmethods__["fanin"] = _EventSim.Gate_fanin_get
    if _newclass:fanin = _swig_property(_EventSim.Gate_fanin_get, _EventSim.Gate_fanin_set)
    __swig_setmethods__["fanout"] = _EventSim.Gate_fanout_set
    __swig_getmethods__["fanout"] = _EventSim.Gate_fanout_get
    if _newclass:fanout = _swig_property(_EventSim.Gate_fanout_get, _EventSim.Gate_fanout_set)
    __swig_setmethods__["output"] = _EventSim.Gate_output_set
    __swig_getmethods__["output"] = _EventSim.Gate_output_get
    if _newclass:output = _swig_property(_EventSim.Gate_output_get, _EventSim.Gate_output_set)
    __swig_setmethods__["primary_output"] = _EventSim.Gate_primary_output_set
    __swig_getmethods__["primary_output"] = _EventSim.Gate_primary_output_get
    if _newclass:primary_output = _swig_property(_EventSim.Gate_primary_output_get, _EventSim.Gate_primary_output_set)
    __swig_setmethods__["verbosity"] = _EventSim.Gate_verbosity_set
    __swig_getmethods__["verbosity"] = _EventSim.Gate_verbosity_get
    if _newclass:verbosity = _swig_property(_EventSim.Gate_verbosity_get, _EventSim.Gate_verbosity_set)
    def __init__(self, *args): 
        this = _EventSim.new_Gate(*args)
        try: self.this.append(this)
        except: self.this = this
    def debug_print(self): return _EventSim.Gate_debug_print(self)
    def nfin(self): return _EventSim.Gate_nfin(self)
    def nfot(self): return _EventSim.Gate_nfot(self)
    __swig_destroy__ = _EventSim.delete_Gate
    __del__ = lambda self : None;
Gate_swigregister = _EventSim.Gate_swigregister
Gate_swigregister(Gate)

class EventSim(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, EventSim, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, EventSim, name)
    __repr__ = _swig_repr
    __swig_setmethods__["bist"] = _EventSim.EventSim_bist_set
    __swig_getmethods__["bist"] = _EventSim.EventSim_bist_get
    if _newclass:bist = _swig_property(_EventSim.EventSim_bist_get, _EventSim.EventSim_bist_set)
    __swig_setmethods__["ckt"] = _EventSim.EventSim_ckt_set
    __swig_getmethods__["ckt"] = _EventSim.EventSim_ckt_get
    if _newclass:ckt = _swig_property(_EventSim.EventSim_ckt_get, _EventSim.EventSim_ckt_set)
    __swig_setmethods__["inputs"] = _EventSim.EventSim_inputs_set
    __swig_getmethods__["inputs"] = _EventSim.EventSim_inputs_get
    if _newclass:inputs = _swig_property(_EventSim.EventSim_inputs_get, _EventSim.EventSim_inputs_set)
    __swig_setmethods__["results"] = _EventSim.EventSim_results_set
    __swig_getmethods__["results"] = _EventSim.EventSim_results_get
    if _newclass:results = _swig_property(_EventSim.EventSim_results_get, _EventSim.EventSim_results_set)
    __swig_setmethods__["dffs"] = _EventSim.EventSim_dffs_set
    __swig_getmethods__["dffs"] = _EventSim.EventSim_dffs_get
    if _newclass:dffs = _swig_property(_EventSim.EventSim_dffs_get, _EventSim.EventSim_dffs_set)
    __swig_setmethods__["cycles"] = _EventSim.EventSim_cycles_set
    __swig_getmethods__["cycles"] = _EventSim.EventSim_cycles_get
    if _newclass:cycles = _swig_property(_EventSim.EventSim_cycles_get, _EventSim.EventSim_cycles_set)
    __swig_setmethods__["events"] = _EventSim.EventSim_events_set
    __swig_getmethods__["events"] = _EventSim.EventSim_events_get
    if _newclass:events = _swig_property(_EventSim.EventSim_events_get, _EventSim.EventSim_events_set)
    __swig_setmethods__["new_events"] = _EventSim.EventSim_new_events_set
    __swig_getmethods__["new_events"] = _EventSim.EventSim_new_events_get
    if _newclass:new_events = _swig_property(_EventSim.EventSim_new_events_get, _EventSim.EventSim_new_events_set)
    def add_to_inputs(self, *args): return _EventSim.EventSim_add_to_inputs(self, *args)
    def add_gate(self, *args): return _EventSim.EventSim_add_gate(self, *args)
    def run(self, *args): return _EventSim.EventSim_run(self, *args)
    def dump_results(self, *args): return _EventSim.EventSim_dump_results(self, *args)
    def dump_result(self, *args): return _EventSim.EventSim_dump_result(self, *args)
    def __init__(self, *args): 
        this = _EventSim.new_EventSim(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _EventSim.delete_EventSim
    __del__ = lambda self : None;
EventSim_swigregister = _EventSim.EventSim_swigregister
EventSim_swigregister(EventSim)

# This file is compatible with both classic and new-style classes.


