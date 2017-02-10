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

from .ccsdskey import CCSDSKey
from ..utils import core


__all__ = ['PACKETCATEGORIES', 'CATEGORYREGISTRATION', 'PACKETCATEGORYSIZES',
            'TABLECATEGORY', 'ACKCATEGORIES']


CATEGORYREGISTRATION = {0: '0000',
                        1: '0001',
                        2: '0010',
                        3: '0011',
                        4: '0100',
                        5: '0101',
                        6: '0110',
                        7: '0111',
                        8: '1000',
                        9: '1001',
                        10: '1010'}

TELECOMMANDID = CCSDSKey(   name='telecommand_id',
                            start=0,
                            l=10,
                            fctunpack=core.bin2int,
                            fctpack=core.int2bin)

PACKETIDMIRROR = CCSDSKey(  name='packet_id_mirror',
                            start=10,
                            l=14,
                            fctunpack=core.bin2int,
                            fctpack=core.int2bin)

ERRORCODE = CCSDSKey(       name='error_code',
                            start=24,
                            l=8,
                            fctunpack=core.bin2int,
                            fctpack=core.int2bin)


CATEGORY_0 = []  # None
CATEGORY_1 = [TELECOMMANDID, PACKETIDMIRROR, ERRORCODE]
CATEGORY_2 = [TELECOMMANDID, PACKETIDMIRROR, ERRORCODE]
CATEGORY_3 = []  # None
CATEGORY_4 = []
CATEGORY_5 = []
CATEGORY_6 = []
CATEGORY_7 = []  # None
CATEGORY_8 = []
CATEGORY_9 = []


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
    PACKETCATEGORYSIZES[k] = sum([key.len for key in cat])//8


TABLECATEGORY =    {0: 'TmcatRcpAcknowledgement',
                    1: 'TmcatFmtAcknowledgement',
                    2: 'TmcatExeAcknowledgement',
                    3: 'TmcatDebug',
                    4: '',
                    5: '',
                    6: '',
                    7: 'TmcatBeacon',
                    8: '',
                    9: ''}
