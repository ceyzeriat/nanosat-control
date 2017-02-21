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


from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.utils import core


__all__ = ['KEYS', 'KEYSSIZE', 'unpack', 'disp']


KEYS = [CCSDSKey(name='hkErrorFlags', start=0, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='errorCodes3', start=16, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='errorCodes2', start=32, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='errorCodes1', start=48, l=16, fctunpack=core.bin2int),

        CCSDSKey(name='ant1Undeployed_2', start=66, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant1Timeout_2', start=67, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant1Deploying_2', start=68, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant2Undeployed_2', start=69, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant2Timeout_2', start=70, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant2Deploying_2', start=71, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ignoreFlag_2', start=72, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant3Undeployed_2', start=73, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant3Timeout_2', start=74, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant3Deploying_2', start=75, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant4Undeployed_2', start=76, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant4Timeout_2', start=77, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant4Deploying_2', start=78, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='armed_2', start=79, l=1, fctunpack=core.bin2int),

        CCSDSKey(name='ant1Undeployed_1', start=82, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant1Timeout_1', start=83, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant1Deploying_1', start=84, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant2Undeployed_1', start=85, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant2Timeout_1', start=86, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant2Deploying_1', start=87, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ignoreFlag_1', start=88, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant3Undeployed_1', start=89, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant3Timeout_1', start=90, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant3Deploying_1', start=91, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant4Undeployed_1', start=92, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant4Timeout_1', start=93, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='ant4Deploying_1', start=94, l=1, fctunpack=core.bin2int),
        CCSDSKey(name='armed_1', start=95, l=1, fctunpack=core.bin2int),
        
        CCSDSKey(name='antsBTemp', start=96, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='antsATemp', start=112, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='TrxvuTxPaTemp', start=128, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='TrxvuRxPaTemp', start=144, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='TrxvuRxBoardTemp', start=160, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='solarPanelTemp5', start=176, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='solarPanelTemp4', start=208, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='solarPanelTemp3', start=240, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='solarPanelTemp2', start=272, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='solarPanelTemp1', start=304, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='tempBat2', start=336, l=16, fctunpack=core.bin2intSign),
        CCSDSKey(name='tempBat1', start=352, l=16, fctunpack=core.bin2intSign),
        CCSDSKey(name='batMode', start=368, l=8, fctunpack=core.bin2intSign),
        CCSDSKey(name='vBat', start=376, l=16, fctunpack=core.bin2int),
        CCSDSKey(name='rebootCause', start=392, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='nReboots', start=424, l=32, fctunpack=core.bin2int),
        CCSDSKey(name='satMode', start=456, l=8, fctunpack=core.bin2int)
        ]


KEYSSIZE = sum([item.len for item in KEYS])


def unpack(data):
    """
    Unpacks the data contained in the Beacon packets

    Args:
    * data: the chain of octets to unpack
    """
    data = core.hex2bin(data, pad=len(data)*8)
    res = {}
    for key in KEYS:
        res[key.name] = key.unpack(data)
    return res


def disp(*args):
    pass
