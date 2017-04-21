#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 2016-2017  Guillaume Schworer
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
#  For any information, bug report, idea, donation, hug, beer, please contact
#    guillaume.schworer@gmail.com
#
###############################################################################


from byt import Byt
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore

__all__ = ['TROUSSEAU']


MAXLENGTHBEACONMESSAGE = 29  # octets


def hex2txt(v, **kwargs):
    """
    verbose = "binary -> message"
    """
    return ''.join([chr(i) for i in Byt(v).ints() if i >= 32 and i <= 126])


def txt2hex(txt, **kwargs):
    """
    verbose = "message -> binary"
    """
    return Byt([i for i in Byt(txt).ints() if i >= 32 and i <= 126])


KEYS = [    dict(name='message', start=0, l=MAXLENGTHBEACONMESSAGE, fctunpack=hex2txt, fctpack=txt2hex,
                    verbose="A beacon message",
                    disp='text', pad=False, octets=True),
            dict(name='proc_freq', start=MAXLENGTHBEACONMESSAGE*8+40, l=8, disp="proc_freq",
                    verbose="processor frequency",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=temp_unpack, fctpack=temp_pack)                        
            dict(name='phot', start=MAXLENGTHBEACONMESSAGE*8, l=16, disp="phot",
                    verbose="photometry",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='mode', start=MAXLENGTHBEACONMESSAGE*8+16, l=8, disp="mode",
                    verbose="mode",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='acqmode', start=MAXLENGTHBEACONMESSAGE*8+24, l=8, disp="acqmode",
                    verbose="acquisition mode",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='beacon_flag', start=MAXLENGTHBEACONMESSAGE*8+33, l=1, disp="beacon_flag",
                    verbose="beacon flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),#fctunpack=temp_unpack, fctpack=temp_pack)                                    
            dict(name='tec_flag', start=MAXLENGTHBEACONMESSAGE*8+34, l=1, disp="tec_flag",
                    verbose="tec flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),#fctunpack=temp_unpack, fctpack=temp_pack)                                    
            dict(name='sensors_flag', start=MAXLENGTHBEACONMESSAGE*8+35, l=1, disp="sensors_flag",
                    verbose="sensors flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='hv_flag', start=MAXLENGTHBEACONMESSAGE*8+36, l=1, disp="hv_flag",
                    verbose="high voltage flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),#fctunpack=temp_unpack, fctpack=temp_pack)            
            dict(name='dac_flag', start=MAXLENGTHBEACONMESSAGE*8+37, l=1, disp="dac_flag",
                    verbose="dac flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='interrupt_flag', start=MAXLENGTHBEACONMESSAGE*8+38, l=1, disp="interrupt_flag",
                    verbose="interrupt flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='diode_flag', start=MAXLENGTHBEACONMESSAGE*8+39, l=1, disp="diode_flag",
                    verbose="diode flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin)#fctunpack=temp_unpack, fctpack=temp_pack)
            ]


class PLDBeaconCCSDSTrousseau(CCSDSTrousseau):
    def make_fmt(self):
        """
        Generates the single-line formatting for later display
        Overriding mother's method
        """
        self.fmt = "%s:{%s}" % (KEYS[0]['disp'], KEYS[0]['name'])
        self.fmt += '\n'
        self.fmt += ", ".join(["%s:{%s}" % (key['disp'], key['name']) for key in KEYS[1:]])


TROUSSEAU = PLDBeaconCCSDSTrousseau(KEYS, octets=False)
