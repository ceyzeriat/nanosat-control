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
            return
        (self._telecommand, self.hd), self.inputs, (rack, fack, eack) = ret
        # copy fields to object root
        for k in self.hd.keys():
            setattr(self, k, getattr(self._telecommand, k))
        # load acknowledgements as real Telemetry objects
        self.RACK = None if rack is None else Telemetry(dbid=rack)
        self.FACK = None if rack is None else Telemetry(dbid=fack)
        self.EACK = None if rack is None else Telemetry(dbid=eack)

    def show(self, *args, **kwargs):
        """
        Show pretty packet
        """
        return

    @property
    def issent(self):
        return (self.time_sent is not None)
    @issent.setter
    def issent(self, value):
        pass
    
    @property
    def iserror(self):
        return not((self.FACK is None or bool(self.FACK))\
                    and (self.EACK is None or bool(self.EACK)))
    @iserror.setter
    def iserror(self, value):
        pass

    @property
    def isRACK(self):
        rack = bool(getattr(self, param_ccsds.REQACKRECEPTIONTELECOMMAND.name))
        return (self.RACK is None and rack is False)\
                or (bool(self.RACK) and rack is True)
    @isRACK.setter
    def isRACK(self, value):
        pass

    @property
    def isFACK(self):
        fack = bool(getattr(self, param_ccsds.REQACKFORMATTELECOMMAND.name))
        return (self.FACK is None and fack is False)\
                or (bool(self.FACK) and fack is True)
    @isFACK.setter
    def isFACK(self, value):
        pass

    @property
    def isEACK(self):
        eack = bool(getattr(self, param_ccsds.REQACKEXECUTIONTELECOMMAND.name))
        return (self.EACK is None and eack is False)\
                or (bool(self.EACK) and eack is True)
    @isEACK.setter
    def isEACK(self, value):
        pass

    @property
    def isALLACK(self):
        return self.isRACK and self.isFACK and self.isEACK
    @isALLACK.setter
    def isALLACK(self, value):
        pass    

    @property
    def isok(self):
        return (self.RACK is None or bool(self.RACK))\
                and (self.FACK is None or bool(self.FACK))\
                and (self.EACK is None or bool(self.EACK))
    @isok.setter
    def isok(self, value):
        pass

    @property
    def istimedout(self):
        return getattr(self, '_timedout', None)
    @istimedout.setter
    def istimedout(self, value):
        pass

    @classmethod
    def _fromCommand(cls, name, packet, dbid, hd, hdx, inputs, **kwargs):
        # broadcast on socket to the antenna process and watchdog
        controlling.broadcast_TC(cmdname=name, dbid=dbid, packet=packet,
                        hd=hd, hdx=hdx, inputs=inputs)
        cls._timedout = False
        hd = hd
        hd.update(hdx)
        # no wait
        if not kwargs.pop('wait', core.DEFAULTWAITCMD):
            time.sleep(0.1)
            return cls(dbid=dbid)
        # False if waiting for ACK, else None
        rack = bool(int(hd[param_ccsds.REQACKRECEPTIONTELECOMMAND.name]))
        RACK = None
        fack = bool(int(hd[param_ccsds.REQACKFORMATTELECOMMAND.name]))
        FACK = None
        eack = bool(int(hd[param_ccsds.REQACKEXECUTIONTELECOMMAND.name]))
        EACK = None
        # init ccsds keys, just in case a meteorite kills all form of life
        setattr(cls, param_ccsds.REQACKRECEPTIONTELECOMMAND.name, rack)
        setattr(cls, param_ccsds.REQACKFORMATTELECOMMAND.name, fack)
        setattr(cls, param_ccsds.REQACKEXECUTIONTELECOMMAND.name, eack)
        # don't expect any ack
        if not (rack or fack or eack):
            return cls(dbid=dbid)
        pkid = int(hd[param_ccsds.PACKETID.name])
        doneat = time.time() + kwargs.pop('timeout', core.DEFAULTTIMEOUTCMD)
        # check format first since it may prevent eack from being sent
        while time.time() < doneat:
            # if no ACK is False (waiting for ACK), then break
            if EACK is True or\
                EACK is False or\
                FACK is False or\
                (eack is False and FACK is not None) or\
                (eack is False and fack is False\
                                    and RACK is not None):
                break
            try:
                res = controlling.ACKQUEUE.get(
                                block=True,
                                timeout=max(0, doneat - time.time()))
                controlling.ACKQUEUE.task_done()
            except queue.Empty:
                cls._timedout = True
                break
            # pkid mathcing except for when it is None, meaning it is RACK
            # because TM packets being RACK don't copy the PACKETID of the TC
            if res[0] is None:
                if res[1] == 0:
                    RACK = True
            elif res[0] == pkid:
                if res[1] == 1:
                    FACK = (res[2] == 0)
                elif res[1] == 2:
                    EACK = (res[2] == 0)
        return cls(dbid=dbid)
