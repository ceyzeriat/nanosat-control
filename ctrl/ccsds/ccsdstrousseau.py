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


import math

from ..utils import core
from ..utils import bincore
from . import ccsdsexception
from .ccsdskey import CCSDSKey


__all__ = ['CCSDSTrousseau']


class CCSDSTrousseau(object):
    def __init__(self, keylist, octets, listof=False):
        """
        A collection of CCSDS keys

        Args:
          * keylist (list of dict): the list of input parameter to
            generate the list of CCSDSKey
          * octets (bool): whether the packet should be treated as binary
            or hexadecimal
          * listof (bool): if the trousseau corresponds to a data-structure
            repeated n-times in the packet
        """
        self.keys = []
        self.size = 0
        self.octets = bool(octets)
        self.listof = bool(listof)
        if self.listof and not self.octets:
            raise ccsdsexception.InvalidListOfBits()
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
        if not self.octets:
            # size is always in octets
            self.size = int(math.ceil(self.size / 8.))
        self._make_fmt()

    def _make_fmt(self, splt=", "):
        """
        Generates the single-line formatting for later display

        Args:
          * splt: the split char(s) between each keys
        """
        self.fmt = splt.join(["%s:{%s}" % (key.disp, key.name)\
                                for key in self.keys])

    def pack(self, allvalues, retdbvalues, **kwargs):
        """
        Does the packing loop for the list of CCSDS keys
        Returns the bytes chain and the values encoded

        Args:
          * allvalues (dict): the values to pack
          * retdbvalues (bool): if ``True``, returns the encoded values
            in a format directly compatible with the database

        Kwargs:
          * passed on to the pack method of each key
        """
        values = dict(allvalues)
        retvals = {}
        if not self.octets:
            bits = '0' * (self.size * 8)
        else:
            bits = '\x00' * self.size
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
                                    item.pack(thevalue, **kwargs))
                pos += item.len
            else:
                bits = core.setstr( bits,
                                    item.cut,
                                    item.pack(thevalue, **kwargs))
                pos = item.start + item.len
            # filling in the forced values not given as input
            if item.dic_force is not None:
                retvals[item.name] = item.dic_force
            # these are special cases that we want to fill manually because the
            # forced values are not numbers but dictionary keys that still
            # gotta be valid values for the database
            if retdbvalues and item.non_db_dic:
                retvals[item.name] = bincore.bin2int(item.pack(thevalue))
        if not self.octets:
            return bincore.bin2hex(bits, pad=self.size), retvals
        else:
            return bits, retvals

    def unpack(self, data, **kwargs):
        """
        Unpacks the data according to the list of keys

        Args:
          * data (byts): the data to unpack, given as chain of bytes

        Kwargs are ignored
        """
        if not self.octets:
            if not self.listof:
                data = bincore.hex2bin(data[:self.size])
            else:
                data = bincore.hex2bin(data)
        else:
            if not self.listof:
                data = data[:self.size]
            else:
                pass
        if not self.listof:
            return self._unpack(data)
        else:
            nlines = len(data) // self.size
            res = []
            for idx in range(nlines):
                chunk = data[idx*self.size:(idx+1)*self.size]
                res.append(self._unpack(chunk))
            # returns a list of the pk_id
            return res

    def _unpack(self, data):
        """
        Basic unpack routine
        """
        res = {}
        for item in self.keys:
            res[item.name] = item.unpack(data)
        return res


    def disp(self, vals, charwrap=60, **kwargs):
        """
        Displays the trousseau values

        Args:
          * vals (dict or list of dict): a dictionary containing the
            values to display
          * charwrap: at how many chars should there be a line wrap,
            set to -1 to disable

        Kwargs are ignored
        """
        if not self.listof:
            return self._disp(vals, charwrap)
        else:
            res = [self._disp(line) for line in list(vals)]
        return "\n* ".join(res)

    def _disp(self, vals, charwrap):
        """
        Basic disp routine
        """
        copyvals = dict(vals)
        charwrap = int(charwrap)
        if charwrap > 0:
            newline = "\n    "
            for k, v in copyvals.items():
                v = str(v)
                if len(v) > charwrap:
                    copyvals[k] = newline +\
                                   newline.join([v[i*charwrap:(i+1)*charwrap]\
                                        for i in range(len(v) // charwrap +1)])
        return self.fmt.format(**copyvals)
