#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  
#  CTRL - Ground-Segment software for Cube-Sats
#  Copyright (C) 202-2017  Guillaume Schworer
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
from ctrl.utils import b
from ctrl.utils import O
from ctrl.utils.day import Day
from ctrl.utils.ms import Ms


__all__ = ['TROUSSEAU']


KEYS = [dict( name='telecommand_id_toexecute',
                                start=0*O,
                                l=2*O,
                                typ='uint',
                                verbose="telecommand id of the command to be executed",
                                disp="tcid"),

        dict(  name='packet_id_toexecute',
                            start=2*O,
                            l=2*O,
                            typ='uint',
                            verbose="corresponding packet id count of the command to be executed",
                            disp="pkid"),

        dict( name='date_ofexecution',
                        start=4*O,
                        l=2*O,
                        typ='uint',
#                        fctfix=Day,
                        verbose='planned date of execution',
                        disp="date"),

        dict( name='mscount_ofexecution',
                        start=6*O,
                        l=4*O,
                        typ='uint',
#                        fctfix=Ms,
                        verbose='planned ms of execution',
                        disp="ms")

        ]


TROUSSEAU = CCSDSTrousseau(KEYS, listof=True)
#TROUSSEAU = CCSDSTrousseau(KEYS)
