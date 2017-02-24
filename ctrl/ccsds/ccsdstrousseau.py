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


from ..utils import core
from ..utils import bincore
from . import ccsdsexception
from .ccsdskey import CCSDSKey


__all__ = ['CCSDSTrousseau']


class CCSDSTrousseau(object):
    def __init__(self, keylist, octets):
        """
        A collection of CCSDS keys

        Args:
        * keylist (list of dict): the list of input parameter to
            generate the list of CCSDSKey
        """
        self.keys = []
        self.size = 0
        pos = 0
        for item in keylist:
            if isinstance(item, CCSDSKey):
                new_key = item
            else:
                new_key = CCSDSKey(**item)
            if new_key.relative_only:
                pos += new_key.len
            else:
                pos = new_key.start + new_key.len
            if pos > self.size:
                self.size = pos
            self.keys.append(new_key)
        if not octets:
            # size is always in octets
            self.size //= 8

    def get_keys(self):
        """
        Returns a list of all CCSDS key names
        """
        return [item.name for item in self.keys]

    def pack(self, allvalues, retdbvalues):
        """
        Does the packing loop for the list of CCSDS keys
        Returns the bytes chain and the values encoded

        Args:
        * allvalues (dict): the values to pack
        * retdbvalues (bool): if ``True``, returns the encoded values
          in a format directly compatible with the database
        """
        values = dict(allvalues)
        retvals = {}
        bits = '0' * (self.size * 8)
        pos = 0
        for item in self.keys:
            if item.name not in values.keys() and item.dic_force is None:
                # got no values for this key, wtf
                raise ccsdsexception.PacketValueMissing(item.name)
            thevalue = values.pop(item.name, '')
            retvals[item.name] = thevalue
            if item.relative_only:
                bits = core.setstr( bits,
                                    item.cut_offset(pos),
                                    item.pack(thevalue))
                pos += item.len
            else:
                bits = core.setstr( bits,
                                    item.cut,
                                    item.pack(thevalue))
                pos = item.start + item.len
            # filling in the forced values not given as input
            if item.dic_force is not None:
                retvals[item.name] = item.dic_force
            # these are special cases that we want to fill manually because the
            # forced values are not numbers but dictionary keys that still
            # gotta be valid values for the database
            if retdbvalues and item.non_db_dic:
                retvals[item.name] = bincore.bin2int(item.pack(thevalue))

        return bincore.bin2hex(bits, pad=self.size), retvals

    def unpack(self, data):
        """
        Unpacks the data according to the list of keys

        Args:
        * data (byts): the data to unpack, given as chain of bytes
        """
        res = {}
        if not self.octets:
            data = bincore.hex2bin(data[:self.size], pad=self.size*8)
        else:
            data = data[:self.size]
        for item in self.keys:
            res[item.name] = item.unpack(data)
        return res

    def disp(self, *args, **kwargs):
        return ''

    