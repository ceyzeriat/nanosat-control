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


__all__ = []


CATEGORYREGISTRATIONOBC = { 0:  '00000',  # rec ack
                            1:  '00001',  # beacon
                            2:  '00010',  # boot error report
                            3:  '00011',  # event report
                            4:  '00100'}  # dump answer data


TELECOMMANDIDMIRROR = dict( name='telecommand_id_mirror',
                            start=0,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="telecommand id of the corresponding tc command being ackowledged or answered")

PACKETIDMIRROR = dict(  name='packet_id_mirror',
                        start=16,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="corresponding packet id count of the command being ackowledged or answered")

STARTADDRESS = dict(    name='start_address',
                        start=32,
                        l=32,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Start Adress of Dump")

BYTESNUMBER = dict(     name='bytes_number',
                        start=64,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Length of data in dump packet")


CATEGORY_0 = CCSDSTrousseau([], octets=False)  # rec ack
CATEGORY_1 = CCSDSTrousseau([], octets=False)  # beacon
CATEGORY_2 = CCSDSTrousseau([], octets=False)  # boot error report
CATEGORY_3 = CCSDSTrousseau([], octets=False)  # event report
CATEGORY_4 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, STARTADDRESS, BYTESNUMBER], octets=False)  # dump answer data


ACKCATEGORIESOBC = [0]


# header aux
PACKETCATEGORIESOBC = { 0: CATEGORY_0,  # rec ack
                        1: CATEGORY_1,  # beacon
                        2: CATEGORY_2,  # boot error report
                        3: CATEGORY_3,  # event report
                        4: CATEGORY_4}  # dump answer data


PACKETCATEGORYSIZESOBC = {}
for k, cat in PACKETCATEGORIESOBC.items():
    PACKETCATEGORYSIZESOBC[k] = cat.size


TABLECATEGORYOBC = {0: 'TmcatRcpAcknowledgement',  # rec ack
                    1: 'TmcatFmtAcknowledgement',  # beacon
                    2: 'TmcatExeAcknowledgement',  # boot error report
                    3: 'TmcatDebug',  # event report
                    4: 'TmcatPayloadHk',  # dump answer data
                    5: 'TmcatHfScience',
                    6: None,
                    7: None,
                    8: None,
                    9: None}

TABLEDATAOBC = {    0: None,  # rec ack
                    1: None,  # beacon
                    2: None,  # boot error report
                    3: None,  # event report
                    4: 'DataPayloadHk'}  # dump answer data


FILEDATACRUNCHINGOBC = {0: None,  # rec ack
                        1: 'param_beacon',  # beacon
                        2: None,  # boot error report
                        3: None,  # event report
                        4: 'param_hk_payload'}  # dump answer data


# extend all keys with common categories
for k in param_category_common as cmn.CATEGORYREGISTRATIONCOMMON.keys():
    CATEGORYREGISTRATIONOBC[k] = param_category_common as cmn.CATEGORYREGISTRATIONCOMMON[k]
    PACKETCATEGORIESOBC[k] = param_category_common as cmn.PACKETCATEGORIESCOMMON[k]
    PACKETCATEGORYSIZESOBC[k] = param_category_common as cmn.PACKETCATEGORYSIZESCOMMON[k]
    TABLECATEGORYOBC[k] = param_category_common as cmn.TABLECATEGORYCOMMON[k]
    TABLEDATAOBC[k] = param_category_common as cmn.TABLEDATACOMMON[k]
    FILEDATACRUNCHINGOBC[k] = param_category_common as cmn.FILEDATACRUNCHINGCOMMON[k]

ACKCATEGORIESOBC += ACKCATEGORIESCOMMON
