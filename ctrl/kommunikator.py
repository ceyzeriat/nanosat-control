#!/usr/bin/env python
# -*- coding: utf-8 -*-


import serial
import time
from ctrl.soc import SocTransmitter, SocReceiver
from ctrl.utils import core


__all__ = ['Kommunikator']


class CommTrans(SocTransmitter):
    def _newconnection(self, name):
        """
        Call-back function when a new connection
        is extablished
        """
        print('New reciever on incomming packets broadcast: {}'.format(name))

class CommRec(SocReceiver):
    def process(self, data):
        """
        Sends the data to the antenna
        """
        # send data to antenna
        # écriture COM
        print(data)

    def _newconnection(self):
        """
        New connection or connection restablished
        """
        pass


class Kommunikator(object):
    def __init__(self):
        self.initAntenna()
        self.trans = CommTrans(port=core.TELEMETRYPORT,
                                nreceivermax=core.TELEMETRYPORTLISTENERS,
                                start=True)
        self.rec = CommRec(port=core.TELEMETRYPORT, name="comm",
                            connect=True, connectWait=0.5)
        self._start()
    
    def _start(self):
        if not self._running:
            return
        self._running = True
        loopy = Thread(target=get_data, args=(self, ))
        loopy.daemon = True
        loopy.start()

    def initAntenna(self):
        """
        Establish the port-communication to the antenna
        """
        self.ser = serial.Serial(core.ANTENNAPORT)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def process_data(self):
        # save packet disk (local)
        # envoi packets socket alpha 

def get_data(self):
    """
    Function called in an infinite loop to retrieve the
    data out of the antenna port
    """
    while self._running:
        time.sleep(1./core.ANTENNARPORTREADFREQ)
        n = self.ser.in_waiting()
        if n > 0:
            self.process_data(self.ser.read(size=n))
