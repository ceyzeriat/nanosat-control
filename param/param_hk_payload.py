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


import numpy as np
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.ccsds import ccsdsexception
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


def volt_line_unpack(v, **kwargs):
    volt_line_unpack.verbose = "(binary -> unsigned integer) * 0.00459"
    return bincore.bin2int(v) * 0.00459


def volt_line_pack(v, pad, **kwargs):
    volt_line_pack.verbose = "round(float / 0.00459) -> binary"
    return bincore.int2bin(np.round(v / 0.00459), pad=pad)


def current_line_unpack(v, **kwargs):
    current_line_unpack.verbose = "(binary -> unsigned integer) * 0.00161"
    return bincore.bin2int(v) * 0.00161


def current_line_pack(v, pad, **kwargs):
    current_line_pack.verbose = "round(float / 0.00161) -> binary"
    return bincore.int2bin(np.round(v / 0.00161), pad=pad)


def volt_piezo_unpack(v, **kwargs):
    volt_piezo_unpack.verbose = "(binary -> unsigned integer) * 3.3 / 4096 * 213.77"
    return bincore.bin2int(v) * 3.3 / 4096.0 * 213.77


def volt_piezo_pack(v, pad, **kwargs):
    volt_piezo_pack.verbose = "round(float / 3.3 * 4096 / 213.77) -> binary"
    return bincore.int2bin(np.round(v / 3.3 * 4096.0 / 213.77), pad=pad)


def temp_unpack(v, **kwargs):
    temp_unpack.verbose = "(binary -> unsigned integer) * 0.0625"
    return bincore.bin2int(v) * 0.0625


def temp_pack(v, pad, **kwargs):
    temp_pack.verbose = "round(float / 0.0625) -> binary"
    return bincore.int2bin(np.round(v / 0.0625), pad=pad)


def volt_peltier_unpack(v, **kwargs):
    volt_peltier_unpack.verbose = "(binary -> unsigned integer) * 3.3 / 4096"
    return bincore.bin2int(v) * 3.3 / 4096.0


def volt_peltier_pack(v, pad, **kwargs):
    volt_peltier_pack.verbose = "round(float / 3.3 * 4096.0) -> binary"
    return bincore.int2bin(np.round(v / 3.3 * 4096), pad=pad)


def current_peltier_unpack(v, Vref, **kwargs):
    current_peltier_unpack.verbose = "((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 0.00016"
    return (bincore.bin2int(v) * 3.3 / 4096.0 - Vref) / 0.00016


def current_peltier_pack(v, Vref, pad, **kwargs):
    current_peltier_pack.verbose = "round((float * 0.00016 + Vref) * 4096 / 3.3) -> binary"
    return bincore.int2bin(np.round((v * 0.00016 + Vref) * 4096 / 3.3), pad=pad)


def volt_peltier_err_unpack(v, Vref, **kwargs):
    volt_peltier_err_unpack.verbose = "((binary -> unsigned integer) * 3.3 / 4096.0 - Voltage Peltier) / 25"
    return (bincore.bin2int(v) * 3.3 / 4096.0 - Vref) / 25


def volt_peltier_err_pack(v, Vref, pad, **kwargs):
    volt_peltier_err_pack.verbose = "round((float * 25 + Vref) * 4096 / 3.3) -> binary"
    return bincore.int2bin(np.round((v * 25 + Vref) * 4096 / 3.3), pad=pad)


def temp_diode_unpack(v, Vref, **kwargs):
    temp_diode_unpack.verbose = "293 / (293 / 2918.9 * LOG(50 / 11 * (binary -> unsigned integer) / (Voltage Peltier / 3.3 * 4096 - (binary -> unsigned integer))) + 1) - 273"
    X = bincore.bin2int(v)
    return 293 / (293 / 2918.9\
                    * np.log(50 / 11.0 * X / (Vref / 3.3 * 4096 - X)) + 1) - 273


def temp_diode_pack(v, Vref, pad, **kwargs):
    temp_diode_pack.verbose = "round((Voltage Peltier / 3.3 * 4096) / (1 + 50 / (11 * np.exp(2918.9 / 293 * (293 / (float + 273.0) - 1))))) -> binary"
    return bincore.int2bin(np.round(
                            (Vref / 3.3 * 4096) /\
                            (1 + 50 /\
                                (11 * np.exp(2918.9 / 293.0 *\
                                                (293 / (v + 273.0) - 1))))),
                           pad=pad)


V_KEYS = [  dict(name='volt_5V', start=16, l=16, fctunpack=volt_line_unpack, fctpack=volt_line_pack),
            dict(name='current_5V', start=32, l=16, fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='current_3V', start=48, l=16, fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='volt_piezo', start=64, l=16, fctunpack=volt_piezo_unpack, fctpack=volt_piezo_pack),
            dict(name='current_piezo', start=80, l=16, fctunpack=current_line_unpack, fctpack=current_line_pack),
            dict(name='volt_peltier', start=144, l=16, fctunpack=volt_peltier_unpack, fctpack=volt_peltier_pack),
            dict(name='current_peltier', start=96, l=16, fctunpack=current_peltier_unpack, fctpack=current_peltier_pack),
            dict(name='temp_diode', start=112, l=16, fctunpack=temp_diode_unpack, fctpack=temp_diode_pack),
            dict(name='volt_peltier_err', start=128, l=16, fctunpack=volt_peltier_err_unpack, fctpack=volt_peltier_err_pack),
            dict(name='temp1', start=160, l=16, fctunpack=temp_unpack, fctpack=temp_pack),
            dict(name='temp2', start=176, l=16, fctunpack=temp_unpack, fctpack=temp_pack),
            dict(name='temp3', start=192, l=16, fctunpack=temp_unpack, fctpack=temp_pack),
            ]


# names will be filled in automatically afterwards
F_KEYS = [  dict(name='-', start=4, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=5, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=6, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=7, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=8, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=9, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=10, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=11, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=12, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=13, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=14, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin),
            dict(name='-', start=15, l=1, fctunpack=bincore.bin2bool, fctpack=bincore.bool2bin)
            ]


# fill in names for flags
def value_to_flag_name(txt):
    return 'f_'+txt
for idx, item in enumerate(V_KEYS):
    F_KEYS[idx]['name'] = value_to_flag_name(item['name'])


class HKPayloadCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, **kwargs):
        """
        Unpacks the data contained in the HK Payload packets

        Args:
        * data (byts): the chain of octets to unpack
        """
        nlines = len(data) // self.size
        lines = [{}] * nlines
        for idx in range(nlines):
            lines[idx]['voltage_peltier'] = 0
            dt = data[idx*self.size:(idx+1)*self.size]
            # octets is False
            dt = bincore.hex2bin(dt[:self.size], pad=self.size*8)
            # if octets were True: dt = dt[:self.size]
            for item in self.keys:
                lines[idx][item.name] = item.unpack(
                                            dt,
                                            Vref=lines[idx]['voltage_peltier'])
            for item in V_KEYS:
                v_key = item['name']
                f_key = value_to_flag_name(v_key)
                if not lines[idx][f_key]:
                    lines[idx][v_key] = 0.
        return lines

    def disp(self, hdx, data):
        res = []
        #res += ["ACQ: {acq_mode}, IT: {integration_time}, M: {modulation}, "\
        #        "R: {radius}, NP: {n_points}".format(**hdx)]
        #for line in data['unpacked']:
        #    res += ["S: {step}, C: {counts}, Xc{x_com}, Yc{y_com}, Xp{x_pos}, "\
        #          "Yp{y_pos}".format(**line)]
        return "\n".join(res)

    def pack(self, allvalues, **kwargs):
        """
        Packs the values into a HK Payload packet

        Args:
        * allvalues (dict): the values to pack
        """
        Vref = allvalues['voltage_peltier']
        return Super(HKPayloadCCSDSTrousseau, self).\
                        pack(allvalues, retdbvalues=True, Vref=Vref)


TROUSSEAU = HKPayloadCCSDSTrousseau(F_KEYS + V_KEYS, octets=False)