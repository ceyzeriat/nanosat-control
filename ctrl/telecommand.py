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


from .utils import core
#from .ccsds import ccsdsexception
from . import db


__all__ = ['Telecommand']


class Telecommand(object):
    def __init__(self, *args, **kwargs):
        """
        Sends the telecommand and stores it in the database

        Args ar ignored

        Kwargs:
        * the input parameters of the command
        * rack (bool): ``True`` to get the acknowledgement of reception
        * fack (bool): ``True`` to get the acknowledgement of format
        * eack (bool): ``True`` to get the acknowledgement of execution
        """
        pass

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return self._generate_packet(**kwargs)

    @classmethod
    def _initfromCommand(cls, hd, hdx, inputs):
        tcid = db.save_TC_to_DB(hd, hdx, inputs)
        # broadcast on socket to the antenna process
        # send(packet)
        return cls(**cmd.to_dict())
