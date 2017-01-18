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


from . import cmdexception
from ..utils import core


__all__ = ['PFormat']


AUTHTYPS = ['uint', 'int', 'str', 'float']


class PFormat(object):
    def __init__(self, typ, bits=None):
        """
        Defines a parameter format for the type checking of input parameters

        Args:
        * typ (str): 'uint', 'int', 'str', 'float'
        * bits (int): the bit-length of the format. not applicable for ``str``

        Alternatively, you can pass a string defining a format, e.g. ``int8``,
        ``float32``, ``str``, ``unit16``.
        """
        rep = self._parse(typ)
        if rep is not None:
            typ, bits = rep
        if typ not in AUTHTYPS:
            raise cmdexception.UnknownFormat(typ)
        self._typ = str(typ)
        if self.typ != 'str':
            if bits is None:
                raise cmdexception.MissingFormatInput('bits', self.typ)
            elif not isinstance(bits, int) or bits not in [8, 16, 32, 64]:
                raise cmdexception.WrongFormatBitLength(self.typ, bits)
            self._bits = int(bits)
            self._halfmaxint = 2**(self.bits-1)
            self._maxint = self._halfmaxint * 2
        else:
            self._bits = 0
        self._typdisp = "<{}{}>".format(self.typ, ""\
                                        if self.typ  == 'str'\
                                        else "({})".format(self.bits))

    def __str__(self):
        return self._typdisp

    __repr__ = __str__

    def _parse(self, txt):
        letters = range(97, 123)
        numbers = range(48, 58)
        typ = "".join([letter if (ord(letter) in letters) else ""
                       for letter in str(txt)])
        if not typ in AUTHTYPS:
            return None
        number = "".join([letter if (ord(letter) in numbers) else ""
                          for letter in str(txt)])
        number = 0 if number == "" else int(number)
        if number <= 0 and typ != "str":
            return None
        return typ, number

    def is_valid(self, value):
        """
        Checks the type validity of ``value``.
        Returns ``True`` if it is compliant, otherwise ``False``

        Args:
        * value: must be a single value to be checked
        """
        if hasattr(value, "__iter__"):
            return False
        if self.typ == 'str':
            if not isinstance(value, str):
                return False
            if len(value) > 1:
                return False
        elif self.typ == 'uint':
            if not isinstance(value, int):
                return False
            if not 0 <= value < self._maxint:
                return False
        elif self.typ == 'int':
            if not isinstance(value, int):
                return False
            if not -self._halfmaxint <= value < self._halfmaxint:
                return False
        elif self.typ == 'float':
            if not isinstance(value, (float, core.np.floating)):
                return False
        else:
            raise cmdexception.UnknownFormat(self.typ)
        return True

    def _tohex(self, value):
        if self.typ == 'str':
            return value
        elif self.typ == 'uint':
            return core.padit(core.int2hex(value), self.bits // 8, '\x00')
        elif self.typ == 'int':
            raise cmdexception.NotImplemented()
        elif self.typ == 'float':
            raise cmdexception.NotImplemented()
        else:
            raise cmdexception.UnknownFormat(self.typ)

    @property
    def typ(self):
        return self._typ

    @typ.setter
    def typ(self, value):
        raise cmdexception.ReadOnly('typ')

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        raise cmdexception.ReadOnly('bits')
