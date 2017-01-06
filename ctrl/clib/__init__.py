#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ..utils.core import glob, os
from subprocess import Popen as subprocessPopen
from subprocess import PIPE as subprocessPIPE
from subprocess import STDOUT as subprocessSTDOUT
from ctypes import cdll


# each *.c file must contain 1 and only 1 function that python
# should be aware of. This file should be of format
# <function_name>.c together with the <function_name>.h file.
from ctypes import c_uint
libs_register = [("crc", c_uint, "checksum")]


__all__ = []

"""
ROOTC = os.path.dirname(os.path.abspath(__file__))


for item in libs_register:
    if len(item) == 2:
        lib, typ, wrap = item + (item[0],)
        wrap = lib
    else:
        lib, typ, wrap = item
    # compilation if needed
    if len(glob.glob("{}/{}.so".format(ROOTC, lib))) == 0:
        cmd = "gcc -o {}/{}.so -shared -fPIC {}/{}.c".format(   ROOTC, lib,
                                                                ROOTC, lib)
        dum = subprocessPopen(  cmd, shell=True,
                                stderr=subprocessSTDOUT,
                                stdout=subprocessPIPE)
        print dum.stdout.readlines()
    # load in memory
    _dum = getattr(cdll.LoadLibrary("{}/{}.so".format(ROOTC, lib)), "crc")
    _dum.restype = typ
    locals()[wrap] = _dum
    __all__.append(wrap)


def checksum(message):
    return crc(str(message), len(message))


# export LD_LIBRARY_PATH=.
"""