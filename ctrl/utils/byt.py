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


from . import core


__all__ = ['Byt']


if core.PYTHON3:
    class Byt(bytes):
        def __new__(cls, value):
            if isinstance(value, str):
                # It's a unicode string:
                value = value.encode('ISO-8859-1')
            elif isinstance(value, int):
                value = chr(value).encode('ISO-8859-1')
            return super(Byt, cls).__new__(cls, value)

        def __getitem__(self, pos):
            if isinstance(pos, int):
                return Byt(super(Byt, self).__getitem__(slice(pos, pos+1)))
            else:
                return Byt(super(Byt, self).__getitem__(pos))

        def __str__(self):
            return self.decode('ISO-8859-1')

        def __repr__(self):
            return "{}('{}')".format(self.__class__.__name__, self.decode('ISO-8859-1'))

        def __iter__(self):
            for ch in super(Byt, self).__iter__():
                yield Byt(ch)

        def iterInts(self):
            """
            Returns the iterator of ints
            """
            for ch in super(Byt, self).__iter__():
                yield ch

        def ints(self):
            """
            Returns the list of ints
            """
            return list(self.iterInts())
else:
    class Byt(str):
        def __new__(cls, value):
            if isinstance(value[0], int):
                # It's a list of integers
                value = ''.join([chr(x) for x in value])
            return super(Byt, cls).__new__(cls, value)

        def itemint(self, index):
            return ord(self[index])

        def iterint(self):
            for x in self:
                yield ord(x)
