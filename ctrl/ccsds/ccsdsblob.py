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
from param import param_apid
from param import param_category_common as pcc
from . import param_ccsds
from ..utils import bincore
from . import ccsdsexception as exc
from .ccsdspacker import CCSDSPacker


__all__ = ['CCSDSBlob']


class CCSDSBlob(object):
    def __init__(self, blob, mode='tm'):
        """
        Analyzes a blob of bits to find the first valid packet
        These 4 packet-related parameters are used as assumptions
        to parse and validate the packet

        Args:
        * blob (str): the bytes string
        * mode: 'tm' or 'tc'
        """
        self.blob = blob
        pk = CCSDSPacker(mode=mode)
        vals = {param_ccsds.PID.name: '',
                param_ccsds.PACKETCATEGORY.name:\
                    pcc.CATEGORYREGISTRATIONCOMMON.keys()[0]}
                    # just pick first common one
        # building of possible packet start flags
        self.auth_bits = []
        octcut = (param_ccsds.AUTHPACKETLENGTH // 8 + 1)
        for item in param_apid.PIDREGISTRATION.keys():
            vals[param_ccsds.PID.name] = item
            possible_head = bincore.hex2bin(
                                pk.pack_primHeader(values=vals, datalen=0,
                                        retvalues=False, retdbvalues=False,
                                        withPacketID=False)[:2],
                                pad=octcut)[:param_ccsds.AUTHPACKETLENGTH]
            self.auth_bits.append(possible_head)

    def find(self, start=0):
        """
        Finds the possible start of a packet in the blob.
        Returns the index of the start or None if not found

        Args:
        * start (int): from where the search should start
        """
        if len(self.blob[start:start+2]) == 0:
            return 0
        for i in range(len(self.blob[start:])):
            if bincore.hex2bin(self.blob[start+i:start+i+2])\
                    [:param_ccsds.AUTHPACKETLENGTH]\
                                    in self.auth_bits:
                return i
        else:
            return None

    def grab_data_length(self, start):
        """
        Returns the data-lengh as int, contained in the header of the
        packet

        Args:
        * start (int): the first bit of the packet in the blob
        """
        dum = bincore.hex2bin(self.blob[start:
                                        start+param_ccsds.HEADER_P_KEYS.size])
        return param_ccsds.DATALENGTH.unpack(dum) - param_ccsds.LENGTHMODIFIER

    def find_first_packet(self, start=0):
        """
        Finds the first valid packet, assuming the packet
        parameters provided at initialization.
        Returns a slice, or ``None`` if no valid packet found

        Args:
        * start (int): from where the search should start
        """
        idx = self.find(start=start)
        if idx is None:
            return None
        start += idx
        try:
            length = self.grab_data_length(start=start)
        except:
            # issue, maybe the packet is cut before the data length bit
            return None
        # bullshit length, just restart search further
        if length < param_ccsds.HEADER_P_KEYS.size:
            return self.find_first_packet(start=start+1)
        # bang on, found a new start where you expected it
        elif self.find(start=start+param_ccsds.HEADER_P_KEYS.size+length) == 0:
            return slice(start, start + param_ccsds.HEADER_P_KEYS.size + length)
        # try again
        else:
            return self.find_first_packet(start=start+1)

    def grab_first_packet(self, start=0):
        """
        """
        slc = self.find_first_packet(start=start)
        if slc is None:
            return None
        else:
            return self.blob[slc]
