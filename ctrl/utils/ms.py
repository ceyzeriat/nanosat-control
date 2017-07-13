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


import datetime


__all__ = ['Ms']


class Ms(int):
    def __new__(cls, v): 
        return int(min(86399999, max(0, v)))

    def __init__(self, v):
        super(int, self).__init__()
        self._hour = self // 3600000
        self._min = (self % 3600000) // 60000
        self._sec = (self % 60000) // 1000
        self._msec = self % 1000
        self._time = datetime.time(self._hour, self._min, self._sec,
                                   self._sec*1000)

    def strf(self, fmt='%H:%M:%S'):
        """
        Returns the formatted string of the time

        Args:
        * fmt (time format): %H=hours, %M=minutes, %S=seconds,
          %f=microseconds. Check:
          https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        """
        return self._time.strftime(fmt)

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        pass

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, value):
        pass

    @property
    def sec(self):
        return self._sec

    @sec.setter
    def sec(self, value):
        pass

    @property
    def msec(self):
        return self._msec

    @msec.setter
    def msec(self, value):
        pass
