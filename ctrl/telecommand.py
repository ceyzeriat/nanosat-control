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
from . import db
from .telemetry import Telemetry


__all__ = ['Telecommand']


class Telecommand(object):
    def __init__(self, pkid=None, dbid=None):
        """
        Reads a TC from the database
        """
        # returns None if id not existing, else (hd, inputs)
        ret = db.get_TC(pkid=pkid, dbid=dbid)
        if ret is None:
            print("Could not find this TC id")
        else:
            self._telecommands = ret[0]
            self.hd = ret[1]
            self.inputs = ret[2]
            # copy fields to object root
            for k in self.hd.keys():
                setattr(self, k, self._telecommands[k])
        # load acknowledgements
        theid = getattr(
                self._telecommands.tmcat_rec_acknowledgements_collection[0],
                    'telemetry_packet', None)
        self.tm_RACK = None if theid is None else Telemetry(dbid=theid)
        theid = getattr(
                self._telecommands.tmcat_fmt_acknowledgements_collection[0],
                    'telemetry_packet', None)
        self.tm_FACK = None if theid is None else Telemetry(dbid=theid)
        theid = getattr(
                self._telecommands.tmcat_exe_acknowledgements_collection[0],
                    'telemetry_packet', None)
        self.tm_EACK = None if theid is None else Telemetry(dbid=theid)

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return

    @property
    def iserror(self):
        return self.RACK is False or self.FACK is False or self.EACK is False
    @iserror.setter
    def iserror(self, value):
        pass

    @property
    def isok(self):
        return self.RACK is not False and self.FACK is not False\
                and self.EACK is not False
    @isok.setter
    def isok(self, value):
        pass

    @property
    def istimedout(self):
        return self.timedout
    @istimedout.setter
    def istimedout(self, value):
        pass

    @classmethod
    def _fromCommand(cls, name, packet, dbid, hd, hdx, inputs, **kwargs):
        # broadcast on socket to the antenna process and watchdog
        controlling.broadcast_TC(cmdname=name, dbid=dbid, packet=packet,
                        hd=hd, hdx=hdx, inputs=inputs)
        cls.timedout = False
        cls.hd = hd
        cls.hd.update(hdx)
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
            if cls.EACK is True or\
                cls.EACK is False or\
                cls.FACK is False or\
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
