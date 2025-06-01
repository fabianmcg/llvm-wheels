from .. import llvm_lib_path as _llvm_lib_path

from ctypes import cdll as _cdll

_cdll.LoadLibrary(str(_llvm_lib_path("LLVM")))
