#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .utils import core
#from . import ccsdsexception
from .ccsds import CCSDSUnPacker
from .ccsds import param_ccsds
from .ccsds import param_category
from . import db


__all__ = ['Telemetry']


class Telemetry(object):
    def __init__(self, packet, time_received=None):
        """
        Unpacks and stores the telemetry

        Args:
        * packet (str): the raw packet to unpack
        * time_received (datetime+tz): the reception time of the packet
        """
        self.packet = packet
        self._upk = CCSDSUnPacker(mode='tm')
        self.hd = {}
        self.hdx = {}
        self.data = {}
        self._process(time_received=time_received)

    def _process(self, time_received=None):
        """
        Unpacks the packet and feeds ``hd``, ``hdx`` and
        ``data`` attributes
        """
        self.hd, self.hdx, self.data = self._upk.unpack(self.packet,    
                                                        retdbvalues=True)
        self.hd['raw_file'] = './raw_data'
        self.hd['receiver_id'] = core.RECEIVERID
        self.hd['time_received'] = time_received\
                if isinstance(time_received, core.datetime.datetime)\
                else core.now()
        db.save_TM_to_DB(self.hd, self.hdx, self.data)

    def find_ack_TC(self):
        """
        Searches for the TC of which the TM is the acknowledgement
        """
        if int(self.hd[param_ccsds.PACKETCATEGORY.name])\
                not in param_category.ACKCATEGORIES:
            return None
        res = db.get_ack_TC(timestamp=self.hd['time_received'])
        return res
