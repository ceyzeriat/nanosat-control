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

from ctrl.soc import SocTransmitter
from ctrl.soc import SocReceiver
from ctrl.utils import core
from param import param_all
from ctrl.utils import ctrlexception
from ctrl.utils.report import REPORTS
from ctrl.telemetry import Telemetry
from ctrl.ccsds import CCSDSBlob
from ctrl.kiss import Framer


__all__ = ['init_saving', 'close_saving', 'report']


SAVE_TRANS = None
SAVE_REC_LISTEN = None
save_running = False


class SaveTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection is extablished
        """
        report('newTransConnection', rec=name)
        report('myPID', pid=core.get_pid())


class SaveRec(SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        report('newRecConnection', port=self.portname)
        report('myPID', pid=core.get_pid())

    def process(self, data):
        """
        Saves the packet in the database and does 
        """
        # ignores the reporting
        if core.is_reporting(data):
            return
        report('receivedTM')
        inputs = core.split_socket_info(data)
        if param_all.AX25ENCAPS:
            source, destination, blobish = Framer.decode_radio(inputs['data'])
            report('receivedCallsignTM', source=source, ll=len(blobish),
                        destination=destination)
        else:
            blobish = inputs['data']
            report('receivedRawTM', ll=len(blobish))
        blobparser = CCSDSBlob(blobish)
        start = 0
        pk = blobparser.grab_first_packet(start=start)
        if pk is not None:
            print(pk.hex())
        else:
            print(pk)
        while pk is not None:
            inputs['data'] = pk
            process_incoming(**inputs)
            start += len(pk)
            pk = blobparser.grab_first_packet(start=start)
        return


def process_incoming(t, path, data):
    """
    A callback function that saves the package in the database after
    parsing it
    """
    path = str(path)
    if len(glob.glob(path)) == 0:
        raise ctrlexception.PacketFileMissing(path)
    f = open(path, mode='rb')
    dd = Byt(f.read())
    f.close()
    if not dd == data:
        raise ctrlexception.PacketMismatch(path)
    t = core.strISOstamp2datetime(t)
    #if not t == core.packetfilename2datetime(path):
    #    raise ctrlexception.PacketDateMismatch(path)
    tm = Telemetry._fromPacket(data, time_received=t)
    report('savedTM', dbid=tm.dbid)


def report(report_key, **kwargs):
    """
    Reports to watchdog
    """
    rp = REPORTS[report_key].pack(who=core.SAVINGNAME, **kwargs)
    return SAVE_TRANS.tell(rp)


def init_saving():
    """
    Initializes the saving procedure
    """
    global SAVE_TRANS
    global SAVE_REC_LISTEN
    global save_running
    if save_running:
        return
    SAVE_TRANS = SaveTrans(port=param_all.SAVINGPORT[0],
                            nreceivermax=len(param_all.SAVINGPORTLISTENERS),
                            start=True, portname=param_all.SAVINGPORT[1])
    SAVE_REC_LISTEN = SaveRec(port=param_all.LISTENINGPORT[0],
                                name=param_all.SAVINGNAME, connect=True,
                                connectWait=0.5,
                                portname=param_all.LISTENINGPORT[1])
    save_running = True


def close_saving():
    """
    Closes the saving procedure
    """
    global SAVE_TRANS
    global SAVE_REC_LISTEN
    global save_running
    if not save_running:
        return
    save_running = False
    SAVE_TRANS.close()
    SAVE_REC_LISTEN.stop_connectLoop()
    SAVE_REC_LISTEN.close()
    SAVE_TRANS = None
    SAVE_REC_LISTEN = None
