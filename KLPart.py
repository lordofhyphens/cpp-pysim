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
            fp, pathname, description = imp.find_module('_KLPart', [dirname(__file__)])
        except ImportError:
            import _KLPart
            return _KLPart
        if fp is not None:
            try:
                _mod = imp.load_module('_KLPart', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _KLPart = swig_import_helper()
    del swig_import_helper
else:
    import _KLPart
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
    __swig_destroy__ = _KLPart.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _KLPart.SwigPyIterator_value(self)
    def incr(self, n=1): return _KLPart.SwigPyIterator_incr(self, n)
    def decr(self, n=1): return _KLPart.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _KLPart.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _KLPart.SwigPyIterator_equal(self, *args)
    def copy(self): return _KLPart.SwigPyIterator_copy(self)
    def next(self): return _KLPart.SwigPyIterator_next(self)
    def __next__(self): return _KLPart.SwigPyIterator___next__(self)
    def previous(self): return _KLPart.SwigPyIterator_previous(self)
    def advance(self, *args): return _KLPart.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _KLPart.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _KLPart.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _KLPart.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _KLPart.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _KLPart.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _KLPart.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _KLPart.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class PairStringVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PairStringVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PairStringVector, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _KLPart.new_PairStringVector(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_setmethods__["first"] = _KLPart.PairStringVector_first_set
    __swig_getmethods__["first"] = _KLPart.PairStringVector_first_get
    if _newclass:first = _swig_property(_KLPart.PairStringVector_first_get, _KLPart.PairStringVector_first_set)
    __swig_setmethods__["second"] = _KLPart.PairStringVector_second_set
    __swig_getmethods__["second"] = _KLPart.PairStringVector_second_get
    if _newclass:second = _swig_property(_KLPart.PairStringVector_second_get, _KLPart.PairStringVector_second_set)
    def __len__(self): return 2
    def __repr__(self): return str((self.first, self.second))
    def __getitem__(self, index): 
      if not (index % 2): 
        return self.first
      else:
        return self.second
    def __setitem__(self, index, val):
      if not (index % 2): 
        self.first = val
      else:
        self.second = val
    __swig_destroy__ = _KLPart.delete_PairStringVector
    __del__ = lambda self : None;
PairStringVector_swigregister = _KLPart.PairStringVector_swigregister
PairStringVector_swigregister(PairStringVector)

class StringVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, StringVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, StringVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _KLPart.StringVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _KLPart.StringVector___nonzero__(self)
    def __bool__(self): return _KLPart.StringVector___bool__(self)
    def __len__(self): return _KLPart.StringVector___len__(self)
    def pop(self): return _KLPart.StringVector_pop(self)
    def __getslice__(self, *args): return _KLPart.StringVector___getslice__(self, *args)
    def __setslice__(self, *args): return _KLPart.StringVector___setslice__(self, *args)
    def __delslice__(self, *args): return _KLPart.StringVector___delslice__(self, *args)
    def __delitem__(self, *args): return _KLPart.StringVector___delitem__(self, *args)
    def __getitem__(self, *args): return _KLPart.StringVector___getitem__(self, *args)
    def __setitem__(self, *args): return _KLPart.StringVector___setitem__(self, *args)
    def append(self, *args): return _KLPart.StringVector_append(self, *args)
    def empty(self): return _KLPart.StringVector_empty(self)
    def size(self): return _KLPart.StringVector_size(self)
    def clear(self): return _KLPart.StringVector_clear(self)
    def swap(self, *args): return _KLPart.StringVector_swap(self, *args)
    def get_allocator(self): return _KLPart.StringVector_get_allocator(self)
    def begin(self): return _KLPart.StringVector_begin(self)
    def end(self): return _KLPart.StringVector_end(self)
    def rbegin(self): return _KLPart.StringVector_rbegin(self)
    def rend(self): return _KLPart.StringVector_rend(self)
    def pop_back(self): return _KLPart.StringVector_pop_back(self)
    def erase(self, *args): return _KLPart.StringVector_erase(self, *args)
    def __init__(self, *args): 
        this = _KLPart.new_StringVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _KLPart.StringVector_push_back(self, *args)
    def front(self): return _KLPart.StringVector_front(self)
    def back(self): return _KLPart.StringVector_back(self)
    def assign(self, *args): return _KLPart.StringVector_assign(self, *args)
    def resize(self, *args): return _KLPart.StringVector_resize(self, *args)
    def insert(self, *args): return _KLPart.StringVector_insert(self, *args)
    def reserve(self, *args): return _KLPart.StringVector_reserve(self, *args)
    def capacity(self): return _KLPart.StringVector_capacity(self)
    __swig_destroy__ = _KLPart.delete_StringVector
    __del__ = lambda self : None;
StringVector_swigregister = _KLPart.StringVector_swigregister
StringVector_swigregister(StringVector)

class UintVector(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, UintVector, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, UintVector, name)
    __repr__ = _swig_repr
    def iterator(self): return _KLPart.UintVector_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _KLPart.UintVector___nonzero__(self)
    def __bool__(self): return _KLPart.UintVector___bool__(self)
    def __len__(self): return _KLPart.UintVector___len__(self)
    def pop(self): return _KLPart.UintVector_pop(self)
    def __getslice__(self, *args): return _KLPart.UintVector___getslice__(self, *args)
    def __setslice__(self, *args): return _KLPart.UintVector___setslice__(self, *args)
    def __delslice__(self, *args): return _KLPart.UintVector___delslice__(self, *args)
    def __delitem__(self, *args): return _KLPart.UintVector___delitem__(self, *args)
    def __getitem__(self, *args): return _KLPart.UintVector___getitem__(self, *args)
    def __setitem__(self, *args): return _KLPart.UintVector___setitem__(self, *args)
    def append(self, *args): return _KLPart.UintVector_append(self, *args)
    def empty(self): return _KLPart.UintVector_empty(self)
    def size(self): return _KLPart.UintVector_size(self)
    def clear(self): return _KLPart.UintVector_clear(self)
    def swap(self, *args): return _KLPart.UintVector_swap(self, *args)
    def get_allocator(self): return _KLPart.UintVector_get_allocator(self)
    def begin(self): return _KLPart.UintVector_begin(self)
    def end(self): return _KLPart.UintVector_end(self)
    def rbegin(self): return _KLPart.UintVector_rbegin(self)
    def rend(self): return _KLPart.UintVector_rend(self)
    def pop_back(self): return _KLPart.UintVector_pop_back(self)
    def erase(self, *args): return _KLPart.UintVector_erase(self, *args)
    def __init__(self, *args): 
        this = _KLPart.new_UintVector(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _KLPart.UintVector_push_back(self, *args)
    def front(self): return _KLPart.UintVector_front(self)
    def back(self): return _KLPart.UintVector_back(self)
    def assign(self, *args): return _KLPart.UintVector_assign(self, *args)
    def resize(self, *args): return _KLPart.UintVector_resize(self, *args)
    def insert(self, *args): return _KLPart.UintVector_insert(self, *args)
    def reserve(self, *args): return _KLPart.UintVector_reserve(self, *args)
    def capacity(self): return _KLPart.UintVector_capacity(self)
    __swig_destroy__ = _KLPart.delete_UintVector
    __del__ = lambda self : None;
UintVector_swigregister = _KLPart.UintVector_swigregister
UintVector_swigregister(UintVector)

class ResultMap(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultMap, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ResultMap, name)
    __repr__ = _swig_repr
    def iterator(self): return _KLPart.ResultMap_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _KLPart.ResultMap___nonzero__(self)
    def __bool__(self): return _KLPart.ResultMap___bool__(self)
    def __len__(self): return _KLPart.ResultMap___len__(self)
    def __iter__(self): return self.key_iterator()
    def iterkeys(self): return self.key_iterator()
    def itervalues(self): return self.value_iterator()
    def iteritems(self): return self.iterator()
    def __getitem__(self, *args): return _KLPart.ResultMap___getitem__(self, *args)
    def __delitem__(self, *args): return _KLPart.ResultMap___delitem__(self, *args)
    def has_key(self, *args): return _KLPart.ResultMap_has_key(self, *args)
    def keys(self): return _KLPart.ResultMap_keys(self)
    def values(self): return _KLPart.ResultMap_values(self)
    def items(self): return _KLPart.ResultMap_items(self)
    def __contains__(self, *args): return _KLPart.ResultMap___contains__(self, *args)
    def key_iterator(self): return _KLPart.ResultMap_key_iterator(self)
    def value_iterator(self): return _KLPart.ResultMap_value_iterator(self)
    def __setitem__(self, *args): return _KLPart.ResultMap___setitem__(self, *args)
    def asdict(self): return _KLPart.ResultMap_asdict(self)
    def __init__(self, *args): 
        this = _KLPart.new_ResultMap(*args)
        try: self.this.append(this)
        except: self.this = this
    def empty(self): return _KLPart.ResultMap_empty(self)
    def size(self): return _KLPart.ResultMap_size(self)
    def clear(self): return _KLPart.ResultMap_clear(self)
    def swap(self, *args): return _KLPart.ResultMap_swap(self, *args)
    def get_allocator(self): return _KLPart.ResultMap_get_allocator(self)
    def begin(self): return _KLPart.ResultMap_begin(self)
    def end(self): return _KLPart.ResultMap_end(self)
    def rbegin(self): return _KLPart.ResultMap_rbegin(self)
    def rend(self): return _KLPart.ResultMap_rend(self)
    def count(self, *args): return _KLPart.ResultMap_count(self, *args)
    def erase(self, *args): return _KLPart.ResultMap_erase(self, *args)
    def find(self, *args): return _KLPart.ResultMap_find(self, *args)
    def lower_bound(self, *args): return _KLPart.ResultMap_lower_bound(self, *args)
    def upper_bound(self, *args): return _KLPart.ResultMap_upper_bound(self, *args)
    __swig_destroy__ = _KLPart.delete_ResultMap
    __del__ = lambda self : None;
ResultMap_swigregister = _KLPart.ResultMap_swigregister
ResultMap_swigregister(ResultMap)

class ResultQueue(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultQueue, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ResultQueue, name)
    __repr__ = _swig_repr
    def iterator(self): return _KLPart.ResultQueue_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _KLPart.ResultQueue___nonzero__(self)
    def __bool__(self): return _KLPart.ResultQueue___bool__(self)
    def __len__(self): return _KLPart.ResultQueue___len__(self)
    def __iter__(self): return self.key_iterator()
    def iterkeys(self): return self.key_iterator()
    def itervalues(self): return self.value_iterator()
    def iteritems(self): return self.iterator()
    def __getitem__(self, *args): return _KLPart.ResultQueue___getitem__(self, *args)
    def __delitem__(self, *args): return _KLPart.ResultQueue___delitem__(self, *args)
    def has_key(self, *args): return _KLPart.ResultQueue_has_key(self, *args)
    def keys(self): return _KLPart.ResultQueue_keys(self)
    def values(self): return _KLPart.ResultQueue_values(self)
    def items(self): return _KLPart.ResultQueue_items(self)
    def __contains__(self, *args): return _KLPart.ResultQueue___contains__(self, *args)
    def key_iterator(self): return _KLPart.ResultQueue_key_iterator(self)
    def value_iterator(self): return _KLPart.ResultQueue_value_iterator(self)
    def __setitem__(self, *args): return _KLPart.ResultQueue___setitem__(self, *args)
    def asdict(self): return _KLPart.ResultQueue_asdict(self)
    def __init__(self, *args): 
        this = _KLPart.new_ResultQueue(*args)
        try: self.this.append(this)
        except: self.this = this
    def empty(self): return _KLPart.ResultQueue_empty(self)
    def size(self): return _KLPart.ResultQueue_size(self)
    def clear(self): return _KLPart.ResultQueue_clear(self)
    def swap(self, *args): return _KLPart.ResultQueue_swap(self, *args)
    def get_allocator(self): return _KLPart.ResultQueue_get_allocator(self)
    def begin(self): return _KLPart.ResultQueue_begin(self)
    def end(self): return _KLPart.ResultQueue_end(self)
    def rbegin(self): return _KLPart.ResultQueue_rbegin(self)
    def rend(self): return _KLPart.ResultQueue_rend(self)
    def count(self, *args): return _KLPart.ResultQueue_count(self, *args)
    def erase(self, *args): return _KLPart.ResultQueue_erase(self, *args)
    def find(self, *args): return _KLPart.ResultQueue_find(self, *args)
    def lower_bound(self, *args): return _KLPart.ResultQueue_lower_bound(self, *args)
    def upper_bound(self, *args): return _KLPart.ResultQueue_upper_bound(self, *args)
    __swig_destroy__ = _KLPart.delete_ResultQueue
    __del__ = lambda self : None;
ResultQueue_swigregister = _KLPart.ResultQueue_swigregister
ResultQueue_swigregister(ResultQueue)

class KLPartition(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, KLPartition, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, KLPartition, name)
    __repr__ = _swig_repr
    def __init__(self): 
        this = _KLPart.new_KLPartition()
        try: self.this.append(this)
        except: self.this = this
    __swig_getmethods__["ckt"] = _KLPart.KLPartition_ckt_get
    if _newclass:ckt = _swig_property(_KLPart.KLPartition_ckt_get)
    def partition_once(self, *args): return _KLPart.KLPartition_partition_once(self, *args)
    def add_gate(self, *args): return _KLPart.KLPartition_add_gate(self, *args)
    __swig_destroy__ = _KLPart.delete_KLPartition
    __del__ = lambda self : None;
KLPartition_swigregister = _KLPart.KLPartition_swigregister
KLPartition_swigregister(KLPartition)

# This file is compatible with both classic and new-style classes.


