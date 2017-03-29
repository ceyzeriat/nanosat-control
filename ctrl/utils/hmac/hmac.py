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

from .. import core


__all__ = ['hmac']


_hmacfct = cdll.LoadLibrary(core.rel_dir('ctrl', 'utils', 'hmac', '_hmac.so'))\
                .hmacSha256
_hmacfct.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]


# compile it with:
# gcc -shared -o _hmac.so -fPIC L0AppHmac.c L0AppSha256.c


def hmac(txt):
    """
    Calculates the HMAC-SHA256 of the ``txt`` given as output
    """
    txt = Byt(txt)
    digest = create_string_buffer(core.KEYLENGTH)
    if core.VITELACLE is not None:
        _hmacfct(core.VITELACLE, txt, len(txt), digest)
    else:
        print('No key found, using NULL')
        _hmacfct(Byt("\x00"*core.KEYLENGTH), txt, len(txt), digest)
    return Byt(digest.raw)

