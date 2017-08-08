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


from ctypes import cdll, c_char_p, c_uint, create_string_buffer
from byt import Byt
import os
from nanoparam import param_all_processed as param_all


from ..param_sys import HMACLIBLINUX


__all__ = ['hmac']


_hmacfct = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),
                                         HMACLIBLINUX)).hmacSha256
_hmacfct.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]


# on linux compile it with:
# gcc -shared -o hmaclib.so -fPIC L0AppHmac.c L0AppSha256.c


def hmac(txt):
    """
    Calculates the HMAC-SHA256 of the ``txt`` given as input
    """
    txt = Byt(txt)
    digest = create_string_buffer(param_all.KEYLENGTH)
    if param_all.VITELACLE is not None:
        _hmacfct(param_all.VITELACLE, txt, len(txt), digest)
    else:
        print('No key found, using NULL')
        _hmacfct(Byt("\x00"*param_all.KEYLENGTH), txt, len(txt), digest)
    return Byt(digest.raw)

