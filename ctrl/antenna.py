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


import serial
import time
import glob
from .soc import SocTransmitter
from .soc import SocReceiver
from .utils import core
from .telemetry import Telemetry
from .utils import ctrlexception


__all__ = ['process_data', 'init_antenna', 'close_antenna']


COMM_TRANS = None
COMM_REC = None
ANTENNA = None
comm_running = False


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
        Sends the data to the antenna
        """
        ANTENNA.write(data)

    def _newconnection(self):
        """
        New connection or connection restablished
        """
        print('Listening socket: {}'.format(self._soc))


def process_data(data):
    """
    A callback function that saves the package and sends it
    over the TM socket
    """
    now = core.now()
    name = now.strftime(core.TELEMETRYNAMEFORMAT)
    name = core.concat_dir(core.TELEMETRYDUMPFOLDER, name)
    if len(glob.glob(name)) > 0:
        name += ".{}".format(len(glob.glob(name))+1)
    # sauvegarde locale
    f = open(name, mode='w')
    f.write(data)
    f.close()
    # envoi packets socket alpha
    dum = COMM_TRANS.tell(core.merge_socket_info(now, name, data))


def init_checkoutbox():
    global ANTENNA


def init_serial():
    global ANTENNA
    ANTENNA = serial.Serial(core.ANTENNAPORT)
    ANTENNA.open()
    ANTENNA.reset_input_buffer()
    ANTENNA.reset_output_buffer()
    ANTENNA.timetout = 0


def init_antenna(antenna):
    """
    Initializes the antenna

    ``antenna`` can be:
      * ``checkoutbox``: the ISIS rfcheckoutbox
    """
    global COMM_TRANS
    global COMM_REC
    global ANTENNA
    global comm_running
    COMM_TRANS = CommTrans(port=core.TELEMETRYPORT,
                            nreceivermax=core.TELEMETRYPORTLISTENERS,
                            start=True)
    COMM_REC = CommRec(port=core.TELECOMMANDPORT, name=core.COMMLISTENTCNAME,
                        connect=True, connectWait=0.5)
    print("Setting up antenna: '{}'".format(antenna))
    if antenna == 'checkoutbox':
        init_checkoutbox()
    else:
        raise ctrlexception.UnknownAntenna(antenna)
    comm_running = True


def close_antenna():
    """
    Closes the antenna
    """
    global COMM_TRANS
    global COMM_REC
    global ANTENNA
    global comm_running
    comm_running = False
    COMM_TRANS.close()
    COMM_REC.stop_connectLoop()
    COMM_REC.close()
    ANTENNA.close()
    COMM_TRANS = None
    COMM_REC = None
    ANTENNA = None
