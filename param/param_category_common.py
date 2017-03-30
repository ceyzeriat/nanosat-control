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


__all__ = ['CATEGORYREGISTRATIONCOMMON', 'ACKCATEGORIESCOMMON',
            'PACKETCATEGORIESCOMMON', 'PACKETCATEGORYSIZESCOMMON',
            'TABLECATEGORYCOMMON', 'TABLEDATACOMMON',
            'FILEDATACRUNCHINGCOMMON']


EACKCAT = 31
FACKCAT = 30
TELECOMMANDANSWERCAT = 29


CATEGORYREGISTRATIONCOMMON = {  EACKCAT: '11111',  # exec ack
                                FACKCAT: '11110',  # fmt ack
                                TELECOMMANDANSWERCAT: '11101'}  # tc answer


TELECOMMANDIDMIRROR = dict( name='telecommand_id_mirror',
                            start=0,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="telecommand id of the corresponding tc command being ackowledged or answered",
                            disp="tcid")

PACKETIDMIRROR = dict(      name='packet_id_mirror',
                            start=16,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="corresponding packet id count of the command being ackowledged or answered",
                            disp="pkid")

ERRORCODE = dict(           name='error_code',
                            start=32,
                            l=16,
                            fctunpack=bincore.bin2int,
                            fctpack=bincore.int2bin,
                            verbose="error code: 0 if successful, else error codes",
                            disp="errcode")


CATEGORY_EACKCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, ERRORCODE],
                                octets=False)  # exec ack
CATEGORY_FACKCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, ERRORCODE],
                                octets=False)  # fmt ack
CATEGORY_TELECOMMANDANSWERCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR],
                                octets=False)  # tc answer


# (payloadd, category)
ACKCATEGORIESCOMMON = [(0, EACKCAT),
                       (0, FACKCAT),
                       (1, EACKCAT),
                       (1, FACKCAT)]


# header aux
PACKETCATEGORIESCOMMON = {  EACKCAT: CATEGORY_EACKCAT,  # exec ack
                            FACKCAT: CATEGORY_FACKCAT,  # fmt ack
                            TELECOMMANDANSWERCAT: CATEGORY_TELECOMMANDANSWERCAT}  # tc answer


PACKETCATEGORYSIZESCOMMON = {}
for k, cat in PACKETCATEGORIESCOMMON.items():
    PACKETCATEGORYSIZESCOMMON[k] = cat.size



TABLECATEGORYCOMMON = { EACKCAT: 'TmcatExeAcknowledgement',  # exec ack
                        FACKCAT: 'TmcatFmtAcknowledgement',  # fmt ack
                        TELECOMMANDANSWERCAT: 'TmcatTelecommandAnswer'}  # tc answer


TABLEDATACOMMON = { EACKCAT: 'DataExeAcknowledgement',  # exec ack
                    FACKCAT: None,  # fmt ack
                    TELECOMMANDANSWERCAT: 'DataTelecommandAnswer'}  # tc answer


FILEDATACRUNCHINGCOMMON = { EACKCAT: 'param_exe_ack',  # exec ack
                            FACKCAT: None,  # fmt ack
                            TELECOMMANDANSWERCAT: 'param_tc_answer'}  # tc answer
