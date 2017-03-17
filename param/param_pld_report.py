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


__all__ = ['TROUSSEAU']


MAXLENGTHMESSAGE = 235


def hex2txt(v, **kwargs):
    """
    verbose = "binary -> message"
    """
    return ''.join([chr(i) for i in v.ints() if i >= 32 and i <= 126])


def txt2hex(txt, **kwargs):
    """
    verbose = "message -> binary"
    """
    return Byt([i for i in Byt(txt).ints() if i >= 32 and i <= 126])


KEYS = [dict(name='message', start=0, l=MAXLENGTHMESSAGE, fctunpack=hex2txt, fctpack=txt2hex,
                verbose="A report message (ascii string)",
                disp='text')]


class PLDRepCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the payload report

        Args:
        * data (byts): the chain of octets to unpack
        """
        return {self.keys[0].name: str(data[:MAXLENGTHMESSAGE])}


TROUSSEAU = PLDRepCCSDSTrousseau(KEYS, octets=True)
