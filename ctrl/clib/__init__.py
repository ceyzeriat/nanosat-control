#!/usr/bin/env python
# -*- coding: utf-8 -*-


import glob
import os
import time
from subprocess import Popen as subprocessPopen
from subprocess import PIPE as subprocessPIPE
from subprocess import STDOUT as subprocessSTDOUT
from ctypes import cdll


# each *.c file must contain 1 and only 1 function that python
# should be aware of. This file should be of format
# <function_name>.c together with the <function_name>.h file.
from ctypes import c_uint
libs_register = [("crc", c_uint, "checksum"),
                 ("crc_chained", c_uint, "checksum_chained")]


__all__ = []


ROOTC = os.path.dirname(os.path.abspath(__file__))

_calling = {}
for item in libs_register:
    if len(item) == 2:
        lib, typ = item
        wrap = None
    else:
        lib, typ, wrap = item
    # compilation if needed
    if len(glob.glob("{}/{}.so".format(ROOTC, lib))) == 0:
        print("Compiling '{}'".format(lib))
        cmd = "gcc -o {}/{}.so -shared -fPIC {}/{}.c".format(   ROOTC, lib,
                                                                ROOTC, lib)
        dum = subprocessPopen(  cmd, shell=True,
                                stderr=subprocessSTDOUT,
                                stdout=subprocessPIPE)
        time.sleep(1)
    # load in memory
    _dum = getattr(cdll.LoadLibrary("{}/{}.so".format(ROOTC, lib)), lib)
    _dum.restype = typ
    if wrap is None:
        locals()[lib] = _dum
        __all__.append(lib)
    else:
        _calling[wrap] = "_"+lib
        locals()["_"+lib] = _dum
        __all__.append(wrap)


def checksum(message):
    return globals()[_calling["checksum"]](str(message), len(message))

def checksum_chained(crc, message):
    return globals()[_calling["checksum_chained"]](crc, str(message), len(message))    


# export LD_LIBRARY_PATH=.

