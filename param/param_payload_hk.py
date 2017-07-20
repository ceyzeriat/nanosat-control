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
from ctrl.utils import b
from ctrl.utils import O


__all__ = ['TROUSSEAU']


def volt_line_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = x * 0.00459
    """
    return v * 0.00459


def current_line_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = x * 0.00161
    """
    return v * 0.00161


def volthv_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = x * 3.3 / 4096 * 213.77
    """
    return v * 3.3 / 4096.0 * 213.77


def temp_unpack(v, **kwargs):
    """
    type = signed integer
    verbose = x * 0.0625
    """
    return v * 0.0625


def volt_peltier_unpack(v, **kwargs):
    """
    type = unsigned integer
    verbose = x * 3.3 / 4096
    """
    return v * 3.3 / 4096.0


def vitec_unpack(v, Vref, **kwargs):
    """
    type = unsigned integer
    verbose = ((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 0.00016
    """
    if Vref == 0:
        Vref = 1
    return (v * 3.3 / 4096.0 - Vref) / 0.00016


def vitec_pack(v, Vref, pad, **kwargs):
    """
    verbose = UnsignedInt((float * 0.00016 + Vref) * 4096 / 3.3) -> binary
    """
    if Vref == 0:
        Vref = 1
    return (v * 0.00016 + Vref) * 4096 / 3.3


def errortherm_unpack(v, Vref, **kwargs):
    """
    type = unsigned integer
    verbose = ((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 25
    """
    if Vref == 0:
        Vref = 1
    return (v * 3.3 / 4096.0 - Vref) / 25


def errortherm_pack(v, Vref, pad, **kwargs):
    """
    verbose = UnsignedInt((float * 25 + Vref) * 4096 / 3.3) -> binary
    """
    if Vref == 0:
        Vref = 1
    return (v * 25 + Vref) * 4096 / 3.3


def temp0_unpack(v, Vref, **kwargs):
    """
    type = unsigned integer
    verbose = 293 / (293 / 2918.9 * LOG(50 / 11 * (binary -> unsigned integer) / (Voltage Peltier / 3.3 * 4096 - (binary -> unsigned integer))) + 1) - 273
    """
    if Vref == 0:
        Vref = 1
    X = v
    return 293 / (293 / 2918.9\
                    * math.log(50 / 11.0 * X / (Vref / 3.3 * 4096 - X)) + 1) - 273


def temp0_pack(v, Vref, pad, **kwargs):
    """
    verbose = UnsignedInt((Voltage Peltier / 3.3 * 4096) / (1 + 50 / (11 * math.exp(2918.9 / 293 * (293 / (float + 273.0) - 1))))) -> binary
    """
    if Vref == 0:
        Vref = 1
    return (Vref / 3.3 * 4096) / (1 + 50 /\
                    (11 * math.exp(2918.9 / 293.0 *\
                                    (293 / (v + 273.0) - 1))))


VOLTPELTIER = 'vref'

# put VOLTPELTRIER first because you'll need it t unpack other values
KEYS = [  dict(name=VOLTPELTIER,
                start=16*O,
                l=2*O,
                disp=VOLTPELTIER,
                verbose="vref",
                typ='uint',
                fctunram=volt_peltier_unpack),
            dict(name='volt5',
                start=0*O,
                l=2*O,
                disp="volt5",
                verbose="Voltage line 5V,",
                typ='uint',
                fctunram=volt_line_unpack),
            dict(name='amp5',
                start=2*O,
                l=2*O,
                disp="amp5",
                verbose="amp5",
                typ='uint',
                fctunram=current_line_unpack),
            dict(name='amp3',
                start=4*O,
                l=2*O,
                disp="amp3",
                verbose="amp3",
                typ='uint',
                fctunram=current_line_unpack),
            dict(name='volthv',
                start=6*O,
                l=2*O,
                disp="volthv",
                verbose="volthv",
                typ='uint',
                fctunram=volthv_unpack),
            dict(name='amphv',
                start=8*O,
                l=2*O,
                disp="amphv",
                verbose="amphv",
                typ='uint',
                fctunram=current_line_unpack),
            dict(name='vitec',
                start=10*O,
                l=2*O,
                disp="vitec",
                verbose="vitec",
                typ='uint',
                fctunram=vitec_unpack,
                fctram=vitec_pack),
            dict(name='temp0',
                start=12*O,
                l=2*O,
                disp="temp0",
                verbose="temp0",
                typ='uint',
                fctunram=temp0_unpack,
                fctram=temp0_pack),
            dict(name='errortherm',
                start=14*O,
                l=2*O,
                disp="errortherm",
                verbose="errortherm",
                typ='uint',
                fctunram=errortherm_unpack,
                fctram=errortherm_pack),
            dict(name='temp1',
                start=18*O,
                l=2*O,
                disp="temp1",
                verbose="temp1",
                typ='sint',
                fctunram=temp_unpack),
            dict(name='temp2',
                start=20*O,
                l=2*O,
                disp="temp2",
                verbose="temp2",
                typ='sint',
                fctunram=temp_unpack),
            dict(name='temp3',
                start=22*O,
                l=2*O,
                disp="temp3",
                verbose="temp3",
                typ='sint',
                fctunram=temp_unpack),
            dict(name='temp4',
                start=24*O,
                l=2*O,
                disp="temp4",
                verbose="temp4",
                typ='sint',
                fctunram=temp_unpack)
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


TROUSSEAU = HKPayloadCCSDSTrousseau(KEYS, listof=True)
