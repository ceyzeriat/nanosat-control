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


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


KEYS = [dict(name='hkErrorFlags', start=0, l=16, fctunpack=bincore.bin2int,
                verbose="hkErrorFlags"),
        dict(name='errorCodes3', start=16, l=16, fctunpack=bincore.bin2int,
                verbose="errorCodes3"),
        dict(name='errorCodes2', start=32, l=16, fctunpack=bincore.bin2int,

                verbose="errorCodes2"),
        dict(name='errorCodes1', start=48, l=16, fctunpack=bincore.bin2int,
                verbose="errorCodes1"),

        dict(name='ant1Undeployed_2', start=66, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant1Undeployed_2"),
        dict(name='ant1Timeout_2', start=67, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant1Timeout_2"),
        dict(name='ant1Deploying_2', start=68, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant1Deploying_2"),
        dict(name='ant2Undeployed_2', start=69, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant2Undeployed_2"),
        dict(name='ant2Timeout_2', start=70, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant2Timeout_2"),
        dict(name='ant2Deploying_2', start=71, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant2Deploying_2"),
        dict(name='ignoreFlag_2', start=72, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ignoreFlag_2"),
        dict(name='ant3Undeployed_2', start=73, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant3Undeployed_2"),
        dict(name='ant3Timeout_2', start=74, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant3Timeout_2"),
        dict(name='ant3Deploying_2', start=75, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant3Deploying_2"),
        dict(name='ant4Undeployed_2', start=76, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant4Undeployed_2"),
        dict(name='ant4Timeout_2', start=77, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant4Timeout_2"),
        dict(name='ant4Deploying_2', start=78, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant4Deploying_2"),
        dict(name='armed_2', start=79, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="armed_2"),

        dict(name='ant1Undeployed_1', start=82, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant1Undeployed_1"),
        dict(name='ant1Timeout_1', start=83, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant1Timeout_1"),
        dict(name='ant1Deploying_1', start=84, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant1Deploying_1"),
        dict(name='ant2Undeployed_1', start=85, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant2Undeployed_1"),
        dict(name='ant2Timeout_1', start=86, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant2Timeout_1"),
        dict(name='ant2Deploying_1', start=87, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant2Deploying_1"),
        dict(name='ignoreFlag_1', start=88, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ignoreFlag_1"),
        dict(name='ant3Undeployed_1', start=89, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant3Undeployed_1"),
        dict(name='ant3Timeout_1', start=90, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant3Timeout_1"),
        dict(name='ant3Deploying_1', start=91, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant3Deploying_1"),
        dict(name='ant4Undeployed_1', start=92, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant4Undeployed_1"),
        dict(name='ant4Timeout_1', start=93, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant4Timeout_1"),
        dict(name='ant4Deploying_1', start=94, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="ant4Deploying_1"),
        dict(name='armed_1', start=95, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin,
                verbose="armed_1"),
        
        dict(name='antsBTemp', start=96, l=16, fctunpack=bincore.bin2int,
                verbose="antsBTemp"),
        dict(name='antsATemp', start=112, l=16, fctunpack=bincore.bin2int,
                verbose="antsATemp"),
        dict(name='TrxvuTxPaTemp', start=128, l=16, fctunpack=bincore.bin2int,
                verbose="TrxvuTxPaTemp"),
        dict(name='TrxvuRxPaTemp', start=144, l=16, fctunpack=bincore.bin2int,
                verbose="TrxvuRxPaTemp"),
        dict(name='TrxvuRxBoardTemp', start=160, l=16, fctunpack=bincore.bin2int,
                verbose="TrxvuRxBoardTemp"),
        dict(name='solarPanelTemp5', start=176, l=32, fctunpack=bincore.bin2int,
                verbose="solarPanelTemp5"),
        dict(name='solarPanelTemp4', start=208, l=32, fctunpack=bincore.bin2int,
                verbose="solarPanelTemp4"),
        dict(name='solarPanelTemp3', start=240, l=32, fctunpack=bincore.bin2int,
                verbose="solarPanelTemp3"),
        dict(name='solarPanelTemp2', start=272, l=32, fctunpack=bincore.bin2int,
                verbose="solarPanelTemp2"),
        dict(name='solarPanelTemp1', start=304, l=32, fctunpack=bincore.bin2int,
                verbose="solarPanelTemp1"),
        dict(name='tempBat2', start=336, l=16, fctunpack=bincore.bin2intSign,
                verbose="tempBat2"),
        dict(name='tempBat1', start=352, l=16, fctunpack=bincore.bin2intSign,
                verbose="tempBat1"),
        dict(name='batMode', start=368, l=8, fctunpack=bincore.bin2intSign,
                verbose="batMode"),
        dict(name='vBat', start=376, l=16, fctunpack=bincore.bin2int,
                verbose="vBat"),
        dict(name='rebootCause', start=392, l=32, fctunpack=bincore.bin2int,
                verbose="rebootCause"),
        dict(name='nReboots', start=424, l=32, fctunpack=bincore.bin2int,
                verbose="nReboots"),
        dict(name='satMode', start=456, l=8, fctunpack=bincore.bin2int,
                verbose="satMode")
        ]


TROUSSEAU = CCSDSTrousseau(KEYS, octets=False)
