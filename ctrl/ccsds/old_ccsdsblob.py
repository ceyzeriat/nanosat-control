#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import param_ccsds
from .. import core
from . import ccsdsexception as exc
from .. import param_apid


__all__ = ['CCSDSBlob']


class CCSDSBlob(object):
    def __init__(self, blob, packet_type, secondary_header_flag=1):
        """
        Analyzes a blob of bits to find the first valid packet
        These 4 packet-related parameters are used as assumptions
        to parse and validate the packet

        Args:
        * blob (str): the '\x00\xf0...' string
        * packet_type: 'telemetry' or 'telecommand'
        * secondary_header_flag: 1
        """
        self.blob = blob
        self.param = {}
        self.param['pt'] = packet_type
        self.param['shf'] = int(bool(secondary_header_flag))
        # building of possible packet start flags
        self.auth_first_octets = []
        for item in param_apid.APIDREGISTRATION.values():
            dum = param_ccsds.PACKETVERSION[param_ccsds.PACKETVERSION_VALUE]\
                  + param_ccsds.PACKETTYPE[self.param['pt']]\
                  + param_ccsds.SECONDARYHEADERFLAG[self.param['shf']]\
                  + item
            self.auth_first_octets.append(core.bin2hex(dum))

    def find(self, start=0):
        """
        Finds the possible start of a packet in the blob.
        Returns the index of the start or None if not found
        Does not check the validity, see ``find_first``

        Args:
        * start (int): from where the search should start
        """
        for i in range(len(self.blob[start:])):
            if self.blob[start+i:start+i+2] in self.auth_first_octets:
                return i
        else:
            return None

    def grab_data_length(self, start):
        """
        Returns the data-lengh as int, contained in the header of the
        packet

        Args:
        * start (int): the first bit of the packet in the blob
        """
        dum = core.hex2bin(self.blob[start:start+param_ccsds.HEADER_P_SIZE])
        return param_ccsds.DATALENGTH.grab(dum)

    def find_first_packet(self, start=0):
        """
        Finds the first valid packet, assuming the packet
        parameters provided at initialization.
        Returns a slice, or ``None`` if no valid packet found

        Args:
        * start (int): from where the search should start
        """
        start += self.find(start=start)
        if start is None:
            return None
        else:
            try:
                length = self.grab_data_length(start=start)
            except:
                # issue, maybe the packet is cut before the data length bit
                return None
            # bullshit length, just restart search further
            if length < param_ccsds.HEADER_P_SIZE:
                return self.find_first(start=start+1)
            # bang on, found a new start where you expected it
            elif self.find(start=start+param_ccsds.HEADER_P_SIZE+length) == 0:
                return slice(start, start + param_ccsds.HEADER_P_SIZE + length)
            # try again
            else:
                return self.find_first(start=start+1)

    def grab_first_packet(self, start=0):
        """
        """
        slc = self.find_first_packet(start=start)
        if slc is None:
            return None
        else:
            return self.hx[slc]