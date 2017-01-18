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
import glob

from .soc import SocTransmitter
from .soc import SocReceiver
from .utils import core
from .telemetry import Telemetry
from .ccsds import CCSDSBlob
from . import ctrlexception


__all__ = ['process_data', 'init_saving', 'close_saving']


TM_TRANS = None
TM_REC = None
TM_running = False


class CommTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        print('New receiver on incoming packets broadcast: {}'.format(name))


class CommRec(SocReceiver):
    def process(self, data):
        """
        Saves the packet in the database and does 
        """
        blobparser = CCSDSBlob(data)
        start = 0
        pk = blobparser.grab_first_packet(start=start)
        while pk is not None:
            process_data(pk)
            start += len(pk)
            pk = blobparser.grab_first_packet(start=start)

    def _newconnection(self):
        """
        New connection or connection restablished
        """
        print('Listening socket: {}'.format(self._soc))


def process_data(data):
    """
    A callback function that saves the package in the database after
    parsing it
    """
    time_received, path, thedata = core.split_socket(data)[:3]
    if len(glob.glob(path)) == 0:
        raise ctrlexception.PacketFileMissing(path)
    f = open(path, mode='r')
    dd = f.read()
    f.close()
    if not dd == thedata:
        raise ctrlexception.PacketMismatch(path)
    time_received = core.strISOstamp2datetime(time_received)
    #if not time_received == core.packetfilename2datetime(path):
    #    raise ctrlexception.PacketDateMismatch(path)
    t = Telemetry(thedata, time_received=time_received)
    dum = TM_TRANS.tell(core.merge_socket(now, name, data))


def init_saving():
    """
    Initializes the saving procedure
    """
    global TM_TRANS
    global TM_REC
    global TM_running
    TM_TRANS = CommTrans(port=core.SAVESTATUSPORT,
                            nreceivermax=core.SAVESTATUSPORTLISTENERS,
                            start=True)
    TM_REC = CommRec(port=core.TELEMETRYPORT, name=core.SAVELISTENTMNAME,
                        connect=True, connectWait=0.5)
    TM_running = True


def close_saving():
    """
    Closes the saving procedure
    """
    global TM_TRANS
    global TM_REC
    global TM_running
    TM_running = False
    TM_TRANS.close()
    TM_REC.stop_connectLoop()
    TM_REC.close()
    TM_TRANS = None
    TM_REC = None
