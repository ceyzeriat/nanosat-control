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
KEYS = [dict(name='packet_id', start=0, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex,
                verbose="Segment ID currently received by the satellite",
                disp='pkid', octets=True)]


class PatchListSegCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the patch lsit segs packets

        Args:
        * data (byts): the chain of octets to unpack
        """
        theOnlyKey = self.keys[0]
        nums = []
        for idx in range(len(data) // self.size):
            chunk = data[idx*self.size:(idx+1)*self.size]
            nums.append(theOnlyKey.unpack(chunk))
        # returns a list of the pk_id
        return {theOnlyKey.name: nums}

    def disp(self, vals):
        """
        Display the trousseau values

        Args:
          * vals (dict): a dictionary containing the values to display
        """
        copyvals = dict(vals)
        # transform the list of the pk_id into a string
        copyvals[self.keys[0].name] = repr(vals[self.keys[0].name])
        return super(DumpAnswerDataCCSDSTrousseau, self).disp(copyvals)

    def pack(self, allvalues, retdbvalues, **kwargs):
        pass


TROUSSEAU = PatchListSegCCSDSTrousseau(KEYS, octets=True)
