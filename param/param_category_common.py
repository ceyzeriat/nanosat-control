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
from ctrl.utils import b
from ctrl.utils import O


__all__ = []


TELECOMMANDIDMIRROR = CCSDSKey( name='telecommand_id_mirror',
                                start=0*O,
                                l=2*O,
                                typ='uint',
                                verbose="telecommand id of the corresponding tc command being ackowledged or answered",
                                disp="tcid")

PACKETIDMIRROR = CCSDSKey(      name='packet_id_mirror',
                                start=2*O,
                                l=2*O,
                                typ='uint',
                                verbose="corresponding packet id count of the command being ackowledged or answered",
                                disp="pkid")

ERRORCODE = CCSDSKey(           name='error_code',
                                start=4*O,
                                l=2*O,
                                typ='sint',
                                verbose="error code: 0 if successful, else error codes",
                                disp="errcode")


# exec ack
HEADAUX_EACKCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, ERRORCODE])
# fmt ack
HEADAUX_FACKCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR, ERRORCODE])
# tc answer
HEADAUX_TELECOMMANDANSWERCAT = CCSDSTrousseau([TELECOMMANDIDMIRROR, PACKETIDMIRROR])


EACKCAT = 31
FACKCAT = 30
TELECOMMANDANSWERCAT = 29


CATEGORIESCOMMON = {
            EACKCAT: CCSDSCategory(name='exe acknowledgement',
                                    number=EACKCAT,
                                    aux_trousseau=HEADAUX_EACKCAT,
                                    data_file='param_exe_ack'),

           FACKCAT: CCSDSCategory(name='fmt acknowledgement',
                                    number=FACKCAT,
                                    aux_trousseau=HEADAUX_FACKCAT,
                                    data_file=None),

           TELECOMMANDANSWERCAT: CCSDSCategory(name='tc answer',
                                                number=TELECOMMANDANSWERCAT,
                                                aux_trousseau=HEADAUX_TELECOMMANDANSWERCAT,
                                                data_file='param_tc_answer',
                                                thatsTCANS=True)
                    }

# (payload, category)
ACKCATEGORIESCOMMON = [(0, EACKCAT),
                       (0, FACKCAT),
                       (1, EACKCAT),
                       (1, FACKCAT)]
