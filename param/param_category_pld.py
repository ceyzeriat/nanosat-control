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

from . import param_category_common as cmn


__all__ = ['CATEGORYREGISTRATIONPLD', 'ACKCATEGORIESPLD',
            'PACKETCATEGORIESPLD', 'PACKETCATEGORYSIZESPLD',
            'TABLECATEGORYPLD', 'TABLEDATAPLD', 'FILEDATACRUNCHINGPLD']


CATEGORYREGISTRATIONPLD = { 4: '00100',  # HK
                            5: '00101',  # science HF
                            6: '00110',  # report
                            7: '00111'}  # beacon


ACQMODE = dict(         name='acq_mode',
                        start=0,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Activates science mode (0=Searching, 1=Tracking, 2=Test). Valid for the entire packet.")

INTEGRATIONTIME = dict( name='integration_time',
                        start=8,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Integration time (valid for the entire packet). In ms.")

DELAY = dict(           name='delay',
                        start=24,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Delay between two integrations (in ms/10)")

MODULATION = dict(      name='modulation',
                        start=40,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Modulation pattern (0=Point, 1=Circle, 2=Flower, 3=Calibration pattern). Valid for the entire packet.")

RADIUS = dict(          name='radius',
                        start=48,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Radius of the modulation pattern. Valid for the entire packet.")

NPOINTS = dict(         name='n_points',
                        start=64,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Number of points in the pattern")


CATEGORY_4 = CCSDSTrousseau([], octets=False)  # HK payload, NO HEADER
CATEGORY_5 = CCSDSTrousseau([ACQMODE, INTEGRATIONTIME, DELAY, MODULATION, RADIUS, NPOINTS], octets=False)  # science HF
CATEGORY_6 = CCSDSTrousseau([], octets=False)  # report
CATEGORY_7 = CCSDSTrousseau([], octets=False)  # report


ACKCATEGORIESPLD = []


# header aux
PACKETCATEGORIESPLD = { 4: CATEGORY_4,  # HK
                        5: CATEGORY_5,  # science HF
                        6: CATEGORY_6,  # report
                        7: CATEGORY_7}  # beacon


PACKETCATEGORYSIZESPLD = {}
for k, cat in PACKETCATEGORIESPLD.items():
    PACKETCATEGORYSIZESPLD[k] = cat.size


TABLECATEGORYPLD = {4: None,  # HK
                    5: 'TmcatHfScience',  # science HF
                    6: None,  # report
                    7: None}  # beacon


TABLEDATAPLD = {4: 'DataPayloadHk',  # HK
                5: 'DataHfScience',  # science HF
                6: None,  # report
                7: None}  # beacon


FILEDATACRUNCHINGPLD = {4: 'param_payload_hk',  # HK
                        5: 'param_hf_science',  # science HF
                        6: 'param_payload_report',  # report
                        7: None}  # beacon


# extend all keys with common categories
for k in cmn.CATEGORYREGISTRATIONCOMMON.keys():
    CATEGORYREGISTRATIONPLD[k] = cmn.CATEGORYREGISTRATIONCOMMON[k]
    PACKETCATEGORIESPLD[k] = cmn.PACKETCATEGORIESCOMMON[k]
    PACKETCATEGORYSIZESPLD[k] = cmn.PACKETCATEGORYSIZESCOMMON[k]
    TABLECATEGORYPLD[k] = cmn.TABLECATEGORYCOMMON[k]
    TABLEDATAPLD[k] = cmn.TABLEDATACOMMON[k]
    FILEDATACRUNCHINGPLD[k] = cmn.FILEDATACRUNCHINGCOMMON[k]

ACKCATEGORIESPLD += cmn.ACKCATEGORIESCOMMON
