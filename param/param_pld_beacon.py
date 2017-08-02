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


LENGTHBEACONMESSAGE = 29*8  # bits


KEYS = [    dict(   name='message',
                    start=0,
                    l=LENGTHBEACONMESSAGE,
                    fctunpack=bincore.bin2txt,
                    fctpack=bincore.txt2bin,
                    verbose="A beacon message",
                    disp='text'),

            dict(   name='proc_freq',
                    start=LENGTHBEACONMESSAGE+40,
                    l=8,
                    disp="proc_freq",
                    verbose="processor frequency",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),

            dict(   name='phot', 
                    start=LENGTHBEACONMESSAGE, 
                    l=16, 
                    disp="phot",
                    verbose="photometry",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),

            dict(   name='mode', 
                    start=LENGTHBEACONMESSAGE+16, 
                    l=8, 
                    disp="mode",
                    verbose="mode",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),

            dict(   name='acqmode',
                    start=LENGTHBEACONMESSAGE+24,
                    l=8,
                    disp="acqmode",
                    verbose="acquisition mode",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),

            dict(   name='beacon_flag',
                    start=LENGTHBEACONMESSAGE+32,
                    l=1,
                    disp="beacon_flag",
                    verbose="beacon flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            
            dict(   name='cheatmode_flag',
                    start=LENGTHBEACONMESSAGE+33,
                    l=1,
                    disp="cheatmode_flag",
                    verbose="cheatmode flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),

            dict(   name='tec_flag',
                    start=LENGTHBEACONMESSAGE+34,
                    l=1,
                    disp="tec_flag",
                    verbose="tec flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),

            dict(   name='sensors_flag',
                    start=LENGTHBEACONMESSAGE+35,
                    l=1,
                    disp="sensors_flag",
                    verbose="sensors flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),

            dict(   name='hv_flag',
                    start=LENGTHBEACONMESSAGE+36,
                    l=1,
                    disp="hv_flag",
                    verbose="high voltage flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),

            dict(   name='dac_flag',
                    start=LENGTHBEACONMESSAGE+37,
                    l=1,
                    disp="dac_flag",
                    verbose="dac flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),

            dict(   name='interrupt_flag',
                    start=LENGTHBEACONMESSAGE+38,
                    l=1,
                    disp="interrupt_flag",
                    verbose="interrupt flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),

            dict(   name='diode_flag',
                    start=LENGTHBEACONMESSAGE+39,
                    l=1,
                    disp="diode_flag",
                    verbose="diode flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin)
            ]


class PLDBeaconCCSDSTrousseau(CCSDSTrousseau):
    def _make_fmt(self):
        """
        Generates the single-line formatting for later display
        Overriding mother's method
        """
        self.fmt = "%s:{%s}" % (self.keys[0].disp, self.keys[0].name)
        self.fmt += '\n'
        self.fmt += ", ".join(["%s:{%s}" % (key.disp, key.name)\
                                                    for key in self.keys[1:]])


TROUSSEAU = PLDBeaconCCSDSTrousseau(KEYS, octets=False)
