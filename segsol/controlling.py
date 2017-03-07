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
from hein import SocTransmitter
from ctrl.utils import core
from ctrl.utils import ctrlexception
from ctrl.utils.report import REPORTS
from ctrl.kiss import Framer
from param import param_all

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
        report('myPID', pid=core.get_pid())


def broadcast_TC(cmdname, dbid, packet):
    """
    Sends the packet on the socket
    """
    if not control_running:
        raise ctrlexception.ControllingNotInitialized()
    report('broadcastTC', cmdname=cmdname, dbid=dbid)
    # add the AX25/KISS framing
    if param_all.AX25ENCAPS:
        packet = Framer.encode_radio(packet)
    # or add the ccsds flow splits
    elif param_all.FRAMESFLOW:
        packet = core.merge_flow([packet])
    dum = CONTROL_TRANS.tell(packet)
    ### check who recieved it and report
    return dum


def report(report_key, **kwargs):
    """
    Reports to watchdog
    """
    time.sleep(0.01)
    rp = REPORTS[report_key].pack(who=param_all.CONTROLLINGNAME, **kwargs)
    dum = CONTROL_TRANS.tell(rp)
    time.sleep(0.01)
    return dum


def init_control():
    """
    Initializes the control
    """
    global CONTROL_TRANS
    global control_running
    if control_running:
        return
    CONTROL_TRANS = ControlTrans(port=param_all.CONTROLLINGPORT[0],
                        nreceivermax=len(param_all.CONTROLLINGPORTLISTENERS),
                        start=True, portname=param_all.CONTROLLINGPORT[1])
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
