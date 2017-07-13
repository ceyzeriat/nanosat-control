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


__all__ = ['O', 'b']


class Unit(int): 
    def __new__(cls, v, m, name): 
        v = int(v)
        m = int(m)
        ans = super(Unit, cls).__new__(cls, v*m) 
        ans.v = v
        ans.m = m
        ans.name = str(name[:1])
        return ans

    def __repr__(self):
        return "{}*{}".format(self.v, self.name)

    __str__ = __repr__

    def __mul__(self, other):
        print "mul", other, type(other)
        return type(self)(int(other)*self.v, self.m, self.name)

    def __rmul__(self, other):
        print "rmul", other, type(other)
        return type(self)(int(other)*self.v, self.m, self.name)

    def __add__(self, other):
        if not isinstance(other, Unit):
            other = int(other) * b
        if self.m == other.m:
            return type(self)(self.v + other.v, self.m, self.name)
        if self % other.m == 0 and other % self.m == 0:
            if self.m > other.m:
                return type(self)(self.v//other.m + other.v//self.m, self.m, self.name)
            else:
                return type(self)(self.v//other.m + other.v//self.m, other.m, other.name)
        return type(self)(int(self) + int(other), b.m, b.name)

    def __radd__(self, other):
        return self.__add__(other)


b = Unit(1, 1, 'b')
O = Unit(1, 8, 'O')
