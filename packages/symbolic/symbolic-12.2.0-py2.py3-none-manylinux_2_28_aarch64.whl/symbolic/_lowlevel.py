# auto-generated file
__all__ = ['lib', 'ffi']

import os
from symbolic._lowlevel__ffi import ffi

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), '_lowlevel__lib.so'), 2)
del os
