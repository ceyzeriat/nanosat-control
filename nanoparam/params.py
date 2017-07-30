#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 2016-2017  Guillaume Schworer
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  For any information, bug report, idea, donation, hug, beer, please contact
#    guillaume.schworer@gmail.com
#
###############################################################################


import os
from .param_all import *


# can't have KISS without AX25
AX25ENCAPS = AX25ENCAPS or KISSENCAPS

MAXPACKETID = 2**14

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOME = os.path.expanduser("~")

def concat_dir(*args):
    """
    Concatenates the path in ``args`` into a string-path
    """
    return os.path.join(*args)

def home_dir(*args):
    """
    Concatenates the path in ``args`` into a string-path
    """
    return concat_dir(HOME, *args)

def rel_dir(*args):
    """
    Concatenates the path in ``args`` into a relative
    string-path from the package directory
    """
    return concat_dir(ROOT, *args)
