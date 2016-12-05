#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .ccsds import CCSDS
from .param import *
from .core import *
exc = core.ccsdsexception


__all__ = ['CCSDSBlob']


class CCSDSBlob(object):
    def __init__(self, blob, packet_version, packet_type,
                 secondary_header_flag, apid):
        """
        Analyzes a blob of bits to find the first valid packet
        These 4 packet-related parameters are used as assumptions
        to parse and validate the packet

        Args:
        * blob (str): the '\x00\xf0...' string
        * packet_version: 0
        * packet_type: 'telemetry' or 'telecommand'
        * secondary_header_flag: ``True`` or ``False``
        * apid: 'hk_payload' or 'science_payload'
        """
        self.blob = blob
        self.param = {}
        self.param['pv'] = int(packet_version)
        self.param['pt'] = packet_type
        self.param['shf'] = int(bool(secondary_header_flag))
        self.param['apid'] = apid

    def find(self, idx=0):
        """
        Finds the start of a packet in the blob.
        Returns the index of the start or -1 if not found

        Args:
        * idx (int): from where the search should start
        """
        dum = PACKETVERSION[self.param['pv']]+PACKETTYPE[self.param['pt']]\
              + SECONDARYHEADERFLAG[self.param['shf']]+APID[self.param['apid']]
        key = "".join([bin2hex(item, char=True)\
                       for item in octify(dum)])
        return self.blob.find(key, idx)

    def grab_data_length(self, start):
        """
        Returns the data-lengh as int, contained in the header of the
        packet

        Args:
        * start (int): the first bit of the packet in the blob
        """
        dum = "".join([hex2bin(item) for item in self.blob[start:start+6]])
        return DATALENGTH.grab(dum)

    def find_first_packet(self, idx=0):
        """
        Finds the first valid packet, assuming the packet
        parameters provided at initialization.
        Returns a slice, or ``None`` if no valid packet found

        Args:
        * idx (int): from where the search should start
        """
        idx = self.find(idx=idx)
        if idx == -1:
            return None
        try:
            length = self.grab_data_length(start=idx)
        except:
            # issue, maybe the packet is cut even before the data length bit
            return None
        if len(self.blob[idx:]) < HEADERSIZE + length:
            # the packet is cut in the data bits
            return None
        elif self.find(idx=idx+1) == idx+HEADERSIZE+length:
            return slice(idx, idx+HEADERSIZE+length)
        elif len(self.blob[idx:]) == HEADERSIZE+length:
            return slice(idx, idx+HEADERSIZE+length)
        else:
            return self.find_first_packet(idx=idx+1)

    def grab_first_packet(self, idx=0):
        """
        Finds and returns the first valid packet, as str

        Args:
        * idx (int): from where the search should start
        """
        sl = self.find_first_packet(idx=idx)
        if sl is not None:
            return CCSDS(self.blob[sl])
        else:
            return None
