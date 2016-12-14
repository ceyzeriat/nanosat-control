#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import param_ccsds
from .. import core
from . import ccsdsexception as exc


__all__ = ['CCSDSPacket']


class CCSDSPacket(object):
    def __init__(self, hx, header_p_keys=None, header_s_keys=None):
        """
        A CCSDS packet to be packed of unpacked.

        Args:
        * hx (hex str): the hex string that corresponds to a packet
        * data_keys (list): list of ``CCSDSKey`` in the packet data
        * header_p_keys (list): list of ``CCSDSKey`` in the primary header.
          Leave to ``None`` for default (recommended).
        * header_s_keys (list): list of ``CCSDSKey`` in the secondary header.
          Leave to ``None`` for default (recommended).
        """
        self.header_p_keys = header_p_keys if header_p_keys is not None\
            else param_ccsds.HEADER_P_KEYS
        self.header_s_keys = header_s_keys if header_p_keys is not None\
            else param_ccsds.HEADER_S_KEYS
        self.data_keys = list(data_keys)
        self.hx = hx
        self.header_p = {}
        self.header_s = {}
        self.data = {}
    
    def depack_header_p(self):
        """
        Depacks the primary header of the packet, fills ``header_p``
        """
        where_we_are = 0
        bits = core.hex2bin(self.blob[:param_ccsds.HEADER_P_SIZE])
        for item in self.header_p_keys:
            if not item.relative_only:
                self.header_p[item.name] = self.grab(bits)
            else:
                self.header_p[item.name] = self.grab(bits,
                                                     rel=True,
                                                     offset=-where_we_are)
            where_we_are += item.len

    def depack_header_s(self):
        """
        Depacks the secondary header of the packet, fills ``header_s``
        """
        where_we_are = 0
        start = param_ccsds.HEADER_P_SIZE
        bits = core.hex2bin(self.blob[start:start+param_ccsds.HEADER_S_SIZE])
        for item in self.header_s_keys:
            if not item.relative_only:
                self.header_p[item.name] = self.grab(bits)
            else:
                self.header_p[item.name] = self.grab(bits,
                                                     rel=True,
                                                     offset=-where_we_are)
            where_we_are += item.len

    def depack_data(self, **kwargs):
        pass

    def depack(self, **kwargs):
        """
        Convenience function that calls successively
        ``depack_header_p``, ``depack_header_s``, and
        ``depack_data`` methods

        Kwargs:
        *  Passed on to ``depack_data``
        """
        self.depack_header_p()
        self.depack_header_s()
        self.depack_data(**kwargs)

    def pack_header_p(self, values):
        """
        Encodes the values into a CCSDS primary header, returns hex string

        Args:
        * values (dict): the values to pack. The keys shall
          correspond to ``HEADER_P_KEYS``
        """
        where_we_are = 0
        # init the long chain of bits to 0
        bits = '0' * (param_ccsds.HEADER_P_SIZE * 8)
        for item in self.header_p_keys:
            if not item.relative_only:
                slc = item.cut
            else:
                slc = item.cut_offset(offset=-where_we_are)
            bits[slc] = item.tobits(values[item.name])
            where_we_are += item.len
        return core.bin2hex(bits)

    def pack_header_s(self, values):
        """
        Encodes the values into a CCSDS primary header, returns hex string        

        Args:
        * values (dict): the values to pack. The keys shall
          correspond to ``HEADER_S_KEYS``
        """
        where_we_are = 0
        # init the long chain of bits to 0
        bits = '0' * (param_ccsds.HEADER_S_SIZE * 8)
        for item in self.header_s_keys:
            if not item.relative_only:
                slc = item.cut
            else:
                slc = item.cut_offset(offset=-where_we_are)
            bits[slc] = item.tobits(values[item.name])
            where_we_are += item.len
        return core.bin2hex(bits)

    def pack_data(self, **kwargs):
        return ''

    def pack(self, values, **kwargs):
        """
        Convenience function that concatenates successively
        ``pack_header_p``, ``pack_header_s``, and
        ``pack_data`` methods outputs, returns hex string

        Args:
        * values (dict): the values to pack. The keys shall
          correspond to ``HEADER_P_KEYS``, ``HEADER_S_KEYS``
          and that of the data.

        Kwargs:
        *  Passed on to ``pack_data``
        """
        return self.pack_header_p(values)\
               + self.pack_header_s(values)\
               + self.pack(value, **kwargs)
