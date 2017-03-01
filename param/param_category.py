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


# taken from https://nubes-lesia.obspm.fr/index.php/apps/files?dir=%2FPicSat%2FProjet%2FtrxDoc


from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.utils import bincore


__all__ = ['PACKETCATEGORIES', 'CATEGORYREGISTRATION', 'PACKETCATEGORYSIZES',
            'TABLECATEGORY', 'ACKCATEGORIES']


CATEGORYREGISTRATION = {0:  '0000',
                        1:  '0001',
                        2:  '0010',
                        3:  '0011',
                        4:  '0100',
                        5:  '0101',
                        6:  '0110',
                        7:  '0111',
                        8:  '1000',
                        9:  '1001'}

TELECOMMANDID = dict(   name='telecommand_id',
                        start=0,
                        l=10,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)

PACKETIDMIRROR = dict(  name='packet_id_mirror',
                        start=10,
                        l=14,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)

ERRORCODE = dict(       name='error_code',
                        start=24,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)


ACQMODE = dict(         name='acq_mode',
                        start=0,
                        l=1,
                        fctunpack=bincore.hex2int,
                        fctpack=bincore.int2hex)

INTEGRATIONTIME = dict( name='integration_time',
                        start=1,
                        l=2,
                        fctunpack=bincore.hex2int,
                        fctpack=bincore.int2hex)

MODULATION = dict(      name='modulation',
                        start=3,
                        l=1,
                        fctunpack=bincore.hex2int,
                        fctpack=bincore.int2hex)

RADIUS = dict(          name='radius',
                        start=4,
                        l=2,
                        fctunpack=bincore.hex2int,
                        fctpack=bincore.int2hex)

NPOINTS = dict(         name='n_points',
                        start=6,
                        l=1,
                        fctunpack=bincore.hex2int,
                        fctpack=bincore.int2hex)

REPPLDRACK  = dict(     name='requestAckReception',
                        start=0,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)
REPPLDFACK  = dict(     name='requestAckFormat',
                        start=1,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)
REPPLDEACK  = dict(     name='requestAckExecution',
                        start=2,
                        l=1,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)
REPPLDTCID  = dict(     name='telecommandID',
                        start=3,
                        l=10,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)
REPPLDEID   = dict(     name='emitterID',
                        start=13,
                        l=3,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)
REPPLDSF    = dict(     name='sequenceFlag',
                        start=16,
                        l=2,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)
REPPLDPKID  = dict(     name='PacketCounter',
                        start=18,
                        l=14,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin)



CATEGORY_0 = CCSDSTrousseau([], octets=False)  # Rec Ack, NO HEADER
CATEGORY_1 = CCSDSTrousseau([TELECOMMANDID, PACKETIDMIRROR, ERRORCODE], octets=False)  # Fmt Ack, 
CATEGORY_2 = CCSDSTrousseau([TELECOMMANDID, PACKETIDMIRROR, ERRORCODE], octets=False)  # Exe Ack, 
CATEGORY_3 = CCSDSTrousseau([], octets=False)  # Debug, NO HEADER
CATEGORY_4 = CCSDSTrousseau([], octets=False)  # HK payload, NO HEADER
CATEGORY_5 = CCSDSTrousseau([ACQMODE, INTEGRATIONTIME, MODULATION, RADIUS, NPOINTS], octets=True)  # science HF
CATEGORY_6 = CCSDSTrousseau([REPPLDRACK, REPPLDFACK, REPPLDEACK, REPPLDTCID, REPPLDEID, REPPLDSF, REPPLDPKID], octets=False)  # Reply TC PLD
CATEGORY_7 = CCSDSTrousseau([], octets=False)  # beacon, NO HEADER
CATEGORY_8 = CCSDSTrousseau([], octets=False)  # ???
CATEGORY_9 = CCSDSTrousseau([], octets=False)  # ???


ACKCATEGORIES = [0, 1, 2]


# header aux
PACKETCATEGORIES = {0: CATEGORY_0,
                    1: CATEGORY_1,
                    2: CATEGORY_2,
                    3: CATEGORY_3,
                    4: CATEGORY_4,
                    5: CATEGORY_5,
                    6: CATEGORY_6,
                    7: CATEGORY_7,
                    8: CATEGORY_8,
                    9: CATEGORY_9}


PACKETCATEGORYSIZES = {}
for k, cat in PACKETCATEGORIES.items():
    PACKETCATEGORYSIZES[k] = cat.size


TABLECATEGORY = {   0: 'TmcatRcpAcknowledgement',
                    1: 'TmcatFmtAcknowledgement',
                    2: 'TmcatExeAcknowledgement',
                    3: 'TmcatDebug',
                    4: 'TmcatPayloadHk',
                    5: 'TmcatHfScience',
                    6: None,
                    7: None,
                    8: None,
                    9: None}

TABLEDATA = {   0: None,
                1: None,
                2: None,
                3: None,
                4: 'DataPayloadHk',
                5: 'DataHfScience',
                6: None,
                7: None,
                8: None,
                9: None}


FILEDATACRUNCHING = {   0: None,
                        1: None,
                        2: None,
                        3: None,
                        4: 'param_hk_payload',
                        5: 'param_science_hf',
                        6: 'param_rep_tc_pld,
                        7: 'param_beacon',
                        8: None,
                        9: None}
