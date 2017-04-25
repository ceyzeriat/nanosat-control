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
from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.utils import bincore

from . import param_category_common as cmn


__all__ = ['CATEGORYREGISTRATIONPLD', 'ACKCATEGORIESPLD',
            'PACKETCATEGORIESPLD', 'PACKETCATEGORYSIZESPLD',
            'TABLECATEGORYPLD', 'TABLEDATAPLD', 'FILEDATACRUNCHINGPLD']


CATEGORYREGISTRATIONPLD = { 4: '00100',  # HK
                            5: '00101',  # science HF
                            6: '00110',  # report
                            7: '00111'}  # beacon


ACQMODESCIENCE = CCSDSKey(     name='acq_mode',
                        start=0,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Activates science mode (0=Searching, 1=Tracking, 2=Test). Valid for the entire packet.",
                        disp="mode")

INTEGRATIONTIME = CCSDSKey( name='integration_time',
                            start=8,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="Integration time (valid for the entire packet). In ms.",
                            disp="itime")

DELAY = CCSDSKey(       name='delay',
                        start=24,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Delay between two integrations (in ms/10)",
                        disp="delay")

MODULATION = CCSDSKey(  name='modulation',
                        start=40,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Modulation pattern (0=Point, 1=Circle, 2=Flower, 3=Calibration pattern). Valid for the entire packet.",
                        disp="mod")

RADIUS = CCSDSKey(      name='radius',
                        start=48,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Radius of the modulation pattern. Valid for the entire packet.",
                        disp="rad")

NPOINTS = CCSDSKey(     name='n_points',
                        start=64,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Number of points in the pattern",
                        disp="npts")


HKTICK = CCSDSKey(     name='hk_tick',
                        start=0,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Sampling time for hk data (in ms). Valid for the entire packet.",
                        disp="hk_tick")

BINNING = CCSDSKey(     name='binning',
                        start=16,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Binning of the hk data (real sampling is thus binning*hkTick). Valid for the entire packet.",
                        disp="binning")

MAINMODE = CCSDSKey(     name='main_mode',
                        start=24,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                         verbose="Main mode of the payload (SBY = 0, IDL = 1, SCI = 2, IMG = 3, TST = 4). Valid for the entire packet.",
                        disp="mode")

ACQMODEHK = CCSDSKey(     name='acq_mode',
                        start=32,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Activates science mode (0=Searching, 1=Tracking, 2=Test). Valid for the entire packet.",
                        disp="acq_mode")

DIODEFLAG = CCSDSKey(     name='diode_flag',
                        start=40,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Is diode active?. Valid for the entire packet.",
                        disp="diode_flag")

INTERRUPTFLAG = CCSDSKey(     name='interrupt_flag',
                        start=41,
                        l=2,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Is interrupt active?. Valid for the entire packet.",
                        disp="interrupt_flag")

PIEZOFLAG = CCSDSKey(     name='piezo_flag',
                        start=42,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Is piezo active?. Valid for the entire packet.",
                        disp="piezo_flag")

HVFLAG = CCSDSKey(     name='hv_flag',
                        start=43,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Is high-voltage line active?. Valid for the entire packet.",
                        disp="hv_flag")

SENSORSFLAG = CCSDSKey(     name='sensors_flag',
                        start=44,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Are straing gauges active?. Valid for the entire packet.",
                        disp="sensors_flag")

TECFLAG = CCSDSKey(     name='tec_flag',
                        start=45,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Is tec active?. Valid for the entire packet.",
                        disp="hv_flag")

BEACONFLAG = CCSDSKey(     name='beacon_flag',
                        start=46,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Is beacon active?. Valid for the entire packet.",
                        disp="beacon_flag")

PROCFREQ = CCSDSKey(     name='proc_freq',
                        start=48,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="SYSCLOK frequency (in MHz). Valid for the entire packet.",
                        disp="proc_freq")

TECSETPOINT = CCSDSKey(     name='tec_setpoint',
                        start=56,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Setpoint for the TEC controller (ADU). Valid for the entire packet.",
                        disp="tec_setpoint")


CATEGORY_4 = CCSDSTrousseau([HKTICK, BINNING, MAINMODE, ACQMODEHK, DIODEFLAG, INTERRUPTFLAG, PIEZOFLAG, HVFLAG, SENSORSFLAG, TECFLAG, BEACONFLAG, PROCFREQ, TECSETPOINT], octets=False, name='HK')  # HK payload, NO HEADER
CATEGORY_5 = CCSDSTrousseau([ACQMODESCIENCE, INTEGRATIONTIME, DELAY, MODULATION, RADIUS, NPOINTS], octets=False, name='science HF')  # science HF
CATEGORY_6 = CCSDSTrousseau([], octets=False, name='report')  # report
CATEGORY_7 = CCSDSTrousseau([], octets=False, name='beacon')  # beacon


# (payloadd, category)
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
                6: 'DataPldReport',  # report
                7: 'DataPldBeacon'}  # beacon


FILEDATACRUNCHINGPLD = {4: 'param_payload_hk',  # HK
                        5: 'param_hf_science',  # science HF
                        6: 'param_pld_report',  # report
                        7: 'param_pld_beacon'}  # beacon


# extend all keys with common categories
for k in cmn.CATEGORYREGISTRATIONCOMMON.keys():
    CATEGORYREGISTRATIONPLD[k] = cmn.CATEGORYREGISTRATIONCOMMON[k]
    PACKETCATEGORIESPLD[k] = cmn.PACKETCATEGORIESCOMMON[k]
    PACKETCATEGORYSIZESPLD[k] = cmn.PACKETCATEGORYSIZESCOMMON[k]
    TABLECATEGORYPLD[k] = cmn.TABLECATEGORYCOMMON[k]
    TABLEDATAPLD[k] = cmn.TABLEDATACOMMON[k]
    FILEDATACRUNCHINGPLD[k] = cmn.FILEDATACRUNCHINGCOMMON[k]

ACKCATEGORIESPLD += cmn.ACKCATEGORIESCOMMON
