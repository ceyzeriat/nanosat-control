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


__all__ = ['KEYS', 'KEYSSIZE', 'unpack', 'disp']


KEYS = [CCSDSKey(name='step', start=0, l=1, fctunpack=core.hex2int),
        CCSDSKey(name='counts', start=1, l=2, fctunpack=core.hex2int),
        CCSDSKey(name='x_com', start=3, l=2, fctunpack=core.hex2int),
        CCSDSKey(name='y_com', start=5, l=2, fctunpack=core.hex2int),
        CCSDSKey(name='x_pos', start=7, l=2, fctunpack=core.hex2int),
        CCSDSKey(name='y_pos', start=9, l=2, fctunpack=core.hex2int)
        ]


KEYSSIZE = sum([item.len for item in KEYS])


def unpack(data):
    """
    Unpacks the data contained in the Science HF packets

    Args:
    * data: the chain of octets to unpack
    """
    nlines = len(data) // KEYSSIZE
    lines = [{}] * nlines
    for idx in range(nlines):
        thedata = data[idx*KEYSSIZE:(idx+1)*KEYSSIZE]
        line = {}
        for key in KEYS:
            line[key.name] = key.unpack(thedata)
        lines[idx] = line
    return lines


def disp(hdx, data):
    print("ACQ: {acq_mode}, IT: {integration_time}, M: {modulation}, "\
          "R: {radius}, NP: {n_points}".format(**hdx))
    for line in data['unpacked']:
        print("S: {step}, C: {counts}, Xc{x_com}, Yc{y_com}, Xp{x_pos}, "\
              "Yp{y_pos}".format(**line))
