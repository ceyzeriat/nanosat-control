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


from . import ccsdsexception
from ..utils import bincore
from ..utils import core


__all__ = ['CCSDSKey']


class CCSDSKey(object):
    def __init__(self, name, dic=None, start=None, l=1, fctunpack=None,
                 fctpack=None, dic_force=None, non_db_dic=False, verbose="",
                 disp=None, octets=False, pad=True):
        """
        CCSDS keys to perform easy extraction from a sequence of bits
        (or octets).
        
        Args:
          * name (str): the name of the dictionary, for referencing
          * dic (dict): dictionary of possible values
          * start (int): start-position in bit from the beginning of the
            primary header, or whatever reference you decided
          * l (int): length of the strip of bits (or octets)
          * fctunpack (callable): function to apply to the raw data to
            get the value. Shall remain ``None`` if ``dic`` is provided
          * fctpack (callable): reverse function of ``fctunpack``
            Shall remain ``None`` if ``dic`` is provided
          * dic_force (bool): whether to force a certain dictionary value
            when (un)packing, no matter the user input
          * non_db_dic (bool): ``True`` if the dictionary keys are non-
            compliant with the corresponding database column. This will
            make sure that the unpacked values are integers instead of
            the non-compliant dictionary keys
          * verbose (string): Human-readable meaning of this key
          * disp (string): short alias for human-reading display
          * octets (bool): if the values are (un)packed as octets or binary
          * pad (bool): whether to pad the raw data up to the length ``l``
          * padchar (str or Byt): the character to be used for padding.
            It shall be a '0' or '1' if ``octets`` is ``True``, or a
            Byt if it is ``False``
        """
        self.name = str(name)
        self.disp = self.name[:3] if disp is None else str(disp)
        self.octets = bool(octets)
        self.pad = bool(pad)
        self._fctunpack = fctunpack if callable(fctunpack) else None
        self._fctpack = fctpack if callable(fctpack) else None
        self.isdic = (dic is not None)
        if self.isdic:
            self.dic = {}
            for k, v in dict(dic).items():
                if core.isStr(k):
                    k = str(k).lower()
                self.dic[k] = v
            if self._fctunpack is not None or self._fctpack is not None:
                raise ccsdsexception.BadDefinition(name=self.name)
        else:
            self.dic = None
            if self._fctunpack is None and self._fctpack is None:
                raise ccsdsexception.BadDefinition(name=self.name)
        self.can_unpack = (self._fctunpack is not None or self.isdic)
        self.can_pack = (self._fctpack is not None or self.isdic)
        self.relative_only = False
        self.len = int(l)
        # just the length is provided
        if start is None:
            self.start = 0
            self.end = self.len
            self.relative_only = True
        elif start is not None:
            self.start = int(start)
            self.end = self.start + self.len
        self.cut = slice(self.start, self.end)
        self.cut_rel = slice(0, self.len)
        self.dic_force = dic_force
        self.non_db_dic = bool(non_db_dic)

    def __str__(self):
        return "{}: <{}>".format(self.name, self.cut)

    __repr__ = __str__

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

    def unpack(self, packet, rel=False, raw=False, offset=None, **kwargs):
        """
        Grabs the slice of relevant bits in the packet and returns
        the corresponding key or applies the unpack function

        Args:
          * packet (str): the packet, either chain of '0' and '1' or hex
            depending how ``start`` and ``l`` were defined
          * rel (bool): if ``False`` follows ``start``, if ``True``
            grabs the bits from the position 0 (or ``offset``) of the
            packet provided. Ignored if ``offset`` is not ``None``
          * raw (bool): if ``True``, returns the raw bit sequence
          * offset (int) [optional]: offset to apply to the slice

        Kwargs:
          * Passed on to ``fctunpack`` if applicable
        """
        if not self.can_unpack and not raw:
            raise ccsdsexception.NoUnpack(name=self.name)
        if not rel and self.relative_only and offset is None:
            raise ccsdsexception.NoAbsGrab(name=self.name)
        if offset is not None:
            chunk = packet[self.cut_offset(offset=int(offset))]
        else:
            chunk = packet[self.cut_rel if rel else self.cut]
        if len(chunk) != self.len and self.pad:
            raise ccsdsexception.GrabFail(name=self.name, l=self.len)
        if raw:
            return chunk
        elif self._fctunpack is None:
            return self._dic_rev(bincore.reverse_if_little_endian(chunk))
        else:
            return self._fctunpack(chunk, **kwargs)

    def pack(self, value, raw=False, pad=None, **kwargs):
        """
        Give a value, returns the sequence of bits from dic or
        generated by fctpack, and finally pads it if necessary

        Args:
          * value: the value to convert to bits
          * raw (bool): if ``True``, a simple int2bin transform is applied
            to the input value, with a padding to the key length,
            unless ``pad`` is provided
          * pad (int or None) [optional]: the padding length to
            apply, or default ``None`` pads to key length .

        Kwargs:
          * Passed on to and ``fctpack`` if applicable
        """
        if self.isdic and self.dic_force is not None:
            value = self.dic_force
        if not self.can_pack and not raw:
            raise ccsdsexception.NoPack(name=self.name)
        if pad is not None:
            # pad integer amount
            pad = int(pad)
        else:
            pad = self.len if self.pad else None
        if raw:
            if not self.octets:
                return bincore.int2bin(value, pad=pad)
            else:
                return bincore.int2hex(value, pad=pad)
        elif self._fctpack is None:
            return bincore.reverse_if_little_endian(self[value])
        else:
            return self._fctpack(value, pad=pad, **kwargs)

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
