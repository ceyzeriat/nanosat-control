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


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore


__all__ = ['TROUSSEAU']


V_KEYS = [  dict(name='volt_5V', start=16, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='current_5V', start=32, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='current_3V', start=48, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='volt_piezo', start=64, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='current_piezo', start=80, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='current_peltier', start=96, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='temp_diode', start=112, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='voltage_peltier_err', start=128, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='voltage_peltier', start=144, l=16, fctunpack=bincore.bin2int, fctpack=bincore.int2bin),
            dict(name='temp1', start=160, l=16, fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin),
            dict(name='temp2', start=176, l=16, fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin),
            dict(name='temp3', start=192, l=16, fctunpack=bincore.bin2intSign, fctpack=bincore.intSign2bin),
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


def value_to_flag_name(txt):
    return 'f_'+txt

for idx, item in enumerate(V_KEYS):
    F_KEYS[idx].name = value_to_flag_name(item.name)


class HKPayloadCCSDSTrousseau(CCSDSTrousseau):
    def unpack(self, data, retdbvalues=True):
        """
        Unpacks the data contained in the Science HF packets

        Args:
        * data (byts): the chain of octets to unpack
        """
        nlines = len(data) // self.size
        lines = [{}] * nlines
        for idx in range(nlines):
            lines[idx] = super(HKPayloadCCSDSTrousseau, self).unpack(
                                        data[idx*self.size:(idx+1)*self.size])
            for item in V_KEYS:
                v_key = item['name']
                f_key = value_to_flag_name(v_key)
                if not lines[idx][f_key]:
                    lines[idx][v_key] = 0.
        return lines

    def disp(self, hdx, data):
        res = []
        res += ["ACQ: {acq_mode}, IT: {integration_time}, M: {modulation}, "\
                "R: {radius}, NP: {n_points}".format(**hdx)]
        for line in data['unpacked']:
            res += ["S: {step}, C: {counts}, Xc{x_com}, Yc{y_com}, Xp{x_pos}, "\
                  "Yp{y_pos}".format(**line)]
        return "\n".join(res)


TROUSSEAU = HKPayloadCCSDSTrousseau(F_KEYS + V_KEYS, octets=False)
