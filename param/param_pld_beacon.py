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
from ctrl.utils import b
from ctrl.utils import O


__all__ = ['TROUSSEAU']


LENGTHBEACONMESSAGE = 29*O


KEYS = [    dict(   name='message',
                    start=0*O,
                    l=LENGTHBEACONMESSAGE,
                    typ='text',
                    verbose="A beacon message",
                    disp='text'),

            dict(   name='phot', 
                    start=LENGTHBEACONMESSAGE, 
                    l=2*O, 
                    disp="phot",
                    verbose="photometry",
                    typ='uint'),

            dict(   name='mode', 
                    start=LENGTHBEACONMESSAGE+2*O,
                    l=1*O, 
                    disp="mode",
                    verbose="mode",
                    typ='uint'),

            dict(   name='acqmode',
                    start=LENGTHBEACONMESSAGE+3*O,
                    l=1*O,
                    disp="acqmode",
                    verbose="acquisition mode",
                    typ='uint'),

            dict(   name='proc_freq',
                    start=LENGTHBEACONMESSAGE+5*O,
                    l=1*O,
                    disp="proc_freq",
                    verbose="processor frequency",
                    typ='uint'),

            dict(   name='beacon_flag',
                    start=LENGTHBEACONMESSAGE+4*O,
                    l=1*b,
                    disp="beacon_flag",
                    verbose="beacon flag",
                    typ='bool'),
            
            dict(   name='cheatmode_flag',
                    start=LENGTHBEACONMESSAGE+4*O+1*b,
                    l=1*b,
                    disp="cheatmode_flag",
                    verbose="cheatmode flag",
                    typ='bool'),

            dict(   name='tec_flag',
                    start=LENGTHBEACONMESSAGE+4*O+2*b,
                    l=1*b,
                    disp="tec_flag",
                    verbose="tec flag",
                    typ='bool'),

            dict(   name='sensors_flag',
                    start=LENGTHBEACONMESSAGE+4*O+3*b,
                    l=1*b,
                    disp="sensors_flag",
                    verbose="sensors flag",
                    typ='bool'),

            dict(   name='hv_flag',
                    start=LENGTHBEACONMESSAGE+4*O+4*b,
                    l=1*b,
                    disp="hv_flag",
                    verbose="high voltage flag",
                    typ='bool'),

            dict(   name='dac_flag',
                    start=LENGTHBEACONMESSAGE+4*O+5*b,
                    l=1*b,
                    disp="dac_flag",
                    verbose="dac flag",
                    typ='bool'),

            dict(   name='interrupt_flag',
                    start=LENGTHBEACONMESSAGE+4*O+6*b,
                    l=1*b,
                    disp="interrupt_flag",
                    verbose="interrupt flag",
                    typ='bool'),

            dict(   name='diode_flag',
                    start=LENGTHBEACONMESSAGE+4*O+7*b,
                    l=1*b,
                    disp="diode_flag",
                    verbose="diode flag",
                    typ='bool')
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


TROUSSEAU = PLDBeaconCCSDSTrousseau(KEYS)
