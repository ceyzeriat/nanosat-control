#!/usr/bin/env python
# -*- coding: utf-8 -*-


import serial
import time
import glob
from .soc import SocTransmitter
from .soc import SocReceiver
from .utils import core
from .telemetry import Telemetry


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
    f = open(name, mode='w')
    f.write(data)
    f.close()
    # envoi packets socket alpha
    dum = COMM_TRANS.tell(core.merge_socket(now, name, data))


def init_antenna():
    """
    Initializes the antenna
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
    ANTENNA = serial.Serial(core.ANTENNAPORT)
    ANTENNA.open()
    ANTENNA.reset_input_buffer()
    ANTENNA.reset_output_buffer()
    ANTENNA.timetout = 0
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
