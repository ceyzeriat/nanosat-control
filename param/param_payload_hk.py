#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 202-2017  Guillaume Schworer
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


import math
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.ccsds import ccsdsexception
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


def volt_line_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = (binary -> unsigned integer) * 0.00459
    """
    return bincore.bin2int(v) * 0.00459


def volt_line_pack(v, pad, **kwargs):
    """
    verbose = UnsignedInt(float / 0.00459) -> binary
    """
    return bincore.int2bin(round(v / 0.00459), pad=pad)


def current_line_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = (binary -> unsigned integer) * 0.00161
    """
    return bincore.bin2int(v) * 0.00161


def current_line_pack(v, pad, **kwargs):
    """
    verbose = UnsignedInt(float / 0.00161) -> binary
    """
    return bincore.int2bin(round(v / 0.00161), pad=pad)


def volthv_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = (binary -> unsigned integer) * 3.3 / 4096 * 213.77
    """
    return bincore.bin2int(v) * 3.3 / 4096.0 * 213.77


def volthv_pack(v, pad, **kwargs):
    """
    verbose = UnsignedInt(float / 3.3 * 4096 / 213.77) -> binary
    """
    return bincore.int2bin(round(v / 3.3 * 4096.0 / 213.77), pad=pad)


def temp_unpack(v, **kwargs):
    """
    type = signed integer
    verbose = (binary -> signed integer) * 0.0625
    """
    return bincore.bin2intSign(v) * 0.0625


def temp_pack(v, pad, **kwargs):
    """
    verbose = SignedInt(float / 0.0625) -> binary
    """
    return bincore.intSign2bin(round(v / 0.0625), pad=pad)


def volt_peltier_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = (binary -> unsigned integer) * 3.3 / 4096
    """
    return bincore.bin2int(v) * 3.3 / 4096.0


def volt_peltier_pack(v, pad, **kwargs):
    """
    verbose = UnsignedInt(float / 3.3 * 4096.0) -> binary
    """
    return bincore.int2bin(round(v / 3.3 * 4096), pad=pad)


def vitec_unpack(v, Vref, **kwargs):
    """
    type = unsigned integer
    verbose = ((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 0.00016
    """
    if Vref == 0:
        Vref = 1
    return (bincore.bin2int(v) * 3.3 / 4096.0 - Vref) / 0.00016


def vitec_pack(v, Vref, pad, **kwargs):
    """
    verbose = UnsignedInt((float * 0.00016 + Vref) * 4096 / 3.3) -> binary
    """
    if Vref == 0:
        Vref = 1
    return bincore.int2bin(round((v * 0.00016 + Vref) * 4096 / 3.3), pad=pad)


def errortherm_unpack(v, Vref, **kwargs):
    """
    type = unsigned integer
    verbose = ((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 25
    """
    if Vref == 0:
        Vref = 1
    return (bincore.bin2int(v) * 3.3 / 4096.0 - Vref) / 25


def errortherm_pack(v, Vref, pad, **kwargs):
    """
    verbose = UnsignedInt((float * 25 + Vref) * 4096 / 3.3) -> binary
    """
    if Vref == 0:
        Vref = 1
    return bincore.int2bin(round((v * 25 + Vref) * 4096 / 3.3), pad=pad)


def temp0_unpack(v, Vref, **kwargs):
    """
    type = unsigned integer
    verbose = 293 / (293 / 2918.9 * LOG(50 / 11 * (binary -> unsigned integer) / (Voltage Peltier / 3.3 * 4096 - (binary -> unsigned integer))) + 1) - 273
    """
    if Vref == 0:
        Vref = 1
    X = bincore.bin2int(v)
    return 293 / (293 / 2918.9\
                    * math.log(50 / 11.0 * X / (Vref / 3.3 * 4096 - X)) + 1) - 273


def temp0_pack(v, Vref, pad, **kwargs):
    """
    verbose = UnsignedInt((Voltage Peltier / 3.3 * 4096) / (1 + 50 / (11 * math.exp(2918.9 / 293 * (293 / (float + 273.0) - 1))))) -> binary
    """
    if Vref == 0:
        Vref = 1
    return bincore.int2bin(round(
                            (Vref / 3.3 * 4096) /\
                            (1 + 50 /\
                                (11 * math.exp(2918.9 / 293.0 *\
                                                (293 / (v + 273.0) - 1))))),
                           pad=pad)


VOLTPELTIER = 'vref'

# put VOLTPELTRIER first because you'll need it t unpack other values
KEYS = [  dict(name=VOLTPELTIER, start=16, l=2, disp=VOLTPELTIER,
                    verbose="vref",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=volt_peltier_unpack, fctpack=volt_peltier_pack),
            dict(name='volt5', start=0, l=2, disp="volt5",
                    verbose="Voltage line 5V,",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=volt_line_unpack, fctpack=volt_line_pack),
            dict(name='amp5', start=2, l=2, disp="amp5",
                    verbose="amp5",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='amp3', start=4, l=2, disp="amp3",
                    verbose="amp3",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='volthv', start=6, l=2, disp="volthv",
                    verbose="volthv",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=volthv_unpack, fctpack=volthv_pack),
            dict(name='amphv', start=8, l=2, disp="amphv",
                    verbose="amphv",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='vitec', start=10, l=2, disp="vitec",
                    verbose="vitec",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=vitec_unpack, fctpack=vitec_pack),
            dict(name='temp0', start=12, l=2, disp="temp0",
                    verbose="temp0",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=temp0_unpack, fctpack=temp0_pack),
            dict(name='errortherm', start=14, l=2, disp="errortherm",
                    verbose="errortherm",
                    fctunpack=bincore.hex2int, fctpack=bincore.int2hex),#fctunpack=errortherm_unpack, fctpack=errortherm_pack),
            dict(name='temp1', start=18, l=2, disp="temp1",
                    verbose="temp1",
                    fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex),#fctunpack=temp_unpack, fctpack=temp_pack),
            dict(name='temp2', start=20, l=2, disp="temp2",
                    verbose="temp2",
                    fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex),#fctunpack=temp_unpack, fctpack=temp_pack),
            dict(name='temp3', start=22, l=2, disp="temp3",
                    verbose="temp3",
                    fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex),#fctunpack=temp_unpack, fctpack=temp_pack)
            dict(name='temp4', start=24, l=2, disp="temp4",
                    verbose="temp4",
                    fctunpack=bincore.hex2intSign, fctpack=bincore.intSign2hex)#fctunpack=temp_unpack, fctpack=temp_pack)            
            ]

class HKPayloadCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the HK Payload packets
        Overriding mother's method

        Args:
        * data (byts): the chain of octets to unpack
        """
        # size and data in octets
        nlines = len(data) // self.size
        lines = [{} for i in range(nlines)]
        for idx in range(nlines):
            lines[idx][VOLTPELTIER] = 0
            dt = data[idx*self.size:(idx+1)*self.size]
            # if octets were False:
            #dt = bincore.hex2bin(dt[:self.size])
            for item in self.keys:
                lines[idx][item.name] = item.unpack(
                                            dt,
                                            Vref=lines[idx][VOLTPELTIER])
        return lines

    def pack(self, allvalues, **kwargs):
        """
        Packs the values into a HK Payload packet
        Overriding mother's method

        Args:
        * allvalues (dict): the values to pack
        """
        pass


TROUSSEAU = HKPayloadCCSDSTrousseau(KEYS, octets=True, listof=True)
