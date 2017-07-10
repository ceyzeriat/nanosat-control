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

from . import ccsdsexception
from ..utils import bincore
from ..utils import core
from ..utils import b
from ..utils import O


__all__ = ['CCSDSKey']


TYP = { 'sint': 'intSign',
        'uint': 'int',
        'byt': 'hex',
        'hexa': 'str',
        'text': 'txt',
        'real': 'float',
        'double': 'double',
        'bool': 'bool'
      }


class CCSDSKey(object):
    def __init__(self, name, start, l, dic=None, typ=None,
                 disp=None, verbose="", fctunram=None,
                 dic_force=None, non_db_dic=False, hard_l=True, **kwargs):
        """
        CCSDS keys to perform value extraction from a sequence of bits
        (or octets if Trousseau is in octet).
        
        Args:
          * name (str): the name of the dictionary, for referencing
          * start (int): start-position in bits (or octets if Trousseau
            is in octet).
          * l (int): length of the strip in bits (or octets if Trousseau
            is in octet).
          * dic (dict): dictionary of possible values
          * typ (str): expected type of the unpacked key
          * disp (string): short alias for human-reading display
          * verbose (string): Human-readable meaning of this key
          * fctunram (callable): [optional] a function to convert the
            raw-unpacked value to a physical value. This function shall
            contain a docstring with the symbolic conversion using x as
            input parameter: e.g. "verbose = 3*x/16."
          * fctram (callable): [optional] a function to convert the
            physical value to a raw-integer raedy for packing. If ``None``,
            this reverse function will be automatically determined from
            fctunram
          * dic_force (bool): whether to force a certain dictionary value
            when (un)packing, no matter the user input
          * non_db_dic (bool): ``True`` if the dictionary keys are non-
            compliant with the corresponding database column. This will
            make sure that the unpacked values are integers instead of
            the non-compliant dictionary keys
          * hard_l (bool): if ``True``: pad the data up to the key length
            ``l``, else leave the data as it is and ``l`` represent the
            maximum length

        Kwargs are unused
        """
        self.name = str(name)
        self.verbose = str(verbose)
        self.disp = self.name[:3] if disp is None else str(disp)
        self.hard_l = bool(hard_l)
        self.unram = fctunram if callable(fctunram) else None
        self.ram = None
        e = re.search(r'verbose *= *([\S ]+)',
                      getattr(self.unram, 'func_doc', ''))
        if e is not None:
            try:
                self.ram = eval('lambda x: {}'.format(core.inverse_eqn(e)))
            except:
                pass
        self.isdic = (dic is not None)
        self.start = start//8*O + start%8*b
        self.len = l//8*O + l%8*b
        self.end = self.start + self.len
        self._hex_slice = slice(self.start//8, int(math.ceil(self.end/8.)))
        self.octets = (self.start%8 == 0 and self.end%8 ==0)
        if self.octets:
            self._bin_sub_slice = slice(self.start%8, self.start%8+self.len)
        self.typ = typ.lower()
        if self.typ not in TYP.keys():
            raise ccsdsexception.BadDefinition(name=self.name)
        if self.isdic:
            if typ is not None:
                raise ccsdsexception.BadDefinition(name=self.name)
            self.dic = {}
            self._fctunpack = None
            self._fctpack = None
            for k, v in dict(dic).items():
                if core.isStr(k):
                    k = str(k).lower()
                self.dic[k] = v
        else:
            if typ is None:
                raise ccsdsexception.BadDefinition(name=self.name)
            self.dic = None
            conv = 'hex' if self.octets else 'bin'
            self._fctunpack = getattr(bincore,
                                      '{}2{}'.format(conv, TYP[self.typ]))
            self._fctpack = getattr(bincore,
                                      '{}2{}'.format(TYP[self.typ], conv))
        self.dic_force = bool(dic_force)
        self.non_db_dic = bool(non_db_dic)

    def __repr__(self):
        return "{}: <{}-->{}>[{}]".format(
                    self.name,
                    self.start//8 if self.octets else int(self.start),
                    self.end//8 if self.octets else int(self.end),
                    'O' is self.octets else 'b')

    __str__ = __repr__

    def cut_offset(self, offset):
        """
        Returns the slice with an offset in position

        Args:
          * offset (int): the offset
        """
        offset = int(offset)
        if self.start + offset < 0:
            raise ccsdsexception.CantApplyOffset(name=self.name,
                                                    start=self.start,
                                                    offset=offset)
        else:
            return slice(self.start + offset, self.end + offset)
    
    def __getitem__(self, key):
        if not self.isdic:
            raise ccsdsexception.NoDic(name=self.name)
        if key in self.dic.keys():
            return self.dic[key]
        elif str(key).lower() in self.dic.keys():
            return self.dic[str(key).lower()]
        else:
            try:
                return self.dic[int(key)]
            except:
                raise ccsdsexception.NoSuchKey(name=self.name, key=key)

    def unpack(self, packet, raw=False, unram=False, **kwargs):
        """
        Grabs the slice of relevant bits in the packet and returns
        the corresponding key or applies the unpack function

        Args:_hex_slice
          * packet (byt): the packet as hex
          * raw (bool): whether to return raw values
          * unram (bool): whether to proceed with value-conversion

        Kwargs:
          * Passed on to ``fctunpack``
        """
        chunk = packet[self._hex_slice]
        if self.octets:
            if len(chunk) != self.len//8 and self.hard_l:
                raise ccsdsexception.GrabFail(name=self.name, l=self.len)
        else:
            chunk = bincore.hex2bin(chunk)[self._bin_sub_slice]
            if len(chunk) != self.len and self.hard_l:
                raise ccsdsexception.GrabFail(name=self.name, l=self.len)
        if raw:
            return chunk
        if self._fctunpack is None:
            res = self._dic_rev(bincore.reverse_if_little_endian(chunk))
        else:
            res = self._fctunpack(chunk, **kwargs)
        if unram and self.unram is not None:
            return self.unram(res, **kwargs)
        else:
            return res

    def pack(self, value, octets=None, **kwargs):
        """
        Give a value, returns the sequence of bits from dic or
        generated by fctpack

        Args:
          * value: the value to convert to hex or bits
          * octets (bool): whether to force return some octets
            or bits. Default is ``ccsdsKey.octets``.

        Kwargs:
          * Passed on to and ``fctpack`` if applicable
        """
        if self.isdic and self.dic_force is not None:
            value = self.dic_force
        if self._fctpack is None:
            res = bincore.reverse_if_little_endian(self[value])
        else:
            pad = self.len if self.hard_l else None
            res = self._fctpack(value, pad=pad, **kwargs)
        # we have octets but forcing to bin
        if self.octets and octets is False:
            return bincore.hex2bin(res, pad=True)
        return res

    def _dic_rev(self, value):
        """
        Performs the reverse search in the dictionary: given a
        value, it will return the corresponding key

        Args:
          * value: the value to search in ``dic``
        """
        found = False
        for k, v in self.dic.items():
            if v == value:
                found = True
            elif str(v) == str(value):
                found = True
            else:
                try:
                    if int(v) == int(value):
                        found = True
                except:
                    pass
            if found:
                return k
        else:
            raise ccsdsexception.NoSuchValue(name=self.name, value=value)
