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


MAXLENGTHMESSAGE = 235  # octets


def hex2txt(v, **kwargs):
    """
    verbose = "binary -> message"
    """
    return ''.join([chr(i) for i in v.ints() if i >= 32 and i <= 126])


def txt2hex(txt, pad, **kwargs):
    """
    verbose = "message -> binary"
    """
    return Byt([i for i in Byt(txt).ints() if i >= 32 and i <= 126])


KEYS = [dict(name='error', start=72, l=16,
                fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin,
                verbose="error code for the error",
                disp='error', pad=False)]


class EventReportCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the payload report

        Args:
        * data (byts): the chain of octets to unpack
        """
        res = dict([])
        dt = bincore.hex2bin(data[:self.size])
        for item in self.keys:
            if item.name == 'message':
                res[item.name] = str(data[:MAXLENGTHMESSAGE])
            else:
                res[item.name] = item.unpack(dt)
        return res

    def pack(self, **kwargs):
        pass

    def disp(self, vals):
        """
        Display the trousseau values

        Args:
          * vals (dict): a dictionary containing the values to display
        """
        return "{}\nhex: {}".format(super(EventReportCCSDSTrousseau, self).disp(vals),
                                    vals[self.keys[0].name].hex())


TROUSSEAU = EventReportCCSDSTrousseau(KEYS, octets=True)
