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


import time
try:
    import Queue as queue
except:
    import queue
from segsol import controlling
from .ccsds import param_ccsds
from .utils import core


__all__ = ['Telecommand']


class Telecommand(object):
    def __init__(self, dbid):
        """
        Reads a telecommand from the database
        """
        self.dbid = dbid
        # TC not saved
        if dbid is None:
            return
        # read database and take a telecommand

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return

    @property
    def any(self):
        return self.RACK is False or self.FACK is False or self.EACK is False
    @any.setter
    def any(self, value):
        pass

    @property
    def all(self):
        return self.RACK is not False and self.FACK is not False\
                and self.EACK is not False
    @all.setter
    def all(self, value):
        pass

    @classmethod
    def _fromCommand(cls, name, packet, dbid, hd, hdx, inputs, **kwargs):
        # broadcast on socket to the antenna process and watchdog
        controlling.broadcast_TC(cmdname=name, dbid=dbid, packet=packet,
                        hd=hd, hdx=hdx, inputs=inputs)
        cls.timedout = False
        cls.hd = hd
        cls.hdx = hdx
        cls.inputs = inputs
        # no wait
        if not kwargs.pop('wait', core.DEFAULTWAITCMD):
            return cls(dbid=dbid)
        # False if waiting for ACK, else None
        cls.rack = bool(int(hd[param_ccsds.REQACKRECEPTIONTELECOMMAND.name]))
        cls.RACK = None
        cls.fack = bool(int(hd[param_ccsds.REQACKFORMATTELECOMMAND.name]))
        cls.FACK = None
        cls.eack = bool(int(hd[param_ccsds.REQACKEXECUTIONTELECOMMAND.name]))
        cls.EACK = None
        # don't expect any ack
        if not (cls.rack or cls.fack or cls.eack):
            return cls(dbid=dbid)
        pkid = int(hd[param_ccsds.PACKETID.name])
        doneat = time.time() + kwargs.pop('timeout', core.DEFAULTTIMEOUTCMD)
        # check format first since it may prevent eack from being sent
        while time.time() < doneat:
            # if no ACK is False (waiting for ACK), then break
            if cls.EACK is not None or\
                (cls.eack is False and cls.FACK is not None) or\
                (cls.eack is False and cls.fack is False\
                                    and cls.RACK is not None):
                break
            try:
                res = controlling.ACKQUEUE.get(
                                block=True,
                                timeout=max(0, doneat - time.time()))
                controlling.ACKQUEUE.task_done()
            except queue.Empty:
                cls.timedout = True
                break
            # pkid mathcing except for when it is None, meaning it is RACK
            # because TM packets being RACK don't copy the PACKETID of the TC
            if res[0] is None:
                if res[1] == 0:
                    cls.RACK = True
            elif res[0] == pkid:
                if res[1] == 1:
                    cls.FACK = (res[2] == 0)
                elif res[1] == 2:
                    cls.EACK = (res[2] == 0)
        return cls(dbid=dbid)
