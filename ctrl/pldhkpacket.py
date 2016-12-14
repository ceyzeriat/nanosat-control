#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .ccsds.ccsdskey import CCSDSKey
from .ccsds.ccsdspacket import CCSDSPacket
import .core


class PLDHKPacket(CCSDSPacket):
	def __init__(self):


    def depack_data(self):
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


