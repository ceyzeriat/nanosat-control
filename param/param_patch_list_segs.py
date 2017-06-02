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


from byt import Byt
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


# there should be only one key here
KEYS = [dict(name='seg_id', start=0, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="Segment ID currently received by the satellite",
                disp='seg', octets=True)]


class PatchListSegCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the patch list segs packets

        Args:
          * data (byts): the chain of octets to unpack
        """
        theOnlyKey = self.keys[0]
        nlines = len(data) // self.size
        nums = []
        for idx in range(nlines):
            chunk = data[idx*self.size:(idx+1)*self.size]
            nums.append({theOnlyKey.name: theOnlyKey.unpack(chunk)})
        # returns a list of the pk_id
        return nums

    def disp(self, data):
        """
        Display the trousseau values
        Overriding mother's method

        Args:
          * data (list of dict): a list of dictionaries containing the
            values to display
        """
        res = [super(PatchListSegCCSDSTrousseau, self).disp(line)\
                    for line in data]
        return "\n".join(res)

    def pack(self, allvalues, retdbvalues, **kwargs):
        pass


TROUSSEAU = PatchListSegCCSDSTrousseau(KEYS, octets=True, listof=True)
