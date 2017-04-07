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
    verbose = "(binary -> unsigned integer) * 0.00459"
    """
    return bincore.bin2int(v) * 0.00459


def volt_line_pack(v, pad, **kwargs):
    """
    verbose = "UnsignedInt(float / 0.00459) -> binary"
    """
    return bincore.int2bin(round(v / 0.00459), pad=pad)


def current_line_unpack(v, **kwargs):
    """
    verbose = "(binary -> unsigned integer) * 0.00161"
    """
    return bincore.bin2int(v) * 0.00161


def current_line_pack(v, pad, **kwargs):
    """
    verbose = "UnsignedInt(float / 0.00161) -> binary"
    """
    return bincore.int2bin(round(v / 0.00161), pad=pad)


def volthv_unpack(v, **kwargs):
    """
    verbose = "(binary -> unsigned integer) * 3.3 / 4096 * 213.77"
    """
    return bincore.bin2int(v) * 3.3 / 4096.0 * 213.77


def volthv_pack(v, pad, **kwargs):
    """
    verbose = "UnsignedInt(float / 3.3 * 4096 / 213.77) -> binary"
    """
    return bincore.int2bin(round(v / 3.3 * 4096.0 / 213.77), pad=pad)


def temp_unpack(v, **kwargs):
    """
    verbose = "(binary -> signed integer) * 0.0625"
    """
    return bincore.bin2intSign(v) * 0.0625


def temp_pack(v, pad, **kwargs):
    """
    verbose = "SignedInt(float / 0.0625) -> binary"
    """
    return bincore.intSign2bin(round(v / 0.0625), pad=pad)


def volt_peltier_unpack(v, **kwargs):
    """
    verbose = "(binary -> unsigned integer) * 3.3 / 4096"
    """
    return bincore.bin2int(v) * 3.3 / 4096.0


def volt_peltier_pack(v, pad, **kwargs):
    """
    verbose = "UnsignedInt(float / 3.3 * 4096.0) -> binary"
    """
    return bincore.int2bin(round(v / 3.3 * 4096), pad=pad)


def vitec_unpack(v, Vref, **kwargs):
    """
    verbose = "((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 0.00016"
    """
    if Vref == 0:
        Vref = 1
    return (bincore.bin2int(v) * 3.3 / 4096.0 - Vref) / 0.00016


def vitec_pack(v, Vref, pad, **kwargs):
    """
    verbose = "UnsignedInt((float * 0.00016 + Vref) * 4096 / 3.3) -> binary"
    """
    if Vref == 0:
        Vref = 1
    return bincore.int2bin(round((v * 0.00016 + Vref) * 4096 / 3.3), pad=pad)


def errortherm_unpack(v, Vref, **kwargs):
    """
    verbose = "((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 25"
    """
    if Vref == 0:
        Vref = 1
    return (bincore.bin2int(v) * 3.3 / 4096.0 - Vref) / 25


def errortherm_pack(v, Vref, pad, **kwargs):
    """
    verbose = "UnsignedInt((float * 25 + Vref) * 4096 / 3.3) -> binary"
    """
    if Vref == 0:
        Vref = 1
    return bincore.int2bin(round((v * 25 + Vref) * 4096 / 3.3), pad=pad)


def temp0_unpack(v, Vref, **kwargs):
    """
    verbose = "293 / (293 / 2918.9 * LOG(50 / 11 * (binary -> unsigned integer) / (Voltage Peltier / 3.3 * 4096 - (binary -> unsigned integer))) + 1) - 273"
    """
    if Vref == 0:
        Vref = 1
    X = bincore.bin2int(v)
    return 293 / (293 / 2918.9\
                    * math.log(50 / 11.0 * X / (Vref / 3.3 * 4096 - X)) + 1) - 273


def temp0_pack(v, Vref, pad, **kwargs):
    """
    verbose = "UnsignedInt((Voltage Peltier / 3.3 * 4096) / (1 + 50 / (11 * math.exp(2918.9 / 293 * (293 / (float + 273.0) - 1))))) -> binary"
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

V_KEYS = [  dict(name='volt5', start=16, l=16, disp="volt5",
                    verbose="Voltage line 5V,",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=volt_line_unpack, fctpack=volt_line_pack),
            dict(name='amp5', start=32, l=16, disp="amp5",
                    verbose="amp5",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='amp3', start=48, l=16, disp="amp3",
                    verbose="amp3",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='volthv', start=64, l=16, disp="volthv",
                    verbose="volthv",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=volthv_unpack, fctpack=volthv_pack),
            dict(name='amphv', start=80, l=16, disp="amphv",
                    verbose="amphv",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name=VOLTPELTIER, start=144, l=16, disp=VOLTPELTIER,
                    verbose="vref",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=volt_peltier_unpack, fctpack=volt_peltier_pack),
            dict(name='vitec', start=96, l=16, disp="vitec",
                    verbose="vitec",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=vitec_unpack, fctpack=vitec_pack),
            dict(name='temp0', start=112, l=16, disp="temp0",
                    verbose="temp0",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=temp0_unpack, fctpack=temp0_pack),
            dict(name='errortherm', start=128, l=16, disp="errortherm",
                    verbose="errortherm",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),#fctunpack=errortherm_unpack, fctpack=errortherm_pack),
            dict(name='temp1', start=160, l=16, disp="temp1",
                    verbose="temp1",
                    fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin),#fctunpack=temp_unpack, fctpack=temp_pack),
            dict(name='temp2', start=176, l=16, disp="temp2",
                    verbose="temp2",
                    fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin),#fctunpack=temp_unpack, fctpack=temp_pack),
            dict(name='temp3', start=192, l=16, disp="temp3",
                    verbose="temp3",
                    fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin)#fctunpack=temp_unpack, fctpack=temp_pack)
            ]


# names will be filled in automatically afterwards
F_KEYS = [  dict(name='-', start=4, l=1, disp="",
                    verbose="Voltage line 5V, measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=5, l=1, disp="",
                    verbose="amp5 measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=6, l=1, disp="",
                    verbose="amp3 measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=7, l=1, disp="",
                    verbose="volthv measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=8, l=1, disp="",
                    verbose="amphv measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=9, l=1, disp="",
                    verbose="vref measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=10, l=1, disp="",
                    verbose="vitec measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=11, l=1, disp="",
                    verbose="temp0 measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=12, l=1, disp="",
                    verbose="errortherm measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=13, l=1, disp="",
                    verbose="temp1 measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=14, l=1, disp="",
                    verbose="temp2 measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=15, l=1, disp="",
                    verbose="temp3 measurement flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin)
            ]


O_KEYS = [  dict(name='proc_freq', start=248, l=8, disp="proc_freq",
                    verbose="proc_freq",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='phot', start=208, l=16, disp="phot",
                    verbose="phot",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='mode', start=224, l=8, disp="mode",
                    verbose="mode",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='acqmode', start=232, l=8, disp="acqmode",
                    verbose="acqmode",
                    fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='beacon_flag', start=241, l=1, disp="beacon_flag",
                    verbose="beacon_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='tec_flag', start=242, l=1, disp="tec_flag",
                    verbose="tec_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='sensors_flag', start=243, l=1, disp="sensors_flag",
                    verbose="sensors_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='hv_flag', start=244, l=1, disp="hv_flag",
                    verbose="hv_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='dac_flag', start=245, l=1, disp="dac_flag",
                    verbose="dac_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='interrupt_flag', start=246, l=1, disp="interrupt_flag",
                    verbose="interrupt_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='diode_flag', start=247, l=1, disp="diode_flag",
                    verbose="diode_flag",
                    fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin)
            ]


# fill in names for flags
def value_to_flag_name(txt):
    return 'f_'+txt


for idx, item in enumerate(V_KEYS):
    F_KEYS[idx]['name'] = value_to_flag_name(item['name'])


class HKPayloadCCSDSTrousseau(CCSDSTrousseau):
    def make_fmt(self):
        """
        Generates the single-line formatting for later display
        Overriding mother's method
        """
        self.fmt = ", ".join(["%s:({%s}){%s}" % (key['disp'],
                                value_to_flag_name(key['name']), key['name'])\
                                    for key in V_KEYS])
        self.fmt += '\n'
        self.fmt += ", ".join(["%s:{%s}" % (key['disp'], key['name']) for key in O_KEYS])
        

    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the HK Payload packets
        Overriding mother's method

        Args:
        * data (byts): the chain of octets to unpack
        """
        nlines = len(data) // self.size
        lines = [{}] * nlines
        for idx in range(nlines):
            lines[idx][VOLTPELTIER] = 0
            dt = data[idx*self.size:(idx+1)*self.size]
            # octets is False
            dt = bincore.hex2bin(dt[:self.size])
            # if octets were True: dt = dt[:self.size]
            for item in self.keys:
                lines[idx][item.name] = item.unpack(
                                            dt,
                                            Vref=lines[idx][VOLTPELTIER])
            for item in V_KEYS:
                v_key = item['name']
                f_key = value_to_flag_name(v_key)
                if not lines[idx][f_key]:
                    lines[idx][v_key] = 0.
        return lines

    def disp(self, data):
        """
        Display the data values of the payload hk
        Overriding mother's method

        Args:
          * data (list of dict): a list of dictionaries containing the
            values to display
        """
        res = [super(HKPayloadCCSDSTrousseau, self).disp(line)\
                    for line in data]
        return "\n".join(res)

    def pack(self, allvalues, **kwargs):
        """
        Packs the values into a HK Payload packet
        Overriding mother's method

        Args:
        * allvalues (dict): the values to pack
        """
        Vref = allvalues[VOLTPELTIER]
        return Super(HKPayloadCCSDSTrousseau, self).\
                        pack(allvalues, retdbvalues=True, Vref=Vref)


TROUSSEAU = HKPayloadCCSDSTrousseau(F_KEYS + V_KEYS + O_KEYS, octets=False)
