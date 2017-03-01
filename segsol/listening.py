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
from ctrl.soc import SocTransmitter
from ctrl.soc import SocReceiver
from ctrl.utils.report import REPORTS
from ctrl.utils import core
from param import param_all
from ctrl.utils import ctrlexception
from ctrl.rfcheckoutbox import RFCheckoutbox
from ctrl.serialusb import SerialUSB


__all__ = ['process_data', 'init_listening', 'close_listening', 'report']


LISTEN_TRANS = None
LISTEN_REC_CONTROL = None
ANTENNA = None
listen_running = False


class ListenTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        report('newTransConnection', rec=name)
        report('myPID', pid=core.get_pid())


class ListenRec(SocReceiver):
    def _newconnection(self):
        """
        New connection or connection restablished
        """
        report('newRecConnection', port=self.portname)
        report('myPID', pid=core.get_pid())

    def process(self, data):
        """
        Sends the data to the antenna
        """
        # ignores the reporting
        if core.is_reporting(data):
            return
        else:
            report('sendingTC')
            ANTENNA.write(data)
            now = core.now()
            ### if success, update hd['time_sent'] in database
            report('sentTC', t=now)


def process_data(data):
    """
    A callback function that saves the package and sends it
    over the TM socket
    """
    if len(data) == 0:
        return
    now = core.now()
    name = now.strftime(param_all.TELEMETRYNAMEFORMAT)
    path = param_all.TELEMETRYDUMPFOLDER + [name]
    name = core.home_dir(*path)
    if os.path.isfile(name):  # already exists
        name += ".{}".format(len(glob.glob(name))+1)
    # locally saved
    f = open(name, mode='wb')
    f.write(data)
    f.close()
    # sends packets on the socket
    dum = LISTEN_TRANS.tell(core.merge_socket_info(t=now, path=name,
                                                    data=data))
    ### check who recieved it and report
    return dum


def init_checkoutbox():
    global ANTENNA
    ANTENNA = RFCheckoutbox()


def init_serial():
    global ANTENNA
    ANTENNA = SerialUSB()


def report(report_key, **kwargs):
    """
    Reports to watchdog
    """
    time.sleep(0.01)
    rp = REPORTS[report_key].pack(who=param_all.LISTENINGNAME, **kwargs)
    dum = LISTEN_TRANS.tell(rp)
    time.sleep(0.01)
    return dum


def init_listening(antenna):
    """
    Initializes the listening

    ``antenna`` can be:
      * ``checkoutbox``: the ISIS rfcheckoutbox
      * ``serial``: the serial/USB port
    """
    global LISTEN_TRANS
    global LISTEN_REC_CONTROL
    global ANTENNA
    global listen_running
    if listen_running:
        return
    LISTEN_TRANS = ListenTrans(port=param_all.LISTENINGPORT[0],
                            nreceivermax=len(param_all.LISTENINGPORTLISTENERS),
                            start=True, portname=param_all.LISTENINGPORT[1])
    LISTEN_REC_CONTROL = ListenRec(port=param_all.CONTROLLINGPORT[0],
                                name=param_all.LISTENINGNAME, connect=True,
                                connectWait=0.5,
                                portname=param_all.CONTROLLINGPORT[1])
    report('SettingUpAntenna', antenna=antenna)
    if antenna == 'checkoutbox':
        init_checkoutbox()
    elif antenna == 'serial':
        init_serial()
    else:
        close_listening()
        raise ctrlexception.UnknownAntenna(antenna)
    listen_running = True


def close_listening():
    """
    Closes the listening
    """
    global LISTEN_TRANS
    global LISTEN_REC_CONTROL
    global ANTENNA
    global listen_running
    if not listen_running:
        return
    listen_running = False
    LISTEN_TRANS.close()
    LISTEN_REC_CONTROL.stop_connectLoop()
    LISTEN_REC_CONTROL.close()
    ANTENNA.close()
    LISTEN_TRANS = None
    LISTEN_REC_CONTROL = None
    ANTENNA = None
