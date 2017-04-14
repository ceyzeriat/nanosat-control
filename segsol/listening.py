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
import os
import glob
import hein
from byt import Byt
from threading import Thread
from ctrl.utils.report import REPORTS
from ctrl.utils import core
from param import param_all
from ctrl.utils import ctrlexception
from ctrl.rfcheckoutbox import RFCheckoutbox
from ctrl.serialusb import SerialUSB


__all__ = ['process_data', 'init', 'close', 'report', 'theloop']


LISTEN_TRANS = None
LISTEN_REC_CONTROL = None
ANTENNA = None
running = False


class ListenTrans(hein.SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        report('newTransConnection', rec=name)
        report('myPID', pid=core.get_pid())


class ListenRec(hein.SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        report('newRecConnection', port=self.portname)
        report('myPID', pid=core.get_pid())

    def process(self, key, data):
        """
        Sends the data to the antenna
        """
        # ignores the reporting
        if key == 'rpt':
            return
        elif key == 'raw':
            report('sendingTC')
            ANTENNA.write(data)
            now = core.now()
            # this report is caught by control, which updates the
            # time_sent in the DB
            report('sentTC', t=now, data=data)


def process_data(data):
    """
    A callback function that saves the package and sends it
    over the TM socket
    """
    if len(data) == 0:
        return
    now = core.now()
    name = now.strftime(param_all.TELEMETRYNAMEFORMAT)
    name = param_all.TELEMETRYDUMPFOLDER + [name]
    name = core.home_dir(*name)
    if os.path.isfile(name):  # already exists
        name += ".{}".format(len(glob.glob(name))+1)
    # locally saved
    f = open(name, mode='wb')
    f.write(data)
    f.close()
    # sends packets on the socket
    LISTEN_TRANS.tell_dict(t=now, path=name, data=data)


def report(*args, **kwargs):
    """
    Reports to watchdog
    """
    key = str(args[0])
    rp = REPORTS[key].pack(who=param_all.LISTENINGNAME, **kwargs)
    LISTEN_TRANS.tell_report(**rp)


def get_data():
    time.sleep(0.01)  # Don't kill the CPU
    n = ANTENNA.in_waiting()
    if n < 0:
        return None
    # grab data
    data = ANTENNA.read(size=n)
    # empty data
    if data is None:
        return None
    if len(data) == 0:
        return None
    return Byt(data)


def proceed(data):
    report('GotBlob', ll=len(data), blob=data)
    # deal with it in a separate thread
    loopy = Thread(target=process_data, args=(data,))
    loopy.daemon = True
    loopy.start()


if not param_all.FRAMESFLOW:
    def theloop():
        while running:
            data = get_data()
            if data is None:
                continue
            proceed(data)
else:
    def theloop():
        inbuff = Byt()
        while running:
            data = get_data()
            if data is None:
                continue
            inbuff += data
            res = core.split_flow(data=inbuff, n=-1)
            if len(res) < 2:
                continue  # didn't find a full packet yet
            inbuff = res.pop(-1)
            for packet in res:
                proceed(packet)


def init(antenna):
    """
    Initializes the listening

    ``antenna`` can be:
      * ``checkoutbox``: the ISIS rfcheckoutbox
      * ``serial``: the serial/USB port
    """
    global LISTEN_TRANS
    global LISTEN_REC_CONTROL
    global ANTENNA
    global running
    if running:
        return
    LISTEN_TRANS = ListenTrans(port=param_all.LISTENINGPORT[0],
                            nreceivermax=len(param_all.LISTENINGPORTLISTENERS),
                            start=True, portname=param_all.LISTENINGPORT[1],
                            timeoutACK=3)
    LISTEN_REC_CONTROL = ListenRec(port=param_all.CONTROLLINGPORT[0],
                                name=param_all.LISTENINGNAME, connect=True,
                                connectWait=0.5,
                                portname=param_all.CONTROLLINGPORT[1],
                                hostname = 'localhost')
    report('SettingUpAntenna', antenna=antenna)
    if antenna == 'checkoutbox':
        ANTENNA = RFCheckoutbox()
    elif antenna == 'serial':
        ANTENNA = SerialUSB()
    else:
        close()
        raise ctrlexception.UnknownAntenna(antenna)
    running = True


def close():
    """
    Closes the listening
    """
    global LISTEN_TRANS
    global LISTEN_REC_CONTROL
    global ANTENNA
    global running
    if not running:
        return
    running = False
    LISTEN_TRANS.close()
    LISTEN_REC_CONTROL.stop_connectLoop()
    LISTEN_REC_CONTROL.close()
    ANTENNA.close()
    LISTEN_TRANS = None
    LISTEN_REC_CONTROL = None
    ANTENNA = None
