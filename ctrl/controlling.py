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


from .soc import SocTransmitter
from .utils import core
from .utils import REPORTS
from .kiss import Framer
from .utils import ctrlexception


__all__ = ['init_control', 'close_control', 'broadcast_TC', 'report']


CONTROL_TRANS = None
control_running = False


class ControlTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        report('newTransConnection', rec=name)


def broadcast_TC(dbid, packet):
    """
    Sends the packet on the socket
    """
    if not control_running:
        raise ctrlexception.ControllingNotInitialized()
    report('broadcastTC', dbid=dbid)
    # add the kiss frame
    kisspacket = Framer.encode_kiss(packet)
    dum = CONTROL_TRANS.tell(kisspacket)
    ### check who recieved it and report
    return dum


def report(report_key, **kwargs):
    """
    Reports to watchdog
    """
    rp = REPORTS[report_key].pack(who=core.CONTROLLINGNAME, **kwargs)
    return CONTROL_TRANS.tell(rp)


def init_control():
    """
    Initializes the control
    """
    global CONTROL_TRANS
    global control_running
    if control_running:
        return
    CONTROL_TRANS = ControlTrans(port=core.CONTROLLINGPORT[0],
                            nreceivermax=len(core.CONTROLLINGPORTLISTENERS),
                            start=True, portname=core.CONTROLLINGPORT[1])
    control_running = True


def close_control():
    """
    Closes the control
    """
    global CONTROL_TRANS
    global control_running
    if not control_running:
        return
    control_running = False
    CONTROL_TRANS.close()
    CONTROL_TRANS = None
