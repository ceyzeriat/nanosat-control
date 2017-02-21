#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 202-2017  Guillaume Schworer
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


from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.utils import core


DATASCIENCEHF = [
                CCSDSKey(name='step', start=0, l=1, fctunpack=core.bin2int),
                CCSDSKey(name='counts', start=8, l=2, fctunpack=core.bin2int),
                CCSDSKey(name='x_com', start=24, l=2, fctunpack=core.bin2int),
                CCSDSKey(name='y_com', start=40, l=2, fctunpack=core.bin2int),
                CCSDSKey(name='x_pos', start=56, l=2, fctunpack=core.bin2int),
                CCSDSKey(name='y_pos', start=72, l=2, fctunpack=core.bin2int)
                ]

DATASCIENCEHFSIZE = sum([item.len for item in DATASCIENCEHF])


def unpack(data):
    """
    Unpacks the data contained in the Science HF packets

    Args:
    * data: the chain of octets to unpack
    """
    nlines = len(data) // DATASCIENCEHFSIZE
    lines = [{}] * nlines
    for idx in range(nlines):
        thedata = data[idx*DATASCIENCEHFSIZE:(idx+1)*DATASCIENCEHFSIZE]
        line = {}
        for key in DATASCIENCEHF:
            line[key.name] = key.unpack(thedata)
        lines[idx] = line
    return lines
