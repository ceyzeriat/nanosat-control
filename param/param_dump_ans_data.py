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


MAXLENGTHDATA = 235  # octets

KEYS = [dict(   name='data',
                start=0,
                l=MAXLENGTHDATA,
                fctunpack=bincore.hex2hex,
                fctpack=bincore.hex2hex,
                verbose="Buffer of bytes containing the dumped data",
                disp='data',
                pad=False)]


class DumpAnswerDataCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the Dump answer data packets

        Args:
        * data (byts): the chain of octets to unpack
        """
        data = Byt(data[:MAXLENGTHDATA])
        return super(DumpAnswerDataCCSDSTrousseau, self).unpack(data)

    def disp(self, vals, **kwargs):
        """
        Display the trousseau values

        Args:
          * vals (dict): a dictionary containing the values to display
        """
        copyvals = dict(vals)
        copyvals[self.keys[0].name] = copyvals[self.keys[0].name].hex()
        return super(DumpAnswerDataCCSDSTrousseau, self).disp(copyvals, **kwargs)

    def pack(self, allvalues, retdbvalues, **kwargs):
        pass


TROUSSEAU = DumpAnswerDataCCSDSTrousseau(KEYS, octets=True)
