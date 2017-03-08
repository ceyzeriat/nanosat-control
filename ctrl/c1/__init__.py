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
from ..cmd import L1CMDS as _ALL
from ..cmd import Command
from ..utils import bincore


__all__ = []


class setDatetime(Command):
    def generate_data(self, *args, **kwargs):
        stamp = kwargs.get('datetime')
        if not isinstance(stamp, datetime):
            raise TypeError
        res = ((stamp.month // 10) << 4) + (stamp.month % 10)
        res = (res << 6) + ((stamp.day // 10) << 4) + (stamp.day % 10)
        res = (res << 6) + ((stamp.hour // 10) << 4) + (stamp.hour % 10)
        res = (res << 7) + ((stamp.minute // 10) << 4) + (stamp.minute % 10)
        res = (res << 7) + ((stamp.second // 10) << 4) + (stamp.second % 10)
        kwargs['datetime'] = res
        return super(Command, self).generate_data(*args, **kwargs)


for _cmd in _ALL:
    if _cmd.name == 'set_datetime':
        _cmd = setDatetime(**_cmd.to_dict())
    locals()[_cmd.name] = _cmd
    __all__.append(_cmd.name)


