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


from .cm import Cm
from ..ccsds import TCPacker
from ..utils import core
#from .ccsds import ccsdsexception
from ..telecommand import Telecommand


__all__ = ['Command']


class Command(Cm):
    def __init__(self, *args, **kwargs):
        """
        Sends the command and stores it in the database

        Args ar ignored

        Kwargs:
        * the input parameters of the command
        * rack (bool): ``True`` to get the acknowledgement of reception
        * fack (bool): ``True`` to get the acknowledgement of format
        * eack (bool): ``True`` to get the acknowledgement of execution
        """
        # sole purpose of this __init__ is overwrite the docstring
        super(Command, self).__init__(*args, **kwargs)

    def _generate_packet(self, **kwargs):
        """
        Generates the full packet and returns the packet (str),
        the values used to generate the prim/sec headers (dict) and the
        input parameters used to generate the data (dict).
        """
        data, inputs = self.generate_data(**kwargs)
        packet, hd, hdx, dat = TCPacker.pack(pid=self.pid, data=data,
                                             tcid=self.number, retvalues=True,
                                             retdbvalues=True, **kwargs)
        return packet, hd, hdx, inputs

    def __call__(self, *args, **kwargs):
        return self.send(**kwargs)

    def send(self, *args, **kwargs):
        """
        Sends the command and stores it in the database

        Args ar ignored

        Kwargs:
        * the input parameters of the command
        * rack (bool): ``True`` to get the acknowledgement of reception
        * fack (bool): ``True`` to get the acknowledgement of format
        * eack (bool): ``True`` to get the acknowledgement of execution
        """
        # generates the packet
        packet, hd, hdx, inputs = self._generate_packet(**kwargs)
        # save to server
        hd['raw_file'] = core.RAWPACKETFILDER
        # saves to DB
        hd['time_sent'] = core.now()
        return Telecommand._initfromCommand(hd=hd, hdx=hdx, inputs=inputs)

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return self._generate_packet(**kwargs)

    @classmethod
    def _initfromCm(cls, cmd):
        return cls(**cmd.to_dict())
