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


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


KEYS = [dict(name='step', start=0, l=1, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="step", disp="step"),
        dict(name='counts', start=1, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="counts", disp="cts"),
        dict(name='x_com', start=3, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="x_com", disp="xc"),
        dict(name='y_com', start=5, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="y_com", disp="yc"),
        dict(name='x_pos', start=7, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="x_pos", disp="xp"),
        dict(name='y_pos', start=9, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="y_pos", disp="yp")
        ]


class HFScienceCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the Science HF packets

        Args:
        * data (byts): the chain of octets to unpack
        """
        nlines = len(data) // self.size
        lines = [{}] * nlines
        for idx in range(nlines):
            lines[idx] = super(HFScienceCCSDSTrousseau, self).unpack(
                                        data[idx*self.size:(idx+1)*self.size])
        return lines

    def disp(self, data):
        res = [super(HFScienceCCSDSTrousseau, self).disp(**line)\
                    for line in data['unpacked']]
        return "\n".join(res)


TROUSSEAU = HFScienceCCSDSTrousseau(KEYS, octets=True)
