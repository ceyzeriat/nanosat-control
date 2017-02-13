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


from param.param_all import DATETIME_REF
import datetime
import time


__all__ = ['Day']


class Day(int):
    def __init__(self, v):
        super(int, self).__init__()
        d = time.gmtime((DATETIME_REF + self) * 86400)        
        self._year = d.tm_year
        self._month = d.tm_mon
        self._day = d.tm_mday
        self._date = datetime.date(self._year, self._month, self._day)

    def strf(self, fmt='%Y/%m/%d'):
        """
        Returns the formatted string of the time

        Args:
        * fmt (time format): check
          https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        """
        return self._date.strftime(fmt)

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        pass

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, value):
        pass

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        pass
