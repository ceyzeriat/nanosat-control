#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .param import *
from .core import *
exc = core.ccsdsexception


__all__ = ['CCSDS']


class CCSDS(object):
    def __init__(self, hx, idx=0):
        self.raise_error = True
        self.hx = hx[int(idx):]
        self.s_header = {}
        self.p_header = {}
        self.data = {}
        # start primary header
        if len(self.hx) < HEADERSIZE:
            exc.raise_it(exc.TruncatedPrimaryHeader, self.raise_error)
            return
        bitstoread = self.hx[:HEADERSIZE]
        dum = "".join([hex2bin(item) for item in bitstoread])
        self.p_header['packet_version'] = PACKETVERSION.grab(dum)
        self.p_header['packet_type'] = PACKETTYPE.grab(dum)
        self.p_header['secondary_header_flag'] = SECONDARYHEADERFLAG.grab(dum)
        self.p_header['apid'] = APID.grab(dum)
        self.p_header['sequence_flag'] = SEQUENCEFLAG.grab(dum)
        self.p_header['name'] = NAME.grab(dum)
        self.p_header['data_length'] = DATALENGTH.grab(dum)
        # start secondary header
        both_headers = HEADERSIZE + HEADERSECSIZE
        if len(self.hx) < both_headers:
            exc.raise_it(exc.TruncatedSecondaryHeader,
                         self.raise_error,
                         name=self.p_header['name'])
            return
        bitstoread = self.hx[HEADERSIZE:both_headers]
        dum = "".join([hex2bin(item) for item in bitstoread])
        self.s_header['extension_flag'] = EXTENSIONFLAG.grab(dum)
        self.s_header['time_code_id'] = TIMECODEID.grab(dum)
        self.s_header['epoch_id'] = EPOCHID.grab(dum)
        self.s_header['length_of_day'] = LENGTHOFDAY.grab(dum)
        self.s_header['length_of_sub_ms'] = LENGTHOFSUBMS.grab(dum)
        self.s_header['days_since_ref'] = DAYSINCEREF.grab(dum)
        self.s_header['msec_since_ref'] = MSECSINCEREF.grab(dum)
        # start data
        tot_length = both_headers + self.p_header['data_length']
        if len(self.hx) < tot_length:
            exc.raise_it(exc.TruncatedData,
                         self.raise_error,
                         name=self.p_header['name'])
            return
        bitstoread = self.hx[both_headers:tot_length]
        self.data[''] = TENSIONLIGNE5V.grab(bitstoread)
        self.data[''] = INTENSITELIGNE5V.grab(bitstoread)
        self.data[''] = INTENSITELIGNE3V.grab(bitstoread)
        self.data[''] = TENSIONPIEZO.grab(bitstoread)
        self.data[''] = INTENSITEPIEZO.grab(bitstoread)
        self.data[''] = TENSIONVITEC.grab(bitstoread)
        self.data[''] = TEMPDIODE.grab(bitstoread)
        self.data[''] = TENSIONERRORTHERM.grab(bitstoread)
        self.data[''] = TENSIONVREF.grab(bitstoread)
        self.data[''] = TEMP1.grab(bitstoread)
        self.data[''] = TEMP2.grab(bitstoread)
        self.data[''] = TEMP3.grab(bitstoread)

