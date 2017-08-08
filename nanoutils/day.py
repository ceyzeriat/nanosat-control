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


from nanoparam import param_all
import datetime
import time


__all__ = ['Day']


class Day(int):
    def __new__(cls, v):
        """
        Takes a satelite daystamp and makes it user-friendly with year,
        month, day, and strf methods/attributes
        """
        v = int(min(24001 - param_all.DATETIME_REF, max(0, v)))
        ans = super(Day, cls).__new__(cls, v) 
        d = time.gmtime((param_all.DATETIME_REF + ans) * 86400)        
        ans._year = d.tm_year
        ans._month = d.tm_mon
        ans._day = d.tm_mday
        ans._date = datetime.date(ans._year, ans._month, ans._day)
        return ans

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
