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


from ctrl.ccsds.ccsdsmetatrousseau import CCSDSMetaTrousseau
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.utils import bincore



__all__ = ['TROUSSEAU']


TROUSSEAUDIC = {1: CCSDSTrousseau([CCSDSKey(name='message', start=0, l=10, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='message',)], octets=True),
                4: CCSDSTrousseau([CCSDSKey(name='time', start=0, l=4, fctunpack=bincore.hex2int, fctpack=bincore.int2hex, verbose='none', disp='time',)], octets=True),
                5: CCSDSTrousseau([CCSDSKey(name='time', start=0, l=4, fctunpack=bincore.hex2int, fctpack=bincore.int2hex, verbose='none', disp='time',)], octets=True),
                6: CCSDSTrousseau([CCSDSKey(name='count', start=0, l=2, fctunpack=bincore.hex2int, fctpack=bincore.int2hex, verbose='none', disp='count',)], octets=True),
                7: CCSDSTrousseau([CCSDSKey(name='temp1', start=0, l=2, fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex, verbose='none', disp='temp1',),
                                   CCSDSKey(name='temp2', start=2, l=2, fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex, verbose='none', disp='temp2',),
                                   CCSDSKey(name='temp3', start=4, l=2, fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex, verbose='none', disp='temp3',),
                                   CCSDSKey(name='temp4', start=6, l=2, fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex, verbose='none', disp='temp4',),
                                   CCSDSKey(name='temp5', start=8, l=2, fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex, verbose='none', disp='temp5',)], octets=True),
                11: CCSDSTrousseau([CCSDSKey(name='data', start=0, l=255, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='data', pad=False)], octets=True),
                17: CCSDSTrousseau([CCSDSKey(name='data', start=0, l=255, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='data', pad=False)], octets=True),
                17: CCSDSTrousseau([CCSDSKey(name='data', start=0, l=255, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='data', pad=False)], octets=True),
                48: CCSDSTrousseau([CCSDSKey(name='crc', start=0, l=4, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='crc',)], octets=True),
                49: CCSDSTrousseau([CCSDSKey(name='crc', start=0, l=4, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='crc',)], octets=True),
                50: CCSDSTrousseau([CCSDSKey(name='crc', start=0, l=4, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='crc',)], octets=True),
                51: CCSDSTrousseau([CCSDSKey(name='crc', start=0, l=4, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='crc',)], octets=True),
                52: CCSDSTrousseau([CCSDSKey(name='crc', start=0, l=4, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='crc',)], octets=True),
                55: CCSDSTrousseau([CCSDSKey(name='crc', start=0, l=4, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='crc',)], octets=True),
                63: CCSDSTrousseau([CCSDSKey(name='patchState', start=0, l=1, fctunpack=bincore.hex2int, fctpack=bincore.int2hex, verbose='none', disp='patchState',)], octets=True),
                81: CCSDSTrousseau([CCSDSKey(name='i2cReply', start=0, l=255, fctunpack=bincore.hex2hex, fctpack=bincore.hex2hex, verbose='none', disp='i2cReply', pad=False)], octets=True),
                82: CCSDSTrousseau([CCSDSKey(name='adcsMode', start=0, l=4, fctunpack=bincore.hex2int, fctpack=bincore.int2hex, verbose='none', disp='adcsMode',)], octets=True),


#PAYLOAD BOOTLOADER
                246: CCSDSTrousseau([CCSDSKey(name='values', start=0, l=255, fctunpack=bincore.hex2str, fctpack=bincore.str2hex, verbose='none', disp='values', pad = False)], octets=True),
                248: CCSDSTrousseau([CCSDSKey(name='message', start=0, l=255, fctunpack=bincore.hex2str, fctpack=bincore.str2hex, verbose='none', disp='msg', pad = False)], octets=True),
                250: CCSDSTrousseau([CCSDSKey(name='flashBytes', start=0, l=255, fctunpack=bincore.hex2str, fctpack=bincore.str2hex, verbose='none', disp='flashBytes', pad = False)], octets=True)
}


TROUSSEAU = CCSDSMetaTrousseau(TROUSSEAUDIC, key='telecommand_id_mirror')
