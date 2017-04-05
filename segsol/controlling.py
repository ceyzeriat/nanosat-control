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
import hein
from byt import Byt
from multiprocessing import Manager
from ctrl.utils import core
from ctrl.utils import ctrlexception
from ctrl.utils.report import REPORTS, EXTRADISPKEY
from ctrl.ccsds import CCSDSBlob
from ctrl.kiss import Framer
from ctrl.ccsds import TMUnPacker
from ctrl.ccsds import TCUnPacker
from ctrl.ccsds import param_ccsds
from ctrl import db
from param import param_all
from param import param_category
from param import param_category_common


__all__ = ['init', 'close', 'broadcast_TC', 'report']


CONTROL_TRANS = None
CONTROL_REC_LISTEN = None
running = False
ACKQUEUE = Manager().Queue(maxsize=0)


class ControlTrans(hein.SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        report('newTransConnection', rec=name)
        report('myPID', pid=core.get_pid())


class ControlRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        report('newRecConnection', port=self.portname)
        report('myPID', pid=core.get_pid())

    def process(self, key, data):
        """
        Checks for feedback from listen
        """
        # ignores anything but dic and rpt if key is sentTC
        if key != 'dic' and key != 'rpt':
            return
        if key == 'rpt':
            print(str(data[param_all.REPORTKEY]), data.keys())
            # case of getting the TC back, update time_sent in DB
            if str(data[param_all.REPORTKEY]) == 'sentTC':
                res = TCUnPacker.unpack_primHeader(data['data'])
                pkid = int(res[0][param_ccsds.PACKETID.name])
                db.update_sent_TC_time(pkid, kwargs['t'])
            else:
                return
        blobish = data['data']
        # skin the AX25 and KISS
        if param_all.AX25ENCAPS:
            source, destination, blobish = Framer.decode_radio(blobish)
        blobparser = CCSDSBlob(blobish)
        start = 0
        pk = blobparser.grab_first_packet(start=start)
        while pk is not None:
            data['data'] = Byt(pk)
            process_incoming(**data)
            start += len(pk)
            pk = blobparser.grab_first_packet(start=start)
        return


def process_incoming(**kwargs):
    """
    A callback function that gives ackowledgement notice
    """
    global ACKQUEUE
    data = kwargs['data']
    hd = TMUnPacker.unpack_primHeader(data)
    cat = int(hd[param_ccsds.PACKETCATEGORY.name])
    pld = int(hd[param_ccsds.PAYLOADFLAG.name])
    # not an acknoledgement
    if (pld, cat) not in param_category.ACKCATEGORIES:
        return
    # if FACK or EACK -> grab error
    if cat != int(param_category.RACKCAT):
        hd = TMUnPacker.unpack_auxHeader(data, pldFlag=pld, pktCat=cat)
        pkid = int(hd[param_category_common.PACKETIDMIRROR.name])
        error = int(hd[param_category_common.ERRORCODE.name])
        thecat = 1 if cat == int(param_category.FACKCAT) else 2
    else:  # just a RACK
        pkid = None  # no pkid mirror for RACK
        error = 0
        thecat = 0
    # add to queue
    report('gotACK', pkid=pkid, thecat=thecat, error=error,
            **{EXTRADISPKEY: False})
    # send it to the queue for telecommand
    ACKQUEUE.put((pkid, thecat, error))


def broadcast_TC(cmdname, dbid, packet, hd, hdx, inputs):
    """
    Sends the packet on the socket
    """
    if not running:
        raise ctrlexception.ControllingNotInitialized()
    report('broadcastTC', cmdname=cmdname, dbid=dbid)
    allinputs = {}
    allinputs.update(hd)
    allinputs.update(hdx)
    allinputs.update(inputs)
    allinputs.update({'cmdname': cmdname, 'dbid': dbid})
    CONTROL_TRANS.tell_key('tcf', **allinputs)
    # add the AX25/KISS framing
    if param_all.AX25ENCAPS:
        packet = Framer.encode_radio(packet)
    # or add the ccsds flow splits
    elif param_all.FRAMESFLOW:
        packet = core.merge_flow([packet])
    CONTROL_TRANS.tell_raw(packet)


def report(*args, **kwargs):
    """
    Reports to watchdog
    """
    key = str(args[0])
    rp = REPORTS[key].pack(who=param_all.CONTROLLINGNAME, **kwargs)
    CONTROL_TRANS.tell_report(**rp)


def init():
    """
    Initializes the control
    """
    global CONTROL_TRANS
    global CONTROL_REC_LISTEN
    global running
    if running:
        return
    CONTROL_TRANS = ControlTrans(port=param_all.CONTROLLINGPORT[0],
                        nreceivermax=len(param_all.CONTROLLINGPORTLISTENERS),
                        start=True, portname=param_all.CONTROLLINGPORT[1])
    CONTROL_REC_LISTEN = ControlRec(port=param_all.LISTENINGPORT[0],
                                name=param_all.CONTROLLINGNAME, connect=True,
                                connectWait=0.5,
                                portname=param_all.LISTENINGPORT[1])
    running = True


def close():
    """
    Closes the control
    """
    global CONTROL_TRANS
    global CONTROL_REC_LISTEN
    global running
    if not running:
        return
    running = False
    CONTROL_TRANS.close()
    CONTROL_REC_LISTEN.stop_connectLoop()
    CONTROL_REC_LISTEN.close()
    CONTROL_TRANS = None
    CONTROL_REC_LISTEN = None
