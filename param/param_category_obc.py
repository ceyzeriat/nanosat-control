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


from ctrl.utils import bincore
from ctrl.ccsds.ccsdstrousseau import CCSDSTrousseau
from ctrl.ccsds.ccsdskey import CCSDSKey
from ctrl.ccsds.ccsdscategory import CCSDSCategory

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


LOGCOUNTER = CCSDSKey(  name='log_counter',
                        start=0,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose='uint16: error counter, analogous to a sequence count / error time ID ',
                        disp="logCounter")
FILECRCCODE = CCSDSKey( name='file_crc_code',
                        start=16,
                        l=32,
                        fctunpack=bincore.bin2hex,
                        fctpack=bincore.hex2bin,
                        verbose='identifies the file where the error occurred, = CRC32(string("source_filename.cpp"));',
                        disp="fileCrcCode")
LINECODE = CCSDSKey(    name='line_code',
                        start=48,
                        l=16,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose='uint16: line where the error occurred',
                        disp="lineCode")
FUNERRCODE = CCSDSKey(  name='fun_err_code',
                        start=64,
                        l=16,
                        fctunpack=bincore.bin2intSign,
                        fctpack=bincore.intSign2bin,
                        verbose='int16: (optional), type of error (from L0AppErrorCode.hpp), or return value of failed function call',
                        disp="funErrCode")
SECHEADERTM = CCSDSKey( name='sec_header_tm',
                        start=80,
                        l=48,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose='time tag',
                        disp="SecHeaderTm")
EVENTDATA = CCSDSKey(   name='data',
                        start=128,
                        l=32,
                        fctunpack=bincore.bin2hex,
                        fctpack=bincore.hex2bin,
                        verbose='uint8[4]: (optinal) aditional data',
                        disp="data")


PARTSELECT = CCSDSKey(  name='hk_part',
                        start=32,
                        len=8,
                        fctunpack=bincore.bin2int,
                        fctpack=bincore.int2bin,
                        verbose='identifies the HK part',
                        disp='partSelect')



HEADAUX_0 = CCSDSTrousseau([], octets=False) # recep ack
HEADAUX_2 = CCSDSTrousseau(BOOTERRORSTRUCT_KEYS, octets=False) # boot error report
HEADAUX_3 = CCSDSTrousseau([LOGCOUNTER, FILECRCCODE, LINECODE,
                            FUNERRCODE, SECHEADERTM, EVENTDATA], octets=False)  # event report
HEADAUX_HKOBC = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, PARTSELECT], octets=False)  # HK
HEADAUX_5 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, STARTADDRESS, BYTESNUMBER], octets=False)  # dump answer data
HEADAUX_6 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, NSEGS], octets=False)  # patch list segments


# acknowledgement of reception
RACKCAT = 0
HKOBC = 4

# (payload, category)
ACKCATEGORIESOBC = [(0, RACKCAT)]


CATEGORIESOBC = {
                RACKCAT: CCSDSCategory(name='rec acknowledgement',
                                        number=RACKCAT,
                                        aux_trousseau=HEADAUX_0,
                                        data_file=None),

               1: CCSDSCategory(name='beacon',
                                number=1,
                                aux_trousseau=None,
                                data_file='param_beacon'),

               2: CCSDSCategory(name='boot error report',
                                number=2,
                                aux_trousseau=HEADAUX_2,
                                data_file=None),

               3: CCSDSCategory(name='event report',
                                number=3,
                                aux_trousseau=HEADAUX_3,
                                data_file=None),

               HKOBC: CCSDSCategory(name='house keeping',
                                number=HKOBC,
                                aux_trousseau=HEADAUX_HKOBC,
                                data_file='param_hk_obc'),

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
