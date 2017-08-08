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


from datetime import datetime
from nanoutils import bincore
from nanoutils import fcts
from nanoparam import param_ccsds


from .commandpatch import CommandPatch


# allow input of datetime or date-tuple instead of a dirty integer timestamp
class GenericDatetime(CommandPatch):
    _datetimeName = "datetime"
    
    def generate_data(self, *args, **kwargs):
        """
        This command has been patched.
        Convert a datetime object to an acceptable format, and sent it 
        to the payload for updating the Real Time Clock. 
        Very useful in combination with datetime.datetime.utcnow().
        @param datetime datetime: the datetime or tuple object to convert. 
        """      
        stamp = kwargs.pop(self._datetimeName, None)
        if stamp is None:
            raise Exception("'{}' is not an optional argument!"\
                                                .format(self._datetimeName))
        if not isinstance(stamp, (datetime, list, tuple)):
            raise TypeError("'{}' should be datetime or date-tuple"\
                                                .format(self._datetimeName))
        if isinstance(stamp, (list, tuple)):
            stamp = datetime(*stamp)
        kwargs['years'] = stamp.year - 1970
        kwargs['months'] = stamp.month
        kwargs['days'] = stamp.day
        kwargs['hours'] = stamp.hour
        kwargs['minutes'] = stamp.minute                
        kwargs['seconds'] = stamp.second
        return super(GenericDatetime, self).generate_data(*args, **kwargs)


# auto compute CRC
class genericCrcPatch(CommandPatch):
    _crcParamName = 'crc'

    def generate_data(self, *args, **kwargs):
        # force 0 on crc
        kwargs[self._crcParamName] = 0
        return super(genericCrcPatch, self).generate_data(*args, **kwargs)

    def _generate_packet(self, *args, **kwargs):
        # record  whether to sign or not if given as input
        signit = kwargs.get('signit')
        # force no signature as first step
        kwargs['signit'] = False
        # call mother's method
        packet, hd, hdx, inputs = super(genericCrcPatch, self)\
                                  ._generate_packet(*args, **kwargs)
        # calculation of CRC on sec header and data
        # 4 is the length of CRC
        bytesForCrc = packet[param_ccsds.HEADER_P_KEYS.size:-4]
        crc = fcts.payload_crc32(bytesForCrc)
        # replacement of CRC in inputs
        inputs[self._crcParamName] = crc
        # force CRC at the end of packet
        packet[-4:] = crc
        if signit is None:  # signit not given, follow default
            kwargs.pop('signit', None)
            packet, sig = self._add_siggy(packet, **kwargs)
        elif signit is True:  # signit was passed and True
            kwargs['signit'] = True
            packet, sig = self._add_siggy(packet, **kwargs)
        return packet, hd, hdx, inputs


# real time clock at bootloader level, just bind auto-CRC and simple-datetime
class configureRTC(GenericDatetime, genericCrcPatch):
    pass

# function set_datetime of PLD
class setDatetime(GenericDatetime):
    pass
