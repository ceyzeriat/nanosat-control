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
from ctrl.ccsds.ccsdscategory import CCSDSCategory
from ctrl.utils import bincore

from . import param_category_common as cmn
from .generated.booterrorstruct import BOOTERRORSTRUCT_KEYS

__all__ = []


TELECOMMANDIDMIRROR = CCSDSKey( name='telecommand_id_mirror',
                                start=0,
                                l=16,
                                fctunpack=bincore.bin2int,
                                fctpack=bincore.int2bin,
                                verbose="telecommand id of the corresponding tc command being ackowledged or answered",
                                disp="tcid")

PACKETIDMIRROR = CCSDSKey(  name='packet_id_mirror',
                            start=16,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="corresponding packet id count of the command being ackowledged or answered",
                            disp="pkid")

STARTADDRESS = CCSDSKey(name='start_address',
                        start=32,
                        l=32,
                        fctunpack=bincore.bin2hex,
                        fctpack=bincore.hex2bin,
                        verbose="Start Adress of Dump",
                        disp='Addr')

BYTESNUMBER = CCSDSKey( name='bytes_number',
                        start=64,
                        l=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Length of data in dump packet",
                        disp='len')

NSEGS = CCSDSKey(       name='n_segments',
                        start=32,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose="Total Number of segments received",
                        disp="Nseg")

HEADAUX_RACKCAT = CCSDSTrousseau([], octets=False)  # rec ack
#HEADAUX_1 = CCSDSTrousseau([], octets=False)  # beacon
#HEADAUX_2 = CCSDSTrousseau([], octets=False report')  # boot error report ?????
HEADAUX_2 = CCSDSTrousseau(BOOTERRORSTRUCT_KEYS, octets = False)
#HEADAUX_3 = CCSDSTrousseau([], octets=False)  # event report ?????
#HEADAUX_4 = CCSDSTrousseau([], octets=False)  # HK
HEADAUX_5 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, STARTADDRESS, BYTESNUMBER], octets=False)  # dump answer data
HEADAUX_6 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, NSEGS], octets=False)  # patch list segments


# acknowledgement of reception
RACKCAT = 0

# (payload, category)
ACKCATEGORIESOBC = [(0, RACKCAT)]


CATEGORIESOBC = {
                RACKCAT: CCSDSCategory(name='recep acknowledgement',
                                        number=RACKCAT,
                                        aux_trousseau=HEADAUX_RACKCAT,
                                        data_file=None),

               1: CCSDSCategory(name='beacon',
                                number=1,
                                aux_trousseau=None,
                                data_file=None),

               2: CCSDSCategory(name='boot error report',
                                number=2,
                                aux_trousseau=HEADAUX_2,
                                data_file=None),

               3: CCSDSCategory(name='event report',
                                number=3,
                                aux_trousseau=None,
                                data_file=None),

               4: CCSDSCategory(name='house keeping',
                                number=4,
                                aux_trousseau=None,
                                data_file=None),

               5: CCSDSCategory(name='dump answer data',
                                number=5,
                                aux_trousseau=HEADAUX_5,
                                data_file='param_dump_ans_data'),

               6: CCSDSCategory(name='patch list segment',
                                number=6,
                                aux_trousseau=HEADAUX_6,
                                data_file='param_patch_list_segs')
                }


# extend all keys with common categories
CATEGORIESOBC.update(cmn.CATEGORIESCOMMON)


ACKCATEGORIESOBC += cmn.ACKCATEGORIESCOMMON
