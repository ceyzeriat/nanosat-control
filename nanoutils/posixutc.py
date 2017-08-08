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
import pytz
import calendar


__all__ = ['PosixUTC']


class PosixUTC(datetime.datetime):
    def __new__(cls, year, month, day, hour, minute, second, microsecond=0,
                    *args, **kwargs):
        """
        Initializes a posix timestamp with UTC timezone
        """
        return datetime.datetime.__new__(cls, year, month, day,
                        hour, minute, second, microsecond, tzinfo=pytz.utc)

    def totimestamp(self):
        """
        Transforms a datetime 'now' with timezone to a posix timestamp
        """
        return calendar.timegm(self.timetuple()) + self.microsecond*0.000001

    @classmethod
    def fromtimestamp(cls, ts):
        """
        Initializes a PosixUTC object from UTC timestamp
        """
        t = datetime.datetime.fromtimestamp(ts, tz=pytz.utc)
        return cls.fromdatetime(t)

    @classmethod
    def fromdatetime(cls, t):
        """
        Initializes a PosixUTC object from UTC datetime object
        """
        return cls(t.year, t.month, t.day, t.hour, t.minute, t.second,
                    t.microsecond)

    @classmethod
    def now(cls):
        """
        Initializes a PosixUTC object with UTC timezone
        """
        t = datetime.datetime.now(tz=pytz.utc)
        return cls.fromdatetime(t)
