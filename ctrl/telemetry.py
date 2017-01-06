#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .utils import core
#from . import ccsdsexception
from .ccsds import CCSDSUnPacker
from . import db


__all__ = ['Telemetry']


class Telemetry(object):
    def __init__(self, packet):
        """
        Unpacks and stores the telemetry

        Args:
        * packet (str): the raw packet to unpack
        """
        self.packet = packet
        self._upk = CCSDSUnPacker(mode='tm')
        self.hd = {}
        self.hdx = {}
        self.data = {}
        self._process()

    def _process(self):
        """
        Unpacks the packet and feeds ``hd``, ``hdx`` and
        ``data`` attributes
        """
        self.hd, self.hdx, self.data = self._upk.unpack(self.packet,    
                                                        retdbvalues=True)
        hd['raw_file'] = './raw_data'
        hd['receiver_id'] = core.RECEIVERID
        hd['time_received'] = core.now()
        db.save_TM_to_DB(hd, hdx, data)

    def find_ack_TC(self):
        """
        Searches for the TC of which the TM is the acknowledgement
        """
        pass
