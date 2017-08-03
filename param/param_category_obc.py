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
from ctrl.utils import b
from ctrl.utils import O
from ctrl.utils.day import Day
from ctrl.utils.ms import Ms


from . import param_category_common as cmn
from .generated.booterrorstruct import BOOTERRORSTRUCT_KEYS


__all__ = []


TELECOMMANDIDMIRROR = CCSDSKey( name='telecommand_id_mirror',
                                start=0*O,
                                l=2*O,
                                typ='uint',
                                verbose="telecommand id of the corresponding tc command being ackowledged or answered",
                                disp="tcid")

PACKETIDMIRROR = CCSDSKey(  name='packet_id_mirror',
                            start=2*O,
                            l=2*O,
                            typ='uint',
                            verbose="corresponding packet id count of the command being ackowledged or answered",
                            disp="pkid")

STARTADDRESS = CCSDSKey(name='start_address',
                        start=4*O,
                        l=4*O,
                        typ='byt',
                        verbose="Start Adress of Dump",
                        disp='Addr')

BYTESNUMBER = CCSDSKey( name='bytes_number',
                        start=8*O,
                        l=1*O,
                        typ='uint',
                        verbose="Length of data in dump packet",
                        disp='len')

NSEGS = CCSDSKey(       name='n_segments',
                        start=4*O,
                        l=2*O,
                        typ='uint',
                        verbose="Total Number of segments received",
                        disp="Nseg")


LOGCOUNTER = CCSDSKey(  name='log_counter',
                        start=0*O,
                        l=2*O,
                        typ='uint',
                        verbose='uint16: error counter, analogous to a sequence count / error time ID ',
                        disp="logCounter")
FILECRCCODE = CCSDSKey( name='file_crc_code',
                        start=2*O,
                        l=4*O,
                        typ='byt',
                        verbose='identifies the file where the error occurred, = CRC32(string("source_filename.cpp"));',
                        disp="fileCrcCode")
LINECODE = CCSDSKey(    name='line_code',
                        start=6*O,
                        l=2*O,
                        typ='uint',
                        verbose='uint16: line where the error occurred',
                        disp="lineCode")
FUNERRCODE = CCSDSKey(  name='fun_err_code',
                        start=8*O,
                        l=2*O,
                        typ='sint',
                        verbose='int16: (optional), type of error (from L0AppErrorCode.hpp), or return value of failed function call',
                        disp="funErrCode")


DATE = CCSDSKey( name='date',
                        start=10*O,
                        l=2*O,
                        typ='uint',
                        fctfix=Day,
                        verbose='Time tag field 1: number of days since reference',
                        disp="date")

MSCOUNT = CCSDSKey( name='mscount',
                        start=12*O,
                        l=4*O,
                        typ='uint',
                        fctfix=Ms,
                        verbose='Time tag field 2: number of miliseconds since start of day',
                        disp="ms")

EVENTDATA = CCSDSKey(   name='data',
                        start=16*O,
                        l=4*O,
                        typ='byt',
                        verbose='uint8[4]: (optinal) aditional data',
                        disp="data")


PARTSELECT = CCSDSKey(  name='hk_part',
                        start=4*O,
                        l=1*O,
                        typ='uint',
                        verbose='identifies the HK part',
                        disp='partSelect')



L1AUXDATAPROCESSED_KEYS = [
    dict(
        name = 'mod_pattern',
        start = 0*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'modPattern'),

    dict(
        name = 'number_of_points',
        start = 8*b,
        l = 8*b,
        typ = 'uint',
        verbose = '[NO DOC STRING]',
        disp = 'numberOfPoints'),

    dict(
        name = 'date_start',
        start = 16*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'Beginning of integration (days)',
        unit = 'day',
        disp = 'dateStart'),

    dict(
        name = 'ms_count_start',
        start = 32*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'Beginning of integration (ms)',
        unit = 'ms',
        disp = 'msCountStart'),

    dict(
        name = 'date_end',
        start = 64*b,
        l = 16*b,
        typ = 'uint',
        verbose = 'End of integration (days)',
        unit = 'day',
        disp = 'dateEnd'),

    dict(
        name = 'ms_count_end',
        start = 80*b,
        l = 32*b,
        typ = 'uint',
        verbose = 'End of integration (ms)',
        unit = 'ms',
        disp = 'msCountEnd'),

]




HEADAUX_0 = CCSDSTrousseau([]) # recep ack
HEADAUX_2 = CCSDSTrousseau(BOOTERRORSTRUCT_KEYS) # boot error report
HEADAUX_3 = CCSDSTrousseau([LOGCOUNTER, FILECRCCODE, LINECODE,
                            FUNERRCODE, DATE, MSCOUNT, EVENTDATA])  # event report
HEADAUX_HKOBC = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, PARTSELECT])  # HK
HEADAUX_5 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, STARTADDRESS, BYTESNUMBER])  # dump answer data
HEADAUX_6 = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, NSEGS])  # patch list segments
# tc answer
HEADAUX_TELECOMMANDANSWERCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR])

# L1 Science Data : 
HEADAUX_SCIENCEOBC= CCSDSTrousseau(L1AUXDATAPROCESSED_KEYS)

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
                                data_file='param_patch_list_segs'),

               10: CCSDSCategory(name='flux mean (reduced data)',
                                number=10,
                                aux_trousseau=HEADAUX_SCIENCEOBC,
                                data_file='param_l1dataprocessed'),

               11: CCSDSCategory(name='flux variance (reduced data)',
                                number=11,
                                aux_trousseau=HEADAUX_SCIENCEOBC,
                                data_file='param_l1datacovar'),

               12: CCSDSCategory(name='sd Card files',
                                number=12,
                                aux_trousseau=HEADAUX_TELECOMMANDANSWERCAT,
                                data_file='param_lsSdCard'),

               13: CCSDSCategory(name='data counters of files in memory (SD card or Ram)',
                                number=13,
                                aux_trousseau=HEADAUX_TELECOMMANDANSWERCAT,
                                data_file='param_dataCounters'),


               15: CCSDSCategory(name='ADCS standard telemetry',
                                number=15,
                                aux_trousseau=None,
                                data_file='param_l1adcsstandard'),


               16: CCSDSCategory(name='ADCS actuator telemetry',
                                number=16,
                                aux_trousseau=None,
                                data_file='param_l1adcsactuator'),


               17: CCSDSCategory(name='ADCS sensor telemetry',
                                number=17,
                                aux_trousseau=None,
                                data_file='param_l1adcssensor'),


               18: CCSDSCategory(name='ADCS attitude telemetry',
                                number=18,
                                aux_trousseau=None,
                                data_file='param_l1adcsattitude'),


               19: CCSDSCategory(name='L1 housekeeping',
                                number=19,
                                aux_trousseau=None,
                                data_file='param_l1hk'),


               20: CCSDSCategory(name='Scheduler Fifo',
                                number=20,
                                aux_trousseau=HEADAUX_TELECOMMANDANSWERCAT,
                                data_file='param_l1Scheduler')
                }


# extend all keys with common categories
CATEGORIESOBC.update(cmn.CATEGORIESCOMMON)


ACKCATEGORIESOBC += cmn.ACKCATEGORIESCOMMON
