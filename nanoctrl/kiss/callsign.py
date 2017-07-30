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
from ..utils import core
from . import utils
from . import kissexception


__all__ = ['Callsign']


class Callsign(object):
    def __init__(self, callsign):
        """
        Defines parts of a Callsign decoded from either ASCII or KISS

        Args:
        * callsign (str): the callsign
        """
        self.callsign = Byt()
        self.ssid = Byt('0')
        self.digi = False
        self.parse(callsign)

    def __repr__(self):
        return str(self.callsign)

    __str__ = __repr__

    def parse(self, callsign=None):
        """
        Parse and extract the components of a Callsign from ASCII or KISS

        Args:
        * callsign (str): the callsign to parse
        """
        if callsign is not None:
            # treat the callsign as a frame, maybe?
            try:
                self._extract_callsign_from_AX25_frame(callsign)
            except IndexError:
                pass
            # if not happy with existing callsign, try parsing it as callsign
            if not utils.valid_callsign(self.callsign):
                self.parse_callsign(callsign)
        # if still no valid callsign at this point
        if not utils.valid_callsign(self.callsign):
            raise kissexception.BadCallsignError(self.callsign)

    def encode_callsign(self):
        """
        Encodes Callsign (or Callsign-SSID) as KISS
        """
        encoded_ssid = ((int(self.ssid) << 1) | 0x60)
        callsign = Byt(self.callsign)

        if self.digi:
            encoded_ssid |= 0x80
        # Pad the callsign to 6 characters
        callsign = core.fillit(callsign, l=6, ch=Byt(' ')).ints()

        encoded_callsign = Byt(p << 1 for p in callsign)

        return encoded_callsign + Byt(encoded_ssid)

    def parse_callsign(self, callsign):
        """
        Parses and extracts a Callsign and SSID from an ASCII-Encoded APRS
        Callsign or Callsign-SSID.

        Args:
        * callsign (str): ASCII-Encoded APRS Callsign
        """
        res = Byt(callsign).split(Byt('-'), 1) + [Byt()]
        callsign, ssid = res[:2]
        if len(ssid) == 0:
            ssid = Byt('0')

        if callsign[-1] == Byt('*'):
            callsign = callsign[:-1]
            self.digi = True

        self.callsign = callsign.strip()
        self.ssid = ssid.strip()

    def _extract_callsign_from_AX25_frame(self, frame):
        """
        Extracts a Callsign and SSID from a KISS-Encoded APRS Frame.

        Args:
        * frame (bytes): KISS-Encoded APRS Frame as str of octs
        """
        frame = Byt(frame[:7]).ints()
        callsign = Byt(x >> 1 for x in frame[:6])
        self.callsign = callsign.strip()
        self.ssid = Byt(str((frame[6] >> 1) & 0x0f))
