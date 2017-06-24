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
from ..utils import bincore
from ..utils import core
from ..ccsds import param_ccsds
from .commandpatch import CommandPatch

# function set_datetime of PLD, aim is to allow the input of a
# datetime or date-tuple instead of a dirty integer timestamp
class setDatetime(CommandPatch):
    def generate_data(self, *args, **kwargs):
        """
        This command has been patched.
        Convert a datetime object to an acceptable format, and sent it 
        to the payload for updating the Real Time Clock. 
        Very useful in combination with datetime.datetime.utcnow().
        @param datetime datetime: the datetime or tuple object to convert. 
        """      
        stamp = kwargs.get('datetime')
        if stamp is None:
            raise Exception("datetime is not an optional argument!")
        if not isinstance(stamp, (datetime, list, tuple)):
            raise TypeError
        if isinstance(stamp, (list, tuple)):
            stamp = datetime(*stamp)
        newkwargs = {}
        newkwargs['years'] = stamp.year - 1970
        newkwargs['months'] = stamp.month
        newkwargs['days'] = stamp.day
        newkwargs['hours'] = stamp.hour
        newkwargs['minutes'] = stamp.minute                
        newkwargs['seconds'] = stamp.second
        return super(setDatetime, self).generate_data(*args, **newkwargs)


# auto compute CRC
class genericCrcPatch(CommandPatch):
    _crcParamName = 'crc'

    def generate_data(self, *args, **kwargs):
        # force 0 sur le crc
        kwargs[self._crcParamName] = 0
        return super(genericCrcPatch, self).generate_data(*args, **kwargs)

    def _generate_packet(self, *args, **kwargs):
        # appel méthode mère
        packet, hd, hdx, inputs = super(genericCrcPatch, self)\
                                  ._generate_packet(*args, **kwargs)
        # on calc le CRC sur le header sec et les data
        bytesForCrc = packet[param_ccsds.HEADER_P_KEYS.size:-4]
        crc = core.payload_crc32(bytesForCrc)
        # on remplace le crc dans les inputs, parce que voilà
        inputs[self._crcParamName] = crc
        # on ré-encode les param de la command avec la méthode mère
        data, inputs = super(genericCrcPatch, self).generate_data(*args,
                                                            **inputs)
        # on remplace les data dans le packet encodé
        packet = packet[:param_ccsds.HEADER_P_KEYS.size+\
                        param_ccsds.HEADER_S_KEYS_TELECOMMAND.size] + data
        return packet, hd, hdx, inputs


# real time clock at bootloader level
class configureRTC(CommandPatch):
    _crcParamName = 'crc'

    def generate_data(self, *args, **kwargs):
        """
        This command has been patched.
        Convert a datetime object to an acceptable format, and sent it 
        to the payload for updating the Real Time Clock. 
        Very useful in combination with datetime.datetime.utcnow().
        @param datetime datetime: the datetime or tuple object to convert. 
        """
        # force 0 sur le crc
        stamp = kwargs.get('datetime')
        if stamp is None:
            raise Exception("datetime is not an optional argument!")
        if not isinstance(stamp, (datetime, list, tuple)):
            raise TypeError
        if isinstance(stamp, (list, tuple)):
            stamp = datetime(*stamp)
        newkwargs = {}
        newkwargs['years'] = stamp.year - 1970
        newkwargs['months'] = stamp.month
        newkwargs['days'] = stamp.day
        newkwargs['hours'] = stamp.hour
        newkwargs['minutes'] = stamp.minute                
        newkwargs['seconds'] = stamp.second
        kwargs[self._crcParamName] = 0
        return super(configureRTC, self).generate_data(*args, **newkwargs)
    
    def _generate_packet(self, *args, **kwargs):
        # appel méthode mère
        packet, hd, hdx, inputs = super(genericCrcPatch, self)\
                                  ._generate_packet(*args, **kwargs)
        # on calc le CRC sur le header sec et les data
        bytesForCrc = packet[param_ccsds.HEADER_P_KEYS.size:-4]
        crc = core.payload_crc32(bytesForCrc)
        # on remplace le crc dans les inputs, parce que voilà
        inputs[self._crcParamName] = crc
        # on ré-encode les param de la command avec la méthode mère
        data, inputs = super(genericCrcPatch, self).generate_data(*args,
                                                            **inputs)
        # on remplace les data dans le packet encodé
        packet = packet[:param_ccsds.HEADER_P_KEYS.size+\
                        param_ccsds.HEADER_S_KEYS_TELECOMMAND.size] + data
        return packet, hd, hdx, inputs    

