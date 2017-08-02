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
from ..utils import bincore
from . import ccsdsexception
from .ccsdskey import CCSDSKey
from param import param_all


__all__ = ['CCSDSTrousseau']


class CCSDSTrousseau(object):
    def __init__(self, keylist, listof=False):
        """
        A collection of CCSDS keys

        Args:
          * keylist (list of dict): the list of input parameter to
            generate the list of CCSDSKey
          * listof (bool): if the trousseau corresponds to a data-structure
            repeated n-times in the packet
        """
        self.keys = []
        self.size = 0
        self.listof = bool(listof)
        self.octets = True
        self.unram_any = False
        for item in keylist:
            if not isinstance(item, CCSDSKey):
                item = CCSDSKey(**item)
            self.octets = (self.octets and item.octets)
            self.size = max(self.size, item.end)
            self.unram_any = (self.unram_any or (item.unram is not None))
            self.keys.append(item)
        self.size = int(self.size/8)
        self._make_fmt()

    def _make_fmt(self, splt=", "):
        """
        Generates the single-line formatting for later display

        Args:
          * splt: the split char(s) between each keys
        """
        l = []
        for key in self.keys:
            txt = "%s:{%s}" % (key.disp, key.name)
            if key.unram is not None:
                txt += " ({%s}%s)" %\
                        (key.name+param_all.SUFIXCONVERSION,
                         ' '+key.unit if key.unit is not None else '')
            l.append(txt)
        self.fmt = splt.join(l)

    def pack(self, allvalues, **kwargs):
        """
        Does the packing loop for the list of CCSDS keys
        Returns the bytes chain and the values encoded

        Args:
          * allvalues (dict): the values to pack

        Kwargs:
          * passed on to the pack method of each key
        """
        values = dict(allvalues)
        retvals = {}
        if not self.octets:
            chunk = '0' * (self.size * 8)
            conv = 1
        else:
            chunk = Byt('\x00' * self.size)
            conv = 8
        for item in self.keys:
            if item.name not in values.keys() and item.dic_force is None:
                # got no values for this key, wtf
                raise ccsdsexception.PacketValueMissing(item.name)
            retvals[item.name] = values[item.name] if item.dic_force is None\
                                                            else item.dic_force
            v = item.pack(retvals[item.name], octets=self.octets, **kwargs)
            chunk = core.setstr(chunk,
                                slice(item.start//conv, item.end//conv),
                                v)
        if not self.octets:
            return bincore.bin2hex(chunk, pad=self.size), retvals
        else:
            return chunk, retvals

    def unpack(self, data, **kwargs):
        """
        Unpacks the data according to the list of keys

        Args:
          * data (byts): the data to unpack, given as chain of bytes

        Kwargs are passed to the CCSDSKey unpack method
        """
        if not self.listof:
            data = data[:self.size]
            return self._unpack(data)
        else:
            nlines = len(data) // self.size
            res = []
            for idx in range(nlines):
                chunk = data[idx*self.size:(idx+1)*self.size]
                res.append(self._unpack(chunk, **kwargs))
            # returns a list of the pk_id
            return res

    def _unpack(self, data, **kwargs):
        """
        Basic unpack routine
        """
        res = {}
        for item in self.keys:
            res[item.name] = item.unpack(data, **kwargs)
            # check if conversion available
            if item.unram is not None:
                # add to result dict
                res[item.name+param_all.SUFIXCONVERSION] =\
                                    item.unram(res[item.name], **kwargs)
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
            res = [self._disp(line, charwrap) for line in list(vals)]
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
