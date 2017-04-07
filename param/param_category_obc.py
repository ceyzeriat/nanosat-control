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


__all__ = []


RACKCAT = 0

CATEGORYREGISTRATIONOBC = { RACKCAT: '00000',  # rec ack
                            1: '00001',  # beacon
                            2: '00010',  # boot error report
                            3: '00011',  # event report
                            4: '00100',  # house keeping
                            5: '00101',  # dump answer data
                            6: '00110'}  # patch list segments


TELECOMMANDIDMIRROR = CCSDSKey( name='telecommand_id_mirror',
                                start=0,
                                l=16,
                                fctunpack=bincore.bin2int,
                                fctpack=bincore.int2bin,
                                verbose="telecommand id of the corresponding tc command being ackowledged or answered")

PACKETIDMIRROR = CCSDSKey(  name='packet_id_mirror',
                            start=16,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="corresponding packet id count of the command being ackowledged or answered")

STARTADDRESS = CCSDSKey(name='start_address',
                        start=32,
                        l=32,
                        fctunpack=bincore.bin2hex,
                        fctpack=bincore.hex2bin,
                        verbose="Start Adress of Dump")

BYTESNUMBER = CCSDSKey( name='bytes_number',
                        start=64,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Length of data in dump packet")

NSEGS = CCSDSKey(       name='n_segments',
                        start=32,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Total Number of segments received")

CATEGORY_RACKCAT = CCSDSTrousseau([], octets=False, name='reception ack')  # rec ack
CATEGORY_1 = CCSDSTrousseau([], octets=False, name='beacon')  # beacon
CATEGORY_2 = CCSDSTrousseau([], octets=False, name='boot error report')  # boot error report ?????
CATEGORY_3 = CCSDSTrousseau([], octets=False, name='event report')  # event report ?????
CATEGORY_4 = CCSDSTrousseau([], octets=False, name='HK')  # HK
CATEGORY_5 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, STARTADDRESS, BYTESNUMBER], octets=False, name='dump answer data')  # dump answer data
CATEGORY_6 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, NSEGS], octets=False, name='patch list segments')  # patch list segments


# (payloadd, category)
ACKCATEGORIESOBC = [(0, RACKCAT)]


# header aux
PACKETCATEGORIESOBC = { RACKCAT: CATEGORY_RACKCAT,  # rec ack
                        1: CATEGORY_1,  # beacon
                        2: CATEGORY_2,  # boot error report
                        3: CATEGORY_3,  # event report
                        4: CATEGORY_4,  # HK
                        5: CATEGORY_5,  # dump answer data
                        6: CATEGORY_6}  # patch list segs


PACKETCATEGORYSIZESOBC = {}
for k, cat in PACKETCATEGORIESOBC.items():
    PACKETCATEGORYSIZESOBC[k] = cat.size


TABLECATEGORYOBC = {RACKCAT: 'TmcatRcpAcknowledgement',  # rec ack
                    1: None,  # beacon
                    2: None,  # boot error report
                    3: None,  # event report
                    4: None,  # HK
                    5: None,  # dump answer data
                    6: None}  # patch list segs

TABLEDATAOBC = {    RACKCAT: None,  # rec ack
                    1: None,  # beacon
                    2: None,  # boot error report
                    3: None,  # event report
                    4: None,  # HK
                    5: None,  # dump answer data
                    6: None}  # patch list segs


FILEDATACRUNCHINGOBC = {RACKCAT: None,  # rec ack
                        1: 'param_beacon',  # beacon
                        2: None,  # boot error report
                        3: None,  # event report
                        4: None, # HK
                        5: 'param_dump_ans_data',  # dump answer data
                        6: 'param_patch_list_segs'}  # patch list segs


# extend all keys with common categories
for k in cmn.CATEGORYREGISTRATIONCOMMON.keys():
    CATEGORYREGISTRATIONOBC[k] = cmn.CATEGORYREGISTRATIONCOMMON[k]
    PACKETCATEGORIESOBC[k] = cmn.PACKETCATEGORIESCOMMON[k]
    PACKETCATEGORYSIZESOBC[k] = cmn.PACKETCATEGORYSIZESCOMMON[k]
    TABLECATEGORYOBC[k] = cmn.TABLECATEGORYCOMMON[k]
    TABLEDATAOBC[k] = cmn.TABLEDATACOMMON[k]
    FILEDATACRUNCHINGOBC[k] = cmn.FILEDATACRUNCHINGCOMMON[k]

ACKCATEGORIESOBC += cmn.ACKCATEGORIESCOMMON
