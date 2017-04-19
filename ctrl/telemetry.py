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
from param import param_category_common as pcc
from .utils import core
from .ccsds import TMUnPacker
from .ccsds import param_ccsds
from . import db


__all__ = ['Telemetry']


class Telemetry(object):
    def __init__(self, pkid=None, dbid=None):
        """
        Gets a telemetry from the database
        """
        # returns None if id not existing, else (hd, inputs)
        ret = db.get_TM(pkid=pkid, dbid=dbid)
        if ret is None:
            print("Could not find this TM id")
        else:
            (self._telemetry, self.hd), (self._telemetry_hdx, self.hdx),\
                (self._telemetry_data, self.data) = ret
            # copy fields to object root
            for k in self.hd.keys():
                setattr(self, k, getattr(self._telemetry, k))
            for k in self.hdx.keys():
                setattr(self, k, getattr(self._telemetry_hdx, k))

    @classmethod
    def _fromPacket(cls, packet, time_received=None, user_id=None, **kwargs):
        """
        Unpacks and stores the telemetry. Feeds ``hd``, ``hdx`` and
        ``data`` attributes

        Args:
        * packet (str): the raw packet to unpack
        * time_received (datetime+tz): the reception time of the packet
        """
        cls.hd, cls.hdx, cls.data = TMUnPacker.unpack(packet, retdbvalues=True)
        cls.hd['raw_file'] = core.RAWPACKETFOLDER
        cls.hd['user_id'] = core.RECEIVERID if user_id is None\
                                    else int(user_id)
        cls.hd['time_received'] = time_received\
                if isinstance(time_received, core.datetime.datetime)\
                else core.now()
        dbid = db.save_TM_to_DB(cls.hd, cls.hdx, cls.data)
        # if it is a RACK, update the TM after checking the TC
        if int(cls.hd[param_ccsds.PACKETCATEGORY.name]) == int(RACKCAT):
            tcid = db.update_RACK_id(dbid=dbid)
        # elif it is a FACK or EACK
        elif (int(cls.hd[param_ccsds.PAYLOADFLAG.name]),
            int(cls.hd[param_ccsds.PACKETCATEGORY.name]))\
                in param_category.ACKCATEGORIES:
            tcid = db.update_ACK_id(dbid=dbid,
                                    pkid=cls.hdx[pcc.PACKETIDMIRROR.name])
        else:
            tcid = None
        cls.tcid = tcid
        return cls(dbid=dbid)
