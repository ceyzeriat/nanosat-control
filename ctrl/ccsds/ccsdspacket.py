#!/usr/bin/env python
# -*- coding: utf-8 -*-


from . import param_ccsds
from .. import param_apid
from .. import core
from . import ccsdsexception as exc


__all__ = ['CCSDSPacket']


class CCSDSPacket(object):
    def __init__(self, data=None, header_aux={}, packet=''):
        """
        A CCSDS packet to be packed of unpacked.

        Args:
        * 
        * packet (hex str): the hex string that corresponds to a packet
        """
        #self.data_keys = list(data_keys)
        self.packet = str(packet)
        self.header_p = {}
        self.header_s = {}
        #self.data = {}
    
    def depack_header(self, mode='tm'):
        """
        Depacks the primary header of the packet, fills ``header_p``
        """
        # header primaire
        mode = 'telemetry' if str(mode).lower()[1] == 'm' else 'telecommand'
        bits = core.hex2bin(self.packet[:param_ccsds.HEADER_P_SIZE])
        for item in param_ccsds.HEADER_P_KEYS:
            self.header_p[item.name] = self.grab(bits)
        # header secondaire
        if mode == 'telemetry':
            hs = param_ccsds.HEADER_S_KEYS_TELEMETRY
        else:
            hs = param_ccsds.HEADER_S_KEYS_TELECOMMAND
        start = param_ccsds.HEADER_P_SIZE
        bits = core.hex2bin(self.packet[start:start+param_ccsds.HEADER_S_SIZE])
        for item in hs:
            self.header_p[item.name] = self.grab(bits)

    def depack_header_hx(self):
        pass

    def depack_data(self, **kwargs):
        pass

    def depack(self, **kwargs):
        """
        Convenience function that calls successively
        ``depack_header_p``, ``depack_header_s``,
        ``depack_header_hx``, and ``depack_data`` methods

        Kwargs:
        *  Passed on to ``depack_data``
        """
        self.depack_header()
        self.depack_header_hx()
        self.depack_data(**kwargs)

    def _pack_header(self, values, mode='tc'):  # ok
        """
        Encodes the values into a CCSDS primary header, returns hex string

        Args:
        * mode (str): 'tm' or 'tc' for telemetry or telecommand
        * values (dict): the values to pack. The keys shall
          correspond to ``HEADER_P_KEYS``, ``HEADER_S_SIZE_TELEMETRY`` and
          ``HEADER_S_SIZE_TELECOMMAND``
        """
        # PRIMARY HEADER
        mode = 'telemetry' if str(mode).lower()[1] == 'm' else 'telecommand'
        values['packet_type'] = mode
        if mode == 'telecommand':
            values['packet_category'] = '0'
        if 'pid' not in values.keys():
            raise exc.PacketValueMissing('pid')
        values['payload_flag'] = param_apid.PLDREGISTRATION[values['pid']]
        values['level_flag'] = param_apid.LVLREGISTRATION[values['pid']]
        # init the long chain of bits to 0
        bits = '0' * (param_ccsds.HEADER_P_SIZE * 8)
        for item in param_ccsds.HEADER_P_KEYS:
            if item.name not in values.keys() and item.dic_force is None:
                raise exc.PacketValueMissing(item.name)
            bits = core.setstr( bits,
                                item.cut,
                                item.pack(values.get(item.name, '')))
        res = core.bin2hex(bits, pad=param_ccsds.HEADER_P_SIZE)
        # SECONDARY HEADER
        # init the long chain of bits to 0
        if mode == 'telecommand':
            hs = param_ccsds.HEADER_S_KEYS_TELECOMMAND
            hdsz = param_ccsds.HEADER_S_SIZE_TELECOMMAND
            values['signature'] = 0
            values['emitter_id'] = core.EMITTER_ID
        else:
            hs = param_ccsds.HEADER_S_KEYS_TELEMETRY
            hdsz = param_ccsds.HEADER_S_SIZE_TELEMETRY
            values['days_since_ref'] = core.now2daystamp()
            values['ms_since_ref'] = core.now2msstamp()
        bits = '0' * (hdsz * 8)
        for item in hs:
            if item.name not in values.keys() and item.dic_force is None:
                raise exc.PacketValueMissing(item.name)
            bits = core.setstr( bits,
                                item.cut,
                                item.pack(values.get(item.name, '')))
        return res + core.bin2hex(bits, pad=hdsz)

    def pack_header_hx(self, **kwargs):
        return ''

    def pack_data(self, **kwargs):
        return ''

    def pack(self, mode, values, **kwargs):
        """
        Convenience function that concatenates successively
        ``pack_header_p``, ``pack_header_s``, ``pack_header_hx``,
        and ``pack_data`` methods outputs, returns hex string

        Args:
        * values (dict): the values to pack. The keys shall
          correspond to ``HEADER_P_KEYS``, ``HEADER_S_KEYS``
          and that of the data.

        Kwargs:
        *  Passed on to ``pack_data``
        """
        return self.pack_header(mode=mode, values=values)\
               + self.pack_header_hx(mode=mode, values=values, **kwargs)\
               + self.pack_data(mode=mode, values=values, **kwargs)
