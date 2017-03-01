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


from param import param_category
from .utils import core
from .ccsds import TMUnPacker
from .ccsds import param_ccsds
from . import db


__all__ = ['Telemetry']


class Telemetry(object):
    def __init__(self, dbid):
        """
        Gets a telemetry from the database
        """
        self.dbid = int(dbid)

    @classmethod
    def _fromPacket(cls, packet, time_received=None):
        """
        Unpacks and stores the telemetry. Feeds ``hd``, ``hdx`` and
        ``data`` attributes

        Args:
        * packet (str): the raw packet to unpack
        * time_received (datetime+tz): the reception time of the packet
        """
        cls.hd, cls.hdx, cls.data = TMUnPacker.unpack(packet, retdbvalues=True)
        print cls.data['unpacked']
        cls.hd['raw_file'] = core.RAWPACKETFOLDER
        cls.hd['receiver_id'] = core.RECEIVERID
        cls.hd['time_received'] = time_received\
                if isinstance(time_received, core.datetime.datetime)\
                else core.now()
        dbid = db.save_TM_to_DB(cls.hd, cls.hdx, cls.data)
        return cls(dbid=dbid)

    def find_ack_TC(self):
        """
        Searches for the TC of which the TM is the acknowledgement
        """
        if int(self.hd[param_ccsds.PACKETCATEGORY.name])\
                not in param_category.ACKCATEGORIES:
            return None
        res = db.get_ack_TC(timestamp=self.hd['time_received'])
        return res
