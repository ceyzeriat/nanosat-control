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


from datetime import datetime

from .command import Command


# function set_datetime of PLD, aim is to allow the input of a
# datetime or date-tuple instead of a dirty integer timestamp
class setDatetime(Command):
    def generate_data(self, *args, **kwargs):
        stamp = kwargs.get('datetime')
        if not isinstance(stamp, (datetime, list, tuple)):
            raise TypeError
        if isinstance(stamp, (list, tuple)):
            stamp = datetime(*stamp)
        newkwargs = {}
        newkwargs['years'] = stamp.year - 1970
        newkwargs['months'] = stamp.month
        newkwargs['days'] = stamp.day
        newkwargs['hours'] = stamp.hour
        newkwargs['minutes'] = stamp.minute                
        newkwargs['seconds'] = stamp.second
        return super(setDatetime, self).generate_data(*args, **newkwargs)
